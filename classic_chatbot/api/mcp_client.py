import json
import os
import select
import shutil
import subprocess
import threading
import time

import frappe

# ============================================================
# Classic Chatbot - MCP ERPNext Bridge (stdio transport)
#
# Frappe Cloud branch: sirf write-tool deny-list discovery ke liye
# short-lived MCPStdioClient chahiye (claude_agent.get_write_tool_names).
# mcp-erpnext binary app ke apne node_modules me vendored hai
# (package.json), aur ERP credentials site_config se aate hain -
# koi wrapper script / erpnext.env file nahi.
#
# HTTP mode npm build me broken hai (Deno globals chahiye), isliye stdio.
# ============================================================

# Write/mutation tools default me blocked (safety)
WRITE_SUFFIXES = ("_create", "_update", "_delete", "_submit", "_cancel")


def app_node_bin(name):
    """App ke vendored node_modules/.bin me se binary ka path."""
    app_root = os.path.dirname(frappe.get_app_path("classic_chatbot"))
    return os.path.join(app_root, "node_modules", ".bin", name)


def node_env():
    """Subprocess env jisme node PATH me guaranteed ho.

    Vendored bins (#!/usr/bin/env node) ko node chahiye; RQ/gunicorn
    worker ka PATH minimal ho sakta hai. site_config
    `classic_chatbot_node_bin` se override, warna `which node`.
    """
    env = dict(os.environ)
    env.setdefault("HOME", os.path.expanduser("~"))
    node_bin = frappe.conf.get("classic_chatbot_node_bin")
    if not node_bin:
        node = shutil.which("node")
        node_bin = os.path.dirname(node) if node else None
    if node_bin:
        env["PATH"] = node_bin + ":" + env.get("PATH", "")
    return env


def get_erpnext_env():
    """mcp-erpnext ke ERP credentials site_config se (service user ke API key/secret)."""
    url = frappe.conf.get("classic_chatbot_erpnext_url")
    key = frappe.conf.get("classic_chatbot_erpnext_api_key")
    secret = frappe.conf.get("classic_chatbot_erpnext_api_secret")
    if not (url and key and secret):
        frappe.throw(
            "Classic Chatbot: classic_chatbot_erpnext_url / _api_key / _api_secret "
            "site_config me set karo (service user ke API credentials)."
        )
    return {
        "ERPNEXT_URL": url,
        "ERPNEXT_API_KEY": key,
        "ERPNEXT_API_SECRET": secret,
    }


def get_mcp_config():
    return {
        "command": frappe.conf.get("classic_chatbot_mcp_command") or app_node_bin("mcp-erpnext"),
        # Default: no category trim -> full mcp-erpnext tool set (120 tools).
        # site_config `classic_chatbot_mcp_categories` se trim kar sakte ho.
        "categories": frappe.conf.get("classic_chatbot_mcp_categories") or "",
        "timeout": int(frappe.conf.get("classic_chatbot_mcp_timeout") or 60),
    }


class MCPStdioClient:
    """Minimal synchronous MCP client over stdio (newline-delimited JSON-RPC)."""

    def __init__(self, command, args=None, timeout=60, env=None):
        self.timeout = timeout
        self._id = 0
        self._io_lock = threading.Lock()
        proc_env = node_env()
        if env:
            proc_env.update(env)
        self.proc = subprocess.Popen(
            [command] + (args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            env=proc_env,
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
            timeout=90,
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
