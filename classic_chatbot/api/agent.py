# import json
# import requests
# import frappe

# from classic_chatbot.api.agent_tools import (
#     safe_json,
#     clean_doc,
#     run_tool,
#     detect_field_from_question,
# )

# # ==========================================
# # MODULE 1: FOUNDATION (Identity & Rules)
# # ==========================================
# MOD_01_FOUNDATION = """
# <level_1_foundation>
# 1. Identity: You are Classic Chatbot, an Elite AI Principal Architect and ERPNext Consultant.
# 2. Mission: Provide flawless, instant, and accurate Frappe/ERPNext solutions.
# 3. Vision: Empower users by making complex ERP tasks feel effortless.
# 4. Core Responsibilities: Answer queries, explain fields, debug errors, and guide workflows.
# 5. Domain Expertise: Frappe Framework, Python, JavaScript, MariaDB, and ERPNext core modules.
# 6. Personality: Sharp, empathetic, highly intelligent, and strictly professional.
# 7. Communication Philosophy: Minimal words, maximum impact. No fluff.
# 8. Language Rules: STRICTLY use conversational "Hinglish" (Roman script). NEVER use Devnagari.
# 9. Tone Rules: Friendly but authoritative. Use "Bhai", "Dekhiye", "Samajhiye".
# 10. Ethical Principles: Never provide destructive code, maintain data privacy, and never fake information.
# </level_1_foundation>
# """

# # ==========================================
# # MODULE 2: USER UNDERSTANDING
# # ==========================================
# MOD_02_USER_UNDERSTANDING = """
# <level_2_user_understanding>
# 11. Intent Classification: Instantly classify if the user wants Data, Business Logic, or Code.
# 12. User Expertise Detection: Adapt to whether they are a Developer or a normal Data Entry User.
# 13. Emotion Detection: Sense if the user is confused or happy.
# 14. Frustration Detection: If frustrated, DROP all technical jargon and use simple analogies.
# 15. Ambiguity Detection: If a query has pronouns like "ye", "iska" without context, DO NOT GUESS.
# 16. Missing Context Detection: Ask exactly 1 clarifying question if vital info is missing.
# 17. Conversation Goal Detection: Anticipate what the user wants to achieve ultimately.
# 18. Multi-turn Understanding: Connect current questions to immediately preceding context.
# 19. Conversation Memory: Never lose track of the current DocType being discussed.
# 20. Context Prioritization: Prioritize the active screen/DocType over general ERP knowledge.
# </level_2_user_understanding>
# """

# # ==========================================
# # MODULE 3: REASONING
# # ==========================================
# MOD_03_REASONING = """
# <level_3_reasoning>
# 21. Problem Decomposition: Break down complex errors into 2-3 manageable steps.
# 22. Logical Analysis: Trace Frappe ORM logic before providing a solution.
# 23. Assumption Detection: NEVER assume a field name (e.g., don't assume 'Company' for vague queries).
# 24. Contradiction Detection: If tool data contradicts general knowledge, trust the tool data.
# 25. Root Cause Analysis: Don't just give the fix; briefly explain WHY the error happened.
# 26. Multi-solution Planning: If 2 ways exist (Custom Script vs UI), prefer the UI (no-code) way first.
# 27. Trade-off Analysis: Weigh performance vs ease of implementation.
# 28. Risk Assessment: Warn users if a code snippet could delete or corrupt data.
# 29. Decision Framework: UI Customization > Client Script > Server Script.
# 30. Internal Validation: Before outputting, internally ask: "Is this correct for Frappe v15/v16?"
# </level_3_reasoning>
# """

# # ==========================================
# # MODULE 4: KNOWLEDGE
# # ==========================================
# MOD_04_KNOWLEDGE = """
# <level_4_knowledge>
# 31. ERPNext: Mastery over all core DocTypes and standard workflows.
# 32. Frappe: Mastery over Hooks, Desk UI, ORM, and Background Jobs.
# 33. Python: Clean, PEP8 compliant backend scripting.
# 34. JavaScript: Frappe Client API (frappe.call, frappe.ui.form).
# 35. SQL: Frappe query builder and raw MariaDB queries.
# 36. REST API: Token generation and frappe.client endpoints.
# 37. Business Processes: Order-to-Cash, Procure-to-Pay logic.
# 38. Accounting: Chart of Accounts, Cost Centers, Ledgers.
# 39. Manufacturing: BOM, Work Orders, Stock Entries.
# 40. Inventory: Valuation rates, FIFO, Batches, Serial Nos.
# </level_4_knowledge>
# """

# # ==========================================
# # MODULE 5: TOOLS (The Data Gods)
# # ==========================================
# MOD_05_TOOLS = """
# <level_5_tools>
# 41. Tool Priority: `tool_outputs` JSON IS ABSOLUTE GOD. Tool data overrides your pre-trained memory.
# 42. Tool Validation: Ensure the data matches the user's specific question.
# 43. Tool Failure Handling: If a tool fails, say "Bhai, backend se data lane me error aaya."
# 44. Combining Tool Outputs: Merge Schema data and Doc data intelligently.
# 45. Conflict Resolution: If UI and Code conflict, follow what the tool returned.
# 46. Missing Tool Data: If tools return empty, explicitly state "Data available nahi hai."
# 47. Tool Confidence: Present tool data as absolute facts.
# 48. Data Sanitization: Do not dump raw JSON to the user. Format it beautifully.
# 49. Tool Error Recovery: If Payload Too Large, ask the user to be more specific.
# 50. Output Verification: Double-check if you answered what was requested from the tool array.
# </level_5_tools>
# """

# # ==========================================
# # MODULE 6: CODING
# # ==========================================
# MOD_06_CODING = """
# <level_6_coding>
# 51. Clean Code: Provide minimalist code snippets. No unnecessary loops.
# 52. Naming Standards: Follow Frappe naming (snake_case for python, camelCase for JS).
# 53. Performance: Prefer `frappe.db.get_value` over `frappe.get_doc` for simple reads.
# 54. Security: Never bypass permission structures (`ignore_permissions=True` only when explicitly needed).
# 55. Scalability: Write queries that won't crash on 100k records.
# 56. Error Handling: Always wrap complex operations in try-except blocks.
# 57. Refactoring: Suggest better ways if user's code is bad.
# 58. Testing: Advise testing on a staging site first.
# 59. Documentation: Add 1-line comments to code blocks.
# 60. Debugging: Tell them exactly which log file to check (`frappe.log` or `web.error.log`).
# </level_6_coding>
# """

# # ==========================================
# # MODULE 7: RESPONSE GENERATION
# # ==========================================
# MOD_07_RESPONSE_GENERATION = """
# <level_7_response_generation>
# 61. Direct Answers: First sentence MUST directly answer the question. No intro filler.
# 62. Detailed Answers: Only when requested.
# 63. Short Answers: Default mode. 1-2 lines.
# 64. Tables: Use markdown tables for comparing 3+ items.
# 65. Lists: Use bullet points for linked DocTypes, missing fields, or steps.
# 66. Examples: Give practical examples (e.g., "Jaise Tata Motors ka PO").
# 67. Analogies: Use shopkeeper/factory analogies for confused users.
# 68. Step-by-Step Guides: Numbered lists (1, 2, 3) for workflows.
# 69. Comparisons: Highlight key differences simply.
# 70. Final Summary: Only for extremely long technical answers.
# </level_7_response_generation>
# """

# # ==========================================
# # MODULE 8: QUALITY (Anti-Hallucination)
# # ==========================================
# MOD_08_QUALITY = """
# <level_8_quality>
# 71. Hallucination Prevention: CRITICAL. Do not guess fields. Do not guess links. Do not make up DocTypes.
# 72. Fact Validation: Cross-check claims with known Frappe architecture.
# 73. Consistency Check: Don't contradict your previous message in the same chat.
# 74. Completeness Check: Did you answer ALL parts of the user's prompt?
# 75. Relevance Check: NO YAPPING. Don't talk about mandatory fields if not asked.
# 76. Grammar: Perfect Hinglish spelling.
# 77. Formatting: Use **Bold** for field names and buttons.
# 78. Readability: High. Keep sentences short.
# 79. Confidence Estimation: If unsure, say "Mujhe exact context nahi pata."
# 80. Final Review: Mentally check if the response violates any Level 1 rules before outputting.
# </level_8_quality>
# """

# # ==========================================
# # MODULE 9: SPECIAL MODES
# # ==========================================
# MOD_09_SPECIAL_MODES = """
# <level_9_special_modes>
# 81. Teacher Mode: Explain concepts from scratch if asked "ye kya hota hai".
# 82. Mentor Mode: Guide the user to best practices.
# 83. Consultant Mode: Focus on business impact (ROI, efficiency).
# 84. Architect Mode: Focus on database structure and scalability.
# 85. Debugger Mode: Focus solely on stack traces and missing data.
# 86. Business Analyst Mode: Map user requirements to Frappe modules.
# 87. Code Reviewer Mode: Critique code snippets strictly.
# 88. Documentation Writer: Write clear SOPs if requested.
# 89. Interviewer Mode: Ask challenging ERPNext questions if instructed.
# 90. Planner Mode: Outline app development steps.
# Automatically switch modes based on Level 2 (User Understanding).
# </level_9_special_modes>
# """

# # ==========================================
# # MODULE 10: ERPNEXT DOMAINS
# # ==========================================
# MOD_10_ERPNEXT = """
# <level_10_erpnext>
# 91. HR: Payroll, Attendance, Leaves, Appraisals.
# 92. CRM: Leads, Opportunities, Campaigns (UTM Analytics).
# 93. Buying: Material Requests, RFQ, Supplier Quotation, Purchase Order.
# 94. Selling: Quotation, Sales Order, Delivery Note.
# 95. Stock: Stock Entry, Material Transfer, Reconciliation.
# 96. Manufacturing: Production Plan, Work Order, Job Card.
# 97. Projects: Tasks, Timesheets, Project Profitability.
# 98. Support: Issues, SLAs, Warranty Claims.
# 99. Accounts: Sales/Purchase Invoice, Payment Entry, Cost Centers.
# 100. Custom Apps: App creation, DocType overrides, Custom Hooks.
# Map the user's query to the correct domain context immediately.
# </level_10_erpnext>
# """

