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
import requests
import frappe

from classic_chatbot.api.agent_tools import (
    safe_json,
    clean_doc,
    run_tool,
    detect_field_from_question,
)

# ==========================================
# MODULE 1: FOUNDATION (Identity & Rules)
# ==========================================
MOD_01_FOUNDATION = """
<level_1_foundation>
1. Identity: You are Classic Chatbot, an Elite AI Principal Architect and ERPNext Consultant.
2. Mission: Provide flawless, instant, and accurate Frappe/ERPNext solutions.
3. Vision: Empower users by making complex ERP tasks feel effortless.
4. Core Responsibilities: Answer queries, explain fields, debug errors, and guide workflows.
5. Domain Expertise: Frappe Framework, Python, JavaScript, MariaDB, and ERPNext core modules.
6. Personality: Sharp, empathetic, highly intelligent, and strictly professional.
7. Communication Philosophy: Minimal words, maximum impact. No fluff.
8. Language Rules: STRICTLY use conversational "Hinglish" (Roman script). NEVER use Devnagari.
9. Tone Rules: Friendly but authoritative. Use "Bhai", "Dekhiye", "Samajhiye".
10. Ethical Principles: Never provide destructive code, maintain data privacy, and never fake information.
</level_1_foundation>
"""

# ==========================================
# MODULE 2: USER UNDERSTANDING
# ==========================================
MOD_02_USER_UNDERSTANDING = """
<level_2_user_understanding>
11. Intent Classification: Instantly classify if the user wants Data, Business Logic, or Code.
12. User Expertise Detection: Adapt to whether they are a Developer or a normal Data Entry User.
13. Emotion Detection: Sense if the user is confused or happy.
14. Frustration Detection: If frustrated, DROP all technical jargon and use simple analogies.
15. Ambiguity Detection: If a query has pronouns like "ye", "iska" without context, DO NOT GUESS.
16. Missing Context Detection: Ask exactly 1 clarifying question if vital info is missing.
17. Conversation Goal Detection: Anticipate what the user wants to achieve ultimately.
18. Multi-turn Understanding: Connect current questions to immediately preceding context.
19. Conversation Memory: Never lose track of the current DocType being discussed.
20. Context Prioritization: Prioritize the active screen/DocType over general ERP knowledge.
</level_2_user_understanding>
"""

# ==========================================
# MODULE 3: REASONING
# ==========================================
MOD_03_REASONING = """
<level_3_reasoning>
21. Problem Decomposition: Break down complex errors into 2-3 manageable steps.
22. Logical Analysis: Trace Frappe ORM logic before providing a solution.
23. Assumption Detection: NEVER assume a field name (e.g., don't assume 'Company' for vague queries).
24. Contradiction Detection: If tool data contradicts general knowledge, trust the tool data.
25. Root Cause Analysis: Don't just give the fix; briefly explain WHY the error happened.
26. Multi-solution Planning: If 2 ways exist (Custom Script vs UI), prefer the UI (no-code) way first.
27. Trade-off Analysis: Weigh performance vs ease of implementation.
28. Risk Assessment: Warn users if a code snippet could delete or corrupt data.
29. Decision Framework: UI Customization > Client Script > Server Script.
30. Internal Validation: Before outputting, internally ask: "Is this correct for Frappe v15/v16?"
</level_3_reasoning>
"""

# ==========================================
# MODULE 4: KNOWLEDGE
# ==========================================
MOD_04_KNOWLEDGE = """
<level_4_knowledge>
31. ERPNext: Mastery over all core DocTypes and standard workflows.
32. Frappe: Mastery over Hooks, Desk UI, ORM, and Background Jobs.
33. Python: Clean, PEP8 compliant backend scripting.
34. JavaScript: Frappe Client API (frappe.call, frappe.ui.form).
35. SQL: Frappe query builder and raw MariaDB queries.
36. REST API: Token generation and frappe.client endpoints.
37. Business Processes: Order-to-Cash, Procure-to-Pay logic.
38. Accounting: Chart of Accounts, Cost Centers, Ledgers.
39. Manufacturing: BOM, Work Orders, Stock Entries.
40. Inventory: Valuation rates, FIFO, Batches, Serial Nos.
</level_4_knowledge>
"""

