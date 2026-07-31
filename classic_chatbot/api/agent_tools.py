# import json
# import re
# import frappe


# NO_VALUE_FIELD_TYPES = {
#     "Section Break",
#     "Column Break",
#     "Tab Break",
#     "HTML",
#     "Button",
#     "Image",
#     "Fold",
#     "Heading",
# }


# def safe_json(value, default=None):
#     if value is None:
#         return default

#     if isinstance(value, (dict, list)):
#         return value

#     if isinstance(value, str):
#         try:
#             return json.loads(value)
#         except Exception:
#             return default if default is not None else value

#     return value


# def clean_doc(doc):
#     if not isinstance(doc, dict):
#         return {}

#     blocked_words = [
#         "password",
#         "api_key",
#         "api_secret",
#         "secret",
#         "token",
#         "access_token",
#         "refresh_token",
#     ]

#     output = {}

#     for key, value in doc.items():
#         key_lower = str(key).lower()

#         if any(word in key_lower for word in blocked_words):
#             output[key] = "***hidden***"
#         else:
#             output[key] = value

#     return output


# def get_doctype_schema(args):
#     doctype = args.get("doctype")

#     if not doctype:
#         return {"error": "DocType missing"}

#     try:
#         if not frappe.db.exists("DocType", doctype):
#             return {"error": f"DocType not found: {doctype}"}

#         if not frappe.has_permission(doctype, "read"):
#             return {"error": f"No read permission for {doctype}"}

#         # Standard fields from DocField table
#         standard_fields = frappe.get_all(
#             "DocField",
#             filters={
#                 "parent": doctype,
#                 "fieldtype": ["not in", list(NO_VALUE_FIELD_TYPES)],
#             },
#             fields=[
#                 "fieldname",
#                 "label",
#                 "fieldtype",
#                 "reqd",
#                 "options",
#                 "idx",
#                 "description",
#                 "read_only",
#                 "hidden",
#                 "default",
#             ],
#             order_by="idx asc",
#         )

#         # Custom fields from Custom Field table
#         custom_fields = frappe.get_all(
#             "Custom Field",
#             filters={
#                 "dt": doctype,
#                 "fieldtype": ["not in", list(NO_VALUE_FIELD_TYPES)],
#             },
#             fields=[
#                 "fieldname",
#                 "label",
#                 "fieldtype",
#                 "reqd",
#                 "options",
#                 "idx",
#                 "description",
#                 "read_only",
#                 "hidden",
#                 "default",
#             ],
#             order_by="idx asc",
#         )

#         all_fields = standard_fields + custom_fields

#         fields = []

#         for df in all_fields:
#             fields.append({
#                 "label": df.get("label"),
#                 "fieldname": df.get("fieldname"),
#                 "fieldtype": df.get("fieldtype"),
#                 "mandatory": bool(df.get("reqd")),
#                 "reqd": bool(df.get("reqd")),
#                 "options": df.get("options"),
#                 "description": df.get("description"),
#                 "read_only": bool(df.get("read_only")),
#                 "hidden": bool(df.get("hidden")),
#                 "default": df.get("default"),
#                 "idx": df.get("idx"),
#             })

#         meta = frappe.get_meta(doctype)

#         return {
#             "doctype": doctype,
#             "module": meta.module,
#             "is_submittable": bool(meta.is_submittable),
#             "is_child_table": bool(meta.istable),
#             "title_field": meta.title_field,
#             "fields": fields,
#             "mandatory_fields": [f for f in fields if f.get("mandatory")],
#         }

#     except Exception as e:
#         return {
#             "error": f"Schema fetch karne me error aaya: {str(e)}",
#             "doctype": doctype,
#         }


# def analyze_current_doc(args):
#     doctype = args.get("doctype")
#     doc = clean_doc(safe_json(args.get("doc"), {}))

#     if not doctype:
#         return {"error": "DocType missing"}

#     try:
#         if not frappe.db.exists("DocType", doctype):
#             return {"error": f"DocType not found: {doctype}"}

#         if not frappe.has_permission(doctype, "read"):
#             return {"error": f"No read permission for {doctype}"}

#         meta = frappe.get_meta(doctype)

#         missing_required = []
#         invalid_links = []
#         filled_summary = []

#         for df in meta.fields:
#             if df.fieldtype in NO_VALUE_FIELD_TYPES:
#                 continue

#             value = doc.get(df.fieldname)

#             if df.reqd and value in (None, "", [], {}):
#                 missing_required.append({
#                     "label": df.label,
#                     "fieldname": df.fieldname,
#                     "fieldtype": df.fieldtype,
#                 })

#             if value not in (None, "", [], {}) and df.fieldtype not in ("Table", "Table MultiSelect"):
#                 filled_summary.append({
#                     "label": df.label,
#                     "fieldname": df.fieldname,
#                     "value": value,
#                 })

