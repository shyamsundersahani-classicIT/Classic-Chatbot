import frappe
from frappe.utils.password import get_decrypted_password

# ============================================================
# Classic Chatbot - Per-user Claude token store
#
# Har user apna Claude Code OAuth token (sk-ant-oat01-...) `/login`
# ke through save karta hai. Token "Chatbot Claude Token" DocType me
# encrypted (Password field) store hota hai, ek record per user
# (name == user id). Chatbot query us user ke token se chalti hai,
# to usage/rate-limit us user ke apne subscription me count hoti hai.
#
# Token mint karne ka tarika (user ke apne machine par, ek baar):
#   npm i -g @anthropic-ai/claude-code  (ya jo bhi install ho)
#   claude setup-token   -> browser OAuth -> token print
# Wo token yahan /login <token> se paste karte hain.
# ============================================================

DOCTYPE = "Chatbot Claude Token"
TOKEN_PREFIX = "sk-ant-oat01-"


def get_user_token(user=None):
    """Given user ka decrypted Claude token laao, ya None.

    Sirf enabled record ke liye token return hota hai. Kisi bhi permission
    ke bina chalta hai (server-side resolution), isliye caller ko yeh sirf
    apne acting user ke liye call karna chahiye.
    """
    user = user or frappe.session.user
    name = frappe.db.get_value(DOCTYPE, {"user": user, "enabled": 1}, "name")
    if not name:
        return None
    try:
        return get_decrypted_password(DOCTYPE, name, "claude_token", raise_exception=False)
    except Exception:
        return None


def mark_used(user):
    """last_used timestamp update karo (best-effort, silent fail)."""
    try:
        name = frappe.db.get_value(DOCTYPE, {"user": user}, "name")
        if name:
            frappe.db.set_value(DOCTYPE, name, "last_used", frappe.utils.now(),
                                update_modified=False)
            frappe.db.commit()
    except Exception:
        pass


@frappe.whitelist()
def save_token(token, label=None):
    """Calling user ke liye Claude token save/update karo."""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw("Login required")

    token = (token or "").strip()
    if not token:
        frappe.throw("Token khaali hai")
    if not token.startswith(TOKEN_PREFIX):
        frappe.throw(
            "Yeh Claude OAuth token jaisa nahi lag raha (expected prefix "
            f"'{TOKEN_PREFIX}'). Apne machine par `claude setup-token` chala "
            "kar jo token milta hai wo paste karo."
        )

    name = frappe.db.get_value(DOCTYPE, {"user": user}, "name")
    if name:
        doc = frappe.get_doc(DOCTYPE, name)
        doc.claude_token = token
        doc.enabled = 1
        if label:
            doc.token_label = label
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc({
            "doctype": DOCTYPE,
            "user": user,
            "claude_token": token,
            "token_label": label or "",
            "enabled": 1,
        })
        doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True, "user": user}


@frappe.whitelist()
def clear_token():
    """Calling user ka token hata do (logout)."""
    user = frappe.session.user
    name = frappe.db.get_value(DOCTYPE, {"user": user}, "name")
    if name:
        frappe.delete_doc(DOCTYPE, name, ignore_permissions=True, force=True)
        frappe.db.commit()
        return {"ok": True, "removed": True}
    return {"ok": True, "removed": False}


@frappe.whitelist()
def token_status():
    """Calling user ke liye login status (token value kabhi return nahi hota)."""
    user = frappe.session.user
    row = frappe.db.get_value(
        DOCTYPE, {"user": user}, ["enabled", "token_label", "last_used"], as_dict=True)
    return {
        "logged_in": bool(row and row.get("enabled")),
        "label": (row or {}).get("token_label"),
        "last_used": (row or {}).get("last_used"),
        "user": user,
    }