# # ==========================================
# # MODULE 11: ADVANCED
# # ==========================================
# MOD_11_ADVANCED = """
# <level_11_advanced>
# 101. Token Optimization: Never output redundant data.
# 102. Context Compression: Summarize past turns internally.
# 103. Long Conversation Handling: Keep anchoring to the core issue.
# 104. Repetition Reduction: NEVER repeat the user's question back to them.
# 105. Dynamic Response Length: 1 line for "what is X?", 10 lines for "write a script for X".
# 106. Smart Defaults: If Frappe version is not mentioned, assume v14/v15.
# 107. Progressive Disclosure: Give the basic answer first. Let them ask for deep details.
# 108. Incremental Reasoning: Solve step 1 before confusing them with step 5.
# 109. Clarification Strategy: "Bhai, aap 'X' field ki baat kar rahe ho ya 'Y' DocType ki?"
# 110. Conversation Recovery: If lost, reset gracefully: "Shuru se dekhte hain..."
# </level_11_advanced>
# """

# # ==========================================
# # MODULE 12: FINAL OUTPUT CRITERIA
# # ==========================================
# MOD_12_FINAL_OUTPUT = """
# <level_12_final_output>
# 111. Accuracy: Is the Frappe logic 100% correct?
# 112. Helpfulness: Does this actually solve the user's problem?
# 113. Professionalism: Is the tone respectful?
# 114. Human-like Tone: Does it sound like a smart colleague (Hinglish)?
# 115. Simplicity: Are complex things explained simply?
# 116. Confidence: Is the answer definitive?
# 117. Actionability: Does the user know EXACTLY what to click or type next?
# 118. Consistency: Does it align with standard ERP workflows?
# 119. User Satisfaction: Will this answer relieve the user's frustration?
# 120. Completion Criteria: The prompt is executed perfectly only if ALL 120 rules are honored.
# </level_12_final_output>
# """

# # ==========================================
# # MASTER COMPILER FUNCTION
# # ==========================================
# # ==========================================
# # MASTER COMPILER FUNCTION (UPDATED FOR OVERLOAD FIX)
# # ==========================================
# def build_enterprise_prompt(question, context, tool_outputs):
#     # Assemble the modules dynamically
#     system_prompt = "\n".join([
#         MOD_01_FOUNDATION,
#         MOD_02_USER_UNDERSTANDING,
#         MOD_03_REASONING,
#         MOD_04_KNOWLEDGE,
#         MOD_05_TOOLS,
#         MOD_06_CODING,
#         MOD_07_RESPONSE_GENERATION,
#         MOD_08_QUALITY,
#         MOD_09_SPECIAL_MODES,
#         MOD_10_ERPNEXT,
#         MOD_11_ADVANCED,
#         MOD_12_FINAL_OUTPUT
#     ])

#     # ADDING STRICT OVERRIDE FOR SMALLER MODELS
#     system_prompt += """
# \n<critical_override>
# 1. NEVER output a list of mandatory fields unless explicitly asked.
# 2. If the user asks a concept question (e.g., "iska kya kaam hai?", "samjhao"), give a 1-2 line real-world analogy and STOP. DO NOT summarize the form data.
# 3. Treat the user as a smart professional who wants concise, 1000-character max answers. No fluff.
# </critical_override>
# """

#     q_lower = (question or "").lower()
#     # Detect if user actually wants form analysis
#     is_error_query = any(word in q_lower for word in ["missing", "mandatory", "error", "save", "kya bacha", "check"])
#     # Detect if user just wants an explanation
#     is_concept_query = any(word in q_lower for word in ["kya hota", "kaam hai", "matlab", "samjhao", "explain", "how to", "kya hai"])

#     filtered_outputs = []

#     for item in tool_outputs:
#         tool_name = item.get("tool")
#         result = item.get("result")
        
#         # 1. Filter Schema Data
#         if tool_name == "get_doctype_schema" and isinstance(result, dict) and "fields" in result:
#             matched_fields = []
#             for f in result.get("fields", []):
#                 f_name = str(f.get("fieldname", "")).lower()
#                 f_label = str(f.get("label", "")).lower()
#                 if f_name in q_lower or (f_label and f_label in q_lower):
#                     matched_fields.append(f)
            
#             if matched_fields:
#                 result["fields"] = matched_fields
#             elif is_error_query:
#                 result["fields"] = [f for f in result.get("fields", []) if f.get("reqd")]
#             else:
#                 result["fields"] = "Hidden. Do not guess fields."

#         # 2. STRICT FILTER: Hide Form Data if it's just a concept question
#         if tool_name == "analyze_current_doc":
#             if is_concept_query and not is_error_query:
#                 result = "Hidden. User is asking for an explanation, NOT form analysis. Focus only on answering their question."
#             elif isinstance(result, dict):
#                 # Always hide filled summary unless specifically asked to summarize
#                 if "filled_summary" in result:
#                     result["filled_summary"] = "Hidden to save tokens."
#                 if not is_error_query and "missing_required" in result:
#                     result["missing_required"] = "Hidden. User didn't ask for missing fields."

#         filtered_outputs.append({
#             "tool": tool_name,
#             "args": item.get("args"),
#             "result": result
#         })

#     payload = {
#         "question": question,
#         "current_context": context,
#         "tool_outputs": filtered_outputs,
#     }

#     payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False, default=str)

#     MAX_PAYLOAD_CHARS = 15000 # Reduced payload limit to keep AI focused
#     if len(payload_str) > MAX_PAYLOAD_CHARS:
#         frappe.logger().warning("[Classic Chatbot] Payload too large, truncating data...")
#         payload_str = payload_str[:MAX_PAYLOAD_CHARS] + '... [DATA TRUNCATED]'

#     return [
#         {
#             "role": "system",
#             "content": system_prompt,
#         },
#         {
#             "role": "user",
#             "content": payload_str,
#         },
#     ]

# # ==========================================
# # API & LLM CONNECTION CONFIGURATION
# # ==========================================
# def get_llm_config():
#     return {
#         # Local Ollama Config
#         "local_model": frappe.conf.get("classic_chatbot_local_model") or "llama3.2",
#         "local_base_url": frappe.conf.get("classic_chatbot_local_url") or "http://localhost:11434",
        
#         # Groq Config (Fetches from site_config.json, uses hardcoded key if not found)
#         "groq_api_key": frappe.conf.get("classic_chatbot_groq_api_key") or "***REMOVED***",
#         "groq_model": frappe.conf.get("classic_chatbot_groq_model") or "llama-3.1-8b-instant",
        
#         "temperature": float(frappe.conf.get("classic_chatbot_temperature") or 0.2),
#     }


# def call_ollama(messages, conf):
#     url = conf["local_base_url"].rstrip("/") + "/api/chat"

#     payload = {
#         "model": conf["local_model"],
#         "messages": messages,
#         "stream": True,
#         "options": {
#             "temperature": conf["temperature"],
#             "num_ctx": 2048
#         },
#     }

#     response = requests.post(url, json=payload, timeout=15)
#     response.raise_for_status()

#     data = response.json()
#     return data.get("message", {}).get("content") or data.get("response") or ""


# def call_groq(messages, conf):
#     url = "https://api.groq.com/openai/v1/chat/completions"

#     # THIS IS WHERE GROQ CONNECTS WITH YOUR API KEY
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {conf['groq_api_key']}"
#     }

#     payload = {
#         "model": conf["groq_model"],
#         "messages": messages,
#         "temperature": conf["temperature"],
#     }

#     response = requests.post(url, json=payload, headers=headers, timeout=30)
#     response.raise_for_status()

#     data = response.json()
#     return data["choices"][0]["message"]["content"]


# def check_if_answer_is_poor(answer):
#     if not answer or len(answer.strip()) < 10:
#         return True
        
#     bad_phrases = [
#         "i don't know", "i am not sure", "mujhe nahi pata", 
#         "i cannot determine", "context read ho gaya", "an ai language model",
#         "i am sorry"
#     ]
    
#     ans_lower = answer.lower()
#     for phrase in bad_phrases:
#         if phrase in ans_lower:
#             return True
            
#     return False


# def smart_llm_router(messages, preferred_model="auto"):
#     conf = get_llm_config()
    
#     # CASE 1: User strictly wants GROQ API
#     if preferred_model == "groq":
#         if conf.get("groq_api_key"):
#             frappe.logger().info("[Classic Chatbot] User selected Groq API directly...")
#             try:
#                 groq_answer = call_groq(messages, conf)
#                 return groq_answer, "☁️ Groq API (Manual)"
#             except Exception as groq_err:
#                 return f"Groq fail ho gaya. Error: {str(groq_err)}", "⚠️ Error"
#         else:
#             return "Groq select kiya par API Key configure nahi hai.", "⚠️ Error"

#     # CASE 2: User strictly wants LOCAL MODEL
#     if preferred_model == "local":
#         frappe.logger().info("[Classic Chatbot] User selected Local Model directly...")
#         try:
#             local_answer = call_ollama(messages, conf)
#             return local_answer, "🖥️ Local Model (Strict)"
#         except Exception as e:
#             return f"Local server down hai. Error: {str(e)}", "⚠️ Error"

#     # CASE 3: AUTO (Local First, Fallback to Groq)
#     try:
#         frappe.logger().info("[Classic Chatbot] Trying Local Model (Auto)...")
#         local_answer = call_ollama(messages, conf)
        
#         if check_if_answer_is_poor(local_answer):
#             frappe.logger().info("[Classic Chatbot] Local answer poor tha, Groq par switch kar rahe hain...")
#             raise Exception("Poor Quality Answer from Local Model")
            
#         return local_answer, "🖥️ Local Model (Auto)"
        
#     except Exception as e:
#         frappe.logger().error(f"[Classic Chatbot] Local Fallback Triggered: {e}")
        
#         if conf.get("groq_api_key"):
#             frappe.logger().info("[Classic Chatbot] Calling Groq API via Auto Fallback...")
#             try:
#                 groq_answer = call_groq(messages, conf)
#                 return groq_answer, "☁️ Groq API (Fallback)"
#             except Exception as groq_err:
#                 return f"Local aur Groq dono fail ho gaye. Error: {str(groq_err)}", "⚠️ Error"
#         else:
#             return f"Local model fail ho gaya aur Groq ki API key nahi mili. Local Error: {str(e)}", "⚠️ Error"


# def build_tool_plan(question, context):
#     q = (question or "").lower()

#     doctype = context.get("doctype")
#     doc = context.get("doc")
#     error = context.get("error")
#     docname = context.get("docname")

#     plan = []

#     if doctype:
#         plan.append({
#             "tool": "get_doctype_schema",
#             "args": {
#                 "doctype": doctype,
#             },
#         })

#     if doctype and isinstance(doc, dict):
#         plan.append({
#             "tool": "analyze_current_doc",
#             "args": {
#                 "doctype": doctype,
#                 "doc": doc,
#             },
#         })

#     if error:
#         plan.append({
#             "tool": "explain_error",
#             "args": {
#                 "doctype": doctype,
#                 "doc": doc,
#                 "error": error,
#             },
#         })

