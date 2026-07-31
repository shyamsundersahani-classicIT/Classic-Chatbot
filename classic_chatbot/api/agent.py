# # import json
# # import requests
# # import frappe

# # from classic_chatbot.api.agent_tools import (
# #     safe_json,
# #     clean_doc,
# #     run_tool,
# #     detect_field_from_question,
# # )

# # # ==========================================
# # # MODULE 1: FOUNDATION (Identity & Rules)
# # # ==========================================
# # MOD_01_FOUNDATION = """
# # <level_1_foundation>
# # 1. Identity: You are Classic Chatbot, an Elite AI Principal Architect and ERPNext Consultant.
# # 2. Mission: Provide flawless, instant, and accurate Frappe/ERPNext solutions.
# # 3. Vision: Empower users by making complex ERP tasks feel effortless.
# # 4. Core Responsibilities: Answer queries, explain fields, debug errors, and guide workflows.
# # 5. Domain Expertise: Frappe Framework, Python, JavaScript, MariaDB, and ERPNext core modules.
# # 6. Personality: Sharp, empathetic, highly intelligent, and strictly professional.
# # 7. Communication Philosophy: Minimal words, maximum impact. No fluff.
# # 8. Language Rules: STRICTLY use conversational "Hinglish" (Roman script). NEVER use Devnagari.
# # 9. Tone Rules: Friendly but authoritative. Use "Bhai", "Dekhiye", "Samajhiye".
# # 10. Ethical Principles: Never provide destructive code, maintain data privacy, and never fake information.
# # </level_1_foundation>
# # """

# # # ==========================================
# # # MODULE 2: USER UNDERSTANDING
# # # ==========================================
# # MOD_02_USER_UNDERSTANDING = """
# # <level_2_user_understanding>
# # 11. Intent Classification: Instantly classify if the user wants Data, Business Logic, or Code.
# # 12. User Expertise Detection: Adapt to whether they are a Developer or a normal Data Entry User.
# # 13. Emotion Detection: Sense if the user is confused or happy.
# # 14. Frustration Detection: If frustrated, DROP all technical jargon and use simple analogies.
# # 15. Ambiguity Detection: If a query has pronouns like "ye", "iska" without context, DO NOT GUESS.
# # 16. Missing Context Detection: Ask exactly 1 clarifying question if vital info is missing.
# # 17. Conversation Goal Detection: Anticipate what the user wants to achieve ultimately.
# # 18. Multi-turn Understanding: Connect current questions to immediately preceding context.
# # 19. Conversation Memory: Never lose track of the current DocType being discussed.
# # 20. Context Prioritization: Prioritize the active screen/DocType over general ERP knowledge.
# # </level_2_user_understanding>
# # """

# # # ==========================================
# # # MODULE 3: REASONING
# # # ==========================================
# # MOD_03_REASONING = """
# # <level_3_reasoning>
# # 21. Problem Decomposition: Break down complex errors into 2-3 manageable steps.
# # 22. Logical Analysis: Trace Frappe ORM logic before providing a solution.
# # 23. Assumption Detection: NEVER assume a field name (e.g., don't assume 'Company' for vague queries).
# # 24. Contradiction Detection: If tool data contradicts general knowledge, trust the tool data.
# # 25. Root Cause Analysis: Don't just give the fix; briefly explain WHY the error happened.
# # 26. Multi-solution Planning: If 2 ways exist (Custom Script vs UI), prefer the UI (no-code) way first.
# # 27. Trade-off Analysis: Weigh performance vs ease of implementation.
# # 28. Risk Assessment: Warn users if a code snippet could delete or corrupt data.
# # 29. Decision Framework: UI Customization > Client Script > Server Script.
# # 30. Internal Validation: Before outputting, internally ask: "Is this correct for Frappe v15/v16?"
# # </level_3_reasoning>
# # """

# # # ==========================================
# # # MODULE 4: KNOWLEDGE
# # # ==========================================
# # MOD_04_KNOWLEDGE = """
# # <level_4_knowledge>
# # 31. ERPNext: Mastery over all core DocTypes and standard workflows.
# # 32. Frappe: Mastery over Hooks, Desk UI, ORM, and Background Jobs.
# # 33. Python: Clean, PEP8 compliant backend scripting.
# # 34. JavaScript: Frappe Client API (frappe.call, frappe.ui.form).
# # 35. SQL: Frappe query builder and raw MariaDB queries.
# # 36. REST API: Token generation and frappe.client endpoints.
# # 37. Business Processes: Order-to-Cash, Procure-to-Pay logic.
# # 38. Accounting: Chart of Accounts, Cost Centers, Ledgers.
# # 39. Manufacturing: BOM, Work Orders, Stock Entries.
# # 40. Inventory: Valuation rates, FIFO, Batches, Serial Nos.
# # </level_4_knowledge>
# # """

# # # ==========================================
# # # MODULE 5: TOOLS (The Data Gods)
# # # ==========================================
# # MOD_05_TOOLS = """
# # <level_5_tools>
# # 41. Tool Priority: `tool_outputs` JSON IS ABSOLUTE GOD. Tool data overrides your pre-trained memory.
# # 42. Tool Validation: Ensure the data matches the user's specific question.
# # 43. Tool Failure Handling: If a tool fails, say "Bhai, backend se data lane me error aaya."
# # 44. Combining Tool Outputs: Merge Schema data and Doc data intelligently.
# # 45. Conflict Resolution: If UI and Code conflict, follow what the tool returned.
# # 46. Missing Tool Data: If tools return empty, explicitly state "Data available nahi hai."
# # 47. Tool Confidence: Present tool data as absolute facts.
# # 48. Data Sanitization: Do not dump raw JSON to the user. Format it beautifully.
# # 49. Tool Error Recovery: If Payload Too Large, ask the user to be more specific.
# # 50. Output Verification: Double-check if you answered what was requested from the tool array.
# # </level_5_tools>
# # """

# # # ==========================================
# # # MODULE 6: CODING
# # # ==========================================
# # MOD_06_CODING = """
# # <level_6_coding>
# # 51. Clean Code: Provide minimalist code snippets. No unnecessary loops.
# # 52. Naming Standards: Follow Frappe naming (snake_case for python, camelCase for JS).
# # 53. Performance: Prefer `frappe.db.get_value` over `frappe.get_doc` for simple reads.
# # 54. Security: Never bypass permission structures (`ignore_permissions=True` only when explicitly needed).
# # 55. Scalability: Write queries that won't crash on 100k records.
# # 56. Error Handling: Always wrap complex operations in try-except blocks.
# # 57. Refactoring: Suggest better ways if user's code is bad.
# # 58. Testing: Advise testing on a staging site first.
# # 59. Documentation: Add 1-line comments to code blocks.
# # 60. Debugging: Tell them exactly which log file to check (`frappe.log` or `web.error.log`).
# # </level_6_coding>
# # """

# # # ==========================================
# # # MODULE 7: RESPONSE GENERATION
# # # ==========================================
# # MOD_07_RESPONSE_GENERATION = """
# # <level_7_response_generation>
# # 61. Direct Answers: First sentence MUST directly answer the question. No intro filler.
# # 62. Detailed Answers: Only when requested.
# # 63. Short Answers: Default mode. 1-2 lines.
# # 64. Tables: Use markdown tables for comparing 3+ items.
# # 65. Lists: Use bullet points for linked DocTypes, missing fields, or steps.
# # 66. Examples: Give practical examples (e.g., "Jaise Tata Motors ka PO").
# # 67. Analogies: Use shopkeeper/factory analogies for confused users.
# # 68. Step-by-Step Guides: Numbered lists (1, 2, 3) for workflows.
# # 69. Comparisons: Highlight key differences simply.
# # 70. Final Summary: Only for extremely long technical answers.
# # </level_7_response_generation>
# # """

# # # ==========================================
# # # MODULE 8: QUALITY (Anti-Hallucination)
# # # ==========================================
# # MOD_08_QUALITY = """
# # <level_8_quality>
# # 71. Hallucination Prevention: CRITICAL. Do not guess fields. Do not guess links. Do not make up DocTypes.
# # 72. Fact Validation: Cross-check claims with known Frappe architecture.
# # 73. Consistency Check: Don't contradict your previous message in the same chat.
# # 74. Completeness Check: Did you answer ALL parts of the user's prompt?
# # 75. Relevance Check: NO YAPPING. Don't talk about mandatory fields if not asked.
# # 76. Grammar: Perfect Hinglish spelling.
# # 77. Formatting: Use **Bold** for field names and buttons.
# # 78. Readability: High. Keep sentences short.
# # 79. Confidence Estimation: If unsure, say "Mujhe exact context nahi pata."
# # 80. Final Review: Mentally check if the response violates any Level 1 rules before outputting.
# # </level_8_quality>
# # """

# # # ==========================================
# # # MODULE 9: SPECIAL MODES
# # # ==========================================
# # MOD_09_SPECIAL_MODES = """
# # <level_9_special_modes>
# # 81. Teacher Mode: Explain concepts from scratch if asked "ye kya hota hai".
# # 82. Mentor Mode: Guide the user to best practices.
# # 83. Consultant Mode: Focus on business impact (ROI, efficiency).
# # 84. Architect Mode: Focus on database structure and scalability.
# # 85. Debugger Mode: Focus solely on stack traces and missing data.
# # 86. Business Analyst Mode: Map user requirements to Frappe modules.
# # 87. Code Reviewer Mode: Critique code snippets strictly.
# # 88. Documentation Writer: Write clear SOPs if requested.
# # 89. Interviewer Mode: Ask challenging ERPNext questions if instructed.
# # 90. Planner Mode: Outline app development steps.
# # Automatically switch modes based on Level 2 (User Understanding).
# # </level_9_special_modes>
# # """

