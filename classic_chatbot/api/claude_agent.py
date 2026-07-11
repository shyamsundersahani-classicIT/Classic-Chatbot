import json
import os
import subprocess
import tempfile
import threading

import frappe

# ============================================================
# Classic Chatbot - Claude Code Headless Agent (Frappe Cloud branch)
#
# `claude -p` (print mode) ko subprocess me chalata hai. Binaries app ke
# vendored node_modules se aate hain (package.json - koi global install /
# nvm nahi). Auth per-user Claude token se (`/login` + token_store);
# site_config `classic_chatbot_require_user_token 1` par bina token ke
# koi subprocess spawn nahi hota. ERP credentials (service user ka API
# key/secret) site_config se inject hote hain - koi erpnext.env file
# nahi. --strict-mcp-config taaki sirf erpnext tools load hon.
# ============================================================

_mcp_config_lock = threading.Lock()
_mcp_config_path = None

# Fallback deny-list agar MCP tools/list se dynamic discovery fail ho.
# mcp_client.WRITE_SUFFIXES se match hone wale known tools.
FALLBACK_WRITE_TOOLS = [
    "erpnext_asset_create", "erpnext_company_create", "erpnext_customer_create",
    "erpnext_customer_update", "erpnext_delivery_note_create", "erpnext_doc_cancel",
    "erpnext_doc_create", "erpnext_doc_delete", "erpnext_doc_submit",
    "erpnext_doc_update", "erpnext_expense_claim_create", "erpnext_item_create",
    "erpnext_item_update", "erpnext_journal_entry_create", "erpnext_kanban_move_card",
    "erpnext_lead_create", "erpnext_leave_application_create", "erpnext_project_create",
    "erpnext_purchase_order_create", "erpnext_quotation_create",
    "erpnext_sales_invoice_create", "erpnext_sales_invoice_submit",
    "erpnext_sales_order_cancel", "erpnext_sales_order_create",
    "erpnext_sales_order_submit", "erpnext_sales_order_update",
    "erpnext_stock_entry_create", "erpnext_supplier_create", "erpnext_task_create",
    "erpnext_task_update", "erpnext_work_order_create",
]

SYSTEM_PROMPT = (
    "You are Classic Chatbot, an ERPNext assistant with live erpnext MCP tools. "
    "Use the tools to fetch real data; never invent data. "
    "erpnext_doc_list works for ANY DocType with Frappe filters. "
    "CRITICAL - finding records by name: NEVER page through list tools and scan "
    "manually (specialized list tools like erpnext_employee_list cannot filter by "
    "name, and old records will not appear in recent pages). ALWAYS use "
    "erpnext_doc_list with a like-filter on the name field instead, e.g. "
    'doctype "Employee" filters [["employee_name","like","%deepak%"]], '
    'or Customer/customer_name, Supplier/supplier_name, User/full_name, '
    'Contact/first_name. Only say a record does not exist after a like-filter '
    "search on the right DocType returned nothing. "
    "Numbers: only report totals/sums you computed from the actual rows fetched; "
    "list the addends mentally one time and re-check the sum before answering. "
    "Reply in conversational Hinglish (Roman script, never Devnagari). "
    "Be concise and direct: answer first, details after. "
    "Use markdown tables when listing 3+ records. "
    "You have read-only access - politely refuse create/update/delete requests."
)


def get_claude_config():
    from classic_chatbot.api.mcp_client import app_node_bin, get_mcp_config

    mcp = get_mcp_config()
    return {
        "bin": frappe.conf.get("classic_chatbot_claude_bin") or app_node_bin("claude"),
        "model": frappe.conf.get("classic_chatbot_claude_model") or "sonnet",
        "timeout": int(frappe.conf.get("classic_chatbot_claude_timeout") or 150),
        "max_turns": int(frappe.conf.get("classic_chatbot_claude_max_turns") or 12),
        "allow_writes": bool(frappe.conf.get("classic_chatbot_claude_allow_writes")),
        "require_user_token": bool(frappe.conf.get("classic_chatbot_require_user_token")),
        "mcp_command": mcp["command"],
        "mcp_categories": mcp["categories"],
    }


