from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import frappe
import requests
from frappe import _
from frappe.utils import cint, getdate, get_datetime


LAYOUT_FIELD_TYPES = {
    "Section Break",
    "Column Break",
    "Tab Break",
    "HTML",
    "Button",
    "Image",
    "Fold",
    "Heading",
}
TABLE_FIELD_TYPES = {"Table", "Table MultiSelect"}
SEMANTIC_FIELD_TYPES = {
    "Data",
    "Small Text",
    "Text",
    "Long Text",
    "Text Editor",
    "Code",
    "Select",
    "Link",
    "Dynamic Link",
    "Int",
    "Long Int",
    "Float",
    "Currency",
    "Percent",
    "Check",
    "Date",
    "Datetime",
    "Time",
    "Duration",
    "Phone",
    "Rating",
}
SENSITIVE_FIELD_WORDS = {
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "api_secret",
    "access_token",
    "refresh_token",
    "otp",
    "private_key",
}
DEFAULT_IGNORED_DOCTYPES = {
    "Access Log",
    "Activity Log",
    "Communication",
    "DocType",
    "Error Log",
    "File",
    "Notification Log",
    "Prepared Report",
    "Property Setter",
    "RQ Job",
    "Scheduled Job Log",
    "Server Script",
    "Client Script",
    "System Settings",
    "User",
    "Version",
}

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_ALLOWED_PATTERN = re.compile(r"^[0-9+\-()\s.]+$")
URL_PATTERN = re.compile(r"^(https?://|www\.)[^\s]+$", re.IGNORECASE)
TIME_PATTERN = re.compile(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$")

FIELD_PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "field_profiles": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fieldname": {"type": "string"},
                    "child_fieldname": {"type": ["string", "null"]},
                    "purpose": {"type": "string"},
                    "expected_value_kinds": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "incompatible_value_kinds": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "related_fieldnames": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                },
                "required": [
                    "fieldname",
                    "purpose",
                    "expected_value_kinds",
                    "incompatible_value_kinds",
                    "related_fieldnames",
                    "confidence",
                ],
            },
        }
    },
    "required": ["field_profiles"],
}

AI_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "is_valid": {"type": "boolean"},
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_type": {"type": "string"},
                    "fieldname": {"type": "string"},
                    "child_fieldname": {"type": ["string", "null"]},
                    "row_index": {"type": ["integer", "null"]},
                    "severity": {
                        "type": "string",
                        "enum": ["error", "warning"],
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "detected_value_kind": {"type": "string"},
                    "expected_value_kind": {"type": "string"},
                    "message": {"type": "string"},
                    "expected": {"type": "string"},
                    "suggested_fieldnames": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "suggested_corrections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "fieldname": {"type": "string"},
                                "value": {
                                    "type": [
                                        "string",
                                        "number",
                                        "boolean",
                                        "null",
                                    ]
                                },
                            },
                            "required": ["fieldname", "value"],
                        },
                    },
                },
                "required": [
                    "issue_type",
                    "fieldname",
                    "severity",
                    "confidence",
                    "message",
                    "expected",
                    "suggested_fieldnames",
                    "suggested_corrections",
                ],
            },
        },
    },
    "required": ["is_valid", "issues"],
}


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _config_list(value: Any) -> set[str]:
    if not value:
        return set()
    if isinstance(value, (list, tuple, set)):
        return {str(item).strip() for item in value if str(item).strip()}
    return {
        item.strip()
        for item in str(value).replace("\n", ",").split(",")
        if item.strip()
    }

def get_validation_config() -> dict[str, Any]:
    """
    Read AI validation settings from site_config.json.

    Production defaults:
    - llama3:latest
    - AI failure does not block document save
    - warnings do not block save
    - only configured DocTypes are validated
    """

    allowed = _config_list(
        frappe.conf.get(
            "classic_chatbot_ai_allowed_doctypes"
        )
    )

    if not allowed:
        allowed = {"Contact"}

    local_model = (
        frappe.conf.get(
            "classic_chatbot_validation_model"
        )
        or frappe.conf.get(
            "classic_chatbot_local_model"
        )
        or "llama3:latest"
    )

    ignored_doctypes = (
        DEFAULT_IGNORED_DOCTYPES
        | _config_list(
            frappe.conf.get(
                "classic_chatbot_ai_ignored_doctypes"
            )
        )
    )

    return {
        "enabled": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_validation_enabled"
            ),
            True,
        ),

        "allowed_doctypes": allowed,

        "ignored_doctypes": ignored_doctypes,

        "local_url": (
            frappe.conf.get(
                "classic_chatbot_local_url"
            )
            or "http://127.0.0.1:11434"
        ),

        "local_model": str(local_model),

        "temperature": float(
            frappe.conf.get(
                "classic_chatbot_validation_temperature"
            )
            or 0.0
        ),

        "timeout": int(
            frappe.conf.get(
                "classic_chatbot_validation_timeout"
            )
            or 60
        ),

        "confidence_threshold": float(
            frappe.conf.get(
                "classic_chatbot_validation_confidence"
            )
            or 0.80
        ),

        "warning_confidence_threshold": float(
            frappe.conf.get(
                "classic_chatbot_validation_warning_confidence"
            )
            or 0.90
        ),

        "cache_seconds": int(
            frappe.conf.get(
                "classic_chatbot_validation_cache_seconds"
            )
            or 300
        ),

        "profile_cache_seconds": int(
            frappe.conf.get(
                "classic_chatbot_validation_profile_cache_seconds"
            )
            or 86400
        ),

        # AI unavailable ho to save block nahi hoga.
        "fail_closed": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_fail_closed"
            ),
            False,
        ),

        # Warnings suggestions rahengi, save block nahi karengi.
        "block_warnings": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_block_warnings"
            ),
            False,
        ),

        "validate_background": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_validate_background"
            ),
            False,
        ),

        "realtime_enabled": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_realtime_enabled"
            ),
            True,
        ),

        "realtime_debounce_ms": int(
            frappe.conf.get(
                "classic_chatbot_ai_realtime_debounce_ms"
            )
            or 1500
        ),

        "use_field_profiles": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_use_field_profiles"
            ),
            True,
        ),

        "use_feedback_memory": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_use_feedback_memory"
            ),
            True,
        ),

        "use_thinking_on_full_check": _as_bool(
            frappe.conf.get(
                "classic_chatbot_ai_think_on_full_check"
            ),
            False,
        ),

        "max_fields": int(
            frappe.conf.get(
                "classic_chatbot_validation_max_fields"
            )
            or 100
        ),

        "max_child_rows": int(
            frappe.conf.get(
                "classic_chatbot_validation_max_child_rows"
            )
            or 20
        ),

        "max_value_chars": int(
            frappe.conf.get(
                "classic_chatbot_validation_max_value_chars"
            )
            or 600
        ),

        "max_feedback_examples": int(
            frappe.conf.get(
                "classic_chatbot_validation_feedback_examples"
            )
            or 12
        ),

        "num_ctx": int(
            frappe.conf.get(
                "classic_chatbot_validation_num_ctx"
            )
            or 4096
        ),

        "num_predict": int(
            frappe.conf.get(
                "classic_chatbot_validation_num_predict"
            )
            or 500
        ),
    }