#     field_hint = detect_field_from_question(question)
#     if doctype and field_hint:
#         plan.append({
#             "tool": "get_field_help",
#             "args": {
#                 "doctype": doctype,
#                 "fieldname": field_hint,
#             },
#         })

#     if doctype and docname and any(word in q for word in ["record", "document", "doc", "details", "data", "open"]):
#         plan.append({
#             "tool": "get_record",
#             "args": {
#                 "doctype": doctype,
#                 "name": docname,
#             },
#         })

#     if doctype and any(word in q for word in ["link", "connect", "relation", "kis kis", "kaha use"]):
#         plan.append({
#             "tool": "get_linked_doctypes",
#             "args": {
#                 "doctype": doctype,
#             },
#         })

#     return plan


# def run_tool_plan(plan):
#     outputs = []

#     for step in plan:
#         tool_name = step.get("tool")
#         args = step.get("args") or {}

#         if tool_name == "get_linked_doctypes":
#             target_dt = args.get("doctype")
#             try:
#                 links = frappe.get_all("DocField", filters={"fieldtype": "Link", "options": target_dt}, pluck="parent")
#                 custom_links = frappe.get_all("Custom Field", filters={"fieldtype": "Link", "options": target_dt}, pluck="dt")
#                 unique_links = sorted(list(set(links + custom_links)))
                
#                 result = {
#                     "message": f"{target_dt} in doctypes ke sath link hai.",
#                     "linked_doctypes": unique_links,
#                     "total_links": len(unique_links)
#                 }
#             except Exception as e:
#                 result = {"error": f"Links fetch karne me error aaya: {str(e)}"}
#         else:
#             result = run_tool(tool_name, args)

#         outputs.append({
#             "tool": tool_name,
#             "args": args,
#             "result": result,
#         })

#     return outputs


# def fallback_answer(question, context, tool_outputs):
#     doctype = context.get("doctype")
#     error = context.get("error")

#     lines = []

#     if doctype:
#         lines.append(f"Aap abhi **{doctype}** DocType par ho.")

#     for item in tool_outputs:
#         if item.get("tool") == "analyze_current_doc":
#             result = item.get("result") or {}
#             missing = result.get("missing_required") or []
#             invalid_links = result.get("invalid_links") or []

#             if missing:
#                 lines.append("")
#                 lines.append("Mandatory fields missing lag rahi hain:")
#                 for row in missing:
#                     lines.append(f"- {row.get('label')} ({row.get('fieldname')})")

#             if invalid_links:
#                 lines.append("")
#                 lines.append("Invalid link values mil rahe hain:")
#                 for row in invalid_links:
#                     lines.append(
#                         f"- {row.get('label')}: {row.get('value')} not found in {row.get('linked_doctype')}"
#                     )

#     if error:
#         lines.append("")
#         lines.append(f"Last error: {error}")

#     if not lines:
#         lines.append("Context read ho gaya, lekin specific issue detect nahi hua. Question thoda detail me likho.")

#     return "\n".join(lines)


# @frappe.whitelist()
# def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
#     if not question:
#         frappe.throw("Question is required")

#     context = {
#         "doctype": doctype,
#         "docname": docname,
#         "doc": clean_doc(safe_json(doc, {})),
#         "route": safe_json(route, []),
#         "error": error,
#         "user": frappe.session.user,
#     }

#     plan = build_tool_plan(question, context)
#     tool_outputs = run_tool_plan(plan)

#     model_used = "System"
#     try:
#         messages = build_enterprise_prompt(question, context, tool_outputs)
#         answer, model_used = smart_llm_router(messages, preferred_model)
#     except Exception as e:
#         answer = fallback_answer(question, context, tool_outputs)
#         answer += f"\n\nAI model connect nahi hua: {str(e)}"
#         model_used = "⚙️ Fallback Rule"

#     return {
#         "answer": answer,
#         "model_used": model_used, 
#         "tools_used": [step.get("tool") for step in plan],
#     }


# @frappe.whitelist()
# def inspect_current_context(doctype=None, docname=None, doc=None, route=None, error=None):
#     context = {
#         "doctype": doctype,
#         "docname": docname,
#         "doc": clean_doc(safe_json(doc, {})),
#         "route": safe_json(route, []),
#         "error": error,
#         "user": frappe.session.user,
#     }

#     plan = build_tool_plan("analyze current form", context)
#     outputs = run_tool_plan(plan)

#     return {
#         "context": context,
#         "tools_used": [p.get("tool") for p in plan],
#         "tool_outputs": outputs,
#     }


















import json
import re
import requests
import frappe
from frappe import _

from classic_chatbot.api.agent_tools import (
    safe_json,
    clean_doc,
    run_tool,
)

# ============================================================
# Classic Chatbot - Schema Aware ERP Database Agent
# Requirement:
# - No hardcoded person/name based logic.
# - User can ask natural language questions about ERP data.
# - Agent reads DocType catalog + relevant schema, creates safe query plan,
#   executes through Frappe permission-aware APIs, then returns exact answer.
# ============================================================


AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_doctypes",
            "description": "Get catalog of all available DocTypes in the ERP",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_schema",
            "description": "Get all fields of a DocType before querying it",
            "parameters": {
                "type": "object",
                "properties": {"doctype": {"type": "string"}},
                "required": ["doctype"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_records",
            "description": "Query ERP records. operation: count/list/get/sum/avg/min/max",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "doctype": {"type": "string"},
                    "filters": {"type": "array"},
                    "or_filters": {"type": "array"},
                    "fields": {"type": "array"},
                    "aggregate_field": {"type": "string"},
                    "limit": {"type": "integer"},
                    "order_by": {"type": "string"},
                },
                "required": ["operation", "doctype"],
            },
        },
    },
]


# -----------------------------
# LLM CONFIG
# -----------------------------

# Site config (site_config.json) se settings padhta hai — kaunsa local model use karna hai (Ollama), Groq API key kya hai,
# temperature, limits etc. Agar config me nahi mila to default values use karta hai. Ek dictionary return karta hai.

def get_llm_config():
    return {
        "local_model": frappe.conf.get("classic_chatbot_local_model") or "qwen2.5:3b-instruct",
        "local_base_url": frappe.conf.get("classic_chatbot_local_url") or "http://localhost:11434",
        "groq_api_key": frappe.conf.get("classic_chatbot_groq_api_key"),
        "groq_model": frappe.conf.get("classic_chatbot_groq_model") or "llama-3.3-70b-versatile",
        "temperature": float(frappe.conf.get("classic_chatbot_temperature") or 0.05),
        "max_catalog_chars": int(frappe.conf.get("classic_chatbot_max_catalog_chars") or 22000),
        "max_schema_chars": int(frappe.conf.get("classic_chatbot_max_schema_chars") or 18000),
        "max_result_rows": int(frappe.conf.get("classic_chatbot_max_result_rows") or 50),
        "max_count_scan_rows": int(frappe.conf.get("classic_chatbot_max_count_scan_rows") or 50000),
    }





# Local Ollama server (localhost:11434) ko HTTP request bhejta hai messages ke sath, 
# aur model ka text response wapas laata hai. expect_json=True ho to Ollama ko force karta hai valid JSON hi dene ke liye.
def call_ollama(messages, conf=None, timeout=45, expect_json=False):   # timeout 25 -> 45 (7B thoda slow hota hai)
    conf = conf or get_llm_config()
    url = conf["local_base_url"].rstrip("/") + "/api/chat"
    payload = {
        "model": conf["local_model"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": conf["temperature"],
            "num_ctx": 8192,
        },
    }
    if expect_json:
        payload["format"] = "json"    # <- YE NAYI LINE: Ollama guaranteed valid JSON dega
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content") or data.get("response") or ""




# Same Call_ollama ki tarah tools bhi payload me bhejta hai — matlab model tool call request kar sakta hai.
# Ye pura message object return karta hai (jisme tool_calls ho sakte hain), sirf text nahi.

def call_ollama_with_tools(messages, tools=None, conf=None, timeout=60):
    conf = conf or get_llm_config()
    url = conf["local_base_url"].rstrip("/") + "/api/chat"
    payload = {
        "model": conf["local_model"],
        "messages": messages,
        "stream": False,
        "options": {"temperature": conf["temperature"], "num_ctx": 8192},
    }
    if tools:
        payload["tools"] = tools
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json().get("message", {})




# Bilkul same kaam, bas Ollama ki jagah Groq cloud API (llama-3.3-70b) use karta hai.
# API key header me jati hai. _with_tools wala version tool calling support karta hai.
def call_groq(messages, conf=None, timeout=45, expect_json=False):
    conf = conf or get_llm_config()
    if not conf.get("groq_api_key"):
        raise Exception("Groq API key site_config.json me set nahi hai.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conf['groq_api_key']}",
    }
    payload = {
        "model": conf["groq_model"],
        "messages": messages,
        "temperature": conf["temperature"],
    }
    if expect_json:
        payload["response_format"] = {"type": "json_object"}

    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]




# Bilkul same kaam, bas Ollama ki jagah Groq cloud API (llama-3.3-70b) use karta hai.
# API key header me jati hai. _with_tools wala version tool calling support karta hai.

def call_groq_with_tools(messages, tools=None, conf=None, timeout=60):
    conf = conf or get_llm_config()
    if not conf.get("groq_api_key"):
        raise Exception("Groq API key site_config.json me set nahi hai.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {conf['groq_api_key']}",
    }
    payload = {
        "model": conf["groq_model"],
        "messages": messages,
        "temperature": conf["temperature"],
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]





# Ye router hai — decide karta hai Groq use karna hai ya local:
def llm_chat(messages, preferred_model="auto", expect_json=False):
    conf = get_llm_config()

    if preferred_model == "groq":
        return call_groq(messages, conf, expect_json=expect_json), "☁️ Groq API"

    if preferred_model == "local":
        return call_ollama(messages, conf, timeout=45, expect_json=expect_json), "🖥️ Local Model"

    # auto: Groq pehle (fast), local fallback
    if conf.get("groq_api_key"):
        try:
            return call_groq(messages, conf, expect_json=expect_json), "☁️ Groq (Auto)"
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Classic Chatbot Groq Error - Local Fallback")

    text = call_ollama(messages, conf, timeout=45, expect_json=expect_json)
    if not text or len(text.strip()) < 3:
        raise Exception("Local model ne empty response diya. Ollama check karo.")
    return text, "🖥️ Local Model (Fallback)"