# # # ==========================================
# # # MODULE 10: ERPNEXT DOMAINS
# # # ==========================================
# # MOD_10_ERPNEXT = """
# # <level_10_erpnext>
# # 91. HR: Payroll, Attendance, Leaves, Appraisals.
# # 92. CRM: Leads, Opportunities, Campaigns (UTM Analytics).
# # 93. Buying: Material Requests, RFQ, Supplier Quotation, Purchase Order.
# # 94. Selling: Quotation, Sales Order, Delivery Note.
# # 95. Stock: Stock Entry, Material Transfer, Reconciliation.
# # 96. Manufacturing: Production Plan, Work Order, Job Card.
# # 97. Projects: Tasks, Timesheets, Project Profitability.
# # 98. Support: Issues, SLAs, Warranty Claims.
# # 99. Accounts: Sales/Purchase Invoice, Payment Entry, Cost Centers.
# # 100. Custom Apps: App creation, DocType overrides, Custom Hooks.
# # Map the user's query to the correct domain context immediately.
# # </level_10_erpnext>
# # """

# # # ==========================================
# # # MODULE 11: ADVANCED
# # # ==========================================
# # MOD_11_ADVANCED = """
# # <level_11_advanced>
# # 101. Token Optimization: Never output redundant data.
# # 102. Context Compression: Summarize past turns internally.
# # 103. Long Conversation Handling: Keep anchoring to the core issue.
# # 104. Repetition Reduction: NEVER repeat the user's question back to them.
# # 105. Dynamic Response Length: 1 line for "what is X?", 10 lines for "write a script for X".
# # 106. Smart Defaults: If Frappe version is not mentioned, assume v14/v15.
# # 107. Progressive Disclosure: Give the basic answer first. Let them ask for deep details.
# # 108. Incremental Reasoning: Solve step 1 before confusing them with step 5.
# # 109. Clarification Strategy: "Bhai, aap 'X' field ki baat kar rahe ho ya 'Y' DocType ki?"
# # 110. Conversation Recovery: If lost, reset gracefully: "Shuru se dekhte hain..."
# # </level_11_advanced>
# # """

# # # ==========================================
# # # MODULE 12: FINAL OUTPUT CRITERIA
# # # ==========================================
# # MOD_12_FINAL_OUTPUT = """
# # <level_12_final_output>
# # 111. Accuracy: Is the Frappe logic 100% correct?
# # 112. Helpfulness: Does this actually solve the user's problem?
# # 113. Professionalism: Is the tone respectful?
# # 114. Human-like Tone: Does it sound like a smart colleague (Hinglish)?
# # 115. Simplicity: Are complex things explained simply?
# # 116. Confidence: Is the answer definitive?
# # 117. Actionability: Does the user know EXACTLY what to click or type next?
# # 118. Consistency: Does it align with standard ERP workflows?
# # 119. User Satisfaction: Will this answer relieve the user's frustration?
# # 120. Completion Criteria: The prompt is executed perfectly only if ALL 120 rules are honored.
# # </level_12_final_output>
# # """

# # # ==========================================
# # # MASTER COMPILER FUNCTION
# # # ==========================================
# # # ==========================================
# # # MASTER COMPILER FUNCTION (UPDATED FOR OVERLOAD FIX)
# # # ==========================================
# # def build_enterprise_prompt(question, context, tool_outputs):
# #     # Assemble the modules dynamically
# #     system_prompt = "\n".join([
# #         MOD_01_FOUNDATION,
# #         MOD_02_USER_UNDERSTANDING,
# #         MOD_03_REASONING,
# #         MOD_04_KNOWLEDGE,
# #         MOD_05_TOOLS,
# #         MOD_06_CODING,
# #         MOD_07_RESPONSE_GENERATION,
# #         MOD_08_QUALITY,
# #         MOD_09_SPECIAL_MODES,
# #         MOD_10_ERPNEXT,
# #         MOD_11_ADVANCED,
# #         MOD_12_FINAL_OUTPUT
# #     ])

# #     # ADDING STRICT OVERRIDE FOR SMALLER MODELS
# #     system_prompt += """
# # \n<critical_override>
# # 1. NEVER output a list of mandatory fields unless explicitly asked.
# # 2. If the user asks a concept question (e.g., "iska kya kaam hai?", "samjhao"), give a 1-2 line real-world analogy and STOP. DO NOT summarize the form data.
# # 3. Treat the user as a smart professional who wants concise, 1000-character max answers. No fluff.
# # </critical_override>
# # """

# #     q_lower = (question or "").lower()
# #     # Detect if user actually wants form analysis
# #     is_error_query = any(word in q_lower for word in ["missing", "mandatory", "error", "save", "kya bacha", "check"])
# #     # Detect if user just wants an explanation
# #     is_concept_query = any(word in q_lower for word in ["kya hota", "kaam hai", "matlab", "samjhao", "explain", "how to", "kya hai"])

# #     filtered_outputs = []

# #     for item in tool_outputs:
# #         tool_name = item.get("tool")
# #         result = item.get("result")
        
# #         # 1. Filter Schema Data
# #         if tool_name == "get_doctype_schema" and isinstance(result, dict) and "fields" in result:
# #             matched_fields = []
# #             for f in result.get("fields", []):
# #                 f_name = str(f.get("fieldname", "")).lower()
# #                 f_label = str(f.get("label", "")).lower()
# #                 if f_name in q_lower or (f_label and f_label in q_lower):
# #                     matched_fields.append(f)
            
# #             if matched_fields:
# #                 result["fields"] = matched_fields
# #             elif is_error_query:
# #                 result["fields"] = [f for f in result.get("fields", []) if f.get("reqd")]
# #             else:
# #                 result["fields"] = "Hidden. Do not guess fields."

# #         # 2. STRICT FILTER: Hide Form Data if it's just a concept question
# #         if tool_name == "analyze_current_doc":
# #             if is_concept_query and not is_error_query:
# #                 result = "Hidden. User is asking for an explanation, NOT form analysis. Focus only on answering their question."
# #             elif isinstance(result, dict):
# #                 # Always hide filled summary unless specifically asked to summarize
# #                 if "filled_summary" in result:
# #                     result["filled_summary"] = "Hidden to save tokens."
# #                 if not is_error_query and "missing_required" in result:
# #                     result["missing_required"] = "Hidden. User didn't ask for missing fields."

# #         filtered_outputs.append({
# #             "tool": tool_name,
# #             "args": item.get("args"),
# #             "result": result
# #         })

# #     payload = {
# #         "question": question,
# #         "current_context": context,
# #         "tool_outputs": filtered_outputs,
# #     }

# #     payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False, default=str)

# #     MAX_PAYLOAD_CHARS = 15000 # Reduced payload limit to keep AI focused
# #     if len(payload_str) > MAX_PAYLOAD_CHARS:
# #         frappe.logger().warning("[Classic Chatbot] Payload too large, truncating data...")
# #         payload_str = payload_str[:MAX_PAYLOAD_CHARS] + '... [DATA TRUNCATED]'

# #     return [
# #         {
# #             "role": "system",
# #             "content": system_prompt,
# #         },
# #         {
# #             "role": "user",
# #             "content": payload_str,
# #         },
# #     ]

# # # ==========================================
# # # API & LLM CONNECTION CONFIGURATION
# # # ==========================================
# # def get_llm_config():
# #     return {
# #         # Local Ollama Config
# #         "local_model": frappe.conf.get("classic_chatbot_local_model") or "llama3.2",
# #         "local_base_url": frappe.conf.get("classic_chatbot_local_url") or "http://localhost:11434",
        
# #         # Groq Config (Fetches from site_config.json, uses hardcoded key if not found)
# #         "groq_api_key": frappe.conf.get("classic_chatbot_groq_api_key") or "***REMOVED***",
# #         "groq_model": frappe.conf.get("classic_chatbot_groq_model") or "llama-3.1-8b-instant",
        
# #         "temperature": float(frappe.conf.get("classic_chatbot_temperature") or 0.2),
# #     }


# # def call_ollama(messages, conf):
# #     url = conf["local_base_url"].rstrip("/") + "/api/chat"

# #     payload = {
# #         "model": conf["local_model"],
# #         "messages": messages,
# #         "stream": True,
# #         "options": {
# #             "temperature": conf["temperature"],
# #             "num_ctx": 2048
# #         },
# #     }

# #     response = requests.post(url, json=payload, timeout=15)
# #     response.raise_for_status()

# #     data = response.json()
# #     return data.get("message", {}).get("content") or data.get("response") or ""


# # def call_groq(messages, conf):
# #     url = "https://api.groq.com/openai/v1/chat/completions"

# #     # THIS IS WHERE GROQ CONNECTS WITH YOUR API KEY
# #     headers = {
# #         "Content-Type": "application/json",
# #         "Authorization": f"Bearer {conf['groq_api_key']}"
# #     }

# #     payload = {
# #         "model": conf["groq_model"],
# #         "messages": messages,
# #         "temperature": conf["temperature"],
# #     }

# #     response = requests.post(url, json=payload, headers=headers, timeout=30)
# #     response.raise_for_status()

# #     data = response.json()
# #     return data["choices"][0]["message"]["content"]


# # def check_if_answer_is_poor(answer):
# #     if not answer or len(answer.strip()) < 10:
# #         return True
        
# #     bad_phrases = [
# #         "i don't know", "i am not sure", "mujhe nahi pata", 
# #         "i cannot determine", "context read ho gaya", "an ai language model",
# #         "i am sorry"
# #     ]
    
# #     ans_lower = answer.lower()
# #     for phrase in bad_phrases:
# #         if phrase in ans_lower:
# #             return True
            
# #     return False


# # def smart_llm_router(messages, preferred_model="auto"):
# #     conf = get_llm_config()
    