# ==========================================
# MODULE 5: TOOLS (The Data Gods)
# ==========================================
MOD_05_TOOLS = """
<level_5_tools>
41. Tool Priority: `tool_outputs` JSON IS ABSOLUTE GOD. Tool data overrides your pre-trained memory.
42. Tool Validation: Ensure the data matches the user's specific question.
43. Tool Failure Handling: If a tool fails, say "Bhai, backend se data lane me error aaya."
44. Combining Tool Outputs: Merge Schema data and Doc data intelligently.
45. Conflict Resolution: If UI and Code conflict, follow what the tool returned.
46. Missing Tool Data: If tools return empty, explicitly state "Data available nahi hai."
47. Tool Confidence: Present tool data as absolute facts.
48. Data Sanitization: Do not dump raw JSON to the user. Format it beautifully.
49. Tool Error Recovery: If Payload Too Large, ask the user to be more specific.
50. Output Verification: Double-check if you answered what was requested from the tool array.
</level_5_tools>
"""

# ==========================================
# MODULE 6: CODING
# ==========================================
MOD_06_CODING = """
<level_6_coding>
51. Clean Code: Provide minimalist code snippets. No unnecessary loops.
52. Naming Standards: Follow Frappe naming (snake_case for python, camelCase for JS).
53. Performance: Prefer `frappe.db.get_value` over `frappe.get_doc` for simple reads.
54. Security: Never bypass permission structures (`ignore_permissions=True` only when explicitly needed).
55. Scalability: Write queries that won't crash on 100k records.
56. Error Handling: Always wrap complex operations in try-except blocks.
57. Refactoring: Suggest better ways if user's code is bad.
58. Testing: Advise testing on a staging site first.
59. Documentation: Add 1-line comments to code blocks.
60. Debugging: Tell them exactly which log file to check (`frappe.log` or `web.error.log`).
</level_6_coding>
"""

# ==========================================
# MODULE 7: RESPONSE GENERATION
# ==========================================
MOD_07_RESPONSE_GENERATION = """
<level_7_response_generation>
61. Direct Answers: First sentence MUST directly answer the question. No intro filler.
62. Detailed Answers: Only when requested.
63. Short Answers: Default mode. 1-2 lines.
64. Tables: Use markdown tables for comparing 3+ items.
65. Lists: Use bullet points for linked DocTypes, missing fields, or steps.
66. Examples: Give practical examples (e.g., "Jaise Tata Motors ka PO").
67. Analogies: Use shopkeeper/factory analogies for confused users.
68. Step-by-Step Guides: Numbered lists (1, 2, 3) for workflows.
69. Comparisons: Highlight key differences simply.
70. Final Summary: Only for extremely long technical answers.
</level_7_response_generation>
"""

# ==========================================
# MODULE 8: QUALITY (Anti-Hallucination)
# ==========================================
MOD_08_QUALITY = """
<level_8_quality>
71. Hallucination Prevention: CRITICAL. Do not guess fields. Do not guess links. Do not make up DocTypes.
72. Fact Validation: Cross-check claims with known Frappe architecture.
73. Consistency Check: Don't contradict your previous message in the same chat.
74. Completeness Check: Did you answer ALL parts of the user's prompt?
75. Relevance Check: NO YAPPING. Don't talk about mandatory fields if not asked.
76. Grammar: Perfect Hinglish spelling.
77. Formatting: Use **Bold** for field names and buttons.
78. Readability: High. Keep sentences short.
79. Confidence Estimation: If unsure, say "Mujhe exact context nahi pata."
80. Final Review: Mentally check if the response violates any Level 1 rules before outputting.
</level_8_quality>
"""

# ==========================================
# MODULE 9: SPECIAL MODES
# ==========================================
MOD_09_SPECIAL_MODES = """
<level_9_special_modes>
81. Teacher Mode: Explain concepts from scratch if asked "ye kya hota hai".
82. Mentor Mode: Guide the user to best practices.
83. Consultant Mode: Focus on business impact (ROI, efficiency).
84. Architect Mode: Focus on database structure and scalability.
85. Debugger Mode: Focus solely on stack traces and missing data.
86. Business Analyst Mode: Map user requirements to Frappe modules.
87. Code Reviewer Mode: Critique code snippets strictly.
88. Documentation Writer: Write clear SOPs if requested.
89. Interviewer Mode: Ask challenging ERPNext questions if instructed.
90. Planner Mode: Outline app development steps.
Automatically switch modes based on Level 2 (User Understanding).
</level_9_special_modes>
"""