def get_mcp_config_file(conf):
    """Ek strict MCP config file banao jisme sirf erpnext server ho.

    ERP credentials site_config se env block me jaate hain (mkstemp file
    0600 hoti hai; sirf bench user padh sakta hai). File per-worker cache
    hoti hai - creds badle to workers restart karo.
    """
    from classic_chatbot.api.mcp_client import get_erpnext_env

    global _mcp_config_path
    with _mcp_config_lock:
        if _mcp_config_path and os.path.exists(_mcp_config_path):
            return _mcp_config_path
        payload = {
            "mcpServers": {
                "erpnext": {
                    "type": "stdio",
                    "command": conf["mcp_command"],
                    "args": [f"--categories={conf['mcp_categories']}"] if conf["mcp_categories"] else [],
                    "env": get_erpnext_env(),
                }
            }
        }
        fd, path = tempfile.mkstemp(prefix="cc_claude_mcp_", suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(payload, f)
        _mcp_config_path = path
        return path


def get_write_tool_names():
    """MCP server se live tool list lekar write tools nikalo (deny-list).

    Result 24h Redis-cache hota hai aur MCP subprocess turant band -
    persistent get_client() yahan mat use karo, warna har rq worker me
    ~100MB ka node process hamesha zinda rehta hai sirf naam list ke liye.
    """
    cached = frappe.cache.get_value("classic_chatbot_write_tools")
    if cached:
        return cached
    client = None
    try:
        from classic_chatbot.api.mcp_client import (
            WRITE_SUFFIXES, MCPStdioClient, get_erpnext_env, get_mcp_config)

        conf = get_mcp_config()
        args = [f"--categories={conf['categories']}"] if conf["categories"] else []
        client = MCPStdioClient(conf["command"], args, timeout=conf["timeout"], env=get_erpnext_env())
        names = [t["name"] for t in client.list_tools()]
        tools = [n for n in names if n.endswith(WRITE_SUFFIXES) or n == "erpnext_kanban_move_card"]
        frappe.cache.set_value("classic_chatbot_write_tools", tools, expires_in_sec=86400)
        return tools
    except Exception:
        return FALLBACK_WRITE_TOOLS
    finally:
        if client:
            client.close()


LOGIN_HINT = (
    "Bhai, chatbot use karne ke liye pehle apna Claude login karna padega. "
    "Apne computer par ek baar `claude setup-token` chalao, jo token milta hai "
    "use yahan bhejo: `/login sk-ant-oat01-...`  "
    "(Ye tumhare apne Claude subscription se chalega.)"
)


@frappe.whitelist()
def ask_claude(question, doctype=None, docname=None, doc=None, route=None, error=None,
               session_id=None, preferred_model=None, acting_user=None):
    if not question:
        frappe.throw("Question is required")

    conf = get_claude_config()

    # Per-user Claude token resolve karo (acting_user = jisne query bheji).
    from classic_chatbot.api.token_store import get_user_token, mark_used
    acting_user = acting_user or frappe.session.user
    user_token = get_user_token(acting_user)

    if not user_token and conf["require_user_token"]:
        return {
            "answer": LOGIN_HINT,
            "model_used": "🔒 Login required",
            "tools_used": [],
            "needs_login": True,
        }

    user_msg = question
    if doctype:
        user_msg += f"\n(active screen DocType: {doctype}"
        if docname:
            user_msg += f", document: {docname}"
        user_msg += ")"
    if error:
        user_msg += f"\n(recent UI error: {error})"

    cmd = [
        conf["bin"], "-p",
        "--output-format", "json",
        "--model", conf["model"],
        "--max-turns", str(conf["max_turns"]),
        "--mcp-config", get_mcp_config_file(conf),
        "--strict-mcp-config",
        "--allowedTools", "mcp__erpnext",
        "--append-system-prompt", SYSTEM_PROMPT,
    ]

    if not conf["allow_writes"]:
        cmd += ["--disallowedTools", ",".join(get_write_tool_names())]

    base_cmd = list(cmd)
    if session_id:
        cmd += ["--resume", session_id]

    from classic_chatbot.api.mcp_client import get_erpnext_env, node_env

    env = node_env()
    # MCP server connect ka wait (ms) - cold start ke liye headroom
    env.setdefault("MCP_TIMEOUT", "60000")
    # ERP creds config-file env ke sath belt-and-braces subprocess env me bhi
    env.update(get_erpnext_env())

    # Per-user token: is user ki query us ke apne Claude subscription se
    # chale. Token env me inject; server ke ~/.claude login se override.
    if user_token:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = user_token
        env.pop("ANTHROPIC_API_KEY", None)
    # Agar token nahi hai to server ka ~/.claude login fallback (dev/single-user).

    try:
        proc = subprocess.run(
            cmd,
            input=user_msg,
            capture_output=True,
            text=True,
            timeout=conf["timeout"],
            env=env,
        )
        # Stale session id (FC deploy par ~/.claude wipe ho jata hai) -
        # resume fail hua to fresh session se ek retry
        if proc.returncode != 0 and session_id:
            proc = subprocess.run(
                base_cmd,
                input=user_msg,
                capture_output=True,
                text=True,
                timeout=conf["timeout"],
                env=env,
            )
    except subprocess.TimeoutExpired:
        return {
            "answer": "Bhai, Claude se response aane me time lag raha hai (timeout). Thoda simple question try karo.",
            "model_used": "⚠️ Claude Timeout",
            "tools_used": [],
        }

    if proc.returncode != 0:
        frappe.log_error(
            f"cmd: {' '.join(cmd)}\nstdout: {proc.stdout[-2000:]}\nstderr: {proc.stderr[-2000:]}",
            "Classic Chatbot Claude Agent Error",
        )
        return {
            "answer": f"Bhai, Claude agent me error aaya: {(proc.stderr or proc.stdout)[-300:]}",
            "model_used": "⚠️ Error",
            "tools_used": [],
        }

    try:
        data = json.loads(proc.stdout)
    except Exception:
        frappe.log_error(proc.stdout[-2000:], "Classic Chatbot Claude Agent Bad JSON")
        return {
            "answer": "Bhai, Claude ka response parse nahi ho paya. Error log check karo.",
            "model_used": "⚠️ Error",
            "tools_used": [],
        }

    if data.get("is_error"):
        # e.g. subscription rate limit hit
        return {
            "answer": f"Bhai, Claude ne error diya: {str(data.get('result'))[:300]}",
            "model_used": "⚠️ Claude Error",
            "tools_used": [],
            "session_id": data.get("session_id"),
        }

    models = [m for m in (data.get("modelUsage") or {}).keys() if "haiku" in m or "sonnet" in m or "opus" in m or "fable" in m]

    if user_token:
        mark_used(acting_user)

    src = "your login" if user_token else "server"
    return {
        "answer": data.get("result") or "Bhai, Claude ne koi answer nahi diya.",
        "model_used": f"🤖 Claude ({conf['model']}, {src})",
        "tools_used": [],
        "session_id": data.get("session_id"),
        "debug": {
            "num_turns": data.get("num_turns"),
            "duration_ms": data.get("duration_ms"),
            "models": models,
        } if frappe.conf.get("classic_chatbot_debug") else None,
    }


# ============================================================
# Async mode: Claude query background (RQ) worker me chalti hai,
# gunicorn worker sirf enqueue + poll karta hai (millisecond-level).
# Result Redis cache me store hota hai, frontend poll karta hai.
# ============================================================

CACHE_PREFIX = "classic_chatbot_job:"
RESULT_TTL = 900  # seconds


@frappe.whitelist()
def ask_claude_async(question, doctype=None, docname=None, doc=None, route=None,
                     error=None, session_id=None, preferred_model=None):
    if not question:
        frappe.throw("Question is required")

    token = frappe.generate_hash(length=24)
    frappe.cache.set_value(
        CACHE_PREFIX + token,
        {"status": "queued", "user": frappe.session.user},
        expires_in_sec=RESULT_TTL,
    )
    frappe.enqueue(
        "classic_chatbot.api.claude_agent.run_claude_job",
        queue="long",
        timeout=max(get_claude_config()["timeout"] + 60, 300),
        job_name=f"classic_chatbot_claude_{token}",
        token=token,
        enqueued_by=frappe.session.user,
        acting_user=frappe.session.user,
        question=question,
        doctype=doctype,
        docname=docname,
        doc=doc,
        route=route,
        error=error,
        session_id=session_id,
    )
    return {"job_token": token}


def run_claude_job(token, enqueued_by=None, **kwargs):
    key = CACHE_PREFIX + token
    frappe.cache.set_value(key, {"status": "running", "user": enqueued_by}, expires_in_sec=RESULT_TTL)
    try:
        result = ask_claude(**kwargs)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot Claude Job Error")
        result = {
            "answer": f"Bhai, background job me error aaya: {str(e)}",
            "model_used": "⚠️ Error",
            "tools_used": [],
        }
    frappe.cache.set_value(
        key,
        {"status": "done", "user": enqueued_by, "result": result},
        expires_in_sec=RESULT_TTL,
    )


@frappe.whitelist()
def poll_claude(job_token):
    data = frappe.cache.get_value(CACHE_PREFIX + job_token)
    if not data:
        return {"status": "expired"}
    # Sirf wahi user apna result padh sakta hai jisne pucha tha
    if data.get("user") and data["user"] != frappe.session.user:
        frappe.throw("Not permitted", frappe.PermissionError)
    return {"status": data.get("status"), "result": data.get("result")}
