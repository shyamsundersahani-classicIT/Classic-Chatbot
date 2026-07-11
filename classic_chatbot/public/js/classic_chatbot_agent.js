// (function () {
//     console.log("[Classic Chatbot v7.0] Loaded with Dynamic SPA Context & Agent Sync");

//     var last_error = "";

//     function esc(text) {
//         if (text === undefined || text === null) return "";
//         return String(text)
//             .replace(/&/g, "&amp;")
//             .replace(/</g, "&lt;")
//             .replace(/>/g, "&gt;")
//             .replace(/"/g, "&quot;")
//             .replace(/'/g, "&#039;");
//     }

//     function getContext() {
//         var route = [];
//         try { route = frappe.get_route ? frappe.get_route() : []; } catch (e) {}
//         var ctx = { route: route, doctype: null, docname: null, doc: null };
        
//         if (route && route[0] === "Form") {
//             ctx.doctype = route[1];
//             ctx.docname = route[2];
//             // FIX: Ensure cur_frm is perfectly synced with the current route
//             if (window.cur_frm && cur_frm.doc && cur_frm.doc.doctype === ctx.doctype) { 
//                 ctx.doc = cur_frm.doc; 
//             }
//         }
//         if (route && route[0] === "List") { 
//             ctx.doctype = route[1]; 
//         }
//         return ctx;
//     }

//     function injectStyle() {
//         if (document.getElementById("classic-chatbot-style-v7")) return;
//         var style = document.createElement("style");
//         style.id = "classic-chatbot-style-v7";
//         style.innerHTML = `
//             #classic-chatbot-launcher { position: fixed; right: 28px; bottom: 28px; width: 72px; height: 72px; border-radius: 50%; border: none; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; font-size: 32px; z-index: 999999; cursor: pointer; box-shadow: 0 18px 45px rgba(124,77,255,.45); transition: transform .3s ease; animation: ccPulse 2s infinite; }
//             #classic-chatbot-launcher:hover { transform: scale(1.08) rotate(4deg); }
//             #classic-chatbot-launcher.cc-hide { opacity: 0; pointer-events: none; transform: scale(.35) rotate(15deg); }
            
//             #classic-chatbot-panel { position: fixed; right: 24px; bottom: 24px; width: 440px; height: 680px; background: white; border-radius: 30px; z-index: 999999; box-shadow: 0 30px 90px rgba(0,0,0,.28); overflow: hidden; opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(55px) scale(.78); transform-origin: bottom right; transition: all .35s ease; }
//             #classic-chatbot-panel.cc-open { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0) scale(1); }
            
//             .cc-head { height: 110px; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; padding: 20px; font-size: 24px; font-weight: 800; position: relative; }
            
//             #classic-chatbot-close { float: right; border: none; background: rgba(255,255,255,.25); color: white; border-radius: 50%; width: 36px; height: 36px; font-size: 22px; cursor: pointer; transition: transform .25s ease; margin-left: 8px; }
//             #classic-chatbot-close:hover { transform: rotate(90deg); }
            
//             #classic-chatbot-refresh { float: right; border: none; background: rgba(255,255,255,.25); color: white; border-radius: 50%; width: 36px; height: 36px; font-size: 16px; cursor: pointer; transition: transform .4s ease; margin-left: 8px; }
//             #classic-chatbot-refresh:hover { transform: rotate(-180deg); background: rgba(255,255,255,.4); }

//             #classic-chatbot-model-select { float: right; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.4); border-radius: 12px; padding: 6px 10px; font-size: 12px; font-weight: 600; outline: none; cursor: pointer; appearance: none; -webkit-appearance: none; }
//             #classic-chatbot-model-select option { color: #333; font-weight: 500; }
//             #classic-chatbot-model-select:hover { background: rgba(255,255,255,0.3); }

//             #classic-chatbot-body { height: 440px; padding: 20px; background: linear-gradient(180deg,#f8f9ff,#eef2ff); overflow-y: auto; scroll-behavior: smooth; }
//             .cc-bot-msg { background: white; padding: 14px 16px; border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,.08); margin-bottom: 12px; color: #263248; line-height: 1.5; animation: ccMsgIn .25s ease; word-wrap: break-word;}
//             .cc-user-msg { background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; padding: 14px 16px; border-radius: 18px; margin-left: auto; margin-bottom: 12px; max-width: 82%; line-height: 1.5; animation: ccMsgIn .25s ease; word-wrap: break-word;}
//             .cc-sys-msg { background: #eef2ff; color: #4f46e5; border-left: 4px solid #4f46e5; padding: 10px; font-size: 13px; margin-bottom: 12px; border-radius: 8px; animation: ccMsgIn .25s ease; }
            
//             /* Quick actions horizontally scrollable for more buttons */
//             .cc-quick { display: flex; gap: 8px; padding: 10px 16px; background: white; border-top: 1px solid #eee; overflow-x: auto; white-space: nowrap; scrollbar-width: none; }
//             .cc-quick::-webkit-scrollbar { display: none; }
//             .cc-quick button { border: 1px solid #ddd6fe; background: #faf5ff; color: #5b21b6; border-radius: 20px; padding: 7px 12px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
//             .cc-quick button:hover { background: #f3e8ff; }
            
//             .cc-foot { padding: 15px; display: flex; gap: 10px; border-top: 1px solid #eee; background: white; }
//             #classic-chatbot-input { flex: 1; height: 48px; border: 1px solid #ddd; border-radius: 24px; padding: 0 16px; outline: none; font-size: 14px; }
//             #classic-chatbot-input:focus { border-color: #8b5cf6; box-shadow: 0 0 0 4px rgba(139,92,246,.12); }
//             #classic-chatbot-send { width: 52px; height: 52px; border-radius: 50%; border: none; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; font-size: 22px; cursor: pointer; transition: transform .2s ease; }
//             #classic-chatbot-send:hover { transform: scale(1.08); }
            
//             .cc-typing span { display: inline-block; width: 7px; height: 7px; margin: 0 2px; border-radius: 50%; background: #8b5cf6; animation: ccTyping 1s infinite ease-in-out; }
//             .cc-typing span:nth-child(2) { animation-delay: .15s; }
//             .cc-typing span:nth-child(3) { animation-delay: .3s; }
            
//             @keyframes ccPulse { 0% { box-shadow: 0 0 0 0 rgba(124,77,255,.42); } 70% { box-shadow: 0 0 0 14px rgba(124,77,255,0); } 100% { box-shadow: 0 0 0 0 rgba(124,77,255,0); } }
//             @keyframes ccMsgIn { from { opacity: 0; transform: translateY(8px) scale(.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
//             @keyframes ccTyping { 0%,80%,100% { transform: scale(.6); opacity: .45; } 40% { transform: scale(1); opacity: 1; } }
//         `;
//         document.head.appendChild(style);
//     }

//     function mountBot() {
//         if (document.getElementById("classic-chatbot-launcher")) return;
//         injectStyle();

//         var launcher = document.createElement("button");
//         launcher.id = "classic-chatbot-launcher";
//         launcher.type = "button";
//         launcher.innerHTML = "🤖";

//         var panel = document.createElement("div");
//         panel.id = "classic-chatbot-panel";

//         panel.innerHTML =
//             '<div class="cc-head">' +
//                 '🤖 Classic Chatbot' +
//                 '<button id="classic-chatbot-close" type="button" title="Close">×</button>' +
//                 '<button id="classic-chatbot-refresh" type="button" title="Clear Chat">🔄</button>' +
//                 '<select id="classic-chatbot-model-select" title="Switch Model">' +
//                     '<option value="auto">🤖 Auto (Local First)</option>' +
//                     '<option value="groq">☁️ Groq (Fast & Paid)</option>' +
//                     '<option value="local">🖥️ Local (Strict Free)</option>' +
//                 '</select>' +
//                 '<div style="font-size:14px;font-weight:400;margin-top:6px;">● Principal Architect Active</div>' +
//             '</div>' +
//             '<div id="classic-chatbot-body">' +
//                 '<div class="cc-bot-msg">Namaste Bhai 🙏 Classic Chatbot ready hai. Boliye, kis Frappe/ERPNext module me help chahiye?</div>' +
//             '</div>' +
//             // NEW QUICK BUTTONS ALIGNED WITH BACKEND SITUATIONAL LOGIC
//             '<div class="cc-quick">' +
//                 '<button type="button" data-q="Is form ke mandatory fields kya hain?">Mandatory?</button>' +
//                 '<button type="button" data-q="Ye DocType kis kis se link hai?">Linked Links</button>' +
//                 '<button type="button" data-q="Is form ka business me kya use hai?">Kya Use Hai?</button>' +
//                 '<button type="button" data-q="Current form me error aa raha hai, fix karo">Fix Error</button>' +
//             '</div>' +
//             '<div class="cc-foot">' +
//                 '<input id="classic-chatbot-input" placeholder="Ask ERPNext issue..." autocomplete="off" />' +
//                 '<button id="classic-chatbot-send" type="button">➤</button>' +
//             '</div>';