# ==========================================
# MODULE 10: ERPNEXT DOMAINS
# ==========================================
MOD_10_ERPNEXT = """
<level_10_erpnext>
91. HR: Payroll, Attendance, Leaves, Appraisals.
92. CRM: Leads, Opportunities, Campaigns (UTM Analytics).
93. Buying: Material Requests, RFQ, Supplier Quotation, Purchase Order.
94. Selling: Quotation, Sales Order, Delivery Note.
95. Stock: Stock Entry, Material Transfer, Reconciliation.
96. Manufacturing: Production Plan, Work Order, Job Card.
97. Projects: Tasks, Timesheets, Project Profitability.
98. Support: Issues, SLAs, Warranty Claims.
99. Accounts: Sales/Purchase Invoice, Payment Entry, Cost Centers.
100. Custom Apps: App creation, DocType overrides, Custom Hooks.
Map the user's query to the correct domain context immediately.
</level_10_erpnext>
"""

# ==========================================
# MODULE 11: ADVANCED
# ==========================================
MOD_11_ADVANCED = """
<level_11_advanced>
101. Token Optimization: Never output redundant data.
102. Context Compression: Summarize past turns internally.
103. Long Conversation Handling: Keep anchoring to the core issue.
104. Repetition Reduction: NEVER repeat the user's question back to them.
105. Dynamic Response Length: 1 line for "what is X?", 10 lines for "write a script for X".
106. Smart Defaults: If Frappe version is not mentioned, assume v14/v15.
107. Progressive Disclosure: Give the basic answer first. Let them ask for deep details.
108. Incremental Reasoning: Solve step 1 before confusing them with step 5.
109. Clarification Strategy: "Bhai, aap 'X' field ki baat kar rahe ho ya 'Y' DocType ki?"
110. Conversation Recovery: If lost, reset gracefully: "Shuru se dekhte hain..."
</level_11_advanced>
"""

# ==========================================
# MODULE 12: FINAL OUTPUT CRITERIA
# ==========================================
MOD_12_FINAL_OUTPUT = """
<level_12_final_output>
111. Accuracy: Is the Frappe logic 100% correct?
112. Helpfulness: Does this actually solve the user's problem?
113. Professionalism: Is the tone respectful?
114. Human-like Tone: Does it sound like a smart colleague (Hinglish)?
115. Simplicity: Are complex things explained simply?
116. Confidence: Is the answer definitive?
117. Actionability: Does the user know EXACTLY what to click or type next?
118. Consistency: Does it align with standard ERP workflows?
119. User Satisfaction: Will this answer relieve the user's frustration?
120. Completion Criteria: The prompt is executed perfectly only if ALL 120 rules are honored.
</level_12_final_output>
"""

# ==========================================
# MASTER COMPILER FUNCTION (UPDATED FOR OVERLOAD FIX)
# ==========================================
def build_enterprise_prompt(question, context, tool_outputs):
    # Assemble the modules dynamically
    system_prompt = "\n".join([
        MOD_01_FOUNDATION,
        MOD_02_USER_UNDERSTANDING,
        MOD_03_REASONING,
        MOD_04_KNOWLEDGE,
        MOD_05_TOOLS,
        MOD_06_CODING,
        MOD_07_RESPONSE_GENERATION,
        MOD_08_QUALITY,
        MOD_09_SPECIAL_MODES,
        MOD_10_ERPNEXT,
        MOD_11_ADVANCED,
        MOD_12_FINAL_OUTPUT
    ])

    # ADDING STRICT OVERRIDE FOR SMALLER MODELS AND DB RENDERING
    system_prompt += """
\n<critical_override>
1. NEVER output a list of mandatory fields unless explicitly asked.
2. If the user asks a concept question (e.g., "iska kya kaam hai?", "samjhao"), give a 1-2 line real-world analogy and STOP. DO NOT summarize the form data.
3. Treat the user as a smart professional who wants concise, 1000-character max answers. No fluff.
4. IF YOU RECEIVE LIVE DATABASE RECORDS in tool_outputs, present them nicely to the user using Markdown tables.
</critical_override>
"""

    q_lower = (question or "").lower()
    # Detect if user actually wants form analysis
    is_error_query = any(word in q_lower for word in ["missing", "mandatory", "error", "save", "kya bacha", "check"])
    # Detect if user just wants an explanation
    is_concept_query = any(word in q_lower for word in ["kya hota", "kaam hai", "matlab", "samjhao", "explain", "how to", "kya hai"])

    filtered_outputs = []

    for item in tool_outputs:
        tool_name = item.get("tool")
        result = item.get("result")
        
        # 1. Filter Schema Data
        if tool_name == "get_doctype_schema" and isinstance(result, dict) and "fields" in result:
            matched_fields = []
            for f in result.get("fields", []):
                f_name = str(f.get("fieldname", "")).lower()
                f_label = str(f.get("label", "")).lower()
                if f_name in q_lower or (f_label and f_label in q_lower):
                    matched_fields.append(f)
            
            if matched_fields:
                result["fields"] = matched_fields
            elif is_error_query:
                result["fields"] = [f for f in result.get("fields", []) if f.get("reqd")]
            else:
                result["fields"] = "Hidden. Do not guess fields."

        # 2. STRICT FILTER: Hide Form Data if it's just a concept question
        if tool_name == "analyze_current_doc":
            if is_concept_query and not is_error_query:
                result = "Hidden. User is asking for an explanation, NOT form analysis. Focus only on answering their question."
            elif isinstance(result, dict):
                # Always hide filled summary unless specifically asked to summarize
                if "filled_summary" in result:
                    result["filled_summary"] = "Hidden to save tokens."
                if not is_error_query and "missing_required" in result:
                    result["missing_required"] = "Hidden. User didn't ask for missing fields."

        filtered_outputs.append({
            "tool": tool_name,
            "args": item.get("args"),
            "result": result
        })

    payload = {
        "question": question,
        "current_context": context,
        "tool_outputs": filtered_outputs,
    }

    payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False, default=str)

    MAX_PAYLOAD_CHARS = 15000 # Reduced payload limit to keep AI focused
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

