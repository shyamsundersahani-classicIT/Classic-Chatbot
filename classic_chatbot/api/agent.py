import json
import requests
import frappe

from classic_chatbot.api.agent_tools import (
    safe_json,
    clean_doc,
    run_tool,
    detect_field_from_question,
)


def get_llm_config():
    return {
        # Local Ollama Config
        # "local_model": frappe.conf.get("classic_chatbot_local_model") or "qwen2.5:7b",
        "local_model": frappe.conf.get("classic_chatbot_local_model") or "llama3.2",
        "local_base_url": frappe.conf.get("classic_chatbot_local_url") or "http://localhost:11434",
        
        # Groq Config (API Key Inserted Here)
        "groq_api_key": frappe.conf.get("classic_chatbot_groq_api_key") or "",
        "groq_model": frappe.conf.get("classic_chatbot_groq_model") or "llama-3.1-8b-instant",
        
        "temperature": float(frappe.conf.get("classic_chatbot_temperature") or 0.2),
    }


def call_ollama(messages, conf):
    url = conf["local_base_url"].rstrip("/") + "/api/chat"

    payload = {
        "model": conf["local_model"],
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": conf["temperature"],
            "num_ctx": 2048
        },
    }

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

    data = response.json()
    return data.get("message", {}).get("content") or data.get("response") or ""


def call_groq(messages, conf):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conf['groq_api_key']}"
    }

    payload = {
        "model": conf["groq_model"],
        "messages": messages,
        "temperature": conf["temperature"],
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]


def check_if_answer_is_poor(answer):
    if not answer or len(answer.strip()) < 10:
        return True
        
    bad_phrases = [
        "i don't know", "i am not sure", "mujhe nahi pata", 
        "i cannot determine", "context read ho gaya", "an ai language model",
        "i am sorry"
    ]
    
    ans_lower = answer.lower()
    for phrase in bad_phrases:
        if phrase in ans_lower:
            return True
            
    return False

# ... (get_llm_config, call_ollama, call_groq, check_if_answer_is_poor functions waise hi rahenge) ...

def smart_llm_router(messages, preferred_model="auto"):
    conf = get_llm_config()
    
    # CASE 1: User strictly wants GROQ API
    if preferred_model == "groq":
        if conf.get("groq_api_key"):
            frappe.logger().info("[Classic Chatbot] User selected Groq API directly...")
            try:
                groq_answer = call_groq(messages, conf)
                return groq_answer, "☁️ Groq API (Manual)"
            except Exception as groq_err:
                return f"Groq fail ho gaya. Error: {str(groq_err)}", "⚠️ Error"
        else:
            return "Groq select kiya par API Key configure nahi hai.", "⚠️ Error"

    # CASE 2: User strictly wants LOCAL MODEL
    if preferred_model == "local":
        frappe.logger().info("[Classic Chatbot] User selected Local Model directly...")
        try:
            local_answer = call_ollama(messages, conf)
            return local_answer, "🖥️ Local Model (Strict)"
        except Exception as e:
            return f"Local server down hai. Error: {str(e)}", "⚠️ Error"

    # CASE 3: AUTO (Local First, Fallback to Groq)
    try:
        frappe.logger().info("[Classic Chatbot] Trying Local Model (Auto)...")
        local_answer = call_ollama(messages, conf)
        
        if check_if_answer_is_poor(local_answer):
            frappe.logger().info("[Classic Chatbot] Local answer poor tha, Groq par switch kar rahe hain...")
            raise Exception("Poor Quality Answer from Local Model")
            
        return local_answer, "🖥️ Local Model (Auto)"
        
    except Exception as e:
        frappe.logger().error(f"[Classic Chatbot] Local Fallback Triggered: {e}")
        
        if conf.get("groq_api_key"):
            frappe.logger().info("[Classic Chatbot] Calling Groq API via Auto Fallback...")
            try:
                groq_answer = call_groq(messages, conf)
                return groq_answer, "☁️ Groq API (Fallback)"
            except Exception as groq_err:
                return f"Local aur Groq dono fail ho gaye. Error: {str(groq_err)}", "⚠️ Error"
        else:
            return f"Local model fail ho gaya aur Groq ki API key nahi mili. Local Error: {str(e)}", "⚠️ Error"