//         document.body.appendChild(launcher);
//         document.body.appendChild(panel);

//         // Frappe SPA Route Change Listener
//         if (window.frappe && frappe.router) {
//             frappe.router.on('change', function() {
//                 setTimeout(function() { // Halka sa delay taaki route puri tarah set ho jaye
//                     var newCtx = getContext();
//                     var body = document.getElementById("classic-chatbot-body");
//                     if (body && newCtx.doctype) {
//                         body.insertAdjacentHTML("beforeend", `<div class="cc-sys-msg">🔄 Switched to <b>${newCtx.doctype}</b>. Context updated.</div>`);
//                         body.scrollTop = body.scrollHeight;
//                     }
//                 }, 500);
//             });
//         }
//     }

//     function openBot() {
//         var launcher = document.getElementById("classic-chatbot-launcher");
//         var panel = document.getElementById("classic-chatbot-panel");
//         if (!launcher || !panel) return;
//         launcher.classList.add("cc-hide");
//         requestAnimationFrame(function () { panel.classList.add("cc-open"); });
//         setTimeout(function () {
//             var input = document.getElementById("classic-chatbot-input");
//             if (input) input.focus();
//         }, 350);
//     }

//     function closeBot() {
//         var launcher = document.getElementById("classic-chatbot-launcher");
//         var panel = document.getElementById("classic-chatbot-panel");
//         if (!launcher || !panel) return;
//         panel.classList.remove("cc-open");
//         setTimeout(function () { launcher.classList.remove("cc-hide"); }, 260);
//     }

//     function addUserMessage(text) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;
//         body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + '</div>');
//         body.scrollTop = body.scrollHeight;
//     }

//     function addBotMessage(text, rawHTML) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;
        
//         var finalHTML = esc(text).replace(/\n/g, "<br>");
//         if (rawHTML) {
//             finalHTML += rawHTML;
//         }
        
//         body.insertAdjacentHTML("beforeend", '<div class="cc-bot-msg">' + finalHTML + '</div>');
//         body.scrollTop = body.scrollHeight;
//     }

//     function showTyping() {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;
//         if (document.getElementById("classic-chatbot-typing")) return;
//         body.insertAdjacentHTML(
//             "beforeend",
//             '<div id="classic-chatbot-typing" class="cc-bot-msg"><span class="cc-typing"><span></span><span></span><span></span></span></div>'
//         );
//         body.scrollTop = body.scrollHeight;
//     }

//     function hideTyping() {
//         var t = document.getElementById("classic-chatbot-typing");
//         if (t) t.remove();
//     }

//     function sendMessage(quickText) {
//         var input = document.getElementById("classic-chatbot-input");
//         var msg = quickText || (input ? input.value.trim() : "");
//         if (!msg) return;
//         if (input) input.value = "";

//         var modelSelect = document.getElementById("classic-chatbot-model-select");
//         var preferredModel = modelSelect ? modelSelect.value : "auto";

//         addUserMessage(msg);
//         showTyping();

//         var ctx = getContext();

//         if (!window.frappe || !frappe.call) {
//             setTimeout(function () {
//                 hideTyping();
//                 addBotMessage("Frappe API available nahi hai. Refresh karo.");
//             }, 400);
//             return;
//         }

//         // Dynamic form data copying (Filtered properly to prevent huge payload crash)
//         var safeDocData = {};
//         if (ctx.doc) {
//             Object.keys(ctx.doc).forEach(function(key) {
//                 // Ignore heavy objects/arrays (like child tables right now) aur internal metadata
//                 if (!key.startsWith("_") && typeof ctx.doc[key] !== "object") {
//                     safeDocData[key] = ctx.doc[key];
//                 }
//             });
//         }

//         frappe.call({
//             method: "classic_chatbot.api.agent.ask", // Backend path
//             args: {
//                 question: msg,
//                 doctype: ctx.doctype,
//                 docname: ctx.docname,
//                 doc: JSON.stringify(safeDocData), 
//                 route: JSON.stringify(ctx.route || []),
//                 error: last_error || "",
//                 preferred_model: preferredModel 
//             },
//             callback: function (r) {
//                 hideTyping();
//                 var answer = "Server ne answer generate nahi kiya.";
//                 var modelBadge = ""; 

//                 if (r && r.message) {
//                     if (r.message.answer) answer = r.message.answer;
//                     if (r.message.model_used) {
//                         var badgeColor = r.message.model_used.includes("Groq") ? "#f59e0b" : "#10b981";
//                         modelBadge = `<div style="font-size: 10px; color: ${badgeColor}; margin-top: 8px; text-align: right; font-weight: 700; border-top: 1px solid #eee; padding-top: 4px;">${r.message.model_used}</div>`;
//                     }
//                 }
//                 addBotMessage(answer, modelBadge);
//             },
//             error: function (err) {
//                 hideTyping();
//                 addBotMessage("API error aa gaya. Browser console ya bench terminal check karo.");
//             }
//         });
//     }

//     document.addEventListener("click", function (e) {
//         var launcher = e.target.closest("#classic-chatbot-launcher");
//         var close = e.target.closest("#classic-chatbot-close");
//         var refresh = e.target.closest("#classic-chatbot-refresh");
//         var send = e.target.closest("#classic-chatbot-send");
//         var quick = e.target.closest(".cc-quick button");

//         if (launcher) { e.preventDefault(); e.stopPropagation(); openBot(); return; }
//         if (close) { e.preventDefault(); e.stopPropagation(); closeBot(); return; }
//         if (refresh) {
//             e.preventDefault(); e.stopPropagation();
//             var body = document.getElementById("classic-chatbot-body");
//             if (body) body.innerHTML = '<div class="cc-bot-msg">Chat refresh ho gayi hai 🔄<br>Naya sawal poocho.</div>';
//             return;
//         }
//         if (send) { e.preventDefault(); e.stopPropagation(); sendMessage(); return; }
//         if (quick) { e.preventDefault(); e.stopPropagation(); sendMessage(quick.getAttribute("data-q")); return; }
//     }, true);

//     document.addEventListener("keydown", function (e) {
//         if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
//             e.preventDefault(); sendMessage();
//         }
//     }, true);

//     window.addEventListener("error", function (event) { last_error = event.message || ""; });
//     window.addEventListener("unhandledrejection", function (event) { last_error = event.reason ? String(event.reason) : ""; });

//     if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", mountBot); } 
//     else { mountBot(); }
//     setTimeout(mountBot, 1000); // Failsafe loader
// })();


















// (function () {
//     console.log("[Classic Chatbot v9.0] Direct ERP Data UI Loaded");

//     var last_error = "";
//     var claude_session_id = "";
//     var chat_history = [];   // pichle turns yaad rakhne ke liye

//     function esc(text) {
//         if (text === undefined || text === null) return "";
//         return String(text)
//             .replace(/&/g, "&amp;")
//             .replace(/</g, "&lt;")
//             .replace(/>/g, "&gt;")
//             .replace(/"/g, "&quot;")
//             .replace(/'/g, "&#039;");
//     }

//     // --- ADVANCED MARKDOWN PARSER (For Tables, Bold, Code) ---
//     function parseMarkdown(text) {
//         let html = text;
            
//         // 1. Code Blocks
//         html = html.replace(/```([\s\S]*?)```/g, '<pre style="background:#1e293b; color:#e2e8f0; padding:12px; border-radius:8px; overflow-x:auto; font-size:12px; margin: 10px 0;"><code>$1</code></pre>');
        
//         // 2. Inline Code
//         html = html.replace(/`([^`]+)`/g, '<code style="background:#f1f5f9; color:#e11d48; padding:2px 6px; border-radius:4px; font-size:13px; font-weight:600;">$1</code>');
        
//         // 3. Bold Text
//         html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
//         // 4. Omniscient Tables
//         html = html.replace(/(?:\|.*\|[ \t]*(?:[\r\n]+|$))+/g, function(match) {
//             let rows = match.trim().split('\n');
//             let table = '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; margin:10px 0; font-size:12px; border-radius:8px; overflow:hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); background:white;"><tbody>';
//             rows.forEach((row, i) => {
//                 if (row.includes('---')) return;
//                 let cols = row.split('|').filter(c => c.trim() !== '');
//                 table += '<tr>';
//                 cols.forEach(col => {
//                     let cell = i === 0 ? 'th' : 'td';
//                     let style = i === 0 ? 'border:1px solid #e2e8f0; padding:10px; background:#f8fafc; text-align:left; color:#334155; font-weight:700;' : 'border:1px solid #e2e8f0; padding:8px 10px; color:#475569;';
//                     table += `<${cell} style="${style}">${col.trim()}</${cell}>`;
//                 });
//                 table += '</tr>';
//             });
//             table += '</tbody></table></div>';
//             return table;
//         });
        