#             if df.fieldtype == "Link" and value and df.options:
#                 try:
#                     if not frappe.db.exists(df.options, value):
#                         invalid_links.append({
#                             "label": df.label,
#                             "fieldname": df.fieldname,
#                             "linked_doctype": df.options,
#                             "value": value,
#                             "issue": f"{value} not found in {df.options}",
#                         })
#                 except Exception as e:
#                     invalid_links.append({
#                         "label": df.label,
#                         "fieldname": df.fieldname,
#                         "linked_doctype": df.options,
#                         "value": value,
#                         "issue": str(e),
#                     })

#         return {
#             "doctype": doctype,
#             "docname": doc.get("name"),
#             "docstatus": doc.get("docstatus"),
#             "missing_required": missing_required,
#             "invalid_links": invalid_links,
#             "filled_field_count": len(filled_summary),
#             "filled_summary_sample": filled_summary[:25],
#         }

#     except Exception as e:
#         return {
#             "error": f"Current document analyze karne me error aaya: {str(e)}",
#             "doctype": doctype,
#         }


# def get_field_help(args):
#     doctype = args.get("doctype")
#     fieldname = args.get("fieldname")

#     if not doctype:
#         return {"error": "DocType missing"}

#     if not fieldname:
#         return {"error": "Field name missing"}

#     try:
#         if not frappe.db.exists("DocType", doctype):
#             return {"error": f"DocType not found: {doctype}"}

#         if not frappe.has_permission(doctype, "read"):
#             return {"error": f"No read permission for {doctype}"}

#         schema = get_doctype_schema({"doctype": doctype})

#         if schema.get("error"):
#             return schema

#         matched = []

#         for df in schema.get("fields", []):
#             search_text = f"{df.get('fieldname')} {df.get('label') or ''}".lower()

#             if fieldname.lower() in search_text:
#                 matched.append({
#                     "label": df.get("label"),
#                     "fieldname": df.get("fieldname"),
#                     "fieldtype": df.get("fieldtype"),
#                     "mandatory": bool(df.get("mandatory")),
#                     "read_only": bool(df.get("read_only")),
#                     "hidden": bool(df.get("hidden")),
#                     "options": df.get("options"),
#                     "description": df.get("description"),
#                     "default": df.get("default"),
#                 })

#         return {
#             "doctype": doctype,
#             "search": fieldname,
#             "matches": matched[:10],
#         }

#     except Exception as e:
#         return {
#             "error": f"Field help fetch karne me error aaya: {str(e)}",
#             "doctype": doctype,
#             "fieldname": fieldname,
#         }


# def get_record(args):
#     doctype = args.get("doctype")
#     name = args.get("name")

#     if not doctype or not name:
#         return {"error": "DocType or record name missing"}

#     try:
#         if not frappe.db.exists("DocType", doctype):
#             return {"error": f"DocType not found: {doctype}"}

#         doc = frappe.get_doc(doctype, name)
#         doc.check_permission("read")

#         return clean_doc(doc.as_dict())

#     except Exception as e:
#         return {"error": str(e)}


# def search_records(args):
#     doctype = args.get("doctype")
#     filters = safe_json(args.get("filters"), {}) or {}
#     limit = int(args.get("limit") or 10)

#     if not doctype:
#         return {"error": "DocType missing"}

#     try:
#         if not frappe.db.exists("DocType", doctype):
#             return {"error": f"DocType not found: {doctype}"}

#         if not frappe.has_permission(doctype, "read"):
#             return {"error": f"No read permission for {doctype}"}

#         limit = min(limit, 20)

#         meta = frappe.get_meta(doctype)
#         fields = ["name", "modified"]

#         if meta.title_field and meta.title_field not in fields:
#             fields.insert(1, meta.title_field)

#         records = frappe.get_all(
#             doctype,
#             filters=filters,
#             fields=fields,
#             limit_page_length=limit,
#             order_by="modified desc",
#         )

#         return {
#             "doctype": doctype,
#             "filters": filters,
#             "records": records,
#         }

#     except Exception as e:
#         return {"error": str(e)}


# def explain_error(args):
#     error = args.get("error") or ""
#     doctype = args.get("doctype")
#     doc = clean_doc(safe_json(args.get("doc"), {}))

#     hints = []
#     lower = error.lower()

#     if "mandatory" in lower or "missing" in lower:
#         hints.append("Koi mandatory field blank ho sakti hai.")

#     if "permission" in lower or "not permitted" in lower:
#         hints.append("User permission, role permission ya document permission issue ho sakta hai.")

#     if "link validation" in lower or "could not find" in lower:
#         hints.append("Kisi Link field me galat ya non-existing master value ho sakti hai.")