# ... (build_tool_plan, run_tool_plan, fallback_answer, build_final_messages waise hi rahenge) ...


@frappe.whitelist()
def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
    if not question:
        frappe.throw("Question is required")

    context = {
        "doctype": doctype,
        "docname": docname,
        "doc": clean_doc(safe_json(doc, {})),
        "route": safe_json(route, []),
        "error": error,
        "user": frappe.session.user,
    }

    plan = build_tool_plan(question, context)
    tool_outputs = run_tool_plan(plan)

    model_used = "System"
    try:
        # NAYA: pass preferred_model to router
        answer, model_used = smart_llm_router(build_final_messages(question, context, tool_outputs), preferred_model)
    except Exception as e:
        answer = fallback_answer(question, context, tool_outputs)
        answer += f"\n\nAI model connect nahi hua: {str(e)}"
        model_used = "⚙️ Fallback Rule"

    return {
        "answer": answer,
        "model_used": model_used, 
        "tools_used": [step.get("tool") for step in plan],
    }

# ... (inspect_current_context waisa hi rahega)


def build_tool_plan(question, context):
    q = (question or "").lower()

    doctype = context.get("doctype")
    doc = context.get("doc")
    error = context.get("error")
    docname = context.get("docname")

    plan = []

    if doctype:
        plan.append({
            "tool": "get_doctype_schema",
            "args": {
                "doctype": doctype,
            },
        })

    if doctype and isinstance(doc, dict):
        plan.append({
            "tool": "analyze_current_doc",
            "args": {
                "doctype": doctype,
                "doc": doc,
            },
        })

    if error:
        plan.append({
            "tool": "explain_error",
            "args": {
                "doctype": doctype,
                "doc": doc,
                "error": error,
            },
        })

    field_hint = detect_field_from_question(question)
    if doctype and field_hint:
        plan.append({
            "tool": "get_field_help",
            "args": {
                "doctype": doctype,
                "fieldname": field_hint,
            },
        })

    if doctype and docname and any(word in q for word in ["record", "document", "doc", "details", "data", "open"]):
        plan.append({
            "tool": "get_record",
            "args": {
                "doctype": doctype,
                "name": docname,
            },
        })

    # NAYA TOOL: Check Linked DocTypes
    if doctype and any(word in q for word in ["link", "connect", "relation", "kis kis", "kaha use"]):
        plan.append({
            "tool": "get_linked_doctypes",
            "args": {
                "doctype": doctype,
            },
        })

    return plan


def run_tool_plan(plan):
    outputs = []

    for step in plan:
        tool_name = step.get("tool")
        args = step.get("args") or {}

        # Custom Tool Execution
        if tool_name == "get_linked_doctypes":
            target_dt = args.get("doctype")
            try:
                links = frappe.get_all("DocField", filters={"fieldtype": "Link", "options": target_dt}, pluck="parent")
                custom_links = frappe.get_all("Custom Field", filters={"fieldtype": "Link", "options": target_dt}, pluck="dt")
                unique_links = sorted(list(set(links + custom_links)))
                
                result = {
                    "message": f"{target_dt} in doctypes ke sath link hai.",
                    "linked_doctypes": unique_links,
                    "total_links": len(unique_links)
                }
            except Exception as e:
                result = {"error": f"Links fetch karne me error aaya: {str(e)}"}
        else:
            result = run_tool(tool_name, args)

        outputs.append({
            "tool": tool_name,
            "args": args,
            "result": result,
        })

    return outputs