//         // 5. Line Breaks
//         html = html.replace(/\n/g, "<br>");
//         return html;
//     }

//     function getContext() {
//         var route = [];
//         try {
//             route = frappe.get_route ? frappe.get_route() : [];
//         } catch (e) {}

//         var ctx = {
//             route: route,
//             doctype: null,
//             docname: null,
//             doc: null
//         };
        
//         if (route && route[0] === "Form") {
//             ctx.doctype = route[1];
//             ctx.docname = route[2];

//             if (window.cur_frm && cur_frm.doc && cur_frm.doc.doctype === ctx.doctype) {
//                 ctx.doc = cur_frm.doc;
//             }
//         }

//         if (route && route[0] === "List") {
//             ctx.doctype = route[1];
//         }

//         return ctx;
//     }

//     function injectStyle() {
//         if (document.getElementById("classic-chatbot-style-v8")) return;

//         var style = document.createElement("style");
//         style.id = "classic-chatbot-style-v8";

//         style.innerHTML = `
//             /* Classic Chatbot v9.0 - Direct ERP Data UI */

//             ::-webkit-scrollbar { width: 6px; height: 6px; }
//             ::-webkit-scrollbar-track { background: transparent; }
//             ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
//             ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

//             #classic-chatbot-launcher {
//                 position: fixed;
//                 right: 28px;
//                 bottom: 28px;
//                 width: 64px;
//                 height: 64px;
//                 border-radius: 50%;
//                 border: none;
//                 background: linear-gradient(135deg, #4f46e5, #9333ea);
//                 color: white;
//                 font-size: 28px;
//                 z-index: 999999;
//                 cursor: pointer;
//                 box-shadow: 0 12px 30px rgba(79,70,229,.4);
//                 transition: all .3s cubic-bezier(0.4, 0, 0.2, 1);
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//             }

//             #classic-chatbot-launcher:hover {
//                 transform: translateY(-5px) scale(1.05);
//                 box-shadow: 0 20px 40px rgba(79,70,229,.5);
//             }

//             #classic-chatbot-launcher.cc-hide {
//                 opacity: 0;
//                 pointer-events: none;
//                 transform: scale(.5) translateY(20px);
//             }
            
//             #classic-chatbot-panel {
//                 position: fixed;
//                 right: 28px;
//                 bottom: 105px;
//                 width: 440px;
//                 height: 650px;
//                 background: rgba(255, 255, 255, 0.95);
//                 backdrop-filter: blur(12px);
//                 border: 1px solid rgba(255,255,255,0.5);
//                 border-radius: 24px;
//                 z-index: 999999;
//                 box-shadow: 0 25px 80px rgba(0,0,0,.15);
//                 display: flex;
//                 flex-direction: column;
//                 overflow: hidden;
//                 opacity: 0;
//                 visibility: hidden;
//                 pointer-events: none;
//                 transform: translateY(40px) scale(.95);
//                 transform-origin: bottom right;
//                 transition: all .4s cubic-bezier(0.16, 1, 0.3, 1);
//             }

//             #classic-chatbot-panel.cc-open {
//                 opacity: 1;
//                 visibility: visible;
//                 pointer-events: auto;
//                 transform: translateY(0) scale(1);
//             }
            
//             .cc-head {
//                 background: linear-gradient(135deg, #4f46e5, #9333ea);
//                 color: white;
//                 padding: 20px;
//                 position: relative;
//                 flex-shrink: 0;
//             }

//             .cc-title {
//                 font-size: 20px;
//                 font-weight: 700;
//                 display: flex;
//                 align-items: center;
//                 gap: 8px;
//             }

//             .cc-status {
//                 font-size: 12px;
//                 font-weight: 500;
//                 opacity: 0.9;
//                 margin-top: 4px;
//                 display: flex;
//                 align-items: center;
//                 gap: 6px;
//             }

//             .cc-status-dot {
//                 width: 8px;
//                 height: 8px;
//                 background: #22c55e;
//                 border-radius: 50%;
//                 display: inline-block;
//                 box-shadow: 0 0 8px #22c55e;
//             }
            
//             .cc-actions {
//                 position: absolute;
//                 right: 15px;
//                 top: 15px;
//                 display: flex;
//                 gap: 8px;
//             }

//             .cc-icon-btn {
//                 background: rgba(255,255,255,0.2);
//                 border: none;
//                 color: white;
//                 width: 32px;
//                 height: 32px;
//                 border-radius: 50%;
//                 cursor: pointer;
//                 transition: all .2s ease;
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//                 backdrop-filter: blur(4px);
//             }

//             .cc-icon-btn:hover {
//                 background: rgba(255,255,255,0.4);
//                 transform: scale(1.1);
//             }

//             #classic-chatbot-model-select {
//                 margin-top: 12px;
//                 background: rgba(0,0,0,0.15);
//                 border: 1px solid rgba(255,255,255,0.2);
//                 color: white;
//                 border-radius: 8px;
//                 padding: 6px 10px;
//                 font-size: 12px;
//                 width: 100%;
//                 outline: none;
//                 cursor: pointer;
//             }

//             #classic-chatbot-model-select option {
//                 color: #333;
//             }

//             #classic-chatbot-body {
//                 flex: 1;
//                 padding: 20px;
//                 overflow-y: auto;
//                 scroll-behavior: smooth;
//                 background: #f8fafc;
//             }

//             .cc-bot-msg,
//             .cc-user-msg {
//                 padding: 12px 16px;
//                 border-radius: 16px;
//                 margin-bottom: 16px;
//                 font-size: 14px;
//                 line-height: 1.5;
//                 word-wrap: break-word;
//                 animation: ccMsgIn .3s ease forwards;
//                 opacity: 0;
//                 transform: translateY(10px);
//             }
            
//             .cc-bot-msg {
//                 background: white;
//                 color: #334155;
//                 border: 1px solid #e2e8f0;
//                 border-bottom-left-radius: 4px;
//                 box-shadow: 0 4px 15px rgba(0,0,0,0.03);
//                 max-width: 90%;
//             }

//             .cc-user-msg {
//                 background: linear-gradient(135deg, #4f46e5, #9333ea);
//                 color: white;
//                 border-bottom-right-radius: 4px;
//                 box-shadow: 0 4px 15px rgba(79,70,229,0.2);
//                 margin-left: auto;
//                 max-width: 85%;
//             }

//             .cc-sys-msg {
//                 text-align: center;
//                 color: #64748b;
//                 font-size: 12px;
//                 margin-bottom: 16px;
//                 font-weight: 500;
//                 animation: ccMsgIn .3s ease forwards;
//             }
            
//             .cc-quick-wrap {
//                 padding: 12px 15px;
//                 background: white;
//                 border-top: 1px solid #e2e8f0;
//                 flex-shrink: 0;
//             }

//             .cc-quick {
//                 display: flex;
//                 gap: 8px;
//                 overflow-x: auto;
//                 padding-bottom: 4px;
//             }

//             .cc-quick button {
//                 flex-shrink: 0;
//                 background: #f1f5f9;
//                 border: 1px solid #cbd5e1;
//                 color: #475569;
//                 border-radius: 16px;
//                 padding: 6px 14px;
//                 font-size: 12px;
//                 font-weight: 600;
//                 cursor: pointer;
//                 transition: all 0.2s;
//             }

//             .cc-quick button:hover {
//                 background: #e0e7ff;
//                 border-color: #818cf8;
//                 color: #4f46e5;
//             }
            
//             .cc-foot {
//                 padding: 15px;
//                 background: white;
//                 border-top: 1px solid #e2e8f0;
//                 display: flex;
//                 gap: 10px;
//                 align-items: center;
//                 border-bottom-left-radius: 24px;
//                 border-bottom-right-radius: 24px;
//             }

//             .cc-empty-state {
//     height: 100%;
//     display: flex;
//     align-items: center;
//     justify-content: center;
// }

// .cc-empty-title {
//     font-size: 22px;
//     font-weight: 500;
//     color: #111827;
// }