# #     # CASE 1: User strictly wants GROQ API
# #     if preferred_model == "groq":
# #         if conf.get("groq_api_key"):
# #             frappe.logger().info("[Classic Chatbot] User selected Groq API directly...")
# #             try:
# #                 groq_answer = call_groq(messages, conf)
# #                 return groq_answer, "☁️ Groq API (Manual)"
# #             except Exception as groq_err:
# #                 return f"Groq fail ho gaya. Error: {str(groq_err)}", "⚠️ Error"
# #         else:
# #             return "Groq select kiya par API Key configure nahi hai.", "⚠️ Error"

# #     # CASE 2: User strictly wants LOCAL MODEL
# #     if preferred_model == "local":
# #         frappe.logger().info("[Classic Chatbot] User selected Local Model directly...")
# #         try:
# #             local_answer = call_ollama(messages, conf)
# #             return local_answer, "🖥️ Local Model (Strict)"
# #         except Exception as e:
# #             return f"Local server down hai. Error: {str(e)}", "⚠️ Error"

# #     # CASE 3: AUTO (Local First, Fallback to Groq)
# #     try:
# #         frappe.logger().info("[Classic Chatbot] Trying Local Model (Auto)...")
# #         local_answer = call_ollama(messages, conf)
        
# #         if check_if_answer_is_poor(local_answer):
# #             frappe.logger().info("[Classic Chatbot] Local answer poor tha, Groq par switch kar rahe hain...")
# #             raise Exception("Poor Quality Answer from Local Model")
            
# #         return local_answer, "🖥️ Local Model (Auto)"
        
# #     except Exception as e:
# #         frappe.logger().error(f"[Classic Chatbot] Local Fallback Triggered: {e}")
        
# #         if conf.get("groq_api_key"):
# #             frappe.logger().info("[Classic Chatbot] Calling Groq API via Auto Fallback...")
# #             try:
# #                 groq_answer = call_groq(messages, conf)
# #                 return groq_answer, "☁️ Groq API (Fallback)"
# #             except Exception as groq_err:
# #                 return f"Local aur Groq dono fail ho gaye. Error: {str(groq_err)}", "⚠️ Error"
# #         else:
# #             return f"Local model fail ho gaya aur Groq ki API key nahi mili. Local Error: {str(e)}", "⚠️ Error"


# # def build_tool_plan(question, context):
# #     q = (question or "").lower()

# #     doctype = context.get("doctype")
# #     doc = context.get("doc")
# #     error = context.get("error")
# #     docname = context.get("docname")

# #     plan = []

# #     if doctype:
# #         plan.append({
# #             "tool": "get_doctype_schema",
# #             "args": {
# #                 "doctype": doctype,
# #             },
# #         })

# #     if doctype and isinstance(doc, dict):
# #         plan.append({
# #             "tool": "analyze_current_doc",
# #             "args": {
# #                 "doctype": doctype,
# #                 "doc": doc,
# #             },
# #         })

# #     if error:
# #         plan.append({
# #             "tool": "explain_error",
# #             "args": {
# #                 "doctype": doctype,
# #                 "doc": doc,
# #                 "error": error,
# #             },
# #         })

# #     field_hint = detect_field_from_question(question)
# #     if doctype and field_hint:
# #         plan.append({
# #             "tool": "get_field_help",
# #             "args": {
# #                 "doctype": doctype,
# #                 "fieldname": field_hint,
# #             },
# #         })

# #     if doctype and docname and any(word in q for word in ["record", "document", "doc", "details", "data", "open"]):
# #         plan.append({
# #             "tool": "get_record",
# #             "args": {
# #                 "doctype": doctype,
# #                 "name": docname,
# #             },
# #         })

# #     if doctype and any(word in q for word in ["link", "connect", "relation", "kis kis", "kaha use"]):
# #         plan.append({
# #             "tool": "get_linked_doctypes",
# #             "args": {
# #                 "doctype": doctype,
# #             },
# #         })

# #     return plan


# # def run_tool_plan(plan):
# #     outputs = []

# #     for step in plan:
# #         tool_name = step.get("tool")
# #         args = step.get("args") or {}

# #         if tool_name == "get_linked_doctypes":
# #             target_dt = args.get("doctype")
# #             try:
# #                 links = frappe.get_all("DocField", filters={"fieldtype": "Link", "options": target_dt}, pluck="parent")
# #                 custom_links = frappe.get_all("Custom Field", filters={"fieldtype": "Link", "options": target_dt}, pluck="dt")
# #                 unique_links = sorted(list(set(links + custom_links)))
                
# #                 result = {
# #                     "message": f"{target_dt} in doctypes ke sath link hai.",
# #                     "linked_doctypes": unique_links,
# #                     "total_links": len(unique_links)
# #                 }
# #             except Exception as e:
# #                 result = {"error": f"Links fetch karne me error aaya: {str(e)}"}
# #         else:
# #             result = run_tool(tool_name, args)

# #         outputs.append({
# #             "tool": tool_name,
# #             "args": args,
# #             "result": result,
# #         })

# #     return outputs


# # def fallback_answer(question, context, tool_outputs):
# #     doctype = context.get("doctype")
# #     error = context.get("error")

# #     lines = []

# #     if doctype:
# #         lines.append(f"Aap abhi **{doctype}** DocType par ho.")

# #     for item in tool_outputs:
# #         if item.get("tool") == "analyze_current_doc":
# #             result = item.get("result") or {}
# #             missing = result.get("missing_required") or []
# #             invalid_links = result.get("invalid_links") or []

# #             if missing:
# #                 lines.append("")
# #                 lines.append("Mandatory fields missing lag rahi hain:")
# #                 for row in missing:
# #                     lines.append(f"- {row.get('label')} ({row.get('fieldname')})")

# #             if invalid_links:
# #                 lines.append("")
# #                 lines.append("Invalid link values mil rahe hain:")
# #                 for row in invalid_links:
# #                     lines.append(
# #                         f"- {row.get('label')}: {row.get('value')} not found in {row.get('linked_doctype')}"
# #                     )

# #     if error:
# #         lines.append("")
# #         lines.append(f"Last error: {error}")

# #     if not lines:
# #         lines.append("Context read ho gaya, lekin specific issue detect nahi hua. Question thoda detail me likho.")

# #     return "\n".join(lines)


# # @frappe.whitelist()
# # def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
# #     if not question:
# #         frappe.throw("Question is required")

# #     context = {
# #         "doctype": doctype,
# #         "docname": docname,
# #         "doc": clean_doc(safe_json(doc, {})),
# #         "route": safe_json(route, []),
# #         "error": error,
# #         "user": frappe.session.user,
# #     }

# #     plan = build_tool_plan(question, context)
# #     tool_outputs = run_tool_plan(plan)

# #     model_used = "System"
# #     try:
# #         messages = build_enterprise_prompt(question, context, tool_outputs)
# #         answer, model_used = smart_llm_router(messages, preferred_model)
# #     except Exception as e:
# #         answer = fallback_answer(question, context, tool_outputs)
# #         answer += f"\n\nAI model connect nahi hua: {str(e)}"
# #         model_used = "⚙️ Fallback Rule"

# #     return {
# #         "answer": answer,
# #         "model_used": model_used, 
# #         "tools_used": [step.get("tool") for step in plan],
# #     }


# # @frappe.whitelist()
# # def inspect_current_context(doctype=None, docname=None, doc=None, route=None, error=None):
# #     context = {
# #         "doctype": doctype,
# #         "docname": docname,
# #         "doc": clean_doc(safe_json(doc, {})),
# #         "route": safe_json(route, []),
# #         "error": error,
# #         "user": frappe.session.user,
# #     }

# #     plan = build_tool_plan("analyze current form", context)
# #     outputs = run_tool_plan(plan)

# #     return {
# #         "context": context,
# #         "tools_used": [p.get("tool") for p in plan],
# #         "tool_outputs": outputs,
# #     }











































































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
        "local_model": (
            frappe.conf.get(
                "classic_chatbot_local_model"
            )
            or "qwen2.5:7b-instruct"
        ),

        "local_base_url": (
            frappe.conf.get(
                "classic_chatbot_local_url"
            )
            or "http://127.0.0.1:11434"
        ),

        "local_timeout": int(
            frappe.conf.get(
                "classic_chatbot_local_timeout"
            )
            or 120
        ),

        "keep_alive": (
            frappe.conf.get(
                "classic_chatbot_keep_alive"
            )
            or "1h"
        ),

        # 2048 is too small for schema planning.
        "num_ctx": int(
            frappe.conf.get(
                "classic_chatbot_num_ctx"
            )
            or 4096
        ),

        "num_predict": int(
            frappe.conf.get(
                "classic_chatbot_num_predict"
            )
            or 300
        ),

        "temperature": float(
            frappe.conf.get(
                "classic_chatbot_temperature"
            )
            or 0.0
        ),

        "groq_api_key": frappe.conf.get(
            "classic_chatbot_groq_api_key"
        ),

        "groq_model": (
            frappe.conf.get(
                "classic_chatbot_groq_model"
            )
            or "llama-3.3-70b-versatile"
        ),

        # Compact prompts only.
        "max_catalog_chars": int(
            frappe.conf.get(
                "classic_chatbot_max_catalog_chars"
            )
            or 7000
        ),

        "max_schema_chars": int(
            frappe.conf.get(
                "classic_chatbot_max_schema_chars"
            )
            or 9000
        ),

        "max_result_rows": int(
            frappe.conf.get(
                "classic_chatbot_max_result_rows"
            )
            or 50
        ),

        "max_count_scan_rows": int(
            frappe.conf.get(
                "classic_chatbot_max_count_scan_rows"
            )
            or 500000
        ),
    }

# Local Ollama server (localhost:11434) ko HTTP request bhejta hai messages ke sath, 
# aur model ka text response wapas laata hai. expect_json=True ho to Ollama ko force karta hai valid JSON hi dene ke liye.