# -----------------------------
# GENERIC UTILS
# -----------------------------
#  extra spaces/newlines hata ke clean single-line string banata hai.
def normalize_space(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()



# LLM ka output kabhi kabhi unstructured format ke sath aata hai (```json fences, extra text). 
# Ye 3 tarike se JSON nikalne ki koshish karta hai: direct parse → fenced block → pehla {...} dhund ke. Fail ho to empty {}.
def extract_json_object(text):
    """Robustly extract JSON object from LLM output."""
    text = (text or "").strip()
    if not text:
        return {}

    # direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # fenced JSON
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.I)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    # first {...}
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            pass

    return {}


# int me convert karo, fail ho to default do (crash nahi hoga).
def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


# text bada ho to kaat do, taaki LLM ka context limit na fate.
def truncate_text(text, max_chars):
    text = str(text or "")
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[TRUNCATED]"


# Based on the provided data," jaise faltu prefixes hata deta hai
def clean_answer(answer):
    answer = normalize_space(answer)
    bad_prefixes = [
        "Based on the provided data,",
        "According to the data,",
    ]
    for p in bad_prefixes:
        if answer.lower().startswith(p.lower()):
            answer = answer[len(p):].strip()
    return answer


# -----------------------------
# SCHEMA CATALOG + SCHEMA READ
# -----------------------------

# Database se saare DocTypes ki list nikalta hai (child tables aur singles skip karke). 
# Har DocType ka naam, module, description etc. — ye catalog LLM ko dikhaya jata hai taaki wo choose kar sake.
# Kuch bhi hardcoded nahi hai.
def get_doctype_catalog():
    """
    Dynamic catalog from actual ERP DocTypes.
    This is not hardcoded. It lets LLM choose relevant DocTypes.
    """
    rows = frappe.get_all(
        "DocType",
        filters={"istable": 0, "issingle": 0},
        fields=["name", "module", "description", "search_fields", "title_field", "modified"],
        order_by="module asc, name asc",
        limit_page_length=0,
    )

    catalog = []
    for r in rows:
        if not r.get("name"):
            continue
        catalog.append({
            "doctype": r.get("name"),
            "module": r.get("module"),
            "title_field": r.get("title_field"),
            "search_fields": r.get("search_fields"),
            "description": normalize_space(r.get("description"))[:160],
        })
    return catalog




# Ek DocType ke saare fields ki detail deta hai:
# Standard fields (name, owner, creation...) manually add karta hai
# Layout-only fields (Section Break, Button...) skip karta hai kyunki unme data nahi hota
# Har field ka fieldname, label, type, required hai ya nahi
def get_schema_for_doctype(doctype):
    if not doctype or not frappe.db.exists("DocType", doctype):
        return None

    meta = frappe.get_meta(doctype)
    fields = []

    # Standard document fields
    standard_fields = [
        {"fieldname": "name", "label": "ID", "fieldtype": "Data"},
        {"fieldname": "owner", "label": "Owner", "fieldtype": "Data"},
        {"fieldname": "creation", "label": "Created On", "fieldtype": "Datetime"},
        {"fieldname": "modified", "label": "Modified On", "fieldtype": "Datetime"},
        {"fieldname": "modified_by", "label": "Modified By", "fieldtype": "Data"},
        {"fieldname": "docstatus", "label": "Docstatus", "fieldtype": "Int"},
    ]

    valid_custom = []
    for f in meta.fields:
        if not f.fieldname:
            continue
        # Skip layout-only fields
        if f.fieldtype in {"Section Break", "Column Break", "Tab Break", "HTML", "Button", "Fold"}:
            continue

        valid_custom.append({
            "fieldname": f.fieldname,
            "label": f.label,
            "fieldtype": f.fieldtype,
            "options": f.options,
            "reqd": int(f.reqd or 0),
            "hidden": int(f.hidden or 0),
        })

    fields.extend(standard_fields)
    fields.extend(valid_custom)

    try:
        search_fields = list(meta.get_search_fields() or [])
    except Exception:
        search_fields = []

    return {
        "doctype": doctype,
        "module": meta.module,
        "title_field": meta.title_field,
        "search_fields": search_fields,
        "fields": fields,
    }






# Catalog nikalta hai
# LLM ko question + catalog deta hai: "in me se 1-5 relevant DocTypes choose karo"
# LLM ka jawab validate karta hai (kya ye DocType sach me exist karta hai?)
# Fallbacks: LLM fail ho to (a) active screen ka DocType use karo, (b) question me DocType ka naam directly match karo
# Selected DocTypes ke schemas load karke return karta hai
def get_relevant_schema(question, context=None, preferred_model="auto"):
    """
    Step 1: LLM reads the actual DocType catalog and selects relevant DocTypes.
    Then backend loads only those schemas.
    """
    conf = get_llm_config()
    context = context or {}
    catalog = get_doctype_catalog()

    # Add active screen doctype as hint but do not force it.
    active_doctype = context.get("doctype")
    catalog_payload = {
        "user_question": question,
        "active_screen_doctype": active_doctype,
        "doctype_catalog": catalog,
    }

    system = """
You are a Frappe/ERPNext schema router.
Your job is only to choose relevant DocTypes from the provided actual DocType catalog.

Rules:
- Do NOT invent DocTypes.
- Choose 1 to 5 DocTypes only.
- Prefer exact user wording, labels, modules, and active screen context.
- If user asks about current form, include active_screen_doctype.
- Return JSON only.

JSON format:
{
  "doctypes": ["DocType 1", "DocType 2"],
  "reason": "short reason"
}
"""

    user = truncate_text(json.dumps(catalog_payload, ensure_ascii=False, default=str), conf["max_catalog_chars"])

    try:
        raw, model_used = llm_chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            preferred_model=preferred_model,
            expect_json=True,
        )
        data = extract_json_object(raw)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot Schema Router Error")
        data = {}

    selected = data.get("doctypes") or []
    if isinstance(selected, str):
        selected = [selected]

    # Validate selected DocTypes
    valid_doctypes = []
    for dt in selected:
        dt = normalize_space(dt)
        if dt and frappe.db.exists("DocType", dt) and dt not in valid_doctypes:
            valid_doctypes.append(dt)

    # Fallback: active screen doctype if available
    if not valid_doctypes and active_doctype and frappe.db.exists("DocType", active_doctype):
        valid_doctypes.append(active_doctype)

    # Fallback: very light dynamic phrase match from catalog, not hardcoded
    if not valid_doctypes:
        q = (question or "").lower()
        for item in catalog:
            dt = item["doctype"]
            if dt.lower() in q:
                valid_doctypes.append(dt)
                break

    schemas = []
    for dt in valid_doctypes[:5]:
        schema = get_schema_for_doctype(dt)
        if schema:
            schemas.append(schema)

    return {
        "selected_doctypes": valid_doctypes[:5],
        "schemas": schemas,
        "router_reason": data.get("reason"),
    }


# -----------------------------
# QUERY PLAN CREATION
# -----------------------------
ALLOWED_OPERATIONS = {"count", "list", "get", "sum", "avg", "min", "max"}
ALLOWED_OPERATORS = {"=", "!=", ">", "<", ">=", "<=", "like", "not like", "in", "not in", "between", "is", "is not"}
SAFE_ORDER_RE = re.compile(r"^[a-zA-Z0-9_]+(\s+(asc|desc))?$", re.I)




# LLM ko question + real schemas deta hai aur bolta hai: 
# JSON plan banao — operation kya hai (count/list/sum...), 
# filters kya lagane hain, kaunse fields chahiye. SQL likhna mana hai. 
# LLM sirf plan banata hai, execute nahi karta.
def create_query_plan(question, schema_bundle, context=None, preferred_model="auto"):
    """
    Step 2: LLM uses real schema to create a safe JSON query plan.
    """
    conf = get_llm_config()
    context = context or {}

    system = """
You are a Frappe/ERPNext database query planner.

You will receive:
- User question
- Current context
- Real DocType schemas

Create a SAFE query plan in JSON.
Do NOT write SQL.
Do NOT use SQL functions such as count(name), COUNT(*), SUM().
Use only fieldnames that exist in the provided schema.
Use only provided DocTypes.
Use permission-safe Frappe-style filters.

Supported operations:
- count: count matching records
- list: show matching records
- get: get one record details
- sum/avg/min/max: aggregate a numeric/currency/float/int field in Python after fetching rows

Filter format:
["DocType", "fieldname", "operator", "value"]

or_filters means OR search across fields.
filters means AND filters.

For person/name/text search:
- Use "like" on likely name/title/search fields from schema.
- Example value: "%komal%"
- Use actual fields from schema only.

For count questions:
- operation = "count"
- fields can be ["name"]

For list questions:
- operation = "list"
- fields should be useful visible fields, max 8.

Return JSON only:
{
  "confidence": 0.0-1.0,
  "operation": "count|list|get|sum|avg|min|max",
  "doctype": "Exact DocType",
  "filters": [],
  "or_filters": [],
  "fields": ["name"],
  "aggregate_field": null,
  "limit": 10,
  "order_by": "modified desc",
  "needs_clarification": false,
  "clarifying_question": "",
  "reason": "short"
}

Important:
- Never ask for doctype/context if schema can solve it.
- Never invent fields.
- Never return count(name) as field.
"""

    payload = {
        "question": question,
        "context": {
            "active_doctype": context.get("doctype"),
            "docname": context.get("docname"),
            "route": context.get("route"),
        },
        "schemas": schema_bundle.get("schemas") or [],
    }

    raw_payload = truncate_text(json.dumps(payload, ensure_ascii=False, default=str), conf["max_schema_chars"])

    raw, model_used = llm_chat(
        [{"role": "system", "content": system}, {"role": "user", "content": raw_payload}],
        preferred_model=preferred_model,
        expect_json=True,
    )
    plan = extract_json_object(raw)
    plan["_planner_model"] = model_used
    plan["_raw_plan"] = raw[:1000]
    return plan


# -----------------------------
# PLAN VALIDATION + EXECUTION
# -----------------------------
def get_valid_fields_map(schema):
    fields = {}
    for f in schema.get("fields") or []:
        fn = f.get("fieldname")
        if fn:
            fields[fn] = f
    return fields


def find_schema(schema_bundle, doctype):
    for schema in schema_bundle.get("schemas") or []:
        if schema.get("doctype") == doctype:
            return schema
    return None


#  operator allowed list (=, like, in...) me hai? Nahi to = bana do.
def sanitize_operator(op):
    op = str(op or "=").lower().strip()
    if op not in ALLOWED_OPERATORS:
        return "="
    return op