//             #classic-chatbot-input {
//                 flex: 1;
//                 height: 44px;
//                 border: 1px solid #cbd5e1;
//                 border-radius: 22px;
//                 padding: 0 16px;
//                 font-size: 14px;
//                 transition: all 0.2s;
//                 outline: none;
//                 background: #f8fafc;
//                 color: #1e293b;
//                 caret-color: #1e293b;
//             }

//             #classic-chatbot-input:focus {
//                 border-color: #818cf8;
//                 background: white;
//                 box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
//             }

//             #classic-chatbot-send {
//                 width: 44px;
//                 height: 44px;
//                 border-radius: 50%;
//                 border: none;
//                 background: #4f46e5;
//                 color: white;
//                 font-size: 18px;
//                 cursor: pointer;
//                 transition: all .2s;
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//             }

//             #classic-chatbot-send:hover {
//                 background: #4338ca;
//                 transform: scale(1.05);
//             }
            
//             .cc-typing {
//                 display: flex;
//                 gap: 4px;
//                 padding: 4px 0;
//             }

//             .cc-typing span {
//                 width: 6px;
//                 height: 6px;
//                 border-radius: 50%;
//                 background: #94a3b8;
//                 animation: ccTyping 1.4s infinite ease-in-out both;
//             }

//             .cc-typing span:nth-child(1) {
//                 animation-delay: -0.32s;
//             }

//             .cc-typing span:nth-child(2) {
//                 animation-delay: -0.16s;
//             }
            
//             @keyframes ccMsgIn {
//                 to {
//                     opacity: 1;
//                     transform: translateY(0);
//                 }
//             }

//             @keyframes ccTyping {
//                 0%, 80%, 100% {
//                     transform: scale(0);
//                 }
//                 40% {
//                     transform: scale(1);
//                 }
//             }
//         `;

//         document.head.appendChild(style);
//     }

//     function updateContextUI() {
//         var ctx = getContext();
//         var statusEl = document.getElementById("cc-context-status");
//         var quickDiv = document.querySelector(".cc-quick");
        
//         if (!statusEl || !quickDiv) return;

//         if (ctx.doctype) {
//             statusEl.innerHTML = `<span class="cc-status-dot"></span> <b>${ctx.doctype}</b> Mode Active`;
//             quickDiv.innerHTML = `
//                 <button type="button" data-q="Is ${ctx.doctype} form ke mandatory fields kya hain?">Missing Fields?</button>
//                 <button type="button" data-q="Current form ka error theek karo">Fix Error</button>
//                 <button type="button" data-q="${ctx.doctype} ke top 5 records dikhao">Top Records</button>
//             `;
//         } else {
//             statusEl.innerHTML = `<span class="cc-status-dot"></span> Direct ERP Data Ready`;
//             quickDiv.innerHTML = `
//                 <button type="button" data-q="Rajesh Bankar ke name se kitne Contact bane hue hain?">Count Contact</button>
//                 <button type="button" data-q="Top 5 pending Purchase Orders dikhao">Pending POs</button>
//                 <button type="button" data-q="Manufacturing process kya hai?">Manufacturing</button>
//             `;
//         }
//     }

//     function isLoggedIn() {
//         if (window.frappe && frappe.session && frappe.session.user) {
//             return frappe.session.user !== "Guest";
//         }
//         var match = document.cookie.match(/(?:^|;\s*)user_id=([^;]*)/);
//         var user = match ? decodeURIComponent(match[1]) : "";
//         return !!user && user !== "Guest";
//     }

//     function mountBot() {
//         if (!isLoggedIn()) return;
//         if (document.getElementById("classic-chatbot-launcher")) return;

//         injectStyle();

//         var launcher = document.createElement("button");
//         launcher.id = "classic-chatbot-launcher";
//         launcher.innerHTML = `<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>`;

//         var panel = document.createElement("div");
//         panel.id = "classic-chatbot-panel";

//         panel.innerHTML = `
//             <div class="cc-head">
//                 <div class="cc-actions">
//                     <button class="cc-icon-btn" id="classic-chatbot-refresh" title="Clear Chat">🔄</button>
//                     <button class="cc-icon-btn" id="classic-chatbot-close" title="Close">✕</button>
//                 </div>

//                 <div class="cc-title">🤖 Classic AI Agent</div>

//                 <div class="cc-status" id="cc-context-status">
//                     <span class="cc-status-dot"></span> Live ERP Data Ready
//                 </div>

//                 <select id="classic-chatbot-model-select" title="Routing Engine">
//                     <option value="claude" selected>🤖 Claude (Subscription)</option>
//                     <option value="auto">⚡ Direct ERP + Multi-Agent Router</option>
//                     <option value="groq">☁️ Groq Llama-3 (Cloud)</option>
//                     <option value="local">🖥️ Local Server Mode</option>
//                 </select>
//             </div>

//             <div id="classic-chatbot-body">
//     <div class="cc-empty-state">
//         <div class="cc-empty-title">What can I help with?</div>
//     </div>
// </div>

//             <div class="cc-quick-wrap">
//                 <div class="cc-quick"></div>
//             </div>

//             <div class="cc-foot">
// <input id="classic-chatbot-input" placeholder="Ask anything..." autocomplete="off" />                <button id="classic-chatbot-send" type="button">➤</button>
//             </div>
//         `;

//         document.body.appendChild(launcher);
//         document.body.appendChild(panel);

//         updateContextUI();

//         if (window.frappe && frappe.router) {
//             frappe.router.on("change", function () {
//                 setTimeout(function () {
//                     updateContextUI();

//                     var ctx = getContext();
//                     var body = document.getElementById("classic-chatbot-body");

//                     if (body && ctx.doctype && !body.innerHTML.includes(`Navigated to ${ctx.doctype}`)) {
//                         body.insertAdjacentHTML("beforeend", `<div class="cc-sys-msg">Navigated to ${ctx.doctype}</div>`);
//                         body.scrollTop = body.scrollHeight;
//                     }
//                 }, 800);
//             });
//         }
//     }

//     function openBot() {
//         var launcher = document.getElementById("classic-chatbot-launcher");
//         var panel = document.getElementById("classic-chatbot-panel");

//         if (!launcher || !panel) return;

//         launcher.classList.add("cc-hide");
//         panel.classList.add("cc-open");

//         setTimeout(function () {
//             var input = document.getElementById("classic-chatbot-input");
//             if (input) input.focus();
//         }, 100);

//         updateContextUI();
//     }

//     function closeBot() {
//         var panel = document.getElementById("classic-chatbot-panel");
//         var launcher = document.getElementById("classic-chatbot-launcher");

//         if (panel) panel.classList.remove("cc-open");

//         setTimeout(function () {
//             if (launcher) launcher.classList.remove("cc-hide");
//         }, 200);
//     }

//     function addUserMessage(text) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;

//         body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + "</div>");
//         body.scrollTop = body.scrollHeight;
//     }

//     function addBotMessage(text, rawHTML) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;

//         var finalHTML = parseMarkdown(esc(text));

//         if (rawHTML) {
//             finalHTML += rawHTML;
//         }

//         body.insertAdjacentHTML("beforeend", '<div class="cc-bot-msg">' + finalHTML + "</div>");
//         body.scrollTop = body.scrollHeight;
//     }

//     function showTyping() {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;

//         if (document.getElementById("classic-chatbot-typing")) return;

//         body.insertAdjacentHTML(
//             "beforeend",
//             '<div id="classic-chatbot-typing" class="cc-bot-msg"><div class="cc-typing"><span></span><span></span><span></span></div></div>'
//         );

//         body.scrollTop = body.scrollHeight;
//     }

//     function hideTyping() {
//         var t = document.getElementById("classic-chatbot-typing");
//         if (t) t.remove();
//     }



//     function sendMessage(quickText) {
//         var input = document.getElementById("classic-chatbot-input");
//         var msg = quickText || (input ? input.value.trim() : "");

//         if (!msg) return;

//         if (input) input.value = "";

//         addUserMessage(msg);
//         showTyping();

//         var ctx = getContext();

//         if (last_error && msg.toLowerCase().includes("error")) {
//             msg += "\n(Recent UI Error Logged: " + last_error + ")";
//             last_error = "";
//         }

//         var safeDocData = {};

//         if (ctx.doc) {
//             Object.keys(ctx.doc).forEach(function (key) {
//                 if (key.startsWith("_")) return;
//                 var val = ctx.doc[key];

//                 if (val === null || val === undefined || val === "") return;