def call_ollama(
    messages,
    conf=None,
    timeout=None,
    expect_json=False,
):
    """
    Send a context-safe request to local Ollama.
    """

    conf = conf or get_llm_config()

    local_model = (
        conf.get("local_model")
        or "qwen2.5:7b-instruct"
    )

    local_base_url = (
        conf.get("local_base_url")
        or "http://127.0.0.1:11434"
    ).rstrip("/")

    request_timeout = (
        int(timeout)
        if timeout is not None
        else int(
            conf.get("local_timeout")
            or 120
        )
    )

    num_ctx = max(
        int(conf.get("num_ctx") or 4096),
        1024,
    )

    num_predict = max(
        int(conf.get("num_predict") or 300),
        50,
    )

    safe_messages = fit_messages_to_context(
        messages=messages or [],
        num_ctx=num_ctx,
        num_predict=num_predict,
    )

    payload = {
        "model": local_model,
        "messages": safe_messages,
        "stream": False,
        "keep_alive": (
            conf.get("keep_alive")
            or "1h"
        ),
        "options": {
            "temperature": float(
                conf.get("temperature")
                or 0.0
            ),
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "top_p": 0.9,
            "repeat_penalty": 1.05,
        },
    }

    if expect_json:
        payload["format"] = "json"

    response = None
    url = f"{local_base_url}/api/chat"

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=request_timeout,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"URL: {url}\n"
                f"Timeout: {request_timeout}\n"
                f"Estimated prompt tokens: "
                f"{estimate_message_tokens(safe_messages)}\n\n"
                f"{frappe.get_traceback()}"
            ),
            title="Classic Chatbot Ollama Timeout",
        )

        raise RuntimeError(
            "Local model response timeout ho gaya."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Ollama Connection Error",
        )

        raise RuntimeError(
            "Ollama server se connection nahi ho raha."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        status_code = (
            response.status_code
            if response is not None
            else "Unknown"
        )

        error_text = (
            response.text[:2000]
            if response is not None
            else ""
        )

        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"URL: {url}\n"
                f"Status: {status_code}\n"
                f"Estimated prompt tokens: "
                f"{estimate_message_tokens(safe_messages)}\n"
                f"Response: {error_text}"
            ),
            title="Classic Chatbot Ollama HTTP Error",
        )

        if status_code == 404:
            raise RuntimeError(
                f"Ollama model `{local_model}` installed nahi hai."
            ) from exc

        if (
            status_code == 400
            and "context" in error_text.lower()
        ):
            raise RuntimeError(
                "Prompt model context se bada tha. "
                "Request automatically stop kar di gayi."
            ) from exc

        raise RuntimeError(
            "Ollama API error. "
            f"Status: {status_code}. "
            f"Details: {error_text or 'No details'}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Ollama Request Error",
        )

        raise RuntimeError(
            f"Ollama request fail ho gayi: {exc}"
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Ollama ne valid JSON response nahi diya."
        ) from exc

    if data.get("error"):
        raise RuntimeError(
            f"Ollama error: {data.get('error')}"
        )

    message = data.get("message") or {}

    return str(
        message.get("content")
        or data.get("response")
        or ""
    ).strip()