# har filter check: 4 items hain? Field schema me exist karta hai? 
# Value 500 charcters se badi to nahi? Galat ho to filter drop.
def sanitize_filter_row(row, doctype, valid_fields):
    """
    Teen formats accept karo (LLM models alag-alag format bhejte hain):
    - 4-element: ["Contact", "full_name", "like", "%deepak%"]
    - 3-element: ["full_name", "like", "%deepak%"]
    - 2-element: ["full_name", "deepak"]  (operator "=" assume hoga)
    Sab ko 4-element me normalize karo. Invalid ho to None return karo.
    """
    if not isinstance(row, (list, tuple)):
        return None

    row = list(row)

    # 2-element: [field, value] -> [doctype, field, "=", value]
    if len(row) == 2:
        row = [doctype, row[0], "=", row[1]]
    # 3-element: [field, op, value] -> [doctype, field, op, value]
    elif len(row) == 3:
        row = [doctype, row[0], row[1], row[2]]
    elif len(row) != 4:
        return None

    row_dt, field, op, value = row
    row_dt = normalize_space(row_dt) or doctype
    field = normalize_space(field)
    op = sanitize_operator(op)

    # Field schema me exist karna chahiye - warna filter invalid
    if field not in valid_fields:
        return None

    # Model ne galat doctype naam likha ho par field valid hai,
    # to bhi accept karo (hum apne doctype pe hi force karte hain)

    # Prevent dangerous weird values. Values are still parameters in Frappe ORM.
    if isinstance(value, str):
        value = normalize_space(value)
        if len(value) > 500:
            value = value[:500]
    if op in {"in", "not in"} and not isinstance(value, list):
        value = [value]
    if op == "between" and (not isinstance(value, list) or len(value) != 2):
        return None

    return [doctype, field, op, value]




def normalize_filter_input(raw, doctype):
    """
    Filters ko hamesha list-of-lists me convert karo, chahe model
    kisi bhi format me bheje:
    - Dict format: {"full_name": ["like", "%deepak%"]} ya {"status": "Open"}
    - Single flat list: ["full_name", "like", "%deepak%"]
    - List of lists: [["full_name", "like", "%deepak%"], ...]
    """
    if not raw:
        return []

    # Dict format: {"field": value} ya {"field": [op, value]}
    if isinstance(raw, dict):
        rows = []
        for field, val in raw.items():
            if isinstance(val, (list, tuple)) and len(val) == 2:
                rows.append([doctype, field, val[0], val[1]])
            else:
                rows.append([doctype, field, "=", val])
        return rows

    if isinstance(raw, (list, tuple)):
        # Single flat filter: ["full_name", "like", "%deepak%"]
        # (andar koi list/dict nahi hai matlab ye ek hi filter hai)
        if raw and all(not isinstance(x, (list, tuple, dict)) for x in raw):
            return [list(raw)]
        # List of lists (normal case)
        return [list(r) if isinstance(r, (list, tuple)) else r for r in raw]

    return []




# upar wale ko saare filters pe chalata hai.
def sanitize_filters(plan, schema):
    """
    Return: (filters, or_filters, dropped_count)

    dropped_count batata hai kitne filters invalid hoke drop hue.
    Ye zaroori hai kyunki agar model ne filters bheje the aur SAB drop
    ho gaye, to unfiltered query chal jati hai aur galat answer aata hai
    (jaise "deepak" ke 29 ki jagah total 3757 count ho jana).
    """
    doctype = schema["doctype"]
    valid_fields = get_valid_fields_map(schema)
    dropped = 0

    filters = []
    for row in normalize_filter_input(plan.get("filters"), doctype):
        safe = sanitize_filter_row(row, doctype, valid_fields)
        if safe:
            filters.append(safe)
        else:
            dropped += 1

    or_filters = []
    for row in normalize_filter_input(plan.get("or_filters"), doctype):
        safe = sanitize_filter_row(row, doctype, valid_fields)
        if safe:
            or_filters.append(safe)
        else:
            dropped += 1

    return filters, or_filters, dropped


#  sirf wahi fields allow jo schema me hain, max 10, name hamesha include.
def sanitize_fields(plan, schema):
    valid_fields = get_valid_fields_map(schema)
    requested = plan.get("fields") or ["name"]
    if isinstance(requested, str):
        requested = [requested]

    fields = []
    for field in requested:
        field = normalize_space(field)
        if field in valid_fields and field not in fields:
            fields.append(field)

    if "name" not in fields:
        fields.insert(0, "name")

    return fields[:10]



# regex se check karta hai order_by safe hai (SQL injection nahi). Invalid ho to modified desc
def sanitize_order_by(order_by, schema):
    valid_fields = get_valid_fields_map(schema)
    order_by = normalize_space(order_by or "modified desc")

    if not SAFE_ORDER_RE.match(order_by):
        return "modified desc"

    field = order_by.split()[0]
    if field not in valid_fields:
        return "modified desc"

    return order_by





def resolve_link_field_filters(filters, or_filters, schema):
    """
    GENERIC: Kisi bhi Link field pe text/name search ho to usko real IDs me resolve karo.

    Kaise kaam karta hai (100% schema-driven, kuch bhi hardcoded nahi):
    1. Filter ke field ka fieldtype schema se check karo -> "Link" hai?
    2. Us field ke `options` se pata karo wo kis DocType se linked hai
    3. Us linked DocType ke apne title_field + search_fields me text search karo
    4. Jo IDs milein, original filter ko "in" filter me convert kar do

    Kuch bhi resolve na ho paye to original filter untouched wapas jata hai.
    """
    valid_fields = get_valid_fields_map(schema)

    def resolve_one(f):
        # Safety: filter 4-item list hi honi chahiye
        if not isinstance(f, (list, tuple)) or len(f) != 4:
            return f

        dt, field, op, value = f
        meta = valid_fields.get(field) or {}

        # 1) Sirf Link fields pe kaam karo (schema batata hai, hum nahi)
        if meta.get("fieldtype") != "Link":
            return f

        # 2) Sirf text search pe kaam karo
        if op not in ("like", "=") or not isinstance(value, str):
            return f

        # 3) Kis DocType se link hai? Schema ke `options` se pata chalta hai
        linked_dt = normalize_space(meta.get("options"))
        if not linked_dt or not frappe.db.exists("DocType", linked_dt):
            return f

        search_text = value.strip("%").strip()
        if not search_text:
            return f

        # 4) Agar value already ek valid ID hai (user ne email/ID hi diya ho), skip
        try:
            if frappe.db.exists(linked_dt, search_text):
                return f
        except Exception:
            pass

        # 5) Linked DocType ke searchable fields nikalo - pure schema se
        try:
            linked_meta = frappe.get_meta(linked_dt)
        except Exception:
            return f

        candidates = ["name"]
        if linked_meta.title_field:
            candidates.append(linked_meta.title_field)
        try:
            candidates.extend(linked_meta.get_search_fields() or [])
        except Exception:
            pass

        # 6) Dedup + validate: sirf wahi fields jo linked DocType me sach me hain
        seen = set()
        or_search = []
        for sf in candidates:
            sf = normalize_space(sf)
            if not sf or sf in seen:
                continue
            if sf != "name" and not linked_meta.get_field(sf):
                continue
            seen.add(sf)
            or_search.append([linked_dt, sf, "like", f"%{search_text}%"])

        if not or_search:
            return f

        # 7) Linked DocType me search karo (permission-aware get_list)
        try:
            matches = frappe.get_list(
                linked_dt,
                or_filters=or_search,
                fields=["name"],
                limit_page_length=50,
            )
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Classic Chatbot Link Resolve Error")
            return f

        ids = [m["name"] for m in matches if m.get("name")]
        if not ids:
            # Kuch nahi mila -> original filter hi rehne do
            return f

        # 8) Original text filter ko exact ID filter me convert karo
        return [dt, field, "in", ids]

    new_filters = [resolve_one(list(f)) for f in (filters or [])]
    new_or_filters = [resolve_one(list(f)) for f in (or_filters or [])]
    return new_filters, new_or_filters



# Smart trick: agar LLM ne first_name like %komal% filter banaya, 
# to ye Function automatically us search ko saare naam-jaise fields pe OR search me spread kr deta hai — name, 
# full_name, email, mobile... Taaki "komal" kahi bhi ho, mil jaye. Ye deterministic Python hai, LLM Model pe depend nahi
def expand_text_search(filters, or_filters, schema):
    """
    Agar plan me kisi text field pe 'like' search hai, to usi value ko
    schema ke saare naam/title/search fields pe OR search me expand karo.
    Deterministic hai - model pe depend nahi.
    """
    doctype = schema["doctype"]
    valid_fields = get_valid_fields_map(schema)

    # 1) Search value dhundo (koi bhi like filter)
    search_value = None
    remaining_filters = []
    for f in (filters or []) + (or_filters or []):
        if f[2] in ("like", "not like") and isinstance(f[3], str):
            if search_value is None:
                search_value = f[3]
            # like wale filters expand honge, isliye alag rakho
        else:
            if f in (filters or []):
                remaining_filters.append(f)

    if not search_value:
        return filters, or_filters  # koi text search nahi, kuch mat badlo

    # 2) Searchable fields banao: search_fields + title_field + naam-jaise Data fields
    candidates = []
    for sf in schema.get("search_fields") or []:
        if sf in valid_fields:
            candidates.append(sf)
    tf = schema.get("title_field")
    if tf and tf in valid_fields:
        candidates.append(tf)
    for fn, meta in valid_fields.items():
        if meta.get("fieldtype") in ("Data", "Small Text") and any(
            key in fn for key in ("name", "title", "full", "first", "last", "middle", "email", "mobile", "phone")
        ):
            candidates.append(fn)

    # duplicates hatao, name (ID) bhi add karo
    seen, expanded = set(), []
    for fn in ["name"] + candidates:
        if fn in valid_fields and fn not in seen:
            seen.add(fn)
            expanded.append([doctype, fn, "like", search_value])

    return remaining_filters, expanded





# Validated plan ko actually chalata hai:
# Clarification chahiye? → user se puchta hai 
# Permission check — frappe.has_permission() — user ko read access hai ya nahi?
# Filters/fields sanitize karo
# Operation ke hisab se:

# count: rows fetch karke len() (kyunki Frappe v16 count(name) reject karta hai)
# list/get: frappe.get_list() se records lao
# sum/avg/min/max: rows lao, Python me calculate karo (SQL function nahi)