def fallback_answer(question, context, tool_outputs):
    doctype = context.get("doctype")
    error = context.get("error")

    lines = []

    if doctype:
        lines.append(f"Aap abhi **{doctype}** DocType par ho.")

    for item in tool_outputs:
        if item.get("tool") == "analyze_current_doc":
            result = item.get("result") or {}
            missing = result.get("missing_required") or []
            invalid_links = result.get("invalid_links") or []

            if missing:
                lines.append("")
                lines.append("Mandatory fields missing lag rahi hain:")
                for row in missing:
                    lines.append(f"- {row.get('label')} ({row.get('fieldname')})")

            if invalid_links:
                lines.append("")
                lines.append("Invalid link values mil rahe hain:")
                for row in invalid_links:
                    lines.append(
                        f"- {row.get('label')}: {row.get('value')} not found in {row.get('linked_doctype')}"
                    )

    if error:
        lines.append("")
        lines.append(f"Last error: {error}")

    if not lines:
        lines.append("Context read ho gaya, lekin specific issue detect nahi hua. Question thoda detail me likho.")

    return "\n".join(lines)


import json
import frappe
import json
import frappe
import json
import frappe

def build_final_messages(question, context, tool_outputs):
    system_prompt = """
<role>
You are an Elite ERPNext Principal Architect, Business Consultant, and Master Debugger. You understand both the BUSINESS side (Procurement, HR, Manufacturing) and the DEVELOPER side (Frappe framework, custom apps). You speak logically, empathetically, and strictly like a highly experienced Indian tech mentor.
</role>

<language_rules>
1. STRICTLY use natural "Hinglish" (Hindi in English script). 
2. NEVER use Devnagari script (e.g., no हिंदी).
3. Tone: Crisp, professional, calm, and slightly informal ("Bhai", "Dekhiye", "Samajhiye").
</language_rules>

<universal_directives>
1. TOOL DATA IS ABSOLUTE GOD: If `tool_outputs` has data (linked doctypes, missing fields, error tracebacks), your ONLY job is to format and present that data neatly. DO NOT give generic UI tutorials if the exact data is already in your hands.
2. ZERO HALLUCINATION: If the context or tool_output does not contain the answer, say "Bhai, context me ye info nahi hai, thoda detail do." Never invent Frappe features or fake fields.
3. NO PARROTING: NEVER start with "Aapne pucha hai..." or repeat the user's prompt. The first word must be the start of the solution.
4. ANTI-FRUSTRATION PROTOCOL: If the user sounds angry, confused, or says "Samajh nahi aaya", drop all technical terms. Explain using a daily-life analogy (like a shopkeeper, rate-card, or simple math).
5. DOMAIN INTELLIGENCE: Automatically adapt your answer based on the DocType. If it's a 'Material Request', think like a Procurement Manager. If it's 'Student', think like an Education Admin.
6. NO OVER-MESSAGING / YAPPING (NEW & CRITICAL): If the user asks a simple question (e.g., "X me kya ayega?"), give a simple, direct 1-line answer. DO NOT add unasked details, DO NOT talk about other fields, and DO NOT use analogies unless the user explicitly asks for "easy language" or says they didn't understand. Stop typing as soon as the exact question is answered.
</universal_directives>

<situational_logic>
Analyze the user's intent and apply the EXACT matching situation:

- SITUATION 1: THE DATA EXTRACTOR (User asks for Lists, Links, or Connections)
  Trigger: "List do", "Print karo", "Kisse link hai?", "Sabke naam batao".
  Action: Parse `tool_outputs` for 'linked_doctypes' or lists. Print a clean, bulleted list immediately. NO extra lectures on how to use search bars.

- SITUATION 2: THE BUSINESS CONSULTANT (User asks what a field/tab does)
  Trigger: "X ka kya kaam hai?", "Y me kya ayega?", "Billing tab kya hai?"
  Action: Explain the REAL-WORLD business reason in exactly 1 crisp line. E.g., "Cost Center me aapko apni company ka wo department select karna hota hai jiske account me ye kharcha ya kamai judegi." NEVER stretch the answer.

- SITUATION 3: THE DEBUGGER (User is stuck with an Error or Save issue)
  Trigger: "Error aa raha hai", "Save kyu nahi ho raha?", "Mandatory kya hai?"
  Action: Look at `tool_outputs` for 'missing_required', 'invalid_links', or 'error'. Say "Bhai, ye error isliye aa raha hai kyunki..." and list the exact missing fields or invalid data. Give the direct solution.

- SITUATION 4: THE DEVELOPER / CUSTOMIZATION (User asks about code or backend)
  Trigger: "Custom field kaise banau?", "Client script", "Backend".
  Action: Give crisp developer instructions (Frappe ORM, JS API) assuming the user is a developer working on a custom app. 

- SITUATION 5: THE VAGUE QUERY (User gives no context)
  Trigger: "Ye kya hai?", "Kaise use karu?", "Help".
  Action: Identify the current DocType from context. Give a 1-line summary of what the form does, and list 2 quick steps to use it. If completely vague, ask: "Bhai, exact field ya error ka naam batao taaki sahi solution de saku."

- SITUATION 6: THE FRUSTRATED USER (User didn't understand)
  Trigger: "Samajh nahi aaya", "Theek se batao", "Easy language".
  Action: Apologize briefly ("Sorry bhai, simple bhasha me batata hu:"). Give a 2-line ELI5 (Explain Like I'm 5) real-world analogy. No ERP terminology.
</situational_logic>
"""

    # --- SMART CONTEXT FILTERING (MAGIC FIX) ---
    q_lower = (question or "").lower()
    filtered_outputs = []

    for item in tool_outputs:
        tool_name = item.get("tool")
        result = item.get("result")

        if tool_name == "get_doctype_schema" and isinstance(result, dict) and "fields" in result:
            matched_fields = []
            mandatory_fields = []
            
            for f in result.get("fields", []):
                f_name = str(f.get("fieldname", "")).lower()
                f_label = str(f.get("label", "")).lower()
                
                if f_name in q_lower or (f_label and f_label in q_lower):
                    matched_fields.append(f)
                
                if f.get("reqd"):
                    mandatory_fields.append(f)

            if matched_fields:
                result["fields"] = matched_fields
            elif any(word in q_lower for word in ["missing", "mandatory", "error", "save", "kya bacha"]):
                result["fields"] = mandatory_fields
            else:
                result["fields"] = "Hidden to save payload size. User didn't ask for specific fields."
        
        filtered_outputs.append(item)

    payload = {
        "question": question,
        "current_context": context,
        "tool_outputs": filtered_outputs,
    }

    payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False, default=str)

    MAX_PAYLOAD_CHARS = 25000 
    if len(payload_str) > MAX_PAYLOAD_CHARS:
        frappe.logger().warning("[Classic Chatbot] Payload too large, truncating data...")
        payload_str = payload_str[:MAX_PAYLOAD_CHARS] + '... [DATA TRUNCATED]'

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": payload_str,
        },
    ]