def call_ollama_with_tools(
    messages,
    tools=None,
    conf=None,
    timeout=None,
):
    """
    Send a tool-enabled request to the configured local Ollama model.

    Returns:
        dict: Complete Ollama assistant message, including tool_calls.
    """

    conf = conf or get_llm_config()

    local_model = (
        conf.get("local_model")
        or "llama3:latest"
    )

    local_base_url = (
        conf.get("local_base_url")
        or "http://127.0.0.1:11434"
    ).rstrip("/")

    request_timeout = (
        int(timeout)
        if timeout is not None
        else int(conf.get("local_timeout") or 180)
    )

    keep_alive = (
        conf.get("keep_alive")
        or "30m"
    )

    temperature = float(
        conf.get("temperature") or 0.05
    )

    num_ctx = int(
        conf.get("num_ctx") or 4096
    )

    num_predict = int(
        conf.get("num_predict") or 600
    )

    url = f"{local_base_url}/api/chat"

    payload = {
        "model": local_model,
        "messages": messages or [],
        "stream": False,
        "keep_alive": keep_alive,
        "options": {
            "temperature": temperature,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "top_p": 0.90,
            "repeat_penalty": 1.05,
        },
    }

    if tools:
        payload["tools"] = tools

    response = None

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=request_timeout,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"URL: {url}\n"
                f"Timeout: {request_timeout} seconds\n\n"
                f"{frappe.get_traceback()}"
            ),
            title="Classic Chatbot Ollama Tool Timeout",
        )

        raise Exception(
            f"Local model `{local_model}` ka tool-call "
            f"{request_timeout} seconds me complete nahi hua."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"URL: {url}\n\n"
                f"{frappe.get_traceback()}"
            ),
            title="Classic Chatbot Ollama Connection Error",
        )

        raise Exception(
            "Ollama server se connection nahi ho raha. "
            f"Configured URL: {local_base_url}."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        status_code = (
            response.status_code
            if response is not None
            else "Unknown"
        )

        error_text = ""

        if response is not None:
            try:
                error_text = response.text[:2000]
            except Exception:
                pass

        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"URL: {url}\n"
                f"Status: {status_code}\n"
                f"Response: {error_text}\n\n"
                f"{frappe.get_traceback()}"
            ),
            title="Classic Chatbot Ollama Tool HTTP Error",
        )

        if status_code == 404:
            raise Exception(
                f"Ollama model `{local_model}` nahi mila. "
                f"`ollama pull {local_model}` run karein."
            ) from exc

        raise Exception(
            "Ollama tool API error aaya. "
            f"Status: {status_code}. "
            f"Details: {error_text or 'No details'}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Classic Chatbot Ollama Tool Request Error",
        )

        raise Exception(
            f"Ollama tool request fail ho gayi: {str(exc)}"
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        response_text = ""

        try:
            response_text = response.text[:2000]
        except Exception:
            pass

        raise Exception(
            "Ollama ne valid JSON response nahi diya. "
            f"Response: {response_text or 'Empty response'}"
        ) from exc

    if data.get("error"):
        raise Exception(
            f"Ollama error: {data.get('error')}"
        )

    message = data.get("message")

    if not isinstance(message, dict):
        frappe.log_error(
            message=(
                f"Model: {local_model}\n"
                f"Full response: "
                f"{json.dumps(data, ensure_ascii=False, default=str)[:3000]}"
            ),
            title="Classic Chatbot Missing Ollama Message",
        )

        raise Exception(
            "Ollama response me assistant message nahi mila."
        )

    message.setdefault("role", "assistant")
    message.setdefault("content", "")

    tool_calls = message.get("tool_calls")

    if tool_calls is not None and not isinstance(tool_calls, list):
        message["tool_calls"] = []

    return message

# Same Call_ollama ki tarah tools bhi payload me bhejta hai — matlab model tool call request kar sakta hai.
# Ye pura message object return karta hai (jisme tool_calls ho sakte hain), sirf text nahi.
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
def llm_chat(
    messages,
    preferred_model="auto",
    expect_json=False,
):
    """
    Model router.

    preferred_model:
        local -> only local Ollama
        groq  -> only Groq
        auto  -> local first, optional Groq fallback
    """

    conf = get_llm_config()

    if preferred_model == "groq":
        text = call_groq(
            messages,
            conf=conf,
            timeout=60,
            expect_json=expect_json,
        )

        return (
            text,
            f"☁️ Groq API · {conf['groq_model']}",
        )

    if preferred_model == "local":
        text = call_ollama(
            messages,
            conf=conf,
            timeout=conf["local_timeout"],
            expect_json=expect_json,
        )

        if not text:
            raise Exception(
                "Local model ne empty response diya."
            )

        return (
            text,
            f"🖥️ Local Ollama · {conf['local_model']}",
        )

    # Auto mode: local Ollama first
    try:
        text = call_ollama(
            messages,
            conf=conf,
            timeout=conf["local_timeout"],
            expect_json=expect_json,
        )

        if not text or len(text.strip()) < 2:
            raise Exception(
                "Local model ne empty response diya."
            )

        return (
            text,
            f"🖥️ Local Ollama · {conf['local_model']}",
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Local Model Error",
        )

        if conf.get("groq_api_key"):
            text = call_groq(
                messages,
                conf=conf,
                timeout=60,
                expect_json=expect_json,
            )

            return (
                text,
                f"☁️ Groq Fallback · {conf['groq_model']}",
            )

        raise










def llm_chat_with_tools(
    messages,
    tools=None,
    preferred_model="auto",
):
    """
    Tool-enabled model router.
    """

    conf = get_llm_config()

    if preferred_model == "groq":
        message = call_groq_with_tools(
            messages,
            tools=tools,
            conf=conf,
            timeout=60,
        )

        return (
            message,
            f"☁️ Groq API · {conf['groq_model']}",
        )

    if preferred_model == "local":
        message = call_ollama_with_tools(
            messages,
            tools=tools,
            conf=conf,
            timeout=conf["local_timeout"],
        )

        return (
            message,
            f"🖥️ Local Ollama · {conf['local_model']}",
        )

    try:
        message = call_ollama_with_tools(
            messages,
            tools=tools,
            conf=conf,
            timeout=conf["local_timeout"],
        )

        return (
            message,
            f"🖥️ Local Ollama · {conf['local_model']}",
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Local Tool Model Error",
        )

        if conf.get("groq_api_key"):
            message = call_groq_with_tools(
                messages,
                tools=tools,
                conf=conf,
                timeout=60,
            )

            return (
                message,
                f"☁️ Groq Fallback · {conf['groq_model']}",
            )

        raise








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



def estimate_message_tokens(messages):
    """
    Conservative approximate token count.

    English/code/JSON ke liye around 4 characters per token hota hai.
    Safety ke liye 3 characters per token use kar rahe hain.
    """

    total_chars = 0

    for message in messages or []:
        if not isinstance(message, dict):
            continue

        total_chars += len(
            str(message.get("role") or "")
        )

        total_chars += len(
            str(message.get("content") or "")
        )

        total_chars += 20

    return max(
        1,
        total_chars // 3,
    )


def fit_messages_to_context(
    messages,
    num_ctx,
    num_predict,
    minimum_output_reserve=150,
):
    """
    Validate that request fits before calling Ollama.

    This prevents Ollama 400:
    request exceeds available context size.
    """

    context_size = max(
        safe_int(num_ctx, 4096),
        1024,
    )

    output_reserve = max(
        safe_int(num_predict, 300),
        minimum_output_reserve,
    )

    input_limit = max(
        context_size - output_reserve - 200,
        500,
    )

    estimated_input_tokens = (
        estimate_message_tokens(messages)
    )

    if estimated_input_tokens <= input_limit:
        return messages

    raise ValueError(
        "Model prompt context se bada hai. "
        f"Estimated input tokens: {estimated_input_tokens}, "
        f"allowed input tokens: {input_limit}. "
        "Schema/payload ko compact karna zaroori hai."
    )


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






def compact_schema_for_prompt(
    schema,
    max_fields=60,
):
    """
    Create a small schema representation for the planner.

    Complete descriptions, hidden fields and unnecessary metadata
    model ko nahi bheji jati.
    """

    if not isinstance(schema, dict):
        return None

    compact_fields = []

    for field in schema.get("fields") or []:
        if not isinstance(field, dict):
            continue

        fieldname = normalize_space(
            field.get("fieldname")
        )

        if not fieldname:
            continue

        if field.get("hidden"):
            continue

        compact_field = {
            "fieldname": fieldname,
            "label": normalize_space(
                field.get("label")
            )[:80],
            "fieldtype": normalize_space(
                field.get("fieldtype")
            ),
        }

        options = normalize_space(
            field.get("options")
        )

        if options:
            compact_field["options"] = (
                options[:100]
            )

        compact_fields.append(
            compact_field
        )

        if len(compact_fields) >= max_fields:
            break

    return {
        "doctype": schema.get("doctype"),
        "title_field": schema.get(
            "title_field"
        ),
        "search_fields": (
            schema.get("search_fields")
            or []
        )[:8],
        "fields": compact_fields,
    }


def compact_schema_bundle_for_prompt(
    schema_bundle,
):
    compact_schemas = []

    for schema in (
        schema_bundle.get("schemas")
        or []
    ):
        compact = compact_schema_for_prompt(
            schema
        )

        if compact:
            compact_schemas.append(compact)

    return {
        "selected_doctypes": (
            schema_bundle.get(
                "selected_doctypes"
            )
            or []
        ),
        "schemas": compact_schemas,
    }





# Catalog nikalta hai
# LLM ko question + catalog deta hai: "in me se 1-5 relevant DocTypes choose karo"
# LLM ka jawab validate karta hai (kya ye DocType sach me exist karta hai?)
# Fallbacks: LLM fail ho to (a) active screen ka DocType use karo, (b) question me DocType ka naam directly match karo
# Selected DocTypes ke schemas load karke return karta hai
def get_relevant_schema(
    question,
    context=None,
    preferred_model="auto",
):
    """
    Select relevant live DocType schemas.

    Fast path:
    - Current form/list DocType available ho to uska schema directly use karo.
    - All-DocType catalog aur LLM routing skip ho jati hai.

    Generic path:
    - Active DocType absent ho tab dynamic catalog routing chalegi.
    """

    context = context or {}

    active_doctype = normalize_space(
        context.get("doctype")
    )

    # ---------------------------------------------------------
    # FAST PATH: current screen already tells us the DocType
    # ---------------------------------------------------------

    if (
        active_doctype
        and frappe.db.exists(
            "DocType",
            active_doctype,
        )
    ):
        schema = get_schema_for_doctype(
            active_doctype
        )

        return {
            "selected_doctypes": [
                active_doctype
            ],
            "schemas": (
                [schema]
                if schema
                else []
            ),
            "router_reason": (
                "Active screen DocType used directly."
            ),
        }

    # ---------------------------------------------------------
    # GENERIC PATH: no active DocType available
    # ---------------------------------------------------------

    conf = get_llm_config()

    catalog = get_doctype_catalog()

    compact_catalog = []

    for row in catalog:
        compact_catalog.append({
            "doctype": row.get("doctype"),
            "module": row.get("module"),
            "title_field": row.get(
                "title_field"
            ),
            "description": truncate_text(
                row.get("description"),
                80,
            ),
        })

    catalog_payload = {
        "user_question": normalize_space(
            question
        ),
        "doctype_catalog": compact_catalog,
    }

    system_prompt = """
You are a Frappe DocType router.

Select only the actual DocTypes needed to answer the user's question.

Rules:
1. Use only DocTypes supplied in the catalog.
2. Never invent a DocType.
3. Select maximum 3 DocTypes.
4. Return JSON only.

Format:
{
  "doctypes": ["Exact DocType"],
  "reason": "short reason"
}
""".strip()

    router_conf = conf.copy()

    router_conf["num_ctx"] = min(
        safe_int(
            conf.get("num_ctx"),
            2048,
        ),
        1536,
    )

    router_conf["num_predict"] = 100
    router_conf["temperature"] = 0.0

    selected_data = {}

    try:
        raw = call_ollama(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": 
                        truncate_text(
                        json.dumps(
                            catalog_payload,
                            ensure_ascii=False,
                            default=str,
                        ),
                        
                            6000
                        
                    ),
                },
            ],
            conf=router_conf,
            timeout=45,
            expect_json=True,
        )

        selected_data = (
            extract_json_object(raw)
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Classic Chatbot Schema Router Error",
        )

    selected = (
        selected_data.get("doctypes")
        or []
    )

    if isinstance(selected, str):
        selected = [selected]

    valid_doctypes = []

    for doctype in selected:
        doctype = normalize_space(
            doctype
        )

        if (
            doctype
            and frappe.db.exists(
                "DocType",
                doctype,
            )
            and doctype
            not in valid_doctypes
        ):
            valid_doctypes.append(
                doctype
            )

    # Dynamic exact-name fallback without business hardcoding.
    if not valid_doctypes:
        question_lower = normalize_space(
            question
        ).lower()

        for row in catalog:
            doctype = row.get("doctype")

            if (
                doctype
                and doctype.lower()
                in question_lower
            ):
                valid_doctypes.append(
                    doctype
                )
                break

    schemas = []

    for doctype in valid_doctypes[:3]:
        schema = get_schema_for_doctype(
            doctype
        )

        if schema:
            schemas.append(schema)

    return {
        "selected_doctypes": (
            valid_doctypes[:3]
        ),
        "schemas": schemas,
        "router_reason": selected_data.get(
            "reason"
        ),
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








def permission_aware_count(
    doctype,
    filters=None,
    or_filters=None,
    order_by="modified desc",
    page_size=5000,
    maximum_rows=500000,
):
    """
    Count permission-visible records safely using pagination.

    frappe.get_list() user permissions apply karta hai.
    Raw SQL aur ignore_permissions use nahi hota.

    maximum_rows accidental extremely large scans ko rokta hai.
    """

    filters = filters or []
    or_filters = or_filters or None

    page_size = safe_int(page_size, 5000)
    page_size = max(100, min(page_size, 10000))

    maximum_rows = safe_int(
        maximum_rows,
        500000,
    )
    maximum_rows = max(
        page_size,
        maximum_rows,
    )

    total = 0
    start = 0
    sample_records = []

    while total < maximum_rows:
        remaining = maximum_rows - total
        current_page_size = min(
            page_size,
            remaining,
        )

        rows = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters,
            fields=["name"],
            limit_start=start,
            limit_page_length=current_page_size,
            order_by=order_by,
        )

        row_count = len(rows)

        if len(sample_records) < 10:
            required = 10 - len(sample_records)
            sample_records.extend(
                rows[:required]
            )

        total += row_count

        if row_count < current_page_size:
            return {
                "count": total,
                "sample_records": sample_records,
                "truncated": False,
            }

        start += row_count

    return {
        "count": total,
        "sample_records": sample_records,
        "truncated": True,
    }





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
    Execute a validated ERP query plan through permission-aware Frappe APIs.

    Supported operations:
    - count
    - list
    - get
    - sum
    - avg
    - min
    - max

    Security:
    - No raw SQL
    - No ignore_permissions
    - Fields and filters are schema validated
    - User read permissions are respected
    """

    if not isinstance(plan, dict):
        return {
            "ok": False,
            "error": "Invalid query plan.",
        }

    if plan.get("needs_clarification"):
        return {
            "ok": False,
            "needs_clarification": True,
            "clarifying_question": (
                plan.get("clarifying_question")
                or "Kripaya apna sawaal thoda specific karein."
            ),
        }

    operation = normalize_space(
        plan.get("operation")
        or "list"
    ).lower()

    if operation not in ALLOWED_OPERATIONS:
        operation = "list"

    doctype = normalize_space(
        plan.get("doctype")
    )

    if not doctype:
        return {
            "ok": False,
            "error": "DocType query plan me missing hai.",
        }

    schema = find_schema(
        schema_bundle,
        doctype,
    )

    if not schema:
        return {
            "ok": False,
            "error": (
                "Relevant DocType schema nahi mila."
            ),
        }

    if not frappe.has_permission(
        doctype,
        "read",
    ):
        return {
            "ok": False,
            "error": (
                f"Aapko {doctype} read karne ki "
                "permission nahi hai."
            ),
        }

    filters, or_filters, dropped = sanitize_filters(
        plan,
        schema,
    )

    original_filter_count = len(
        normalize_filter_input(
            plan.get("filters"),
            doctype,
        )
    )

    original_or_filter_count = len(
        normalize_filter_input(
            plan.get("or_filters"),
            doctype,
        )
    )

    had_requested_filters = bool(
        original_filter_count
        or original_or_filter_count
    )

    if (
        had_requested_filters
        and dropped
        and not filters
        and not or_filters
    ):
        return {
            "ok": False,
            "error": (
                "Query ke saare filters invalid the. "
                "Unfiltered query security ke liye nahi chalayi gayi. "
                "get_schema tool se exact fieldnames dekh kar retry karein. "
                f"Dropped filters: {dropped}"
            ),
        }

    filters, or_filters = resolve_link_field_filters(
        filters,
        or_filters,
        schema,
    )

    filters, or_filters = expand_text_search(
        filters,
        or_filters,
        schema,
    )

    fields = sanitize_fields(
        plan,
        schema,
    )

    order_by = sanitize_order_by(
        plan.get("order_by"),
        schema,
    )

    config = get_llm_config()

    limit = safe_int(
        plan.get("limit"),
        10,
    )

    limit = max(
        1,
        min(
            limit,
            config["max_result_rows"],
        ),
    )

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    if operation == "count":
        count_result = permission_aware_count(
            doctype=doctype,
            filters=filters,
            or_filters=or_filters,
            order_by=order_by,
            page_size=5000,
            maximum_rows=max(
                config["max_count_scan_rows"],
                500000,
            ),
        )

        return {
            "ok": True,
            "operation": "count",
            "doctype": doctype,
            "count": count_result["count"],
            "sample_records": [
                clean_record(row)
                for row in count_result[
                    "sample_records"
                ]
            ],
            "truncated": count_result["truncated"],
            "warning": (
                "Count configured maximum limit tak pahunch gaya. "
                "Actual count isse zyada ho sakta hai."
                if count_result["truncated"]
                else None
            ),
            "plan": {
                "filters": filters,
                "or_filters": or_filters,
                "fields": ["name"],
                "order_by": order_by,
            },
        }

    # ---------------------------------------------------------
    # List / Get
    # ---------------------------------------------------------

    if operation in {"list", "get"}:
        query_limit = (
            1
            if operation == "get"
            else limit
        )

        rows = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters or None,
            fields=fields,
            limit_page_length=query_limit,
            order_by=order_by,
        )

        cleaned_rows = [
            clean_record(row)
            for row in rows
        ]

        return {
            "ok": True,
            "operation": operation,
            "doctype": doctype,
            "records": cleaned_rows,
            "shown_count": len(cleaned_rows),
            "plan": {
                "filters": filters,
                "or_filters": or_filters,
                "fields": fields,
                "order_by": order_by,
                "limit": query_limit,
            },
        }

    # ---------------------------------------------------------
    # Numeric aggregates
    # ---------------------------------------------------------

    aggregate_field = normalize_space(
        plan.get("aggregate_field")
    )

    valid_fields = get_valid_fields_map(
        schema
    )

    if aggregate_field not in valid_fields:
        return {
            "ok": False,
            "error": (
                "Aggregate field schema me valid nahi hai."
            ),
        }

    aggregate_meta = valid_fields[
        aggregate_field
    ]

    allowed_numeric_fieldtypes = {
        "Int",
        "Long Int",
        "Float",
        "Currency",
        "Percent",
        "Duration",
        "Rating",
    }

    if (
        aggregate_meta.get("fieldtype")
        not in allowed_numeric_fieldtypes
    ):
        return {
            "ok": False,
            "error": (
                f"{aggregate_field} numeric field nahi hai. "
                "sum/avg/min/max sirf numeric fields par allowed hain."
            ),
        }

    page_size = 5000
    maximum_rows = max(
        config["max_count_scan_rows"],
        500000,
    )

    start = 0
    matched_rows = 0
    values = []
    truncated = False

    while matched_rows < maximum_rows:
        remaining = (
            maximum_rows
            - matched_rows
        )

        current_page_size = min(
            page_size,
            remaining,
        )

        rows = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters or None,
            fields=[
                "name",
                aggregate_field,
            ],
            limit_start=start,
            limit_page_length=current_page_size,
            order_by=order_by,
        )

        row_count = len(rows)
        matched_rows += row_count

        for row in rows:
            value = row.get(
                aggregate_field
            )

            if value is None or value == "":
                continue

            try:
                values.append(
                    float(value)
                )
            except (
                TypeError,
                ValueError,
            ):
                continue

        if row_count < current_page_size:
            break

        start += row_count

    if matched_rows >= maximum_rows:
        truncated = True

    if operation == "sum":
        aggregate_value = sum(values)

    elif operation == "avg":
        aggregate_value = (
            sum(values) / len(values)
            if values
            else 0
        )

    elif operation == "min":
        aggregate_value = (
            min(values)
            if values
            else 0
        )

    elif operation == "max":
        aggregate_value = (
            max(values)
            if values
            else 0
        )

    else:
        return {
            "ok": False,
            "error": (
                f"Unsupported aggregate operation: {operation}"
            ),
        }

    return {
        "ok": True,
        "operation": operation,
        "doctype": doctype,
        "aggregate_field": aggregate_field,
        "value": aggregate_value,
        "matched_rows": matched_rows,
        "numeric_value_count": len(values),
        "truncated": truncated,
        "warning": (
            "Aggregate configured maximum rows tak calculate hua. "
            "Actual result different ho sakta hai."
            if truncated
            else None
        ),
        "plan": {
            "filters": filters,
            "or_filters": or_filters,
            "fields": [
                "name",
                aggregate_field,
            ],
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
            validation_words = [
                "check", "validate", "validation", "mistake", "galti",
                "wrong", "incorrect", "error", "save", "submit",
                "format", "nature", "field", "filed",
            ]
            validation_tool = (
                "validate_current_document"
                if any(word in q for word in validation_words)
                else "analyze_current_doc"
            )
            plan.append({
                "tool": validation_tool,
                "args": {"doctype": doctype, "doc": doc},
            })
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


FORM_VALIDATION_SYSTEM_PROMPT = """
You are a schema-aware ERP form validation agent.