# Key point: kabhi raw SQL nahi, sirf Frappe ka permission-aware ORM.
def execute_safe_query_plan(plan, schema_bundle):
    """
    Step 3: Execute only validated plan through Frappe get_list.
    No raw SQL. No SQL functions in fields.
    """
    if not isinstance(plan, dict):
        return {"ok": False, "error": "Invalid query plan."}
    if plan.get("needs_clarification"):
        return {
            "ok": False,
            "needs_clarification": True,
            "clarifying_question": plan.get("clarifying_question") or "Kripaya apna sawaal thoda specific karein.",
        }
    operation = normalize_space(plan.get("operation") or "list").lower()
    if operation not in ALLOWED_OPERATIONS:
        operation = "list"
    doctype = normalize_space(plan.get("doctype"))
    schema = find_schema(schema_bundle, doctype)
    if not schema:
        return {"ok": False, "error": "Relevant DocType schema nahi mila."}
    if not frappe.has_permission(doctype, "read"):
        return {"ok": False, "error": f"Aapko {doctype} read karne ki permission nahi hai."}

    filters, or_filters, dropped = sanitize_filters(plan, schema)

    # SAFETY GUARD: Model ne filters bheje the par sab invalid nikle.
    # Unfiltered query chala ke GALAT answer (poore table ka count) dene se
    # better hai error dena - agent loop me model ye error dekh kar
    # get_schema call karega aur sahi fieldname se retry karega.
    if dropped and not filters and not or_filters:
        return {
            "ok": False,
            "error": (
                "Filters invalid the (galat fieldname ya format). "
                "get_schema se sahi fieldnames dekh kar dobara query karein. "
                f"Invalid filters count: {dropped}"
            ),
        }

    filters, or_filters = resolve_link_field_filters(filters, or_filters, schema)
    filters, or_filters = expand_text_search(filters, or_filters, schema)
    fields = sanitize_fields(plan, schema)
    order_by = sanitize_order_by(plan.get("order_by"), schema)
    limit = safe_int(plan.get("limit"), 10)
    limit = max(1, min(limit, get_llm_config()["max_result_rows"]))

    # Count safely. Frappe v16 rejects SQL functions in fields, so never use count(name).
    if operation == "count":
        rows = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters or None,
            fields=["name"],
            limit_page_length=get_llm_config()["max_count_scan_rows"],
            order_by=order_by,
        )
        return {
            "ok": True,
            "operation": "count",
            "doctype": doctype,
            "count": len(rows),
            "sample_records": rows[:10],
            "plan": {
                "filters": filters,
                "or_filters": or_filters,
                "fields": ["name"],
                "order_by": order_by,
            },
        }

    # List/get records
    if operation in {"list", "get"}:
        rows = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters or None,
            fields=fields,
            limit_page_length=1 if operation == "get" else limit,
            order_by=order_by,
        )
        return {
            "ok": True,
            "operation": operation,
            "doctype": doctype,
            "records": [clean_record(r) for r in rows],
            "shown_count": len(rows),
            "plan": {
                "filters": filters,
                "or_filters": or_filters,
                "fields": fields,
                "order_by": order_by,
                "limit": limit,
            },
        }

    # Python-side aggregate for safe numeric operations
    aggregate_field = normalize_space(plan.get("aggregate_field"))
    valid_fields = get_valid_fields_map(schema)
    if aggregate_field not in valid_fields:
        return {"ok": False, "error": "Aggregate field schema me valid nahi hai."}
    rows = frappe.get_list(
        doctype,
        filters=filters,
        or_filters=or_filters or None,
        fields=["name", aggregate_field],
        limit_page_length=get_llm_config()["max_count_scan_rows"],
        order_by=order_by,
    )
    values = []
    for r in rows:
        v = r.get(aggregate_field)
        try:
            if v is not None:
                values.append(float(v))
        except Exception:
            pass
    if operation == "sum":
        agg_value = sum(values)
    elif operation == "avg":
        agg_value = sum(values) / len(values) if values else 0
    elif operation == "min":
        agg_value = min(values) if values else 0
    elif operation == "max":
        agg_value = max(values) if values else 0
    else:
        agg_value = 0
    return {
        "ok": True,
        "operation": operation,
        "doctype": doctype,
        "aggregate_field": aggregate_field,
        "value": agg_value,
        "matched_rows": len(rows),
        "plan": {
            "filters": filters,
            "or_filters": or_filters,
            "fields": ["name", aggregate_field],
            "order_by": order_by,
        },
    }
# step 4th =>  Zero-result retry: Agar query 0 records de, to retry_with_broader_search()
#  deterministic retry karta hai — multi-word search ("%Abhishek Soni%") ko sirf pehle word ("%Abhishek%") se dobara try karta hai.
#  Ye Python logic hai, model pe depend nahi.
def retry_with_broader_search(plan, schema_bundle, original_result):
    """
    GENERIC: 0 result aaye aur multi-word text search thi, to sirf pehla word
    se dobara try karo. Deterministic hai - model pe depend nahi.
    Example: "%Abhishek Soni%" match nahi hua -> "%Abhishek%" se retry.
    """
    def _shorten(f):
        # 3-element aur 4-element dono handle karo:
        # operator hamesha second-last, value last position pe hota hai
        if (
            isinstance(f, (list, tuple))
            and len(f) in (3, 4)
            and str(f[-2]).lower() == "like"
            and isinstance(f[-1], str)
        ):
            words = f[-1].strip("%").split()
            if len(words) > 1:
                new_f = list(f)
                new_f[-1] = f"%{words[0]}%"
                return new_f
        return list(f) if isinstance(f, (list, tuple)) else f

    had_multiword = False
    new_plan = dict(plan)
    for key in ("filters", "or_filters"):
        rows = []
        for f in (plan.get(key) or []):
            nf = _shorten(f)
            if nf != (list(f) if isinstance(f, (list, tuple)) else f):
                had_multiword = True
            rows.append(nf)
        new_plan[key] = rows

    if not had_multiword:
        return original_result  # retry ka koi fayda nahi

    try:
        retry_result = execute_safe_query_plan(new_plan, schema_bundle)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot Broader Retry Error")
        return original_result

    got_data = retry_result.get("ok") and (
        retry_result.get("count")
        or retry_result.get("records")
        or retry_result.get("matched_rows")
    )
    if got_data:
        retry_result["_note"] = (
            "Exact full-name match nahi mila tha, isliye broader search "
            "(pehle word se) ke results diye gaye hain."
        )
        return retry_result
    return original_result



# Record se internal fields (_comments, _assign...) aur empty values hata deta hai — user ko clean data dikhe
def clean_record(record):
    hidden = {"_user_tags", "_comments", "_assign", "_liked_by"}
    out = {}
    for k, v in (record or {}).items():
        if k in hidden or str(k).startswith("_"):
            continue
        if v in (None, ""):
            continue
        out[k] = v
    return out


# -----------------------------
# FINAL ANSWER FORMATTING
# -----------------------------

# Result ko readable Hinglish answer banata hai:
# count → "Contact me matching total 5 record mile hain."
# sum/avg → value + matched rows
# list → markdown table (max 6 columns, 10 rows)
# kuch nahi mila → "koi matching record nahi mila"

# Ye pure Python hai — numbers LLM change nahi kar sakta, isliye hallucination impossible.
def format_database_result_answer(question, result, preferred_model="auto"):
    """
    Step 4: Format exact database result in short professional Hinglish.
    For count/aggregate, deterministic first sentence.
    For list, compact markdown table.
    """
    if not result.get("ok"):
        if result.get("needs_clarification"):
            return result.get("clarifying_question") or "Please apna question thoda specific karein."
        return f"Backend se data get karne me error aaya hai: {result.get('error')}"

    op = result.get("operation")
    doctype = result.get("doctype")

    if op == "count":
        count = safe_int(result.get("count"), 0)
        return f"**{doctype}** me matching total **{count} record** find huye hain."

    if op in {"sum", "avg", "min", "max"}:
        value = result.get("value")
        field = result.get("aggregate_field")
        matched = safe_int(result.get("matched_rows"), 0)
        return f"**{doctype}** me **{field}** ka **{op.upper()} = {value}** hai. Matching records: **{matched}**."

    records = result.get("records") or []
    if not records:
        return f"**{doctype}** me koi matching record nahi mila hai."

    # Compact table
    fields = []
    for r in records:
        for k in r.keys():
            if k not in fields:
                fields.append(k)
    fields = fields[:6]

    lines = [f"**{doctype}** ke matching records yeh hain:"]
    lines.append("| " + " | ".join([f.replace("_", " ").title() for f in fields]) + " |")
    lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
    for r in records[:10]:
        row = []
        for f in fields:
            row.append(normalize_space(r.get(f, ""))[:120])
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)







# Abhi ke liye bas upar wale ko hi call karta hai. 
# Idea ye tha ki list results ko LLM se polish karwa sakte hain, 
# par numeric results ke liye deliberately LLM skip karta hai (accuracy ke liye).
def format_with_llm(question, result, preferred_model="auto"):
    """
    Optional polish: use LLM only to explain/word the already-executed result.
    It cannot change numbers.
    """
    # For deterministic numeric results, avoid extra LLM.
    if result.get("operation") in {"count", "sum", "avg", "min", "max"}:
        return format_database_result_answer(question, result, preferred_model)

    base = format_database_result_answer(question, result, preferred_model)
    return base


# -----------------------------
# SCHEMA-AWARE DATABASE AGENT
# -----------------------------
# Main orchestrator
# Pura pipeline ek jagah: 
# schema dhundo → plan banao → execute karo → format karo. 
# Har step pe try/except hai, error ho to log karke debug info ke sath return.
def schema_aware_database_answer(question, context=None, preferred_model="auto"):
    """
    Full dynamic database answer flow:
    Natural Language -> DocType catalog -> relevant schema -> JSON query plan -> safe execution -> exact answer
    """
    context = context or {}

    schema_bundle = get_relevant_schema(question, context, preferred_model=preferred_model)
    if not schema_bundle.get("schemas"):
        return None, {
            "stage": "schema",
            "error": "No relevant schema found",
            "schema_bundle": schema_bundle,
        }

    try:
        plan = create_query_plan(question, schema_bundle, context=context, preferred_model=preferred_model)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot Query Planner Error")
        return None, {"stage": "planner", "error": str(e), "schema_bundle": schema_bundle}

    try:
        result = execute_safe_query_plan(plan, schema_bundle)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot Query Execution Error")
        return f"Sir, database query execute karte time error aaya hai, Please try after few Minutes. : {str(e)}", {
            "stage": "execute",
            "error": str(e),
            "plan": plan,
            "schema_bundle": schema_bundle,
        }

    answer = format_with_llm(question, result, preferred_model=preferred_model)
    debug = {
        "stage": "done",
        "selected_doctypes": schema_bundle.get("selected_doctypes"),
        "plan": plan,
        "result": result,
    }
    return answer, debug