#     if "duplicate" in lower:
#         hints.append("Duplicate record/name/unique field value ka issue ho sakta hai.")

#     if "submit" in lower:
#         hints.append("Submit ke liye document status, workflow, stock/account validation check karna hoga.")

#     analysis = {}

#     if doctype and doc:
#         analysis = analyze_current_doc({
#             "doctype": doctype,
#             "doc": doc,
#         })

#     return {
#         "doctype": doctype,
#         "error": error,
#         "quick_hints": hints,
#         "current_doc_analysis": analysis,
#     }


# TOOL_REGISTRY = {
#     "get_doctype_schema": get_doctype_schema,
#     "analyze_current_doc": analyze_current_doc,
#     "get_field_help": get_field_help,
#     "get_record": get_record,
#     "search_records": search_records,
#     "explain_error": explain_error,
# }


# def run_tool(tool_name, args):
#     if tool_name not in TOOL_REGISTRY:
#         return {"error": f"Unknown tool: {tool_name}"}

#     try:
#         return TOOL_REGISTRY[tool_name](args or {})
#     except Exception as e:
#         return {"error": str(e)}


# def available_tools():
#     return list(TOOL_REGISTRY.keys())


# def detect_field_from_question(question):
#     if not question:
#         return None

#     q = question.lower()

#     patterns = [
#         r"`([^`]+)`",
#         r"field\s+([a-zA-Z0-9_ ]+)",
#         r"filed\s+([a-zA-Z0-9_ ]+)",
#         r"([a-zA-Z0-9_ ]+)\s+field",
#     ]

#     for pattern in patterns:
#         match = re.search(pattern, q)

#         if match:
#             return match.group(1).strip()

#     return None


































import json
import re
from typing import Any

import frappe

from classic_chatbot.api.validation import (
    get_live_doctype_schema,
    validate_document_payload,
)


NO_VALUE_FIELD_TYPES = {
    "Section Break",
    "Column Break",
    "Tab Break",
    "HTML",
    "Button",
    "Image",
    "Fold",
    "Heading",
}

SENSITIVE_WORDS = {
    "password",
    "passwd",
    "api_key",
    "api_secret",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "otp",
}