You will receive:

1. The current Frappe DocType name.
2. The complete live DocType field schema.
3. Current unsaved values entered by the user.
4. Child-table schemas and child-table values.
5. Deterministic validation results from Frappe.
6. The user's question or validation issue.

Your job is to understand the intended nature of every field dynamically.

Validation rules:

- Never use hardcoded knowledge about a particular DocType or field.
- Never assume that a specific field always has a fixed business meaning.
- Use the live field label, fieldname, fieldtype, description, options,
  mandatory state, dependencies, sibling fields and current values.
- Compare each value with the purpose indicated by its field metadata.
- Detect semantic mismatches, misplaced data, contradictory data,
  incomplete data, unsuitable formatting and values that appear to belong
  to another available field.
- Analyze relationships between sibling fields.
- Analyze child-table fields and their row values.
- Never invent a field that is not present in the supplied schema.
- Never claim that a field is empty when the current value is supplied.
- Do not flag harmless style differences unless the schema or description
  clearly requires a particular style.
- Only report a semantic mistake when confidence is high.
- If metadata is insufficient to establish a mistake, say that the issue
  cannot be confirmed from the schema.
- Give the correction based on the actual schema and current values.
- Do not apply a field-specific fallback rule.
- Do not use database query planning for this task.

Reply in professional conversational Hinglish using Roman script.

Response format:

Issue:
<what is wrong>

Reason:
<why it conflicts with the field schema or related fields>

Correction:
<what the user should enter or change>

Affected Field:
<exact field label and fieldname from the supplied schema>