@frappe.whitelist()
def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
    if not question:
        frappe.throw("Question is required")

    context = {
        "doctype": doctype,
        "docname": docname,
        "doc": clean_doc(safe_json(doc, {})),
        "route": safe_json(route, []),
        "error": error,
        "user": frappe.session.user,
    }

    plan = build_tool_plan(question, context)
    tool_outputs = run_tool_plan(plan)

    model_used = "System"
    try:
        # NAYA: pass preferred_model to router
        answer, model_used = smart_llm_router(build_final_messages(question, context, tool_outputs), preferred_model)
    except Exception as e:
        answer = fallback_answer(question, context, tool_outputs)
        answer += f"\n\nAI model connect nahi hua: {str(e)}"
        model_used = "⚙️ Fallback Rule"

    return {
        "answer": answer,
        "model_used": model_used, 
        "tools_used": [step.get("tool") for step in plan],
    }

@frappe.whitelist()
def inspect_current_context(doctype=None, docname=None, doc=None, route=None, error=None):
    context = {
        "doctype": doctype,
        "docname": docname,
        "doc": clean_doc(safe_json(doc, {})),
        "route": safe_json(route, []),
        "error": error,
        "user": frappe.session.user,
    }

    plan = build_tool_plan("analyze current form", context)
    outputs = run_tool_plan(plan)

    return {
        "context": context,
        "tools_used": [p.get("tool") for p in plan],
        "tool_outputs": outputs,
    }