//                 if (Array.isArray(val)) {
//                     // Child tables / MultiSelect: har row ka halka summary bhejo
//                     var rows = val.slice(0, 10).map(function (row) {
//                         if (typeof row !== "object" || !row) return row;
//                         var slim = {};
//                         Object.keys(row).forEach(function (rk) {
//                             var rv = row[rk];
//                             if (!rk.startsWith("_") && typeof rv !== "object" &&
//                                 rv !== null && rv !== "" &&
//                                 ["name","owner","creation","modified","modified_by",
//                                  "docstatus","doctype","parent","parentfield",
//                                  "parenttype","idx"].indexOf(rk) === -1) {
//                                 slim[rk] = rv;
//                             }
//                         });
//                         return slim;
//                     });
//                     if (rows.length) safeDocData[key] = rows;
//                 } else if (typeof val !== "object") {
//                     safeDocData[key] = val;
//                 }
//             });
//         }

//         var modelSelect = document.getElementById("classic-chatbot-model-select");
//         var preferredModel = modelSelect ? modelSelect.value : "claude";

//         var args = {
//             question: msg,
//             doctype: ctx.doctype,
//             docname: ctx.docname,
//             doc: JSON.stringify(safeDocData),
//             route: JSON.stringify(ctx.route || []),
//             preferred_model: preferredModel,
//             history: JSON.stringify(chat_history.slice(-6))
//         };

//         if (preferredModel === "claude" && claude_session_id) {
//             args.session_id = claude_session_id;
//         }

//         function renderBotResponse(m) {
//             hideTyping();

//             var answer = "Server ne answer generate nahi kiya.";
//             var badge = "";

//             if (m) {
//                 if (m.answer) {
//                     answer = m.answer;
//                 }

//                 if (m.session_id) {
//                     claude_session_id = m.session_id;
//                 }

//                 if (m.model_used) {
//                     var tools = Array.isArray(m.tools_used) && m.tools_used.length
//                         ? " · Tools: " + esc(m.tools_used.join(", "))
//                         : "";

//                     badge = `<div style="font-size: 10px; color: #64748b; margin-top: 8px; text-align: right; border-top: 1px solid #e2e8f0; padding-top: 6px;">Served by: <b>${esc(m.model_used)}</b>${tools}</div>`;
//                 }
//             }

//             addBotMessage(answer, badge);

//             // Conversation memory: is exchange ko yaad rakho
//             chat_history.push({ role: "user", content: msg });
//             chat_history.push({ role: "assistant", content: answer });
//             if (chat_history.length > 12) chat_history = chat_history.slice(-12);
//         }

//         function showFailure() {
//             hideTyping();
//             addBotMessage("⚠️ API Server disconnect ho gaya. Kripya bench/terminal, method path, aur browser console check karein.");
//         }

//         if (preferredModel === "claude") {
//             // Async mode: enqueue karo, phir har 3s me result poll karo.
//             frappe.call({
//                 method: "classic_chatbot.api.claude_agent.ask_claude_async",
//                 args: args,
//                 callback: function (r) {
//                     var token = r && r.message && r.message.job_token;
//                     if (!token) return showFailure();

//                     var polls = 0;
//                     var poller = setInterval(function () {
//                         polls++;
//                         if (polls > 100) {
//                             clearInterval(poller);
//                             return showFailure();
//                         }
//                         frappe.call({
//                             method: "classic_chatbot.api.claude_agent.poll_claude",
//                             args: { job_token: token },
//                             callback: function (pr) {
//                                 var m = pr && pr.message;
//                                 if (!m) return;
//                                 if (m.status === "done") {
//                                     clearInterval(poller);
//                                     renderBotResponse(m.result);
//                                 } else if (m.status === "expired") {
//                                     clearInterval(poller);
//                                     showFailure();
//                                 }
//                             },
//                             error: function () {
//                                 clearInterval(poller);
//                                 showFailure();
//                             }
//                         });
//                     }, 3000);
//                 },
//                 error: showFailure
//             });
//         } else {
//             frappe.call({
//                 method: "classic_chatbot.api.agent.ask",
//                 args: args,
//                 callback: function (r) {
//                     renderBotResponse(r && r.message);
//                 },
//                 error: showFailure
//             });
//         }
//     }



    
//     document.addEventListener("click", function (e) {
//         var launcher = e.target.closest("#classic-chatbot-launcher");
//         var close = e.target.closest("#classic-chatbot-close");
//         var refresh = e.target.closest("#classic-chatbot-refresh");
//         var send = e.target.closest("#classic-chatbot-send");
//         var quick = e.target.closest(".cc-quick button");

//         if (launcher) {
//             e.preventDefault();
//             openBot();
//         } else if (close) {
//             e.preventDefault();
//             closeBot();
//         } else if (refresh) {
//             e.preventDefault();

//             var body = document.getElementById("classic-chatbot-body");

//             claude_session_id = "";

//             if (body) {
//                 body.innerHTML = '<div class="cc-sys-msg">Memory Cleared ✨</div><div class="cc-bot-msg">Chat refresh ho gayi hai. Naya sawal poocho.</div>';
//             }
//         } else if (send) {
//             e.preventDefault();
//             sendMessage();
//         } else if (quick) {
//             e.preventDefault();
//             sendMessage(quick.getAttribute("data-q"));
//         }
//     });

//     document.addEventListener("keydown", function (e) {
//         if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
//             e.preventDefault();
//             sendMessage();
//         }
//     });

//     // Auto-capture UI Errors silently
//     window.addEventListener("error", function (e) {
//         last_error = e.message || "";
//     });

//     window.addEventListener("unhandledrejection", function (e) {
//         last_error = e.reason ? String(e.reason) : "";
//     });

//     if (document.readyState === "loading") {
//         document.addEventListener("DOMContentLoaded", mountBot);
//     } else {
//         mountBot();
//     }
// })();



