If no mistake can be confirmed, clearly say:
"No high-confidence semantic mistake was found from the available schema."
"""


def _serialize_field_value(value, depth=0):
    """
    Convert current form values into safe JSON-compatible data.
    Keeps numbers, zero values, checks, dates and child-table rows.
    """

    if depth > 5:
        return None

    if value is None:
        return None

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ):
        return value

    if isinstance(value, list):
        return [
            _serialize_field_value(
                row,
                depth + 1,
            )
            for row in value[:100]
        ]

    if isinstance(value, dict):
        output = {}

        for key, child_value in value.items():
            key_text = str(key)

            if key_text.startswith("__"):
                continue

            if key_text in {
                "_liked_by",
                "_comments",
                "_assign",
                "_user_tags",
            }:
                continue

            output[key_text] = (
                _serialize_field_value(
                    child_value,
                    depth + 1,
                )
            )

        return output

    return str(value)


def _build_field_schema(
    df,
    current_value=None,
):
    """
    Build one field definition entirely from live Frappe metadata.
    No field or business rule is hardcoded.
    """

    return {
        "fieldname": df.fieldname,
        "label": df.label,
        "fieldtype": df.fieldtype,
        "options": df.options,
        "description": df.description,
        "mandatory": bool(df.reqd),
        "read_only": bool(df.read_only),
        "hidden": bool(df.hidden),
        "default": df.default,
        "unique": bool(
            getattr(
                df,
                "unique",
                False,
            )
        ),
        "length": getattr(
            df,
            "length",
            None,
        ),
        "depends_on": getattr(
            df,
            "depends_on",
            None,
        ),
        "mandatory_depends_on": getattr(
            df,
            "mandatory_depends_on",
            None,
        ),
        "read_only_depends_on": getattr(
            df,
            "read_only_depends_on",
            None,
        ),
        "fetch_from": getattr(
            df,
            "fetch_from",
            None,
        ),
        "current_value": (
            _serialize_field_value(
                current_value
            )
        ),
    }


def build_live_form_validation_context(
    doctype,
    doc_data,
):
    """
    Read the actual current DocType schema and current unsaved form data.

    The function does not know or assume any business field names.
    """

    if not doctype:
        raise ValueError(
            "Current DocType is missing."
        )

    if not frappe.db.exists(
        "DocType",
        doctype,
    ):
        raise ValueError(
            f"DocType not found: {doctype}"
        )

    if not frappe.has_permission(
        doctype,
        "read",
    ):
        raise frappe.PermissionError(
            f"No read permission for {doctype}"
        )

    meta = frappe.get_meta(doctype)

    cleaned_document = clean_doc(
        _serialize_field_value(
            doc_data or {}
        )
    )

    parent_fields = []
    child_tables = []

    for df in meta.fields:
        if not df.fieldname:
            continue

        if (
            df.fieldtype
            in FORM_LAYOUT_FIELD_TYPES
        ):
            continue

        current_value = cleaned_document.get(
            df.fieldname
        )

        parent_fields.append(
            _build_field_schema(
                df,
                current_value=current_value,
            )
        )

        if (
            df.fieldtype
            not in {
                "Table",
                "Table MultiSelect",
            }
            or not df.options
        ):
            continue

        try:
            child_meta = frappe.get_meta(
                df.options
            )
        except Exception:
            continue

        child_field_schema = []

        for child_df in child_meta.fields:
            if not child_df.fieldname:
                continue

            if (
                child_df.fieldtype
                in FORM_LAYOUT_FIELD_TYPES
            ):
                continue

            child_field_schema.append(
                _build_field_schema(
                    child_df
                )
            )

        child_rows = current_value

        if not isinstance(
            child_rows,
            list,
        ):
            child_rows = []

        child_tables.append(
            {
                "parent_fieldname": (
                    df.fieldname
                ),
                "parent_label": (
                    df.label
                ),
                "child_doctype": (
                    df.options
                ),
                "fields": (
                    child_field_schema
                ),
                "rows": (
                    child_rows[:50]
                ),
            }
        )

    deterministic_analysis = run_tool(
        "analyze_current_doc",
        {
            "doctype": doctype,
            "doc": cleaned_document,
        },
    )

    return {
        "doctype": doctype,
        "module": meta.module,
        "title_field": meta.title_field,
        "is_submittable": bool(
            meta.is_submittable
        ),
        "fields": parent_fields,
        "child_tables": child_tables,
        "current_document": (
            cleaned_document
        ),
        "deterministic_analysis": (
            deterministic_analysis
        ),
    }


def answer_dynamic_form_validation(
    question,
    context,
    preferred_model="local",
):
    """
    Ask the local model to determine the mistake from live metadata.

    No field-specific rule or fallback exists here.
    """

    doctype = context.get("doctype")

    document_data = context.get("doc")

    if not doctype:
        raise ValueError(
            "Open a DocType form before running form validation."
        )

    if not isinstance(
        document_data,
        dict,
    ):
        raise ValueError(
            "Current form data is not available."
        )

    validation_context = (
        build_live_form_validation_context(
            doctype=doctype,
            doc_data=document_data,
        )
    )

    payload = {
        "user_question": question,
        "active_doctype": doctype,
        "current_docname": (
            context.get("docname")
        ),
        "form_context": (
            validation_context
        ),
    }

    messages = [
        {
            "role": "system",
            "content": (
                FORM_VALIDATION_SYSTEM_PROMPT
            ),
        },
        {
            "role": "user",
            "content": truncate_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    default=str,
                ),
                30000,
            ),
        },
    ]

    answer, model_used = llm_chat(
        messages,
        preferred_model=(
            preferred_model or "local"
        ),
        expect_json=False,
    )

    answer = normalize_space(
        answer
    )

    if not answer:
        raise RuntimeError(
            "Local model returned an empty validation answer."
        )

    return (
        answer,
        model_used,
        validation_context,
    )


def is_form_validation_request(
    question,
    context,
):
    """
    This only routes the request.

    It does not decide the field, mistake type or correction.
    """

    if not context.get("doctype"):
        return False

    if not isinstance(
        context.get("doc"),
        dict,
    ):
        return False

    question_text = normalize_space(
        question
    ).lower()

    routing_terms = {
        "validation",
        "validate",
        "field error",
        "form error",
        "incorrect value",
        "wrong value",
        "correct value",
        "mandatory",
        "cannot be blank",
        "missing field",
        "current form",
        "check form",
        "fix form",
        "galti",
        "galat",
        "sahi value",
    }

    return any(
        term in question_text
        for term in routing_terms
    )








CURRENT_DOCUMENT_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "handled": {
            "type": "boolean",
        },
        "operation": {
            "type": "string",
            "enum": [
                "count_rows",
                "count_non_empty",
                "get_value",
                "sum_values",
                "average_values",
                "minimum_value",
                "maximum_value",
            ],
        },
        "fieldname": {
            "type": [
                "string",
                "null",
            ],
        },
        "child_fieldname": {
            "type": [
                "string",
                "null",
            ],
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "reason": {
            "type": "string",
        },
    },
    "required": [
        "handled",
        "operation",
        "fieldname",
        "child_fieldname",
        "confidence",
        "reason",
    ],
}


def _field_has_value(value):
    """
    Generic Frappe value-presence check.
    """

    return value not in (
        None,
        "",
        [],
        {},
    )


def _safe_live_rows(value):
    """
    Return active rows from a current unsaved child-table value.

    Browser-marked deleted rows are excluded.
    """

    if not isinstance(value, list):
        return []

    rows = []

    for row in value:
        if not isinstance(row, dict):
            continue

        if row.get("__deleted"):
            continue

        rows.append(row)

    return rows


def build_current_document_query_catalog(
    doctype,
    document,
):
    """
    Build a compact, completely metadata-driven catalog of the
    current document.

    No DocType name, business word or fieldname is assumed.
    """

    if not doctype:
        return {
            "doctype": None,
            "fields": [],
        }

    if not isinstance(document, dict):
        return {
            "doctype": doctype,
            "fields": [],
        }

    meta = frappe.get_meta(doctype)
    catalog = []

    for df in meta.fields:
        if not df.fieldname:
            continue

        if df.fieldtype in {
            "Section Break",
            "Column Break",
            "Tab Break",
            "HTML",
            "Button",
            "Image",
            "Fold",
            "Heading",
        }:
            continue

        value = document.get(df.fieldname)

        field_data = {
            "fieldname": df.fieldname,
            "label": df.label or df.fieldname,
            "fieldtype": df.fieldtype,
            "options": df.options,
            "description": normalize_space(
                df.description
            )[:250],
            "has_value": _field_has_value(value),
        }

        if df.fieldtype in {
            "Table",
            "Table MultiSelect",
        }:
            rows = _safe_live_rows(value)

            child_fields = []

            if df.options:
                try:
                    child_meta = frappe.get_meta(
                        df.options
                    )

                    for child_df in child_meta.fields:
                        if not child_df.fieldname:
                            continue

                        if child_df.fieldtype in {
                            "Section Break",
                            "Column Break",
                            "Tab Break",
                            "HTML",
                            "Button",
                            "Image",
                            "Fold",
                            "Heading",
                        }:
                            continue

                        child_fields.append({
                            "fieldname": (
                                child_df.fieldname
                            ),
                            "label": (
                                child_df.label
                                or child_df.fieldname
                            ),
                            "fieldtype": (
                                child_df.fieldtype
                            ),
                            "options": (
                                child_df.options
                            ),
                            "description": normalize_space(
                                child_df.description
                            )[:180],
                        })

                except Exception:
                    frappe.log_error(
                        frappe.get_traceback(),
                        (
                            "Classic Chatbot Current "
                            "Document Child Metadata Error"
                        ),
                    )

            field_data.update({
                "row_count": len(rows),
                "child_doctype": df.options,
                "child_fields": child_fields,
            })

        else:
            field_data["value_preview"] = (
                _json_safe_for_current_query(
                    value
                )
            )

        catalog.append(field_data)

    return {
        "doctype": doctype,
        "title_field": meta.title_field,
        "fields": catalog,
    }


def _json_safe_for_current_query(
    value,
    max_chars=300,
):
    """
    Prepare a small safe preview for query routing.
    """

    if value is None:
        return None

    if isinstance(
        value,
        (
            int,
            float,
            bool,
        ),
    ):
        return value

    if isinstance(value, str):
        return normalize_space(value)[
            :max_chars
        ]

    return str(value)[:max_chars]


def _get_current_query_llm_config():
    """
    Small and fast configuration for current-document routing.
    """

    base = get_llm_config().copy()

    base["num_ctx"] = 1024
    base["num_predict"] = 100
    base["temperature"] = 0.0

    return base


def resolve_current_document_query(
    question,
    context,
):
    """
    Let the local model map a natural-language question to one exact
    field from the current live DocType metadata.

    Important:
    - No fixed DocType names.
    - No fixed fieldnames.
    - No fixed business vocabulary.
    - Model only selects from supplied live metadata.
    - Python executes the selected operation.
    """

    doctype = context.get("doctype")
    document = context.get("doc")

    if not doctype:
        return {
            "handled": False,
        }

    if not isinstance(document, dict):
        return {
            "handled": False,
        }

    if not frappe.db.exists(
        "DocType",
        doctype,
    ):
        return {
            "handled": False,
        }

    if not (
        frappe.has_permission(
            doctype,
            "read",
        )
        or frappe.has_permission(
            doctype,
            "create",
        )
    ):
        return {
            "handled": False,
        }

    catalog = (
        build_current_document_query_catalog(
            doctype=doctype,
            document=document,
        )
    )

    if not catalog.get("fields"):
        return {
            "handled": False,
        }

    system_prompt = """
You are a routing engine for a currently open Frappe document.

Determine whether the user's question can be answered directly from the
supplied current-document metadata and current unsaved values.

You must not answer the question yourself. Return only a JSON execution plan.

Rules:
1. Never invent a DocType or field.
2. fieldname must exactly match one supplied top-level fieldname.
3. child_fieldname must exactly match a supplied child field when required.
4. Use count_rows only for the number of rows in one supplied table field.
5. Use count_non_empty for the number of populated values in a table child field.
6. Use get_value for one top-level field's current value.
7. Use sum_values, average_values, minimum_value or maximum_value only for
   numeric values in one supplied table child field.