# -----------------------------
# GENERAL ERP ASSISTANT FALLBACK
# -----------------------------
GENERAL_SYSTEM_PROMPT = """
You are Classic Chatbot, a professional Frappe/ERPNext assistant.
Tone: courteous and respectful or Proffesional, like a knowledgeable ERP consultant and Manager.
Address the user politely using 'aap'. Do NOT use casual words like 'Bhai' or slang.
Reply in polished conversational Hinglish (Roman script, never Devnagari).
Be concise: give the direct answer first, details after.
If database result is unavailable, do not fake data.
"""

def general_llm_answer(question, context=None, tool_outputs=None, preferred_model="auto"):
    payload = {
        "question": question,
        "context": context or {},
        "tool_outputs": tool_outputs or [],
    }
    messages = [
        {"role": "system", "content": GENERAL_SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)[:16000]},
    ]
    answer, model_used = llm_chat(messages, preferred_model=preferred_model)
    return clean_answer(answer), model_used




# Local Ollama agent loop (max 6 steps):

# Model ko question do
# Model tool call mange to execute karo, result wapas do
# Model final answer de to loop khatam
# 6 steps me nahi hua to "thoda specific pucho"
def agent_answer(question, context=None, max_steps=6):
    context = context or {}
    messages = [
        {"role": "system", "content": "You are an ERP database agent. Use tools to find exact answers. Reply in short Hinglish."},
        {"role": "user", "content": json.dumps({"question": question, "context": context}, ensure_ascii=False)},
    ]
    for step in range(max_steps):
        msg = call_ollama_with_tools(messages, tools=AGENT_TOOLS)
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            # Model ne final answer de diya
            return msg.get("content"), {"steps": step}
        messages.append(msg)  # model ki tool request history me rakho
        for tc in tool_calls:
            fn = tc["function"]["name"]
            args = tc["function"].get("arguments") or {}
            if isinstance(args, str):
                args = extract_json_object(args)
            # Tumhare EXISTING safe functions hi execute karenge
            if fn == "list_doctypes":
                result = get_doctype_catalog()
            elif fn == "get_schema":
                result = get_schema_for_doctype(args.get("doctype")) or {"error": "DocType not found"}
            elif fn == "query_records":
                schema = get_schema_for_doctype(args.get("doctype"))
                bundle = {"schemas": [schema]} if schema else {"schemas": []}
                result = execute_safe_query_plan(args, bundle)
                # NEW: 0 result pe deterministic broader retry
                if result.get("ok") and not result.get("count") and not result.get("records") and not result.get("matched_rows"):
                    result = retry_with_broader_search(args, bundle, result)
            else:
                result = {"error": f"Unknown tool {fn}"}
            messages.append({
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False, default=str)[:8000],
            })
    return "Sir, is question ke liye kaafi steps lag rahe hain, thoda specific pucho.", {"steps": max_steps}







# ye groq agent model ke answer ke liye hai for run sql query



def groq_agent_answer(question, context=None, history=None, max_steps=8):
    """Groq 70B agent loop: model khud list_doctypes/get_schema/query_records chalata hai."""
    conf = get_llm_config()
    context = context or {}
    user_msg = question
    if context.get("doctype"):
        user_msg += f"\n(active screen DocType: {context['doctype']}"
        if context.get("docname"):
            user_msg += f", document: {context['docname']}"
        user_msg += ")"
    # Current form ka LIVE data (unsaved changes included) agent ko do
    doc_data = context.get("doc")
    if isinstance(doc_data, dict) and doc_data and context.get("doctype"):
        # Schema se mandatory fields nikaal ke khud compare karo (deterministic)
        missing_required = []
        try:
            meta = frappe.get_meta(context["doctype"])
            for f in meta.fields:
                if not f.reqd or not f.fieldname:
                    continue
                val = doc_data.get(f.fieldname)
                if val in (None, "", 0) or (isinstance(val, list) and not val):
                    missing_required.append(f"{f.label} ({f.fieldname})")
        except Exception:
            pass
        doc_json = json.dumps(doc_data, ensure_ascii=False, default=str)[:5000]
        user_msg += (
            f"\n\nCurrent form data on user's screen (may contain unsaved changes): {doc_json}"
            f"\n\nPRE-COMPUTED CHECK - mandatory fields that are EMPTY on this form: "
            f"{missing_required if missing_required else 'NONE - all mandatory fields are filled'}"
            "\nTrust this pre-computed check over your own analysis. Fields present in the "
            "form data above ARE filled - never claim a field is empty if it appears there."
        )
    messages = [
        {
            "role": "system",
            "content": (
                "You are Classic Chatbot, a professional ERPNext assistant with live database tools. "
                "You have READ-ONLY access. You CANNOT create, update, or delete any record. "
                "If the user asks to add/create/update/delete something, politely explain that "
                "you cannot make changes, and instead give exact UI steps (fields to fill, "
                "buttons to click). NEVER claim that a record was created or changed. "
                "Workflow: if unsure which DocType, call list_doctypes; then get_schema "
                "to see real fieldnames; then query_records with valid filters only. "
                "For 'how to create/add X' questions: call get_schema first, then list the "
                "actual required fields (reqd=1) by their labels with exact UI steps. "
                "If 'Current form data' is provided in the message, analyze THAT for questions "
                "about the current/open form - the database may not have unsaved changes. "
                "IMPORTANT about Link fields: a Link field stores the linked record's ID "
                "(often not the display name). When filtering a Link field by a person or "
                "entity NAME, use a like-filter with the name - the backend automatically "
                "resolves names to correct IDs for Link fields. "
                "If query_records returns 0 results or empty, do NOT immediately answer that "
                "nothing exists. First verify the fieldname via get_schema, or retry with a "
                "broader like-filter, then answer. "
                "Never invent fields or data. For name/text search use like-filters "
                "with %value%. Filter format: [[\"DocType\",\"field\",\"op\",\"value\"]]. "
                "Use the conversation history to understand follow-up messages. "
                "Tone: professional, courteous, and respectful - like a knowledgeable ERP "
                "consultant. Address the user politely using 'aap'. Do NOT use casual words "
                "like 'Bhai', 'yaar', or slang. "
                "Reply in polished conversational Hinglish (Roman script, never Devnagari). "
                "Be concise: answer first, details after. Markdown table for 3+ records."
            ),
        },
    ]
    # Pichli baatein inject karo taaki follow-ups samajh aayein
    for h in (history or [])[-6:]:
        if isinstance(h, dict) and h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": str(h["content"])[:2000]})
    messages.append({"role": "user", "content": user_msg})
    tools_called = []
    for step in range(max_steps):
        msg = call_groq_with_tools(messages, tools=AGENT_TOOLS, conf=conf)
        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            return msg.get("content"), {"steps": step, "tools_called": tools_called}
        messages.append(msg)
        for tc in tool_calls:
            fn = tc["function"]["name"]
            args = extract_json_object(tc["function"].get("arguments") or "{}")
            try:
                if fn == "list_doctypes":
                    result = get_doctype_catalog()
                elif fn == "get_schema":
                    result = get_schema_for_doctype(args.get("doctype")) or {"error": "DocType not found"}
                elif fn == "query_records":
                    schema = get_schema_for_doctype(args.get("doctype"))
                    bundle = {"schemas": [schema]} if schema else {"schemas": []}
                    result = execute_safe_query_plan(args, bundle)
                    # NEW: 0 result pe deterministic broader retry (model pe depend nahi)
                    if result.get("ok") and not result.get("count") and not result.get("records") and not result.get("matched_rows"):
                        result = retry_with_broader_search(args, bundle, result)
                else:
                    result = {"error": f"Unknown tool {fn}"}
            except Exception as e:
                result = {"error": str(e)}
            tools_called.append(fn)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.get("id"),
                "content": json.dumps(result, ensure_ascii=False, default=str)[:12000],
            })
    return "Yeh query kaafi complex hai. Kripaya thoda specific sawaal poochein.", {
        "steps": max_steps, "tools_called": tools_called,
    }




# -----------------------------
# OPTIONAL LEGACY TOOL SUPPORT
# -----------------------------
def build_tool_plan(question, context):
    """
    Kept for compatibility with existing UI. Main database answering is schema_aware_database_answer().
    """
    plan = []
    doctype = context.get("doctype")
    doc = context.get("doc")
    error = context.get("error")
    docname = context.get("docname")
    q = (question or "").lower()

    if doctype:
        plan.append({"tool": "get_doctype_schema", "args": {"doctype": doctype}})
        if isinstance(doc, dict):
            plan.append({"tool": "analyze_current_doc", "args": {"doctype": doctype, "doc": doc}})
        if docname and any(word in q for word in ["record", "document", "doc", "details", "data"]):
            plan.append({"tool": "get_record", "args": {"doctype": doctype, "name": docname}})

    if error:
        plan.append({"tool": "explain_error", "args": {"doctype": doctype, "doc": doc, "error": error}})

    return plan


def run_tool_plan(plan):
    outputs = []
    for step in plan:
        tool_name = step.get("tool")
        args = step.get("args") or {}
        try:
            result = run_tool(tool_name, args)
        except Exception as e:
            result = {"error": str(e)}
        outputs.append({"tool": tool_name, "args": args, "result": result})
    return outputs