def safe_json(value: Any, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, (dict, list, tuple)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return default if default is not None else value
    return value


def clean_doc(doc: Any) -> dict:
    if not isinstance(doc, dict):
        return {}

    output = {}
    for key, value in doc.items():
        key_lower = str(key).lower()
        if any(word in key_lower for word in SENSITIVE_WORDS):
            output[key] = "***hidden***"
        elif isinstance(value, list):
            output[key] = [
                clean_doc(row) if isinstance(row, dict) else row
                for row in value
            ]
        else:
            output[key] = value
    return output


def _check_doctype_access(doctype: str) -> dict | None:
    if not doctype:
        return {"error": "DocType missing"}
    if not frappe.db.exists("DocType", doctype):
        return {"error": f"DocType not found: {doctype}"}
    if not (
        frappe.has_permission(doctype, "read")
        or frappe.has_permission(doctype, "create")
    ):
        return {"error": f"No read/create permission for {doctype}"}
    return None


def get_doctype_schema(args):
    doctype = args.get("doctype")
    error = _check_doctype_access(doctype)
    if error:
        return error

    try:
        schema = get_live_doctype_schema(doctype)
        schema["mandatory_fields"] = [
            field
            for field in schema.get("fields", [])
            if field.get("mandatory")
        ]
        return schema
    except Exception as exc:
        return {
            "error": f"Schema fetch karne me error aaya: {exc}",
            "doctype": doctype,
        }


def analyze_current_doc(args):
    doctype = args.get("doctype")
    doc = clean_doc(safe_json(args.get("doc"), {}) or {})
    error = _check_doctype_access(doctype)
    if error:
        return error

    try:
        # Deterministic schema validation only. The save-time validator runs
        # the local AI semantic review separately.
        result = validate_document_payload(
            doctype,
            doc,
            run_ai=False,
        )

        missing_required = [
            issue
            for issue in result.get("issues", [])
            if issue.get("type") == "mandatory"
        ]
        invalid_links = [
            issue
            for issue in result.get("issues", [])
            if issue.get("type") in {
                "invalid_link",
                "invalid_dynamic_link",
            }
        ]

        return {
            "doctype": doctype,
            "docname": doc.get("name"),
            "docstatus": doc.get("docstatus"),
            "ok": result.get("ok"),
            "issue_count": result.get("issue_count"),
            "first_issue": result.get("first_issue"),
            "issues": result.get("issues", []),
            "missing_required": missing_required,
            "invalid_links": invalid_links,
        }
    except Exception as exc:
        return {
            "error": f"Current document analyze karne me error aaya: {exc}",
            "doctype": doctype,
        }


def validate_current_document(args):
    """Run complete schema + local Ollama semantic validation on current data."""
    doctype = args.get("doctype")
    doc = clean_doc(safe_json(args.get("doc"), {}) or {})
    error = _check_doctype_access(doctype)
    if error:
        return error

    try:
        return validate_document_payload(
            doctype,
            doc,
            run_ai=True,
        )
    except Exception as exc:
        return {
            "error": f"AI validation me error aaya: {exc}",
            "doctype": doctype,
        }


def get_field_help(args):
    doctype = args.get("doctype")
    fieldname = str(args.get("fieldname") or "").strip()
    error = _check_doctype_access(doctype)
    if error:
        return error
    if not fieldname:
        return {"error": "Field name missing"}

    try:
        schema = get_live_doctype_schema(doctype)
        needle = fieldname.lower()
        matches = []

        for field in schema.get("fields", []):
            search_text = (
                f"{field.get('fieldname')} {field.get('label') or ''}"
            ).lower()
            if needle in search_text:
                matches.append(field)

            for child in field.get("child_fields") or []:
                child_search = (
                    f"{child.get('fieldname')} {child.get('label') or ''}"
                ).lower()
                if needle in child_search:
                    matches.append({
                        **child,
                        "parent_table_field": field.get("fieldname"),
                        "parent_table_label": field.get("label"),
                    })

        return {
            "doctype": doctype,
            "search": fieldname,
            "matches": matches[:20],
        }
    except Exception as exc:
        return {
            "error": f"Field help fetch karne me error aaya: {exc}",
            "doctype": doctype,
            "fieldname": fieldname,
        }


def get_record(args):
    doctype = args.get("doctype")
    name = args.get("name")
    if not doctype or not name:
        return {"error": "DocType or record name missing"}

    try:
        doc = frappe.get_doc(doctype, name)
        doc.check_permission("read")
        return clean_doc(doc.as_dict())
    except Exception as exc:
        return {"error": str(exc)}


def search_records(args):
    doctype = args.get("doctype")
    filters = safe_json(args.get("filters"), {}) or {}
    limit = min(int(args.get("limit") or 10), 50)
    error = _check_doctype_access(doctype)
    if error:
        return error

    try:
        meta = frappe.get_meta(doctype)
        fields = ["name", "modified"]
        if meta.title_field and meta.title_field not in fields:
            fields.insert(1, meta.title_field)

        records = frappe.get_list(
            doctype,
            filters=filters,
            fields=fields,
            limit_page_length=limit,
            order_by="modified desc",
        )
        return {
            "doctype": doctype,
            "filters": filters,
            "records": records,
        }
    except Exception as exc:
        return {"error": str(exc)}


def explain_error(args):
    error_text = str(args.get("error") or "")
    doctype = args.get("doctype")
    doc = clean_doc(safe_json(args.get("doc"), {}) or {})
    lower = error_text.lower()
    hints = []

    if "mandatory" in lower or "missing" in lower:
        hints.append("Koi mandatory field blank ho sakti hai.")
    if "permission" in lower or "not permitted" in lower:
        hints.append("User/role/document permission issue ho sakta hai.")
    if "link validation" in lower or "could not find" in lower:
        hints.append("Kisi Link field me non-existing master value ho sakti hai.")
    if "duplicate" in lower:
        hints.append("Unique field ya document name duplicate ho sakta hai.")
    if "submit" in lower:
        hints.append("Workflow, docstatus, stock, ya accounting rule check karein.")

    analysis = {}
    if doctype and doc:
        analysis = analyze_current_doc({
            "doctype": doctype,
            "doc": doc,
        })

    return {
        "doctype": doctype,
        "error": error_text,
        "quick_hints": hints,
        "current_doc_analysis": analysis,
    }


TOOL_REGISTRY = {
    "get_doctype_schema": get_doctype_schema,
    "analyze_current_doc": analyze_current_doc,
    "validate_current_document": validate_current_document,
    "get_field_help": get_field_help,
    "get_record": get_record,
    "search_records": search_records,
    "explain_error": explain_error,
}


def run_tool(tool_name, args):
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {tool_name}"}
    try:
        return TOOL_REGISTRY[tool_name](args or {})
    except Exception as exc:
        return {"error": str(exc)}


def available_tools():
    return list(TOOL_REGISTRY.keys())


def detect_field_from_question(question):
    if not question:
        return None

    q = question.lower()
    patterns = [
        r"`([^`]+)`",
        r"field\s+([a-zA-Z0-9_ ]+)",
        r"filed\s+([a-zA-Z0-9_ ]+)",
        r"([a-zA-Z0-9_ ]+)\s+field",
    ]

    for pattern in patterns:
        match = re.search(pattern, q)
        if match:
            return match.group(1).strip()
    return None