def _is_doctype_allowed(doctype: str | None, config: dict[str, Any]) -> bool:
    return bool(
        doctype
        and doctype in config["allowed_doctypes"]
        and doctype not in config["ignored_doctypes"]
    )


# -----------------------------------------------------------------------------
# Generic helpers
# -----------------------------------------------------------------------------


def _safe_json(value: Any, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, (dict, list, tuple)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return default
    return value


def _parse_name_set(value: Any) -> set[str]:
    parsed = _safe_json(value, [])
    if isinstance(parsed, (list, tuple, set)):
        return {
            str(item).strip()
            for item in parsed
            if str(item).strip()
        }
    return set()


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _field_is_sensitive(fieldname: str | None) -> bool:
    lowered = str(fieldname or "").lower()
    return any(word in lowered for word in SENSITIVE_FIELD_WORDS)


def _json_safe(value: Any, max_chars: int = 600) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return "<binary>"
    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()[:max_chars]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(value)[:max_chars]


def _stable_hash(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _cache_get(key: str) -> Any:
    try:
        value = frappe.cache.get_value(key)
        if not value:
            return None
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        if isinstance(value, str):
            return json.loads(value)
        return value
    except Exception:
        return None


def _cache_set(key: str, value: Any, seconds: int) -> None:
    try:
        frappe.cache.set_value(
            key,
            json.dumps(value, ensure_ascii=False, default=str),
            expires_in_sec=seconds,
        )
    except Exception:
        pass


def _make_issue(
    *,
    issue_type: str,
    fieldname: str,
    label: str,
    message: str,
    expected: str = "",
    value: Any = None,
    severity: str = "error",
    source: str = "schema",
    child_fieldname: str | None = None,
    row_index: int | None = None,
    confidence: float = 1.0,
    detected_value_kind: str = "",
    expected_value_kind: str = "",
    suggested_fieldnames: list[str] | None = None,
    suggested_corrections: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "type": issue_type,
        "severity": severity,
        "source": source,
        "fieldname": fieldname,
        "child_fieldname": child_fieldname,
        "row_index": row_index,
        "label": label,
        "message": message,
        "expected": expected,
        "value": _json_safe(value),
        "confidence": confidence,
        "detected_value_kind": detected_value_kind,
        "expected_value_kind": expected_value_kind,
        "suggested_fieldnames": suggested_fieldnames or [],
        "suggested_corrections": suggested_corrections or [],
    }


# -----------------------------------------------------------------------------
# Reusable metadata tools (also exposed through the optional MCP server)
# -----------------------------------------------------------------------------


def _linked_doctype_summary(linked_doctype: str | None) -> dict[str, Any] | None:
    if not linked_doctype or not frappe.db.exists("DocType", linked_doctype):
        return None
    try:
        meta = frappe.get_meta(linked_doctype)
        return {
            "doctype": linked_doctype,
            "module": meta.module,
            "title_field": meta.title_field,
            "search_fields": list(meta.get_search_fields() or []),
            "autoname": getattr(meta, "autoname", None),
            "description": re.sub(
                r"\s+", " ", str(getattr(meta, "description", "") or "")
            ).strip()[:300],
        }
    except Exception:
        return {"doctype": linked_doctype}


def _field_to_schema(
    df,
    *,
    section_label: str = "",
    child_fields: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    select_options: list[str] = []
    if df.fieldtype == "Select" and df.options:
        select_options = [
            item.strip()
            for item in str(df.options).splitlines()
            if item.strip()
        ][:50]

    linked_summary = None
    if df.fieldtype == "Link" and df.options:
        linked_summary = _linked_doctype_summary(str(df.options))

    return {
        "fieldname": df.fieldname,
        "label": df.label or df.fieldname,
        "fieldtype": df.fieldtype,
        "options": df.options,
        "select_options": select_options,
        "linked_doctype": linked_summary,
        "description": re.sub(r"\s+", " ", str(df.description or "")).strip(),
        "mandatory": bool(df.reqd),
        "read_only": bool(df.read_only),
        "hidden": bool(df.hidden),
        "unique": bool(getattr(df, "unique", 0)),
        "length": cint(getattr(df, "length", 0)) or None,
        "precision": cint(getattr(df, "precision", 0)) or None,
        "idx": cint(getattr(df, "idx", 0)),
        "section_label": section_label,
        "depends_on": getattr(df, "depends_on", None),
        "mandatory_depends_on": getattr(df, "mandatory_depends_on", None),
        "child_fields": child_fields or [],
    }


def get_live_doctype_schema(doctype: str) -> dict[str, Any]:
    """Read merged metadata, including custom fields and Property Setters."""
    meta = frappe.get_meta(doctype)
    fields: list[dict[str, Any]] = []
    current_section = ""

    for df in meta.fields:
        if df.fieldtype == "Section Break":
            current_section = str(df.label or "").strip()
            continue
        if not df.fieldname or df.fieldtype in LAYOUT_FIELD_TYPES:
            continue

        child_fields: list[dict[str, Any]] = []
        if df.fieldtype in TABLE_FIELD_TYPES and df.options:
            try:
                child_meta = frappe.get_meta(df.options)
                child_section = ""
                for child_df in child_meta.fields:
                    if child_df.fieldtype == "Section Break":
                        child_section = str(child_df.label or "").strip()
                        continue
                    if (
                        not child_df.fieldname
                        or child_df.fieldtype in LAYOUT_FIELD_TYPES
                    ):
                        continue
                    child_fields.append(
                        _field_to_schema(
                            child_df,
                            section_label=child_section,
                        )
                    )
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    "Classic Chatbot Child Metadata Error",
                )

        fields.append(
            _field_to_schema(
                df,
                section_label=current_section,
                child_fields=child_fields,
            )
        )

    return {
        "doctype": doctype,
        "module": meta.module,
        "title_field": meta.title_field,
        "search_fields": list(meta.get_search_fields() or []),
        "is_submittable": bool(meta.is_submittable),
        "is_child_table": bool(meta.istable),
        "fields": fields,
    }


def get_field_metadata(doctype: str, fieldname: str) -> dict[str, Any] | None:
    schema = get_live_doctype_schema(doctype)
    for field in schema["fields"]:
        if field["fieldname"] == fieldname:
            return field
    return None


def get_related_fields(doctype: str, fieldname: str) -> list[dict[str, Any]]:
    """
    Return candidate sibling fields without any field-specific hardcoding.

    Same section, nearby order, shared label tokens and common linked targets are
    treated as metadata evidence. The LLM still makes the semantic decision.
    """
    schema = get_live_doctype_schema(doctype)
    fields = schema["fields"]
    target = next((f for f in fields if f["fieldname"] == fieldname), None)
    if not target:
        return []

    def tokens(field: dict[str, Any]) -> set[str]:
        text = " ".join(
            [
                str(field.get("fieldname") or ""),
                str(field.get("label") or ""),
                str(field.get("section_label") or ""),
                str(field.get("options") or ""),
            ]
        ).lower()
        return {
            token
            for token in re.findall(r"[a-z0-9]+", text.replace("_", " "))
            if len(token) >= 3
            and token
            not in {"the", "and", "for", "from", "custom", "field"}
        }

    target_tokens = tokens(target)
    target_idx = cint(target.get("idx"))
    candidates: list[tuple[int, dict[str, Any]]] = []

    for other in fields:
        if other["fieldname"] == fieldname or other.get("read_only"):
            continue
        score = 0
        if target.get("section_label") and (
            target.get("section_label") == other.get("section_label")
        ):
            score += 4
        distance = abs(target_idx - cint(other.get("idx"))) if target_idx else 99
        if distance <= 4:
            score += 3
        elif distance <= 10:
            score += 1
        score += 2 * len(target_tokens & tokens(other))
        if target.get("options") and target.get("options") == other.get("options"):
            score += 2
        if score > 0:
            candidates.append((score, other))

    candidates.sort(key=lambda item: (-item[0], cint(item[1].get("idx"))))
    return [item[1] for item in candidates[:12]]


# -----------------------------------------------------------------------------
# Deterministic schema validation
# -----------------------------------------------------------------------------


def _validate_data_option(df, value: Any) -> str | None:
    option = str(df.options or "").strip().lower()
    text = str(value).strip()
    if option == "email" and not EMAIL_PATTERN.match(text):
        return "Enter one valid email address, for example name@example.com."
    if option in {"phone", "mobile"}:
        digit_count = len(re.sub(r"\D", "", text))
        if (
            not PHONE_ALLOWED_PATTERN.match(text)
            or digit_count < 7
            or digit_count > 15
        ):
            return "Enter a valid phone number containing 7 to 15 digits."
    if option == "url" and not URL_PATTERN.match(text):
        return "Enter a complete URL beginning with http://, https://, or www."
    return None


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        Decimal(str(value).replace(",", ""))
        return True
    except (InvalidOperation, ValueError, TypeError):
        return False


def _is_integer(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        number = Decimal(str(value).replace(",", ""))
        return number == number.to_integral_value()
    except (InvalidOperation, ValueError, TypeError):
        return False


def _valid_time(value: Any) -> bool:
    if hasattr(value, "hour") and hasattr(value, "minute"):
        return True
    match = TIME_PATTERN.match(str(value).strip())
    if not match:
        return False
    hour, minute, second = match.groups()
    return (
        0 <= int(hour) <= 23
        and 0 <= int(minute) <= 59
        and 0 <= int(second or 0) <= 59
    )


def _validate_field_value(
    *,
    df,
    value: Any,
    row_data: dict[str, Any],
    target_fieldname: str,
    child_fieldname: str | None = None,
    row_index: int | None = None,
    is_required: bool = False,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    label = df.label or df.fieldname

    if is_required and _is_empty(value):
        prefix = f"Row {row_index}: " if row_index else ""
        return [
            _make_issue(
                issue_type="mandatory",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=f"{prefix}{label} is mandatory and cannot be blank.",
                expected=f"A valid value for {label}",
            )
        ]

    if _is_empty(value):
        return issues

    fieldtype = df.fieldtype

    if fieldtype == "Link" and df.options:
        try:
            if not frappe.db.exists(df.options, value):
                issues.append(
                    _make_issue(
                        issue_type="invalid_link",
                        fieldname=target_fieldname,
                        child_fieldname=child_fieldname,
                        row_index=row_index,
                        label=label,
                        value=value,
                        message=(
                            f"{label} value '{value}' does not exist in {df.options}."
                        ),
                        expected=f"An existing {df.options} record",
                    )
                )
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Classic Chatbot Link Validation Error",
            )

    elif fieldtype == "Dynamic Link" and df.options:
        linked_doctype = row_data.get(df.options)
        if linked_doctype and frappe.db.exists("DocType", linked_doctype):
            try:
                if not frappe.db.exists(linked_doctype, value):
                    issues.append(
                        _make_issue(
                            issue_type="invalid_dynamic_link",
                            fieldname=target_fieldname,
                            child_fieldname=child_fieldname,
                            row_index=row_index,
                            label=label,
                            value=value,
                            message=(
                                f"{label} value '{value}' does not exist in "
                                f"{linked_doctype}."
                            ),
                            expected=f"An existing {linked_doctype} record",
                        )
                    )
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    "Classic Chatbot Dynamic Link Validation Error",
                )

    elif fieldtype == "Select" and df.options:
        options = [
            option.strip()
            for option in str(df.options).splitlines()
            if option.strip()
        ]
        if options and str(value).strip() not in options:
            issues.append(
                _make_issue(
                    issue_type="invalid_select",
                    fieldname=target_fieldname,
                    child_fieldname=child_fieldname,
                    row_index=row_index,
                    label=label,
                    value=value,
                    message=f"'{value}' is not a valid option for {label}.",
                    expected="One of: " + ", ".join(options[:20]),
                )
            )

    elif fieldtype == "Data":
        expected = _validate_data_option(df, value)
        if expected:
            issues.append(
                _make_issue(
                    issue_type="invalid_format",
                    fieldname=target_fieldname,
                    child_fieldname=child_fieldname,
                    row_index=row_index,
                    label=label,
                    value=value,
                    message=f"{label} has an invalid format.",
                    expected=expected,
                )
            )

    elif fieldtype in {"Int", "Long Int"} and not _is_integer(value):
        issues.append(
            _make_issue(
                issue_type="invalid_integer",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=f"{label} must contain a whole number.",
                expected="An integer such as 0, 1, or 25",
            )
        )

    elif fieldtype in {"Float", "Currency", "Percent", "Duration"} and not _is_number(value):
        issues.append(
            _make_issue(
                issue_type="invalid_number",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=f"{label} must contain a numeric value.",
                expected="A valid number",
            )
        )

    elif fieldtype == "Check" and value not in {0, 1, True, False, "0", "1"}:
        issues.append(
            _make_issue(
                issue_type="invalid_check",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=f"{label} must be checked or unchecked.",
                expected="0 or 1",
            )
        )

    elif fieldtype == "Date":
        try:
            getdate(value)
        except Exception:
            issues.append(
                _make_issue(
                    issue_type="invalid_date",
                    fieldname=target_fieldname,
                    child_fieldname=child_fieldname,
                    row_index=row_index,
                    label=label,
                    value=value,
                    message=f"{label} is not a valid date.",
                    expected="A valid date, normally YYYY-MM-DD",
                )
            )

    elif fieldtype == "Datetime":
        try:
            get_datetime(value)
        except Exception:
            issues.append(
                _make_issue(
                    issue_type="invalid_datetime",
                    fieldname=target_fieldname,
                    child_fieldname=child_fieldname,
                    row_index=row_index,
                    label=label,
                    value=value,
                    message=f"{label} is not a valid date and time.",
                    expected="A valid date-time value",
                )
            )

    elif fieldtype == "Time" and not _valid_time(value):
        issues.append(
            _make_issue(
                issue_type="invalid_time",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=f"{label} is not a valid time.",
                expected="HH:MM or HH:MM:SS",
            )
        )

    elif fieldtype == "JSON":
        try:
            if isinstance(value, str):
                json.loads(value)
        except Exception:
            issues.append(
                _make_issue(
                    issue_type="invalid_json",
                    fieldname=target_fieldname,
                    child_fieldname=child_fieldname,
                    row_index=row_index,
                    label=label,
                    value=value,
                    message=f"{label} contains invalid JSON.",
                    expected="A valid JSON object or array",
                )
            )

    max_length = cint(getattr(df, "length", 0))
    if max_length and isinstance(value, str) and len(value) > max_length:
        issues.append(
            _make_issue(
                issue_type="maximum_length",
                fieldname=target_fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=value,
                message=(
                    f"{label} is {len(value)} characters long, but the maximum "
                    f"length is {max_length}."
                ),
                expected=f"Maximum {max_length} characters",
            )
        )

    return issues


def deterministic_validate(
    doctype: str,
    doc_data: dict[str, Any],
    *,
    required_fields: set[str] | None = None,
    visible_fields: set[str] | None = None,
    mode: str = "full",
    changed_field: str | None = None,
) -> list[dict[str, Any]]:
    meta = frappe.get_meta(doctype)
    required_fields = required_fields or set()
    visible_fields = visible_fields or set()
    issues: list[dict[str, Any]] = []

    for df in meta.fields:
        if not df.fieldname or df.fieldtype in LAYOUT_FIELD_TYPES:
            continue
        if mode == "field" and changed_field and df.fieldname != changed_field:
            continue

        is_visible = (
            df.fieldname in visible_fields if visible_fields else not bool(df.hidden)
        )
        if not is_visible:
            continue

        is_required = False
        if mode == "full":
            is_required = (
                df.fieldname in required_fields
                if required_fields
                else bool(df.reqd)
            )

        value = doc_data.get(df.fieldname)
        issues.extend(
            _validate_field_value(
                df=df,
                value=value,
                row_data=doc_data,
                target_fieldname=df.fieldname,
                is_required=is_required,
            )
        )

        if df.fieldtype not in TABLE_FIELD_TYPES or not df.options:
            continue
        rows = value or []
        if not isinstance(rows, list):
            issues.append(
                _make_issue(
                    issue_type="invalid_table",
                    fieldname=df.fieldname,
                    label=df.label or df.fieldname,
                    value=value,
                    message=f"{df.label or df.fieldname} must contain table rows.",
                    expected="A list of child-table rows",
                )
            )
            continue

        try:
            child_meta = frappe.get_meta(df.options)
        except Exception:
            continue

        for row_index, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                continue
            for child_df in child_meta.fields:
                if (
                    not child_df.fieldname
                    or child_df.fieldtype in LAYOUT_FIELD_TYPES
                ):
                    continue
                issues.extend(
                    _validate_field_value(
                        df=child_df,
                        value=row.get(child_df.fieldname),
                        row_data=row,
                        target_fieldname=df.fieldname,
                        child_fieldname=child_df.fieldname,
                        row_index=row_index,
                        is_required=(mode == "full" and bool(child_df.reqd)),
                    )
                )

    return _deduplicate_issues(issues)


# -----------------------------------------------------------------------------
# Semantic field profiles
# -----------------------------------------------------------------------------


def _schema_for_model(
    schema: dict[str, Any],
    *,
    visible_fields: set[str] | None,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    visible_fields = visible_fields or set()
    output: list[dict[str, Any]] = []

    for field in schema.get("fields") or []:
        if len(output) >= config["max_fields"]:
            break
        fieldname = str(field.get("fieldname") or "")
        if (
            not fieldname
            or field.get("hidden")
            or field.get("read_only")
            or _field_is_sensitive(fieldname)
        ):
            continue
        if visible_fields and fieldname not in visible_fields:
            continue

        row = {
            "fieldname": fieldname,
            "label": field.get("label"),
            "fieldtype": field.get("fieldtype"),
            "description": str(field.get("description") or "")[:300],
            "options": str(field.get("options") or "")[:200],
            "select_options": field.get("select_options") or [],
            "linked_doctype": field.get("linked_doctype"),
            "section_label": field.get("section_label"),
            "idx": field.get("idx"),
            "mandatory": field.get("mandatory"),
        }

        if field.get("fieldtype") in TABLE_FIELD_TYPES:
            row["child_fields"] = [
                {
                    "fieldname": child.get("fieldname"),
                    "label": child.get("label"),
                    "fieldtype": child.get("fieldtype"),
                    "description": str(child.get("description") or "")[:240],
                    "options": str(child.get("options") or "")[:160],
                    "section_label": child.get("section_label"),
                    "idx": child.get("idx"),
                }
                for child in (field.get("child_fields") or [])[:40]
                if not child.get("hidden")
                and not child.get("read_only")
                and not _field_is_sensitive(child.get("fieldname"))
            ]

        output.append(row)

    return output


def _ollama_chat_json(
    *,
    messages: list[dict[str, Any]],
    response_schema: dict[str, Any],
    config: dict[str, Any],
    think: bool = False,
    num_predict: int | None = None,
) -> dict[str, Any]:
    url = str(config["local_url"]).rstrip("/") + "/api/chat"
    payload = {
        "model": config["local_model"],
        "messages": messages,
        "stream": False,
        "format": response_schema,
        "think": bool(think),
        "keep_alive": "30m",
        "options": {
            "temperature": config["temperature"],
            "num_ctx": config["num_ctx"],
            "num_predict": num_predict or config["num_predict"],
            "top_p": 0.85,
            "repeat_penalty": 1.05,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=config["timeout"])
        response.raise_for_status()
    except requests.Timeout as exc:
        raise RuntimeError(
            f"Local AI validation timed out after {config['timeout']} seconds."
        ) from exc
    except requests.ConnectionError as exc:
        raise RuntimeError(
            f"Ollama server se connection nahi ho paya. URL check karein: "
            f"{config['local_url']}"
        ) from exc
    except requests.HTTPError as exc:
        response_text = ""
        try:
            response_text = exc.response.text[:1000] if exc.response else ""
        except Exception:
            pass
        raise RuntimeError(
            f"Ollama HTTP request fail hui: {exc}. {response_text}"
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Ollama request fail hui: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Ollama ne valid HTTP JSON response nahi diya.") from exc

    raw = ((payload.get("message") or {}).get("content") or payload.get("response") or "")
    if not raw:
        raise RuntimeError("Local model returned an empty validation response.")
    if isinstance(raw, dict):
        result = raw
    else:
        try:
            result = json.loads(str(raw).strip())
        except json.JSONDecodeError as exc:
            raise RuntimeError("Local model returned invalid validation JSON.") from exc
    if not isinstance(result, dict):
        raise RuntimeError("Local model validation result must be a JSON object.")
    return result


def _fallback_field_profiles(model_fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for field in model_fields:
        purpose_parts = [
            str(field.get("label") or field.get("fieldname") or ""),
            str(field.get("description") or ""),
        ]
        if field.get("linked_doctype"):
            purpose_parts.append(
                "Linked to " + str(field["linked_doctype"].get("doctype") or "")
            )
        profiles.append(
            {
                "fieldname": field.get("fieldname"),
                "child_fieldname": None,
                "purpose": " ".join(part for part in purpose_parts if part).strip(),
                "expected_value_kinds": [
                    str(field.get("fieldtype") or "general field value")
                ],
                "incompatible_value_kinds": [],
                "related_fieldnames": [],
                "confidence": 0.35,
            }
        )
        for child in field.get("child_fields") or []:
            profiles.append(
                {
                    "fieldname": field.get("fieldname"),
                    "child_fieldname": child.get("fieldname"),
                    "purpose": " ".join(
                        [
                            str(child.get("label") or child.get("fieldname") or ""),
                            str(child.get("description") or ""),
                        ]
                    ).strip(),
                    "expected_value_kinds": [
                        str(child.get("fieldtype") or "general field value")
                    ],
                    "incompatible_value_kinds": [],
                    "related_fieldnames": [],
                    "confidence": 0.30,
                }
            )
    return profiles


def _get_or_build_field_profiles(
    doctype: str,
    model_fields: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], bool, str | None]:
    schema_hash = _stable_hash(model_fields)
    cache_key = (
        f"classic_chatbot:field_profiles:v3:{doctype}:"
        f"{config['local_model']}:{schema_hash}"
    )
    cached = _cache_get(cache_key)
    if isinstance(cached, dict) and isinstance(cached.get("field_profiles"), list):
        return cached["field_profiles"], True, None

    if not config["use_field_profiles"]:
        return _fallback_field_profiles(model_fields), False, None

    system_prompt = """
You are a form-semantics architect.

Infer the intended purpose of every supplied Frappe field from its fieldname,
label, fieldtype, description, options, linked DocType, section, order and
sibling fields. Use normal world knowledge to understand common concepts such
as a person's name, organisation, designation, phone, email, address, project,
date, quantity and identifier. Do not create company-specific business rules.

For every parent and child field return a concise semantic profile:
- purpose: what information belongs in the field
- expected_value_kinds: semantic kinds that fit
- incompatible_value_kinds: clearly different kinds that do not fit
- related_fieldnames: exact supplied fields that may hold related parts
- confidence

Important:
- Analyse the form globally, not only nearby fields.
- When separate fields represent parts of one concept, list them as related.
- Never invent fieldnames.
- Return only JSON matching the supplied schema.
""".strip()

    user_payload = {
        "doctype": doctype,
        "fields": model_fields,
        "response_schema": FIELD_PROFILE_SCHEMA,
    }

    try:
        result = _ollama_chat_json(
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(
                        user_payload,
                        ensure_ascii=False,
                        default=str,
                        separators=(",", ":"),
                    ),
                },
            ],
            response_schema=FIELD_PROFILE_SCHEMA,
            config=config,
            think=False,
            num_predict=max(2500, config["num_predict"]),
        )
        raw_profiles = result.get("field_profiles") or []
        valid_parent = {field["fieldname"]: field for field in model_fields}
        profiles: list[dict[str, Any]] = []

        for profile in raw_profiles:
            if not isinstance(profile, dict):
                continue
            fieldname = str(profile.get("fieldname") or "").strip()
            child_fieldname = str(profile.get("child_fieldname") or "").strip() or None
            if fieldname not in valid_parent:
                continue
            if child_fieldname:
                valid_child = {
                    str(child.get("fieldname") or "")
                    for child in valid_parent[fieldname].get("child_fields") or []
                }
                if child_fieldname not in valid_child:
                    continue
            related = [
                str(item).strip()
                for item in (profile.get("related_fieldnames") or [])
                if str(item).strip() in valid_parent
            ]
            profiles.append(
                {
                    "fieldname": fieldname,
                    "child_fieldname": child_fieldname,
                    "purpose": re.sub(
                        r"\s+", " ", str(profile.get("purpose") or "").strip()
                    )[:500],
                    "expected_value_kinds": [
                        re.sub(r"\s+", " ", str(item).strip())[:120]
                        for item in (profile.get("expected_value_kinds") or [])[:10]
                        if str(item).strip()
                    ],
                    "incompatible_value_kinds": [
                        re.sub(r"\s+", " ", str(item).strip())[:120]
                        for item in (profile.get("incompatible_value_kinds") or [])[:10]
                        if str(item).strip()
                    ],
                    "related_fieldnames": related[:12],
                    "confidence": max(
                        0.0,
                        min(1.0, float(profile.get("confidence") or 0)),
                    ),
                }
            )

        if not profiles:
            profiles = _fallback_field_profiles(model_fields)
        _cache_set(
            cache_key,
            {"field_profiles": profiles},
            config["profile_cache_seconds"],
        )
        return profiles, False, None
    except Exception as exc:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Field Profile Error",
        )
        return _fallback_field_profiles(model_fields), False, str(exc)


# -----------------------------------------------------------------------------
# Feedback memory: prompt-level learning without hardcoded if/else rules
# -----------------------------------------------------------------------------


def _feedback_doctype_exists() -> bool:
    try:
        return bool(frappe.db.exists("DocType", "AI Validation Feedback"))
    except Exception:
        return False


def _load_feedback_examples(
    doctype: str,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    if not config["use_feedback_memory"] or not _feedback_doctype_exists():
        return []
    try:
        rows = frappe.get_all(
            "AI Validation Feedback",
            filters={"reference_doctype": doctype},
            fields=[
                "fieldname",
                "child_fieldname",
                "verdict",
                "value_preview",
                "issue_json",
                "creation",
            ],
            order_by="creation desc",
            limit_page_length=config["max_feedback_examples"],
            ignore_permissions=True,
        )
    except Exception:
        return []

    examples: list[dict[str, Any]] = []
    for row in rows:
        issue = _safe_json(row.get("issue_json"), {}) or {}
        examples.append(
            {
                "fieldname": row.get("fieldname"),
                "child_fieldname": row.get("child_fieldname"),
                "verdict": row.get("verdict"),
                "value_preview": row.get("value_preview"),
                "previous_ai_message": issue.get("message"),
                "previous_expected": issue.get("expected"),
            }
        )
    return examples


@frappe.whitelist()
def submit_validation_feedback(
    doctype: str,
    fieldname: str,
    verdict: str,
    issue: Any = None,
    current_value: Any = None,
    docname: str | None = None,
    child_fieldname: str | None = None,
    row_index: Any = None,
):
    if frappe.session.user == "Guest":
        frappe.throw(_("Please log in before submitting feedback."))
    config = get_validation_config()
    if not _is_doctype_allowed(doctype, config):
        frappe.throw(_("AI validation is not enabled for this DocType."))
    if verdict not in {"correct_issue", "false_positive"}:
        frappe.throw(_("Invalid feedback verdict."))
    if not _feedback_doctype_exists():
        return {
            "stored": False,
            "message": "AI Validation Feedback DocType is not installed.",
        }

    issue_data = _safe_json(issue, {}) or {}
    row = frappe.get_doc(
        {
            "doctype": "AI Validation Feedback",
            "reference_doctype": doctype,
            "reference_name": docname,
            "fieldname": str(fieldname or "")[:140],
            "child_fieldname": str(child_fieldname or "")[:140] or None,
            "row_index": cint(row_index) or None,
            "verdict": verdict,
            "value_preview": str(_json_safe(current_value, 240) or "")[:240],
            "issue_json": json.dumps(
                issue_data,
                ensure_ascii=False,
                default=str,
            )[:10000],
            "feedback_user": frappe.session.user,
            "model": config["local_model"],
        }
    )
    row.insert(ignore_permissions=True)
    return {"stored": True, "name": row.name}


# -----------------------------------------------------------------------------
# Full-form semantic validation
# -----------------------------------------------------------------------------


def _serialize_form_for_ai(
    *,
    doctype: str,
    doc_data: dict[str, Any],
    schema: dict[str, Any],
    model_fields: list[dict[str, Any]],
    field_profiles: list[dict[str, Any]],
    visible_fields: set[str] | None,
    mode: str,
    changed_field: str | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    visible_fields = visible_fields or set()
    profile_map = {
        (profile.get("fieldname"), profile.get("child_fieldname")): profile
        for profile in field_profiles
    }
    model_map = {field["fieldname"]: field for field in model_fields}
    fields: list[dict[str, Any]] = []

    for field in schema.get("fields") or []:
        fieldname = str(field.get("fieldname") or "")
        if fieldname not in model_map:
            continue
        if visible_fields and fieldname not in visible_fields:
            continue

        value = doc_data.get(fieldname)
        row = dict(model_map[fieldname])
        row["profile"] = profile_map.get((fieldname, None), {})
        row["is_empty"] = _is_empty(value)
        row["current_value"] = (
            None
            if _is_empty(value)
            else _json_safe(value, config["max_value_chars"])
        )
        row["candidate_related_fields"] = [
            {
                "fieldname": related.get("fieldname"),
                "label": related.get("label"),
                "fieldtype": related.get("fieldtype"),
                "is_empty": _is_empty(doc_data.get(related.get("fieldname"))),
            }
            for related in get_related_fields(doctype, fieldname)[:10]
        ]

        if field.get("fieldtype") in TABLE_FIELD_TYPES:
            child_rows: list[dict[str, Any]] = []
            raw_rows = value if isinstance(value, list) else []
            for row_index, child_row in enumerate(
                raw_rows[: config["max_child_rows"]],
                start=1,
            ):
                if not isinstance(child_row, dict):
                    continue
                child_values = []
                for child in field.get("child_fields") or []:
                    child_fieldname = str(child.get("fieldname") or "")
                    if (
                        not child_fieldname
                        or child.get("hidden")
                        or child.get("read_only")
                        or _field_is_sensitive(child_fieldname)
                    ):
                        continue
                    child_value = child_row.get(child_fieldname)
                    child_values.append(
                        {
                            "fieldname": child_fieldname,
                            "label": child.get("label"),
                            "fieldtype": child.get("fieldtype"),
                            "description": str(child.get("description") or "")[:240],
                            "options": str(child.get("options") or "")[:160],
                            "profile": profile_map.get(
                                (fieldname, child_fieldname), {}
                            ),
                            "is_empty": _is_empty(child_value),
                            "current_value": (
                                None
                                if _is_empty(child_value)
                                else _json_safe(
                                    child_value,
                                    config["max_value_chars"],
                                )
                            ),
                        }
                    )
                child_rows.append(
                    {"row_index": row_index, "fields": child_values}
                )
            row["rows"] = child_rows

        fields.append(row)

    return {
        "doctype": doctype,
        "mode": mode,
        "changed_field": changed_field,
        "instruction": (
            "In field mode, review the changed field deeply while using the "
            "complete form as context. In full mode, review every non-empty "
            "editable field and every supplied child-row value."
        ),
        "fields": fields,
    }


def _call_semantic_validator(
    *,
    doctype: str,
    semantic_payload: dict[str, Any],
    feedback_examples: list[dict[str, Any]],
    mode: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    cache_key = (
        "classic_chatbot:semantic:v9:"
        + _stable_hash(
            {
                "model": config["local_model"],
                "payload": semantic_payload,
                "feedback": feedback_examples,
            }
        )
    )
    cached = _cache_get(cache_key)
    if isinstance(cached, dict):
        cached["cached"] = True
        return cached

    system_prompt = """
You are a powerful full-form semantic validation agent for Frappe/ERPNext.

Your job is not ordinary datatype validation. Another deterministic validator
already handles mandatory fields, Links, Select options, dates and numbers.
Your job is to understand the meaning of every entered value and verify that it
was placed in the most appropriate supplied field.

For each non-empty field, reason globally:
1. Classify what the entered value most likely represents using normal language
   and world knowledge.
2. Read the supplied field profile, label, fieldname, type, description,
   options, linked DocType, section and sibling fields to infer the field's
   intended nature.
3. Compare the value with the current field and with every other supplied field.
4. Detect when data belongs in a different field, when several concepts are
   combined in one field, when one concept should be split across available
   component fields, or when related fields contradict each other.
5. For child tables, perform the same review for each supplied row.

Important behaviour:
- Do not depend on hardcoded field names. Use the supplied metadata and profiles.
- You MAY use general world knowledge to distinguish concepts such as a human
  name, organisation, job title, email, phone, address, project/site, identifier,
  date, quantity, amount and free-form notes.
- Do not invent company-specific rules, unavailable fields or unavailable values.
- Analyse all candidate fields, not only nearby or token-similar fields.
- A field can be syntactically valid but semantically wrong.
- If one entered string contains several clearly separable pieces and suitable
  fields exist, report the current field and suggest exact supplied fields.
- Only return a blocking error when the mismatch is clear and confidence is high.
- Return a warning for a useful but less certain concern.
- Avoid false positives for genuinely ambiguous values.
- Previous feedback examples are guidance: "false_positive" means a similar AI
  finding was rejected by a human; "correct_issue" means it was confirmed.
- Suggested corrections must use exact supplied fieldnames. Do not overwrite a
  non-empty target field unless the proposed value is clearly consistent.
- Write message and expected in clear professional Hinglish using Roman script.
- Keep each issue concise, specific and actionable.
- Before output, internally re-check every proposed issue against the complete
  form and remove weak or speculative findings.
- Return only JSON matching the response schema.
""".strip()

    user_payload = {
        "task": (
            "Validate whether every entered value is in the correct field and "
            "whether the right kind of data was entered."
        ),
        "doctype": doctype,
        "form": semantic_payload,
        "human_feedback_examples": feedback_examples,
        "response_schema": AI_RESPONSE_SCHEMA,
    }

    result = _ollama_chat_json(
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(
                    user_payload,
                    ensure_ascii=False,
                    default=str,
                    separators=(",", ":"),
                ),
            },
        ],
        response_schema=AI_RESPONSE_SCHEMA,
        config=config,
        think=(mode == "full" and config["use_thinking_on_full_check"]),
    )
    result["cached"] = False
    result["model"] = config["local_model"]
    _cache_set(cache_key, result, config["cache_seconds"])
    return result


def _filter_ai_issues(
    *,
    raw_result: dict[str, Any],
    schema: dict[str, Any],
    doc_data: dict[str, Any],
    mode: str,
    changed_field: str | None,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    parent_fields = {
        str(field.get("fieldname")): field
        for field in schema.get("fields") or []
        if field.get("fieldname")
    }
    issues: list[dict[str, Any]] = []

    for raw_issue in raw_result.get("issues") or []:
        if not isinstance(raw_issue, dict):
            continue
        fieldname = str(raw_issue.get("fieldname") or "").strip()
        child_fieldname = str(raw_issue.get("child_fieldname") or "").strip() or None
        if fieldname not in parent_fields:
            continue
        if mode == "field" and changed_field and fieldname != changed_field:
            continue

        field_schema = parent_fields[fieldname]
        label = field_schema.get("label") or fieldname
        valid_child_fields: set[str] = set()
        if child_fieldname:
            valid_child_fields = {
                str(child.get("fieldname"))
                for child in field_schema.get("child_fields") or []
                if child.get("fieldname")
            }
            if child_fieldname not in valid_child_fields:
                continue
            child_schema = next(
                child
                for child in field_schema.get("child_fields") or []
                if child.get("fieldname") == child_fieldname
            )
            label = child_schema.get("label") or child_fieldname

        try:
            confidence = max(
                0.0,
                min(1.0, float(raw_issue.get("confidence") or 0)),
            )
        except Exception:
            confidence = 0.0
        severity = str(raw_issue.get("severity") or "warning").lower()
        if severity not in {"error", "warning"}:
            severity = "warning"
        threshold = (
            config["confidence_threshold"]
            if severity == "error"
            else config["warning_confidence_threshold"]
        )
        if confidence < threshold:
            continue

        message = re.sub(r"\s+", " ", str(raw_issue.get("message") or "")).strip()
        expected = re.sub(r"\s+", " ", str(raw_issue.get("expected") or "")).strip()
        if not message:
            continue

        row_index = raw_issue.get("row_index")
        try:
            row_index = int(row_index) if row_index is not None else None
        except Exception:
            row_index = None

        suggested_fieldnames = []
        for item in raw_issue.get("suggested_fieldnames") or []:
            item = str(item or "").strip()
            if item in parent_fields and item not in suggested_fieldnames:
                suggested_fieldnames.append(item)

        suggestions: list[dict[str, Any]] = []
        for suggestion in raw_issue.get("suggested_corrections") or []:
            if not isinstance(suggestion, dict):
                continue
            target = str(suggestion.get("fieldname") or "").strip()
            if target not in parent_fields:
                continue
            value = _json_safe(suggestion.get("value"), config["max_value_chars"])
            current_target_value = doc_data.get(target)
            # Never allow automatic overwrite of an already-filled different value.
            if (
                not _is_empty(current_target_value)
                and str(current_target_value).strip() != str(value or "").strip()
            ):
                continue
            suggestions.append({"fieldname": target, "value": value})

        issues.append(
            _make_issue(
                issue_type=str(raw_issue.get("issue_type") or "semantic_mismatch")[:80],
                fieldname=fieldname,
                child_fieldname=child_fieldname,
                row_index=row_index,
                label=label,
                value=doc_data.get(fieldname),
                severity=severity,
                source="local_ai_full_form",
                confidence=confidence,
                message=message[:700],
                expected=expected[:900],
                detected_value_kind=str(
                    raw_issue.get("detected_value_kind") or ""
                )[:160],
                expected_value_kind=str(
                    raw_issue.get("expected_value_kind") or ""
                )[:160],
                suggested_fieldnames=suggested_fieldnames[:12],
                suggested_corrections=suggestions[:12],
            )
        )

    return _deduplicate_issues(issues)


def _deduplicate_issues(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for issue in issues:
        key = (
            issue.get("type"),
            issue.get("fieldname"),
            issue.get("child_fieldname"),
            issue.get("row_index"),
            re.sub(r"\s+", " ", str(issue.get("message") or "")).lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        output.append(issue)
    return output


def _skipped_result(doctype: str | None, reason: str) -> dict[str, Any]:
    return {
        "ok": True,
        "skipped": True,
        "skip_reason": reason,
        "doctype": doctype,
        "docname": None,
        "issue_count": 0,
        "blocking_issue_count": 0,
        "first_issue": None,
        "issues": [],
        "warnings": [],
        "model_used": "Validation skipped",
        "ai_error": None,
        "ai_cached": False,
        "profile_cached": False,
        "profile_error": None,
    }


def validate_document_payload(
    doctype: str,
    doc_data: dict[str, Any],
    *,
    required_fields: set[str] | None = None,
    visible_fields: set[str] | None = None,
    run_ai: bool = True,
    mode: str = "full",
    changed_field: str | None = None,
) -> dict[str, Any]:
    config = get_validation_config()
    if not config["enabled"]:
        return _skipped_result(doctype, "AI validation is disabled.")
    if not _is_doctype_allowed(doctype, config):
        return _skipped_result(doctype, "DocType is not enabled for AI validation.")

    mode = "field" if mode == "field" else "full"
    changed_field = str(changed_field or "").strip() or None
    schema = get_live_doctype_schema(doctype)

    deterministic_issues = deterministic_validate(
        doctype,
        doc_data,
        required_fields=required_fields,
        visible_fields=visible_fields,
        mode=mode,
        changed_field=changed_field,
    )

    ai_issues: list[dict[str, Any]] = []
    ai_error = None
    ai_cached = False
    profile_cached = False
    profile_error = None

    if run_ai:
        model_fields = _schema_for_model(
            schema,
            visible_fields=visible_fields,
            config=config,
        )
        profiles, profile_cached, profile_error = _get_or_build_field_profiles(
            doctype,
            model_fields,
            config,
        )
        semantic_payload = _serialize_form_for_ai(
            doctype=doctype,
            doc_data=doc_data,
            schema=schema,
            model_fields=model_fields,
            field_profiles=profiles,
            visible_fields=visible_fields,
            mode=mode,
            changed_field=changed_field,
            config=config,
        )
        feedback_examples = _load_feedback_examples(doctype, config)

        # In field mode, do not call AI for a blank field. Clearing a field should
        # simply remove its prior semantic issue; mandatory checks run on save.
        changed_is_blank = bool(
            mode == "field"
            and changed_field
            and _is_empty(doc_data.get(changed_field))
        )
        if not changed_is_blank:
            try:
                raw_ai_result = _call_semantic_validator(
                    doctype=doctype,
                    semantic_payload=semantic_payload,
                    feedback_examples=feedback_examples,
                    mode=mode,
                    config=config,
                )
                ai_cached = bool(raw_ai_result.get("cached"))
                ai_issues = _filter_ai_issues(
                    raw_result=raw_ai_result,
                    schema=schema,
                    doc_data=doc_data,
                    mode=mode,
                    changed_field=changed_field,
                    config=config,
                )
            except Exception as exc:
                ai_error = str(exc)
                frappe.log_error(
                    frappe.get_traceback(),
                    "Classic Chatbot Full-Form AI Validation Error",
                )

    all_issues = _deduplicate_issues(deterministic_issues + ai_issues)
    blocking_issues = [
        issue
        for issue in all_issues
        if issue.get("severity") == "error" or config["block_warnings"]
    ]

    if ai_error and config["fail_closed"] and mode == "full":
        unavailable = _make_issue(
            issue_type="ai_unavailable",
            fieldname="",
            label="Local AI Validator",
            message="Local AI semantic validation service available nahi hai.",
            expected="Ollama service aur configured model check karein, phir save karein.",
            source="system",
        )
        all_issues.append(unavailable)
        blocking_issues.append(unavailable)

    return {
        "ok": not bool(blocking_issues),
        "skipped": False,
        "skip_reason": None,
        "doctype": doctype,
        "docname": doc_data.get("name"),
        "mode": mode,
        "changed_field": changed_field,
        "issue_count": len(all_issues),
        "blocking_issue_count": len(blocking_issues),
        "first_issue": (
            blocking_issues[0]
            if blocking_issues
            else (all_issues[0] if all_issues else None)
        ),
        "issues": all_issues[:100],
        "warnings": [
            issue for issue in all_issues if issue.get("severity") == "warning"
        ][:100],
        "model_used": f"Local Ollama semantic agent: {config['local_model']}",
        "ai_error": ai_error,
        "ai_cached": ai_cached,
        "profile_cached": profile_cached,
        "profile_error": profile_error,
        "feedback_memory_used": bool(_load_feedback_examples(doctype, config)),
    }


# -----------------------------------------------------------------------------
# Public API and server-side guard
# -----------------------------------------------------------------------------


@frappe.whitelist()
def warm_validation_profiles(
    doctype: str,
    visible_fields: Any = None,
):
    """Build and cache semantic field-purpose profiles before the user saves."""
    config = get_validation_config()
    if not _is_doctype_allowed(doctype, config):
        return {"ok": True, "skipped": True, "profile_count": 0}
    if not (
        frappe.has_permission(doctype, "read")
        or frappe.has_permission(doctype, "create")
        or frappe.has_permission(doctype, "write")
    ):
        frappe.throw(_("You do not have permission to inspect {0}.").format(doctype))

    schema = get_live_doctype_schema(doctype)
    model_fields = _schema_for_model(
        schema,
        visible_fields=_parse_name_set(visible_fields),
        config=config,
    )
    profiles, cached, error = _get_or_build_field_profiles(
        doctype,
        model_fields,
        config,
    )
    return {
        "ok": not bool(error),
        "skipped": False,
        "profile_count": len(profiles),
        "cached": cached,
        "error": error,
        "model": config["local_model"],
    }


@frappe.whitelist()
def get_validator_client_config(doctype: str | None = None):
    config = get_validation_config()
    return {
        "enabled": config["enabled"] and _is_doctype_allowed(doctype, config),
        "allowed_doctypes": sorted(config["allowed_doctypes"]),
        "realtime_enabled": config["realtime_enabled"],
        "realtime_debounce_ms": config["realtime_debounce_ms"],
        "fail_closed": config["fail_closed"],
        "model": config["local_model"],
    }


@frappe.whitelist()
def validate_current_form(
    doctype: str | None = None,
    docname: str | None = None,
    doc: Any = None,
    required_fields: Any = None,
    visible_fields: Any = None,
    run_ai: Any = 1,
    mode: str = "full",
    changed_field: str | None = None,
):
    if not doctype:
        frappe.throw(_("DocType is required."))
    if not frappe.db.exists("DocType", doctype):
        frappe.throw(_("DocType {0} does not exist.").format(doctype))

    config = get_validation_config()
    if not _is_doctype_allowed(doctype, config):
        return _skipped_result(doctype, "DocType is not enabled for AI validation.")

    if not (
        frappe.has_permission(doctype, "read")
        or frappe.has_permission(doctype, "create")
        or frappe.has_permission(doctype, "write")
    ):
        frappe.throw(_("You do not have permission to validate {0}.").format(doctype))

    doc_data = _safe_json(doc, {}) or {}
    if not isinstance(doc_data, dict):
        frappe.throw(_("Current document data is invalid."))
    doc_data["doctype"] = doctype
    if docname and not doc_data.get("name"):
        doc_data["name"] = docname

    return validate_document_payload(
        doctype,
        doc_data,
        required_fields=_parse_name_set(required_fields),
        visible_fields=_parse_name_set(visible_fields),
        run_ai=_as_bool(run_ai, True),
        mode=mode,
        changed_field=changed_field,
    )


def _should_skip_server_validation(doc) -> bool:
    if not doc:
        return True
    config = get_validation_config()
    if not config["enabled"] or not _is_doctype_allowed(doc.doctype, config):
        return True
    if getattr(doc.flags, "ignore_ai_validation", False):
        return True
    if any(
        _as_bool(getattr(frappe.flags, flag, False))
        for flag in ("in_install", "in_migrate", "in_patch", "in_test", "in_import")
    ):
        return True
    try:
        if frappe.get_meta(doc.doctype).istable:
            return True
    except Exception:
        return True
    if not config["validate_background"]:
        request = getattr(getattr(frappe, "local", None), "request", None)
        if request is None:
            return True
    return False


def _issues_to_html(issues: list[dict[str, Any]]) -> str:
    rows = []
    for issue in issues[:8]:
        label = frappe.utils.escape_html(issue.get("label") or "Field")
        message = frappe.utils.escape_html(issue.get("message") or "")
        expected = frappe.utils.escape_html(issue.get("expected") or "")
        location = f" (Row {cint(issue['row_index'])})" if issue.get("row_index") else ""
        expected_html = f"<br><small>Expected: {expected}</small>" if expected else ""
        rows.append(f"<li><b>{label}{location}</b>: {message}{expected_html}</li>")
    return "<ul>" + "".join(rows) + "</ul>"

def strict_ai_backend_validator(doc, method=None):
    """
    Production-safe server-side document validation.

    Important:
    - Save ke andar local AI call nahi hoti.
    - Only deterministic schema errors block save.
    - Semantic AI validation client-side/API validation se chalegi.
    """

    if _should_skip_server_validation(doc):
        return

    try:
        result = validate_document_payload(
            doc.doctype,
            doc.as_dict(),
            run_ai=False,
            mode="full",
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Server Validation Error",
        )

        # Production save ko unexpected AI-validator error se block mat karo.
        return

    issues = result.get("issues") or []

    blocking_issues = [
        issue
        for issue in issues
        if issue.get("severity") == "error"
    ]

    if not blocking_issues:
        return

    frappe.throw(
        _issues_to_html(blocking_issues),
        title=_("Form Validation"),
        exc=frappe.ValidationError,
    )