8. If the question is not specifically about the current open document,
   return handled=false.
9. If the requested target cannot be selected confidently from the supplied
   labels, fieldnames, descriptions and types, return handled=false.
10. Do not use database knowledge, general field assumptions or hidden fields.
11. Return JSON only.
""".strip()

    payload = {
        "question": normalize_space(question),
        "current_document": catalog,
        "response_schema": (
            CURRENT_DOCUMENT_QUERY_SCHEMA
        ),
    }

    conf = _get_current_query_llm_config()

    raw = call_ollama(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": truncate_text(
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        default=str,
                    ),
                    16000,
                ),
            },
        ],
        conf=conf,
        timeout=45,
        expect_json=True,
    )

    plan = extract_json_object(raw)

    if not isinstance(plan, dict):
        return {
            "handled": False,
        }

    if not plan.get("handled"):
        return {
            "handled": False,
        }

    try:
        confidence = float(
            plan.get("confidence") or 0
        )
    except (
        TypeError,
        ValueError,
    ):
        confidence = 0.0

    if confidence < 0.70:
        return {
            "handled": False,
        }

    return validate_current_document_plan(
        plan=plan,
        catalog=catalog,
    )


def validate_current_document_plan(
    plan,
    catalog,
):
    """
    Validate every model-selected field against the actual live catalog.
    """

    allowed_operations = {
        "count_rows",
        "count_non_empty",
        "get_value",
        "sum_values",
        "average_values",
        "minimum_value",
        "maximum_value",
    }

    operation = normalize_space(
        plan.get("operation")
    )

    if operation not in allowed_operations:
        return {
            "handled": False,
        }

    fieldname = normalize_space(
        plan.get("fieldname")
    )

    if not fieldname:
        return {
            "handled": False,
        }

    field_map = {
        field.get("fieldname"): field
        for field in (
            catalog.get("fields") or []
        )
        if field.get("fieldname")
    }

    selected_field = field_map.get(
        fieldname
    )

    if not selected_field:
        return {
            "handled": False,
        }

    child_fieldname = normalize_space(
        plan.get("child_fieldname")
    ) or None

    table_operations = {
        "count_rows",
        "count_non_empty",
        "sum_values",
        "average_values",
        "minimum_value",
        "maximum_value",
    }

    child_operations = {
        "count_non_empty",
        "sum_values",
        "average_values",
        "minimum_value",
        "maximum_value",
    }

    if (
        operation in table_operations
        and selected_field.get(
            "fieldtype"
        )
        not in {
            "Table",
            "Table MultiSelect",
        }
    ):
        return {
            "handled": False,
        }

    if operation in child_operations:
        if not child_fieldname:
            return {
                "handled": False,
            }

        child_field_map = {
            field.get("fieldname"): field
            for field in (
                selected_field.get(
                    "child_fields"
                )
                or []
            )
            if field.get("fieldname")
        }

        if (
            child_fieldname
            not in child_field_map
        ):
            return {
                "handled": False,
            }

    if operation == "get_value":
        if selected_field.get(
            "fieldtype"
        ) in {
            "Table",
            "Table MultiSelect",
        }:
            return {
                "handled": False,
            }

    return {
        "handled": True,
        "operation": operation,
        "fieldname": fieldname,
        "child_fieldname": (
            child_fieldname
        ),
        "selected_field": (
            selected_field
        ),
        "confidence": plan.get(
            "confidence"
        ),
        "reason": plan.get(
            "reason"
        ),
    }


def _to_numeric_value(value):
    """
    Convert one current-document value to float without guessing.
    """

    if isinstance(value, bool):
        return None

    if value in (
        None,
        "",
    ):
        return None

    try:
        return float(
            str(value).replace(
                ",",
                "",
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        return None


def execute_current_document_plan(
    plan,
    context,
):
    """
    Execute the validated plan against the current unsaved document.
    """

    document = context.get("doc") or {}

    fieldname = plan["fieldname"]
    operation = plan["operation"]
    child_fieldname = plan.get(
        "child_fieldname"
    )

    selected_field = plan.get(
        "selected_field"
    ) or {}

    label = (
        selected_field.get("label")
        or fieldname
    )

    if operation == "get_value":
        value = document.get(fieldname)

        display_value = (
            value
            if _field_has_value(value)
            else "Blank"
        )

        return {
            "answer": (
                f"**{label}** ki current value: "
                f"**{display_value}**"
            ),
            "model_used": (
                "Python Verified Renderer"
            ),
            "tools_used": [
                "live_doctype_metadata",
                "current_unsaved_document",
                "current_document_router",
            ],
            "debug": None,
        }

    rows = _safe_live_rows(
        document.get(fieldname)
    )

    if operation == "count_rows":
        result_value = len(rows)

        return {
            "answer": (
                f"Current form ke **{label}** "
                f"table me **{result_value} rows** hain."
            ),
            "model_used": (
                "Python Verified Renderer"
            ),
            "tools_used": [
                "live_doctype_metadata",
                "current_unsaved_document",
                "current_document_router",
                "deterministic_row_count",
            ],
            "debug": None,
        }

    child_label = (
        child_fieldname
        or ""
    )

    for child_field in (
        selected_field.get(
            "child_fields"
        )
        or []
    ):
        if (
            child_field.get("fieldname")
            == child_fieldname
        ):
            child_label = (
                child_field.get("label")
                or child_fieldname
            )
            break

    child_values = [
        row.get(child_fieldname)
        for row in rows
    ]

    if operation == "count_non_empty":
        result_value = sum(
            1
            for value in child_values
            if _field_has_value(value)
        )

    else:
        numeric_values = []

        for value in child_values:
            numeric_value = (
                _to_numeric_value(value)
            )

            if numeric_value is not None:
                numeric_values.append(
                    numeric_value
                )

        if operation == "sum_values":
            result_value = sum(
                numeric_values
            )

        elif operation == "average_values":
            result_value = (
                sum(numeric_values)
                / len(numeric_values)
                if numeric_values
                else 0
            )

        elif operation == "minimum_value":
            result_value = (
                min(numeric_values)
                if numeric_values
                else 0
            )

        elif operation == "maximum_value":
            result_value = (
                max(numeric_values)
                if numeric_values
                else 0
            )

        else:
            return None

    return {
        "answer": (
            f"Current form ke **{label}** table me "
            f"**{child_label}** ka result: "
            f"**{result_value}**"
        ),
        "model_used": (
            "Python Verified Renderer"
        ),
        "tools_used": [
            "live_doctype_metadata",
            "current_unsaved_document",
            "current_document_router",
            "deterministic_calculation",
        ],
        "debug": None,
    }


def answer_from_current_document(
    question,
    context,
):
    """
    Generic current-document route.

    Resolver uses the live schema.
    Executor uses Python.
    """

    try:
        plan = resolve_current_document_query(
            question=question,
            context=context,
        )

        if not plan.get("handled"):
            return None

        return execute_current_document_plan(
            plan=plan,
            context=context,
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            (
                "Classic Chatbot Current "
                "Document Query Error"
            ),
        )

        # Full agent can continue if compact router fails.
        return None






# -----------------------------
# PUBLIC API
# -----------------------------
@frappe.whitelist()
# def ask(question, doctype=None, docname=None, doc=None, route=None, error=None, preferred_model="auto"):
def ask(question, doctype=None, docname=None, doc=None, route=None, error=None,
        preferred_model="local", history=None):

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
    
    
    
    
        # ========================================================
    # GENERIC CURRENT DOCUMENT QUERY
    # Live schema decides the field; Python calculates result.
    # ========================================================

    current_document_answer = (
        answer_from_current_document(
            question=question,
            context=context,
        )
    )

    if current_document_answer:
        return current_document_answer




        # ========================================================
    # DYNAMIC FORM VALIDATION ROUTE
    # Only routes the request; field analysis is done by AI.
    # ========================================================

    if is_form_validation_request(
        question,
        context,
    ):
        try:
            (
                answer,
                model_used,
                validation_context,
            ) = answer_dynamic_form_validation(
                question=question,
                context=context,
                preferred_model=(
                    preferred_model
                    or "local"
                ),
            )

            return {
                "answer": answer,
                "model_used": model_used,
                "tools_used": [
                    "live_doctype_schema",
                    "current_unsaved_document",
                    "child_table_schema",
                    "deterministic_form_analysis",
                    "local_semantic_validation",
                ],
                "debug": (
                    validation_context
                    if frappe.conf.get(
                        "classic_chatbot_debug"
                    )
                    else None
                ),
            }

        except Exception as exc:
            frappe.log_error(
                frappe.get_traceback(),
                (
                    "Classic Chatbot Dynamic "
                    "Form Validation Error"
                ),
            )

            return {
                "answer": (
                    "Local form validation model "
                    "current schema ko analyse nahi "
                    f"kar paya. Error: {str(exc)}"
                ),
                "model_used": (
                    "⚠️ Local Validation Error"
                ),
                "tools_used": [
                    "live_doctype_schema",
                    "current_unsaved_document",
                ],
                "debug": None,
            }

















    

    # 0) Groq mode: full agent loop (model khud tools decide karta hai)
    if preferred_model == "groq" and get_llm_config().get("groq_api_key"):
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
    






















@frappe.whitelist()
def validate_current_form(
    doctype=None,
    docname=None,
    doc=None,
    required_fields=None,
    visible_fields=None,
    run_ai=1,
):
    """
    Current avatar may call:

    classic_chatbot.api.agent.validate_current_form

    Actual validation is handled by validation.py.
    """

    from classic_chatbot.api.validation import (
        validate_current_form as execute_validation,
    )

    return execute_validation(
        doctype=doctype,
        docname=docname,
        doc=doc,
        required_fields=required_fields,
        visible_fields=visible_fields,
        run_ai=run_ai,
    )