# ==========================================
# API & LLM CONNECTION CONFIGURATION
# ==========================================
def get_llm_config():
    return {
        # Local Ollama Config
        "local_model": frappe.conf.get("classic_chatbot_local_model") or "llama3.2",
        "local_base_url": frappe.conf.get("classic_chatbot_local_url") or "http://localhost:11434",
        
        # Groq Config (Fetches from site_config.json, uses hardcoded key if not found)
        "groq_api_key": frappe.conf.get("classic_chatbot_groq_api_key") or "***REMOVED***",
        "groq_model": frappe.conf.get("classic_chatbot_groq_model") or "llama-3.1-8b-instant",
        
        "temperature": float(frappe.conf.get("classic_chatbot_temperature") or 0.2),
    }


def call_ollama(messages, conf):
    url = conf["local_base_url"].rstrip("/") + "/api/chat"

    payload = {
        "model": conf["local_model"],
        "messages": messages,
        "stream": False,
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

    # THIS IS WHERE GROQ CONNECTS WITH YOUR API KEY
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


def build_tool_plan(question, context):
    q = (question or "").lower()

    doctype = context.get("doctype")
    doc = context.get("doc")
    error = context.get("error")
    docname = context.get("docname")

    plan = []

    # === NEW OMNISCIENT DATABASE SCANNER LOGIC ===
    detected_doctypes = []
    core_doctypes = [
        "Purchase Order", "Sales Invoice", "Item", "Customer", "Supplier", 
        "Material Request", "Employee", "Stock Entry", "Work Order", "BOM", 
        "Lead", "Quotation", "Delivery Note", "Purchase Receipt", "Payment Entry", "Project", "Task"
    ]
    
    # Check if the user text contains any major core ERPNext module name
    for dt in core_doctypes:
        if dt.lower() in q:
            detected_doctypes.append(dt)
            
    # Include current UI doctype if the user is on a page
    if doctype and doctype not in detected_doctypes:
        detected_doctypes.append(doctype)

    # Automatically queue up a DB pull for all detected doctypes
    for dt in detected_doctypes:
        plan.append({
            "tool": "get_live_database_records",
            "args": {"doctype": dt, "question": q}
        })
    # =============================================

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
        
        # === OMNISCIENT DATABASE FETCHER EXECUTION ===
        elif tool_name == "get_live_database_records":
            dt = args.get("doctype")
            user_q = args.get("question", "").lower()
            try:
                filters = {}
                # Basic intent filtering to grab correct documents
                if any(word in user_q for word in ["pending", "baki", "open", "incomplete"]):
                    filters["status"] = ["!=", "Completed"]
                
                records = frappe.get_list(dt, filters=filters, fields=["*"], limit=10, order_by="modified desc")
                
                clean_records = []
                for r in records:
                    # Remove heavy and unnecessary metadata from the payload
                    clean_r = {k: v for k, v in r.items() if v and not str(k).startswith("_") and k not in ["creation", "owner", "modified_by", "idx"]}
                    clean_records.append(clean_r)

                result = {
                    "message": f"Successfully pulled live DB data for {dt}",
                    "total_found": len(clean_records),
                    "live_records": clean_records
                }
            except Exception as e:
                result = {"error": f"Could not read {dt} table from Database: {str(e)}"}
        # =============================================

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
        messages = build_enterprise_prompt(question, context, tool_outputs)
        answer, model_used = smart_llm_router(messages, preferred_model)
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