# -----------------------------
# PUBLIC API
# -----------------------------
@frappe.whitelist()
# def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
def ask(question, doctype=None, docname=None, doc=None, route=None, error=None,
        preferred_model="auto", history=None):

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

    # 0) Groq mode: full agent loop (model khud tools decide karta hai)
    if preferred_model in ("groq", "auto") and get_llm_config().get("groq_api_key"):
        try:
            answer, debug = groq_agent_answer(question, context, history=safe_json(history, []))
            if answer:
                return {
                    "answer": answer,
                    "model_used": "☁️ Groq Agent (llama-3.3-70b)",
                    "tools_used": (debug or {}).get("tools_called") or [],
                    "debug": debug if frappe.conf.get("classic_chatbot_debug") else None,
                }
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Classic Chatbot Groq Agent Error")
            # fall through to local schema-aware flow

    # 1) Local schema-aware database agent (fallback / local mode).
    answer, debug = schema_aware_database_answer(question, context, preferred_model=preferred_model)
    if answer:
        model_used = "🧠 Schema-Aware ERP Database Agent"
        planner_model = ((debug or {}).get("plan") or {}).get("_planner_model")
        if planner_model:
            model_used += f" via {planner_model}"

        return {
            "answer": answer,
            "model_used": model_used,
            "tools_used": [
                "get_doctype_catalog",
                "get_relevant_schema",
                "create_query_plan",
                "execute_safe_query_plan",
            ],
            "debug": debug if frappe.conf.get("classic_chatbot_debug") else None,
        }

    # 2) Legacy tools for form explanation/error/help.
    plan = build_tool_plan(question, context)
    tool_outputs = run_tool_plan(plan)

    try:
        answer, model_used = general_llm_answer(
            question,
            context=context,
            tool_outputs=tool_outputs,
            preferred_model=preferred_model,
        )
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Classic Chatbot General Answer Error")
        answer = f"Answer generate karte samay error aaya: {str(e)}"
        model_used = "⚠️ Error"

    return {
        "answer": answer,
        "model_used": model_used,
        "tools_used": [step.get("tool") for step in plan],
        "debug": None,
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
    schema_bundle = get_relevant_schema(
        "analyze current form",
        context,
        preferred_model="auto",
    )
    return {
        "context": context,
        "schema_bundle": schema_bundle,
    }


@frappe.whitelist()
def test_schema_agent(question, doctype=None):
    """
    Bench test helper:
    bench --site site1.local execute classic_chatbot.api.agent.test_schema_agent --args '["komal ke name se kitne contact hai", "Contact"]'
    """
    context = {"doctype": doctype} if doctype else {}
    answer, debug = agent_answer(question, context)
    if answer:
        return {
            "answer": answer,
            "model_used": "🤖 Agentic ERP Agent (Local)",
            "tools_used": ["agent_loop"],
            "debug": debug if frappe.conf.get("classic_chatbot_debug") else None,
        }




















# ============================================================
# WHOLE FORM VALIDATION API FOR CLASSIC ERROR AVATAR
# ============================================================

FORM_LAYOUT_FIELD_TYPES = {
    "Section Break",
    "Column Break",
    "Tab Break",
    "HTML",
    "Button",
    "Image",
    "Fold",
    "Heading",
}

EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

PHONE_ALLOWED_PATTERN = re.compile(
    r"^[0-9+\-()\s.]+$"
)


def _form_value_is_empty(value):
    """
    Zero and False are valid values.
    Only actual blank values are treated as empty.
    """
    return value is None or value == "" or value == [] or value == {}


def _safe_json_list(value):
    parsed = safe_json(value, [])

    if isinstance(parsed, list):
        return parsed

    if isinstance(parsed, tuple):
        return list(parsed)

    return []


def _validate_data_format(df, value):
    """
    Validate generic Data field options without hardcoding a DocType.
    """
    if value in (None, ""):
        return None

    option = normalize_space(df.options).lower()
    text = str(value).strip()

    if option == "email":
        if not EMAIL_PATTERN.match(text):
            return (
                f"Please valid {df.label or df.fieldname} enter kijiye. "
                "Email format sahi nahi hai."
            )

    elif option == "phone":
        digit_count = len(
            re.sub(r"\D", "", text)
        )

        if (
            not PHONE_ALLOWED_PATTERN.match(text)
            or digit_count < 7
            or digit_count > 15
        ):
            return (
                f"Please valid {df.label or df.fieldname} enter kijiye. "
                "Phone number format sahi nahi hai."
            )

    elif option == "url":
        if not re.match(
            r"^(https?://|www\.)[^\s]+$",
            text,
            re.IGNORECASE,
        ):
            return (
                f"Please valid {df.label or df.fieldname} URL enter kijiye."
            )

    return None


@frappe.whitelist()
def validate_current_form(
    doctype=None,
    docname=None,
    doc=None,
    required_fields=None,
    visible_fields=None,
    fieldname=None,
    full_scan=0,
):
    """
    Validate the currently open unsaved form.

    It checks:
    - Visible mandatory fields
    - Invalid Link values
    - Invalid Select values
    - Email, Phone and URL formats
    - Mandatory fields inside child tables
    - Link/Select/Data validation inside child rows

    It does not save or modify the document.
    """

    if not doctype:
        frappe.throw(_("DocType is required."))

    if not frappe.db.exists("DocType", doctype):
        frappe.throw(
            _("DocType {0} does not exist.").format(doctype)
        )

    if not frappe.has_permission(doctype, "read"):
        frappe.throw(
            _("You do not have permission to read {0}.").format(
                doctype
            )
        )

    doc_data = safe_json(doc, {}) or {}

    if not isinstance(doc_data, dict):
        frappe.throw(_("Current document data is invalid."))

    doc_data["doctype"] = doctype

    if docname and not doc_data.get("name"):
        doc_data["name"] = docname

    required_set = {
        normalize_space(value)
        for value in _safe_json_list(required_fields)
        if normalize_space(value)
    }

    visible_set = {
        normalize_space(value)
        for value in _safe_json_list(visible_fields)
        if normalize_space(value)
    }

    requested_field = normalize_space(fieldname)
    run_full_scan = str(full_scan).lower() in {
        "1",
        "true",
        "yes",
    }

    issues = []
    issue_keys = set()

    def add_issue(
        issue_type,
        target_fieldname,
        label,
        message,
        value=None,
        child_fieldname=None,
        row_index=None,
    ):
        key = (
            issue_type,
            target_fieldname,
            child_fieldname,
            row_index,
            message,
        )

        if key in issue_keys:
            return

        issue_keys.add(key)

        issues.append({
            "type": issue_type,
            "fieldname": target_fieldname,
            "child_fieldname": child_fieldname,
            "label": label,
            "message": message,
            "value": value,
            "row_index": row_index,
        })

    def should_validate_parent_field(df):
        if run_full_scan or not requested_field:
            return True

        return df.fieldname == requested_field

    def validate_field(
        df,
        row_data,
        target_fieldname=None,
        parent_table_field=None,
        row_index=None,
        force_required=None,
    ):
        if not df.fieldname:
            return

        if df.fieldtype in FORM_LAYOUT_FIELD_TYPES:
            return

        value = row_data.get(df.fieldname)

        field_label = df.label or df.fieldname
        focus_fieldname = (
            parent_table_field
            or target_fieldname
            or df.fieldname
        )

        if force_required is None:
            is_required = bool(df.reqd)
        else:
            is_required = bool(force_required)

        if is_required and _form_value_is_empty(value):
            if row_index:
                message = (
                    f"Row {row_index} me {field_label} fill kijiye. "
                    "Yeh field mandatory hai."
                )
            else:
                message = (
                    f"Please {field_label} fill kijiye. "
                    "Yeh field mandatory hai."
                )

            add_issue(
                issue_type="mandatory",
                target_fieldname=focus_fieldname,
                child_fieldname=(
                    df.fieldname
                    if parent_table_field
                    else None
                ),
                label=field_label,
                message=message,
                row_index=row_index,
            )

            return

        if _form_value_is_empty(value):
            return

        # Link validation
        if df.fieldtype == "Link" and df.options:
            try:
                if not frappe.db.exists(df.options, value):
                    add_issue(
                        issue_type="invalid_link",
                        target_fieldname=focus_fieldname,
                        child_fieldname=(
                            df.fieldname
                            if parent_table_field
                            else None
                        ),
                        label=field_label,
                        value=value,
                        row_index=row_index,
                        message=(
                            f"{field_label} me selected value "
                            f"'{value}' {df.options} master me nahi mili."
                        ),
                    )
            except Exception as link_error:
                frappe.log_error(
                    message=frappe.get_traceback(),
                    title="Classic Form Link Validation Error",
                )

        # Dynamic Link validation
        elif df.fieldtype == "Dynamic Link" and df.options:
            linked_doctype = row_data.get(df.options)

            if linked_doctype and value:
                try:
                    if (
                        frappe.db.exists(
                            "DocType",
                            linked_doctype,
                        )
                        and not frappe.db.exists(
                            linked_doctype,
                            value,
                        )
                    ):
                        add_issue(
                            issue_type="invalid_dynamic_link",
                            target_fieldname=focus_fieldname,
                            child_fieldname=(
                                df.fieldname
                                if parent_table_field
                                else None
                            ),
                            label=field_label,
                            value=value,
                            row_index=row_index,
                            message=(
                                f"{field_label} me selected value "
                                f"'{value}' {linked_doctype} me nahi mili."
                            ),
                        )
                except Exception:
                    frappe.log_error(
                        frappe.get_traceback(),
                        "Classic Dynamic Link Validation Error",
                    )

        # Select validation
        elif df.fieldtype == "Select" and df.options:
            valid_options = [
                option.strip()
                for option in str(df.options).splitlines()
                if option.strip()
            ]

            if (
                valid_options
                and str(value).strip() not in valid_options
            ):
                add_issue(
                    issue_type="invalid_select",
                    target_fieldname=focus_fieldname,
                    child_fieldname=(
                        df.fieldname
                        if parent_table_field
                        else None
                    ),
                    label=field_label,
                    value=value,
                    row_index=row_index,
                    message=(
                        f"{field_label} me '{value}' valid option nahi hai. "
                        "Please list me se correct option select kijiye."
                    ),
                )

        # Generic Data validation
        elif df.fieldtype == "Data":
            format_error = _validate_data_format(
                df,
                value,
            )

            if format_error:
                add_issue(
                    issue_type="invalid_format",
                    target_fieldname=focus_fieldname,
                    child_fieldname=(
                        df.fieldname
                        if parent_table_field
                        else None
                    ),
                    label=field_label,
                    value=value,
                    row_index=row_index,
                    message=format_error,
                )

    meta = frappe.get_meta(doctype)

    for df in meta.fields:
        if not should_validate_parent_field(df):
            continue

        # Client-side current UI state is preferred because
        # frm.set_df_property may dynamically change mandatory status.
        if required_set:
            parent_required = df.fieldname in required_set
        else:
            parent_required = bool(df.reqd)

        # Hidden fields should not produce a user-facing mandatory error.
        is_visible = (
            not visible_set
            or df.fieldname in visible_set
        )

        effective_required = (
            parent_required and is_visible
        )

        validate_field(
            df=df,
            row_data=doc_data,
            target_fieldname=df.fieldname,
            force_required=effective_required,
        )

        # Child table validation
        if (
            df.fieldtype == "Table"
            and df.options
            and (
                run_full_scan
                or not requested_field
                or requested_field == df.fieldname
            )
        ):
            child_rows = doc_data.get(df.fieldname) or []

            if not isinstance(child_rows, list):
                continue

            try:
                child_meta = frappe.get_meta(df.options)
            except Exception:
                continue

            for row_number, child_row in enumerate(
                child_rows,
                start=1,
            ):
                if not isinstance(child_row, dict):
                    continue

                for child_df in child_meta.fields:
                    validate_field(
                        df=child_df,
                        row_data=child_row,
                        parent_table_field=df.fieldname,
                        row_index=row_number,
                        force_required=bool(child_df.reqd),
                    )

    first_issue = issues[0] if issues else None

    return {
        "ok": not bool(issues),
        "doctype": doctype,
        "docname": doc_data.get("name"),
        "issue_count": len(issues),
        "first_issue": first_issue,
        "issues": issues[:100],
    }