(function () {
    console.log("[Classic Chatbot] Force Loading ChatGPT Dark UI (Transparent) + Functional Tools 🌙");

    var last_error = "";
    var claude_session_id = "";
    var chat_history = [];
    
    // Tool States
    var webSearchActive = false;
    var reasoningActive = false;

    function esc(text) {
        if (text === undefined || text === null) return "";
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // --- ADVANCED MARKDOWN PARSER ---
    function parseMarkdown(text) {
        let html = text;
        
        // 1. Code Blocks
        html = html.replace(/\`\`\`([\s\S]*?)\`\`\`/g, '<pre style="background:rgba(0,0,0,0.6); color:#e2e8f0; padding:16px; border-radius:12px; overflow-x:auto; font-size:13px; margin: 12px 0; border:1px solid rgba(255,255,255,0.1);"><code>$1</code></pre>');
        
        // 2. Inline Code
        html = html.replace(/\`([^\`]+)\`/g, '<code style="background:rgba(47,47,47,0.8); color:#ff9800; padding:3px 6px; border-radius:6px; font-size:13px; font-weight:600; border: 1px solid rgba(255,255,255,0.1);">$1</code>');
        
        // 3. Bold Text
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#ffffff;">$1</strong>');
        
        // 4. Tables
        html = html.replace(/(?:\|.*\|[ \t]*(?:[\r\n]+|$))+/g, function(match) {
            let rows = match.trim().split('\n');
            let table = '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; border-radius:10px; overflow:hidden; background:rgba(47,47,47,0.6);"><tbody>';
            rows.forEach((row, i) => {
                if (row.includes('---')) return;
                let cols = row.split('|').filter(c => c.trim() !== '');
                table += '<tr>';
                cols.forEach(col => {
                    let cell = i === 0 ? 'th' : 'td';
                    let style = i === 0 ? 'border-bottom:1px solid rgba(255,255,255,0.1); padding:12px; background:rgba(33,33,33,0.8); text-align:left; color:#fff; font-weight:700;' : 'border-bottom:1px solid rgba(255,255,255,0.05); padding:10px 12px; color:#ddd;';
                    table += `<${cell} style="${style}">${col.trim()}</${cell}>`;
                });
                table += '</tr>';
            });
            table += '</tbody></table></div>';
            return table;
        });
        
        // 5. Line Breaks
        html = html.replace(/\n/g, "<br>");
        return html;
    }

    function getContext() {
        var route = [];
        try {
            route = frappe.get_route ? frappe.get_route() : [];
        } catch (e) {}

        var ctx = { route: route, doctype: null, docname: null, doc: null };
        
        if (route && route[0] === "Form") {
            ctx.doctype = route[1];
            ctx.docname = route[2];

            if (window.cur_frm && cur_frm.doc && cur_frm.doc.doctype === ctx.doctype) {
                ctx.doc = cur_frm.doc;
            }
        }
        if (route && route[0] === "List") {
            ctx.doctype = route[1];
        }
        return ctx;
    }

    // --- UI NOTIFICATION TOAST ---
    function showToast(text) {
        var panel = document.getElementById("classic-chatbot-panel");
        if (!panel) return;
        var toast = document.getElementById("cc-toast");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "cc-toast";
            panel.appendChild(toast);
        }
        toast.innerText = text;
        toast.classList.add("show");
        setTimeout(function() { toast.classList.remove("show"); }, 2000);
    }

    // --- VOICE TO TEXT IMPLEMENTATION ---
    function startDictation(btnElement) {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            showToast("Microphone not supported in this browser.");
            return;
        }
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US'; 
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            btnElement.classList.add("cc-tool-recording");
            showToast("Listening...");
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const input = document.getElementById("classic-chatbot-input");
            if(input) {
                input.value = (input.value + " " + transcript).trim();
                input.focus();
            }
        };

        recognition.onerror = function(event) {
            showToast("Mic error: " + event.error);
            btnElement.classList.remove("cc-tool-recording");
        };

        recognition.onend = function() {
            btnElement.classList.remove("cc-tool-recording");
        };

        recognition.start();
    }

    function injectStyle() {
        document.querySelectorAll("style[id^='classic-chatbot-style']").forEach(el => el.remove());

        var style = document.createElement("style");
        style.id = "classic-chatbot-style-chatgpt-dark";

        style.innerHTML = `
            /* 🌙 ChatGPT App Dark Mode Style (Transparent Glass) 🌙 */

            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }

            @keyframes ccMsgIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Launcher Button */
            #classic-chatbot-launcher {
                position: fixed;
                right: 30px;
                bottom: 30px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: none;
                background: rgba(255, 255, 255, 0.95) !important;
                color: #212121 !important;
                font-size: 26px;
                z-index: 999999;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
            }

            #classic-chatbot-launcher:hover {
                transform: scale(1.08);
            }

            #classic-chatbot-launcher.cc-hide {
                opacity: 0;
                pointer-events: none;
                transform: scale(0.5);
            }
            
            /* Main Chat Panel */
            #classic-chatbot-panel {
                position: fixed;
                right: 30px;
                bottom: 110px;
                width: 420px;
                height: 720px;
                background: rgba(33, 33, 33, 0.75) !important;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 32px !important;
                z-index: 999999;
                box-shadow: 0 30px 80px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,255,255,0.08) inset !important;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                opacity: 0;
                visibility: hidden;
                pointer-events: none;
                transform: translateY(40px) scale(0.95);
                transform-origin: bottom right;
                transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            }

            #classic-chatbot-panel.cc-open {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
                transform: translateY(0) scale(1);
            }
            
            /* Header */
            .cc-head {
                background: transparent !important;
                color: #ececec !important;
                padding: 20px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-shrink: 0;
                border-bottom: 1px solid rgba(255,255,255,0.05) !important;
            }

            .cc-title {
                font-size: 16px;
                font-weight: 600;
                display: flex;
                flex-direction: column;
            }

            .cc-status {
                font-size: 11px;
                font-weight: 500;
                color: rgba(255,255,255,0.6);
                margin-top: 2px;
            }
            
            .cc-actions {
                display: flex;
                gap: 12px;
            }

            .cc-icon-btn {
                background: transparent;
                border: none;
                color: #ececec;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .cc-icon-btn:hover {
                background: rgba(255,255,255,0.1);
            }

            /* Model Selector */
            #classic-chatbot-model-select {
                display: block; 
                background: rgba(255, 255, 255, 0.08);
                color: #ececec;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 4px 8px;
                font-size: 11px;
                outline: none;
                cursor: pointer;
                transition: all 0.2s;
                backdrop-filter: blur(4px);
            }
            #classic-chatbot-model-select:hover {
                background: rgba(255, 255, 255, 0.15);
            }
            #classic-chatbot-model-select option {
                background: #212121;
                color: #ececec;
            }

            /* Chat Body */
            #classic-chatbot-body {
                flex: 1;
                padding: 24px 24px 0 24px;
                overflow-y: auto;
                scroll-behavior: smooth;
            }

            .cc-bot-msg,
            .cc-user-msg {
                margin-bottom: 24px;
                font-size: 15px;
                line-height: 1.6;
                word-wrap: break-word;
                animation: ccMsgIn 0.3s ease forwards;
            }
            
            .cc-bot-msg {
                background: transparent !important;
                color: #ececec !important;
                padding: 0 !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                border: none !important;
                max-width: 95%;
            }

            .cc-user-msg {
                background: rgba(47, 47, 47, 0.6) !important;
                color: #ececec !important;
                padding: 12px 18px !important;
                border-radius: 20px !important;
                border-bottom-right-radius: 4px !important;
                margin-left: auto;
                max-width: 80%;
                width: fit-content;
                box-shadow: none !important;
                border: 1px solid rgba(255,255,255,0.05) !important;
            }

            .cc-sys-msg {
                text-align: center;
                color: rgba(255,255,255,0.5);
                font-size: 12px;
                margin-bottom: 24px;
                font-weight: 500;
                animation: ccMsgIn 0.3s ease forwards;
            }
            
            /* Quick Actions */
            .cc-foot-wrapper {
                padding: 10px 16px 20px 16px;
                background: transparent;
                flex-shrink: 0;
            }

            .cc-quick {
                display: flex;
                gap: 8px;
                overflow-x: auto;
                padding-bottom: 12px;
                scrollbar-width: none;
            }
            .cc-quick::-webkit-scrollbar { display: none; }

            .cc-quick button {
                flex-shrink: 0;
                background: rgba(47, 47, 47, 0.6) !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                color: #ececec !important;
                border-radius: 20px !important;
                padding: 8px 14px !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                cursor: pointer;
                transition: background 0.2s;
                backdrop-filter: blur(4px);
            }

            .cc-quick button:hover {
                background: rgba(63, 63, 63, 0.8) !important;
            }

            /* Floating Island Input */
            .cc-input-container {
                background: rgba(47, 47, 47, 0.5);
                border: 1px solid rgba(255,255,255,0.08);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border-radius: 26px;
                padding: 12px 6px 6px 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            #classic-chatbot-input {
                width: 100%;
                background: transparent !important;
                border: none !important;
                color: #ececec !important;
                font-size: 16px !important;
                outline: none !important;
                padding-right: 12px;
                font-family: inherit;
                box-shadow: none !important;
            }
            #classic-chatbot-input::placeholder {
                color: rgba(255,255,255,0.4) !important;
            }

            /* Tools Toolbar */
            .cc-input-toolbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .cc-tools-left {
                display: flex;
                gap: 6px;
            }

            .cc-tool-btn {
                background: transparent;
                border: 1px solid rgba(255,255,255,0.15);
                color: #ececec;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .cc-tool-btn:hover { background: rgba(255,255,255,0.1); }
            .cc-tool-btn svg { width: 16px; height: 16px; opacity: 0.8; }

            /* ACTIVE & RECORDING STATES */
            .cc-tool-active {
                background: rgba(255, 255, 255, 0.9) !important;
                color: #000000 !important;
                border-color: transparent !important;
            }
            .cc-tool-active svg { opacity: 1; }
            
            .cc-tool-recording {
                background: #ef4444 !important;
                color: #ffffff !important;
                border-color: transparent !important;
                animation: pulseRecord 1.5s infinite;
            }
            @keyframes pulseRecord {
                0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
                70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
                100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
            }

            .cc-tools-right {
                display: flex;
                gap: 6px;
                align-items: center;
            }

            #classic-chatbot-send {
                width: 34px;
                height: 34px;
                border-radius: 50%;
                border: none;
                background: rgba(255, 255, 255, 0.9) !important;
                color: #000000 !important;
                cursor: pointer;
                transition: transform 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 4px;
            }

            #classic-chatbot-send:hover {
                transform: scale(1.05);
                background: #ffffff !important;
            }
            #classic-chatbot-send svg { width: 20px; height: 20px; }

            /* Empty State */
            .cc-empty-state {
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                opacity: 1;
            }
            .cc-empty-title {
                font-size: 28px;
                font-weight: 600;
                color: rgba(255,255,255,0.9);
                text-align: center;
            }

            /* Toast Notification */
            #cc-toast {
                position: absolute;
                bottom: 100px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.9);
                color: #000;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: 1000;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }
            #cc-toast.show { opacity: 1; }

            /* Typing Indicator */
            .cc-typing { display: flex; gap: 4px; padding: 12px 0; }
            .cc-typing span {
                width: 8px; height: 8px; border-radius: 50%;
                background: #ececec; opacity: 0.5;
                animation: ccTypingBounce 1.4s infinite ease-in-out both;
            }
            .cc-typing span:nth-child(1) { animation-delay: -0.32s; }
            .cc-typing span:nth-child(2) { animation-delay: -0.16s; }
            @keyframes ccTypingBounce {
                0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
                40% { transform: scale(1); opacity: 1; }
            }
        `;

        document.head.appendChild(style);
    }

    function updateContextUI() {
        var ctx = getContext();
        var statusEl = document.getElementById("cc-context-status");
        var quickDiv = document.querySelector(".cc-quick");
        
        if (!statusEl || !quickDiv) return;

        if (ctx.doctype) {
            statusEl.innerHTML = `${ctx.doctype} Mode`;
            quickDiv.innerHTML = `
                <button type="button" data-q="Is ${ctx.doctype} form ke mandatory fields kya hain?">Missing Fields?</button>
                <button type="button" data-q="Current form ka error theek karo">Fix Error</button>
                <button type="button" data-q="${ctx.doctype} ke top 5 records dikhao">Top Records</button>
            `;
        } else {
            statusEl.innerHTML = `Direct ERP Data`;
            quickDiv.innerHTML = `
                <button type="button" data-q="Rajesh Bankar ke name se kitne Contact bane hue hain?">Count Contact</button>
                <button type="button" data-q="Top 5 pending Purchase Orders dikhao">Pending POs</button>
                <button type="button" data-q="Manufacturing process kya hai?">Manufacturing</button>
            `;
        }
    }

    function isLoggedIn() {
        if (window.frappe && frappe.session && frappe.session.user) {
            return frappe.session.user !== "Guest";
        }
        var match = document.cookie.match(/(?:^|;\s*)user_id=([^;]*)/);
        var user = match ? decodeURIComponent(match[1]) : "";
        return !!user && user !== "Guest";
    }

    function mountBot() {
        if (!isLoggedIn()) return;
        
        var oldLauncher = document.getElementById("classic-chatbot-launcher");
        if (oldLauncher) oldLauncher.remove();
        var oldPanel = document.getElementById("classic-chatbot-panel");
        if (oldPanel) oldPanel.remove();

        injectStyle();

        var launcher = document.createElement("button");
        launcher.id = "classic-chatbot-launcher";
        launcher.innerHTML = `<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;

        var panel = document.createElement("div");
        panel.id = "classic-chatbot-panel";

        panel.innerHTML = `
            <div class="cc-head">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="cc-title">
                        <div>AI Agent</div>
                        <div class="cc-status" id="cc-context-status">Direct ERP Data</div>
                    </div>
                    <select id="classic-chatbot-model-select">
                        <option value="claude" selected>Claude</option>
                        <option value="auto">Auto</option>
                        <option value="groq">Groq</option>
                        <option value="local">Local</option>
                    </select>
                </div>
                <div class="cc-actions">
                    <button class="cc-icon-btn" id="classic-chatbot-refresh" title="Clear Chat">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"></path><path d="M21 3v5h-5"></path></svg>
                    </button>
                    <button class="cc-icon-btn" id="classic-chatbot-close" title="Close">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </div>
            </div>

            <div id="classic-chatbot-body">
                <div class="cc-empty-state">
                    <div class="cc-empty-title">What can I help with?</div>
                </div>
            </div>

            <div class="cc-foot-wrapper">
                <div class="cc-quick"></div>
                <div class="cc-input-container">
                    <input id="classic-chatbot-input" placeholder="Ask anything" autocomplete="off" />
                    
                    <div class="cc-input-toolbar">
                        <div class="cc-tools-left">
                            <button class="cc-tool-btn" id="cc-btn-attach" type="button" title="Attach File"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg></button>
                            <button class="cc-tool-btn" id="cc-btn-web" type="button" title="Toggle Web Search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></button>
                            <button class="cc-tool-btn" id="cc-btn-reason" type="button" title="Deep Reasoning Mode"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A6 6 0 1 0 7.5 11.5c.76.76 1.23 1.52 1.41 2.5h6.18z"></path></svg></button>
                            <button class="cc-tool-btn" id="cc-btn-live" type="button" title="Sync ERP Context"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2"></circle><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48 0a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"></path></svg></button>
                            <button class="cc-tool-btn" id="cc-btn-mic" type="button" title="Voice to Text"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg></button>
                            
                            <!-- Hidden File Input -->
                            <input type="file" id="cc-hidden-file" style="display:none;" />
                        </div>
                        
                        <div class="cc-tools-right">
                            <button id="classic-chatbot-send" type="button">
                                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(launcher);
        document.body.appendChild(panel);

        updateContextUI();

        if (window.frappe && frappe.router) {
            frappe.router.on("change", function () {
                setTimeout(function () {
                    updateContextUI();

                    var ctx = getContext();
                    var body = document.getElementById("classic-chatbot-body");

                    if (body && ctx.doctype && !body.innerHTML.includes(`Mapsd to ${ctx.doctype}`)) {
                        var emptyState = body.querySelector(".cc-empty-state");
                        if(emptyState) emptyState.remove();

                        body.insertAdjacentHTML("beforeend", `<div class="cc-sys-msg">Navigated to ${ctx.doctype}</div>`);
                        body.scrollTop = body.scrollHeight;
                    }
                }, 800);
            });
        }
    }

    function openBot() {
        var launcher = document.getElementById("classic-chatbot-launcher");
        var panel = document.getElementById("classic-chatbot-panel");

        if (!launcher || !panel) return;

        launcher.classList.add("cc-hide");
        panel.classList.add("cc-open");

        setTimeout(function () {
            var input = document.getElementById("classic-chatbot-input");
            if (input) input.focus();
        }, 100);

        updateContextUI();
    }

    function closeBot() {
        var panel = document.getElementById("classic-chatbot-panel");
        var launcher = document.getElementById("classic-chatbot-launcher");

        if (panel) panel.classList.remove("cc-open");

        setTimeout(function () {
            if (launcher) launcher.classList.remove("cc-hide");
        }, 300);
    }

    function addUserMessage(text) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;
        
        var emptyState = body.querySelector(".cc-empty-state");
        if(emptyState) emptyState.remove();

        body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + "</div>");
        body.scrollTop = body.scrollHeight;
    }

    function addBotMessage(text, rawHTML) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;

        var emptyState = body.querySelector(".cc-empty-state");
        if(emptyState) emptyState.remove();

        var finalHTML = parseMarkdown(esc(text));

        if (rawHTML) {
            finalHTML += rawHTML;
        }

        body.insertAdjacentHTML("beforeend", '<div class="cc-bot-msg">' + finalHTML + "</div>");
        body.scrollTop = body.scrollHeight;
    }

    function showTyping() {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;

        if (document.getElementById("classic-chatbot-typing")) return;

        body.insertAdjacentHTML(
            "beforeend",
            '<div id="classic-chatbot-typing" class="cc-bot-msg"><div class="cc-typing"><span></span><span></span><span></span></div></div>'
        );

        body.scrollTop = body.scrollHeight;
    }

    function hideTyping() {
        var t = document.getElementById("classic-chatbot-typing");
        if (t) t.remove();
    }

    function handleSlashCommand(rawMsg) {
        // /login <token>, /logout, /whoami — Claude subscription auth per user.
        var m = rawMsg.match(/^\/(login|logout|whoami)\b\s*(.*)$/i);
        if (!m) return false;

        var cmd = m[1].toLowerCase();
        var arg = (m[2] || "").trim();

        // Token ko chat me plain na dikhao — masked user message.
        addUserMessage(cmd === "login" && arg ? "/login ••••••••" : rawMsg);

        if (cmd === "login") {
            if (!arg) {
                addBotMessage("Usage: `/login sk-ant-oat01-...`  — apne computer par `claude setup-token` chala kar jo token milta hai wo paste karo. Ye tumhare apne Claude subscription se chalega, kisi aur ko dikhega nahi.");
                return true;
            }
            showTyping();
            frappe.call({
                method: "classic_chatbot.api.token_store.save_token",
                args: { token: arg },
                callback: function (r) {
                    hideTyping();
                    if (r && r.message && r.message.ok) {
                        claude_session_id = "";
                        addBotMessage("✅ Claude login save ho gaya. Ab tum apne subscription se chatbot use kar sakte ho. Koi bhi ERP sawaal pucho.");
                    } else {
                        addBotMessage("⚠️ Token save nahi hua.");
                    }
                },
                error: function (err) {
                    hideTyping();
                    var msg = (err && err._server_messages) ? "Token reject hua — sahi `claude setup-token` token paste karo." : "Token save karne me error.";
                    addBotMessage("⚠️ " + msg);
                }
            });
            return true;
        }

        if (cmd === "logout") {
            showTyping();
            frappe.call({
                method: "classic_chatbot.api.token_store.clear_token",
                callback: function (r) {
                    hideTyping();
                    claude_session_id = "";
                    addBotMessage((r && r.message && r.message.removed)
                        ? "✅ Claude login hata diya. Dobara use karne ke liye `/login <token>` bhejo."
                        : "Tumhara koi Claude login save nahi tha.");
                },
                error: function () { hideTyping(); addBotMessage("⚠️ Logout me error."); }
            });
            return true;
        }

        if (cmd === "whoami") {
            showTyping();
            frappe.call({
                method: "classic_chatbot.api.token_store.token_status",
                callback: function (r) {
                    hideTyping();
                    var s = r && r.message;
                    if (s && s.logged_in) {
                        var lbl = s.label ? (" (" + esc(s.label) + ")") : "";
                        addBotMessage("🔓 Claude login active" + lbl + ". Chatbot tumhare apne subscription se chal raha hai.");
                    } else {
                        addBotMessage("🔒 Abhi koi Claude login save nahi hai. `/login <token>` bhejo.");
                    }
                },
                error: function () { hideTyping(); addBotMessage("⚠️ Status check me error."); }
            });
            return true;
        }
        return false;
    }

    function sendMessage(quickText) {
        var input = document.getElementById("classic-chatbot-input");
        var rawMsg = quickText || (input ? input.value.trim() : "");

        if (!rawMsg) return;
        if (input) input.value = "";

        if (handleSlashCommand(rawMsg)) return;

        addUserMessage(rawMsg);
        showTyping();

        var ctx = getContext();

        // Include UI Tool States contextually before sending
        var finalQuestion = rawMsg;
        if (webSearchActive) finalQuestion = "[Web Search Mode] " + finalQuestion;
        if (reasoningActive) finalQuestion = "[Deep Reasoning] " + finalQuestion;

        if (last_error && rawMsg.toLowerCase().includes("error")) {
            finalQuestion += "\n(Recent UI Error Logged: " + last_error + ")";
            last_error = "";
        }

        var safeDocData = {};

        if (ctx.doc) {
            Object.keys(ctx.doc).forEach(function (key) {
                if (key.startsWith("_")) return;
                var val = ctx.doc[key];

                if (val === null || val === undefined || val === "") return;

                if (Array.isArray(val)) {
                    var rows = val.slice(0, 10).map(function (row) {
                        if (typeof row !== "object" || !row) return row;
                        var slim = {};
                        Object.keys(row).forEach(function (rk) {
                            var rv = row[rk];
                            if (!rk.startsWith("_") && typeof rv !== "object" &&
                                rv !== null && rv !== "" &&
                                ["name","owner","creation","modified","modified_by",
                                 "docstatus","doctype","parent","parentfield",
                                 "parenttype","idx"].indexOf(rk) === -1) {
                                slim[rk] = rv;
                            }
                        });
                        return slim;
                    });
                    if (rows.length) safeDocData[key] = rows;
                } else if (typeof val !== "object") {
                    safeDocData[key] = val;
                }
            });
        }

        var modelSelect = document.getElementById("classic-chatbot-model-select");
        var preferredModel = modelSelect ? modelSelect.value : "claude";

        var args = {
            question: finalQuestion, // Sending modified question
            doctype: ctx.doctype,
            docname: ctx.docname,
            doc: JSON.stringify(safeDocData),
            route: JSON.stringify(ctx.route || []),
            preferred_model: preferredModel,
            history: JSON.stringify(chat_history.slice(-6))
        };

        if (preferredModel === "claude" && claude_session_id) {
            args.session_id = claude_session_id;
        }

        function renderBotResponse(m) {
            hideTyping();

            var answer = "Server ne answer generate nahi kiya.";
            var badge = "";

            if (m) {
                if (m.answer) {
                    answer = m.answer;
                }

                if (m.session_id) {
                    claude_session_id = m.session_id;
                }

                if (m.model_used) {
                    var tools = Array.isArray(m.tools_used) && m.tools_used.length
                        ? " · " + esc(m.tools_used.join(", "))
                        : "";
                    badge = `<div style="font-size: 11px; color: rgba(255,255,255,0.4); margin-top: 12px; font-weight: 500;">${esc(m.model_used)}${tools}</div>`;
                }
            }

            addBotMessage(answer, badge);

            chat_history.push({ role: "user", content: rawMsg });
            chat_history.push({ role: "assistant", content: answer });
            if (chat_history.length > 12) chat_history = chat_history.slice(-12);
        }

        function showFailure() {
            hideTyping();
            addBotMessage("⚠️ API Server disconnect ho gaya. Kripya check karein.");
        }

        if (preferredModel === "claude") {
            frappe.call({
                method: "classic_chatbot.api.claude_agent.ask_claude_async",
                args: args,
                callback: function (r) {
                    var token = r && r.message && r.message.job_token;
                    if (!token) return showFailure();

                    var polls = 0;
                    var poller = setInterval(function () {
                        polls++;
                        if (polls > 100) {
                            clearInterval(poller);
                            return showFailure();
                        }
                        frappe.call({
                            method: "classic_chatbot.api.claude_agent.poll_claude",
                            args: { job_token: token },
                            callback: function (pr) {
                                var m = pr && pr.message;
                                if (!m) return;
                                if (m.status === "done") {
                                    clearInterval(poller);
                                    renderBotResponse(m.result);
                                } else if (m.status === "expired") {
                                    clearInterval(poller);
                                    showFailure();
                                }
                            },
                            error: function () {
                                clearInterval(poller);
                                showFailure();
                            }
                        });
                    }, 3000);
                },
                error: showFailure
            });
        } else {
            frappe.call({
                method: "classic_chatbot.api.agent.ask",
                args: args,
                callback: function (r) {
                    renderBotResponse(r && r.message);
                },
                error: showFailure
            });
        }
    }

    // --- EVENT LISTENERS ---
    document.addEventListener("click", function (e) {
        var launcher = e.target.closest("#classic-chatbot-launcher");
        var close = e.target.closest("#classic-chatbot-close");
        var refresh = e.target.closest("#classic-chatbot-refresh");
        var send = e.target.closest("#classic-chatbot-send");
        var quick = e.target.closest(".cc-quick button");
        
        // Toolbar Tools
        var btnAttach = e.target.closest("#cc-btn-attach");
        var btnWeb = e.target.closest("#cc-btn-web");
        var btnReason = e.target.closest("#cc-btn-reason");
        var btnLive = e.target.closest("#cc-btn-live");
        var btnMic = e.target.closest("#cc-btn-mic");

        if (launcher) {
            e.preventDefault();
            openBot();
        } else if (close) {
            e.preventDefault();
            closeBot();
        } else if (refresh) {
            e.preventDefault();
            var body = document.getElementById("classic-chatbot-body");
            claude_session_id = "";
            chat_history = [];
            if (body) {
                body.innerHTML = `
                <div class="cc-empty-state">
                    <div class="cc-empty-title">What can I help with?</div>
                </div>`;
            }
            showToast("Chat Cleared");
        } else if (send) {
            e.preventDefault();
            sendMessage();
        } else if (quick) {
            e.preventDefault();
            sendMessage(quick.getAttribute("data-q"));
        } 
        
        // Tool Functions
        else if (btnAttach) {
            e.preventDefault();
            document.getElementById("cc-hidden-file").click();
        } else if (btnWeb) {
            e.preventDefault();
            webSearchActive = !webSearchActive;
            btnWeb.classList.toggle("cc-tool-active", webSearchActive);
            showToast(webSearchActive ? "Web Search: Enabled" : "Web Search: Disabled");
        } else if (btnReason) {
            e.preventDefault();
            reasoningActive = !reasoningActive;
            btnReason.classList.toggle("cc-tool-active", reasoningActive);
            showToast(reasoningActive ? "Reasoning Mode: ON" : "Reasoning Mode: OFF");
        } else if (btnLive) {
            e.preventDefault();
            updateContextUI();
            showToast("Context Synced!");
        } else if (btnMic) {
            e.preventDefault();
            startDictation(btnMic);
        }
    });

    // File Input Listener
    document.addEventListener("change", function(e) {
        if(e.target && e.target.id === "cc-hidden-file") {
            if(e.target.files && e.target.files.length > 0) {
                var fileName = e.target.files[0].name;
                var input = document.getElementById("classic-chatbot-input");
                if (input) {
                    input.value = "[Attached: " + fileName + "] " + input.value;
                    input.focus();
                }
                showToast("File Attached");
                e.target.value = ""; 
            }
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    window.addEventListener("error", function (e) {
        last_error = e.message || "";
    });

    window.addEventListener("unhandledrejection", function (e) {
        last_error = e.reason ? String(e.reason) : "";
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", mountBot);
    } else {
        mountBot();
    }
})();
























