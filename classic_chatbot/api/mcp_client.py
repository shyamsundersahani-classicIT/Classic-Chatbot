import json
import select
import subprocess
import threading
import time

import frappe

# ============================================================
# Classic Chatbot - MCP ERPNext Bridge (stdio transport)
#
# Ek persistent mcp-erpnext subprocess per worker. Newline-delimited
# JSON-RPC over stdin/stdout (MCP stdio transport). HTTP mode is npm
# build me broken hai (Deno globals chahiye), isliye stdio.
# ============================================================

_lock = threading.Lock()
_client = None


# Generic doc tools hamesha included - kisi bhi DocType (User, Employee, PO...)
# ka data nikal sakte hain. Baaki specialized tools question-keywords se select
# hote hain, kyunki CPU-only 7B model 26+ tool schemas handle nahi kar pata.
ALWAYS_TOOLS = ["erpnext_doc_list", "erpnext_doc_get"]

# Question keywords -> specialized tool prefixes
TOOL_KEYWORDS = {
    "erpnext_customer_list": ["customer", "grahak", "client", "party"],
    "erpnext_sales_order_list": ["sales order", "so ", "order"],
    "erpnext_sales_invoice_list": ["invoice", "bill", "billing"],
    "erpnext_quotation_list": ["quotation", "quote"],
    "erpnext_item_list": ["item", "product", "maal"],
    "erpnext_stock_balance": ["stock", "balance", "qty", "quantity", "inventory"],
    "erpnext_warehouse_list": ["warehouse", "godown"],
    "erpnext_stock_entry_list": ["stock entry", "material transfer"],
}

# Write/mutation tools default me blocked (safety)
WRITE_SUFFIXES = ("_create", "_update", "_delete", "_submit", "_cancel")

MAX_SELECTED_TOOLS = 5


def get_mcp_config():
    allowlist = frappe.conf.get("classic_chatbot_mcp_tools")
    if isinstance(allowlist, str):
        allowlist = [t.strip() for t in allowlist.split(",") if t.strip()]
    return {
        "command": frappe.conf.get("classic_chatbot_mcp_command")
        or "/home/frappeuser/.claude/mcp-wrappers/erpnext.sh",
        "categories": frappe.conf.get("classic_chatbot_mcp_categories") or "sales,inventory,operations",
        "timeout": int(frappe.conf.get("classic_chatbot_mcp_timeout") or 60),
        "tool_allowlist": allowlist,  # set karo to router bypass ho jata hai
        "allow_writes": bool(frappe.conf.get("classic_chatbot_mcp_allow_writes")),
    }


class MCPStdioClient:
    """Minimal synchronous MCP client over stdio (newline-delimited JSON-RPC)."""

    def __init__(self, command, args=None, timeout=60):
        self.timeout = timeout
        self._id = 0
        self._io_lock = threading.Lock()
        self.proc = subprocess.Popen(
            [command] + (args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._initialize()

    def is_alive(self):
        return self.proc.poll() is None

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass

    def _send(self, method, params=None, is_notification=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not is_notification:
            self._id += 1
            msg["id"] = self._id
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        return None if is_notification else self._id

    def _reply(self, msg):
        """Server->client requests ka jawab do taaki loop block na ho."""
        req_id = msg.get("id")
        if msg.get("method") == "ping":
            out = {"jsonrpc": "2.0", "id": req_id, "result": {}}
        else:
            out = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Method not found"},
            }
        self.proc.stdin.write(json.dumps(out) + "\n")
        self.proc.stdin.flush()

    def _read_response(self, want_id, timeout):
        deadline = time.time() + timeout
        while time.time() < deadline:
            ready, _, _ = select.select([self.proc.stdout], [], [], deadline - time.time())
            if not ready:
                break
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("MCP server closed stdout")
            try:
                msg = json.loads(line)
            except Exception:
                continue

            if msg.get("id") == want_id and ("result" in msg or "error" in msg):
                if "error" in msg:
                    raise RuntimeError(f"MCP error: {msg['error'].get('message')}")
                return msg["result"]

            # Server-initiated request (ping etc.)
            if "method" in msg and "id" in msg:
                self._reply(msg)
            # Notifications ignore

        raise TimeoutError(f"MCP response timeout for request id {want_id}")

    def request(self, method, params=None, timeout=None):
        with self._io_lock:
            rid = self._send(method, params)
            return self._read_response(rid, timeout or self.timeout)

    def _initialize(self):
        self.request(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "classic-chatbot", "version": "0.1"},
            },
            timeout=90,  # pehli baar npx cold start slow ho sakta hai
        )
        self._send("notifications/initialized", is_notification=True)
        self._tools_cache = None

    def list_tools(self):
        if self._tools_cache is None:
            self._tools_cache = self.request("tools/list", {}).get("tools") or []
        return self._tools_cache

    def call_tool(self, name, arguments=None):
        result = self.request("tools/call", {"name": name, "arguments": arguments or {}})
        texts = []
        for item in result.get("content") or []:
            if item.get("type") == "text":
                texts.append(item.get("text") or "")
        return strip_ui_meta("\n".join(texts))


def strip_ui_meta(text):
    """Tool results me viewer/navigation metadata hota hai - LLM context bachao."""
    try:
        data = json.loads(text)
    except Exception:
        return text

    def clean(obj):
        if isinstance(obj, dict):
            return {
                k: clean(v)
                for k, v in obj.items()
                if k not in {"_meta", "_rowAction", "_sendMessageHints", "_drillDown", "_trendDrillDown", "refreshRequest"}
            }
        if isinstance(obj, list):
            return [clean(v) for v in obj]
        return obj

    return json.dumps(clean(data), ensure_ascii=False, default=str)


def get_client():
    """Per-worker persistent client. Dead process par transparent reconnect."""
    global _client
    with _lock:
        if _client is None or not _client.is_alive():
            conf = get_mcp_config()
            args = []
            if conf["categories"]:
                args.append(f"--categories={conf['categories']}")
            _client = MCPStdioClient(conf["command"], args, timeout=conf["timeout"])
        return _client


def select_tool_names(question, conf):
    """Per-question tool selection: generic doc tools + keyword-matched specialized tools."""
    if conf["tool_allowlist"]:
        return conf["tool_allowlist"]

    q = (question or "").lower()
    selected = list(ALWAYS_TOOLS)
    for tool_name, keywords in TOOL_KEYWORDS.items():
        if len(selected) >= MAX_SELECTED_TOOLS:
            break
        if any(kw in q for kw in keywords):
            selected.append(tool_name)
    return selected


def get_ollama_tools(question=None, max_description_chars=150):
    """MCP tool schemas -> Ollama/OpenAI function-calling format (router filtered)."""
    conf = get_mcp_config()
    wanted = select_tool_names(question, conf)
    tools = []
    for t in get_client().list_tools():
        if t["name"] not in wanted:
            continue
        if not conf["allow_writes"] and t["name"].endswith(WRITE_SUFFIXES):
            continue
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": (t.get("description") or "")[:max_description_chars],
                    "parameters": t.get("inputSchema") or {"type": "object", "properties": {}},
                },
            }
        )
    return tools


def call_mcp_tool(name, arguments=None):
    return get_client().call_tool(name, arguments)
