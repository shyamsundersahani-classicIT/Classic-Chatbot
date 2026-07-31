// (function () {
//     console.log("[Classic Chatbot] Force Loading ChatGPT Dark UI (Transparent) + Functional Tools 🌙");

//     var last_error = "";
//     var chat_history = [];

//     // Tool States
//     var webSearchActive = false;
//     var reasoningActive = false;

//     function esc(text) {
//         if (text === undefined || text === null) return "";
//         return String(text)
//             .replace(/&/g, "&amp;")
//             .replace(/</g, "&lt;")
//             .replace(/>/g, "&gt;")
//             .replace(/"/g, "&quot;")
//             .replace(/'/g, "&#039;");
//     }

//     // --- ADVANCED MARKDOWN PARSER ---
//     function parseMarkdown(text) {
//         let html = text;
        
//         // 1. Code Blocks
//         html = html.replace(/\`\`\`([\s\S]*?)\`\`\`/g, '<pre style="background:rgba(0,0,0,0.6); color:#e2e8f0; padding:16px; border-radius:12px; overflow-x:auto; font-size:13px; margin: 12px 0; border:1px solid rgba(255,255,255,0.1);"><code>$1</code></pre>');
        
//         // 2. Inline Code
//         html = html.replace(/\`([^\`]+)\`/g, '<code style="background:rgba(47,47,47,0.8); color:#ff9800; padding:3px 6px; border-radius:6px; font-size:13px; font-weight:600; border: 1px solid rgba(255,255,255,0.1);">$1</code>');
        
//         // 3. Bold Text
//         html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#ffffff;">$1</strong>');
        
//         // 4. Tables
//         html = html.replace(/(?:\|.*\|[ \t]*(?:[\r\n]+|$))+/g, function(match) {
//             let rows = match.trim().split('\n');
//             let table = '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; border-radius:10px; overflow:hidden; background:rgba(47,47,47,0.6);"><tbody>';
//             rows.forEach((row, i) => {
//                 if (row.includes('---')) return;
//                 let cols = row.split('|').filter(c => c.trim() !== '');
//                 table += '<tr>';
//                 cols.forEach(col => {
//                     let cell = i === 0 ? 'th' : 'td';
//                     let style = i === 0 ? 'border-bottom:1px solid rgba(255,255,255,0.1); padding:12px; background:rgba(33,33,33,0.8); text-align:left; color:#fff; font-weight:700;' : 'border-bottom:1px solid rgba(255,255,255,0.05); padding:10px 12px; color:#ddd;';
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

//         var ctx = { route: route, doctype: null, docname: null, doc: null };
        
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

//     // --- UI NOTIFICATION TOAST ---
//     function showToast(text) {
//         var panel = document.getElementById("classic-chatbot-panel");
//         if (!panel) return;
//         var toast = document.getElementById("cc-toast");
//         if (!toast) {
//             toast = document.createElement("div");
//             toast.id = "cc-toast";
//             panel.appendChild(toast);
//         }
//         toast.innerText = text;
//         toast.classList.add("show");
//         setTimeout(function() { toast.classList.remove("show"); }, 2000);
//     }

//     // --- VOICE TO TEXT IMPLEMENTATION ---
//     function startDictation(btnElement) {
//         if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
//             showToast("Microphone not supported in this browser.");
//             return;
//         }
//         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//         const recognition = new SpeechRecognition();
        
//         recognition.lang = 'en-US'; 
//         recognition.interimResults = false;
//         recognition.maxAlternatives = 1;

//         recognition.onstart = function() {
//             btnElement.classList.add("cc-tool-recording");
//             showToast("Listening...");
//         };

//         recognition.onresult = function(event) {
//             const transcript = event.results[0][0].transcript;
//             const input = document.getElementById("classic-chatbot-input");
//             if(input) {
//                 input.value = (input.value + " " + transcript).trim();
//                 input.focus();
//             }
//         };

//         recognition.onerror = function(event) {
//             showToast("Mic error: " + event.error);
//             btnElement.classList.remove("cc-tool-recording");
//         };

//         recognition.onend = function() {
//             btnElement.classList.remove("cc-tool-recording");
//         };

//         recognition.start();
//     }

//     function injectStyle() {
//         document.querySelectorAll("style[id^='classic-chatbot-style']").forEach(el => el.remove());

//         var style = document.createElement("style");
//         style.id = "classic-chatbot-style-chatgpt-dark";

//         style.innerHTML = `
//             /* 🌙 ChatGPT App Dark Mode Style (Transparent Glass) 🌙 */

//             ::-webkit-scrollbar { width: 6px; height: 6px; }
//             ::-webkit-scrollbar-track { background: transparent; }
//             ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
//             ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }

//             @keyframes ccMsgIn {
//                 from { opacity: 0; transform: translateY(10px); }
//                 to { opacity: 1; transform: translateY(0); }
//             }

//             /* Launcher Button */
//             #classic-chatbot-launcher {
//                 position: fixed;
//                 right: 30px;
//                 bottom: 30px;
//                 width: 60px;
//                 height: 60px;
//                 border-radius: 50%;
//                 border: none;
//                 background: rgba(255, 255, 255, 0.95) !important;
//                 color: #212121 !important;
//                 font-size: 26px;
//                 z-index: 999999;
//                 cursor: pointer;
//                 transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//                 box-shadow: 0 10px 30px rgba(0,0,0,0.5);
//                 backdrop-filter: blur(8px);
//                 -webkit-backdrop-filter: blur(8px);
//             }

//             #classic-chatbot-launcher:hover {
//                 transform: scale(1.08);
//             }

//             #classic-chatbot-launcher.cc-hide {
//                 opacity: 0;
//                 pointer-events: none;
//                 transform: scale(0.5);
//             }
            
//             /* Main Chat Panel */
//             #classic-chatbot-panel {
//                 position: fixed;
//                 right: 30px;
//                 bottom: 110px;
//                 width: 420px;
//                 height: 720px;
//                 background: rgba(33, 33, 33, 0.75) !important;
//                 backdrop-filter: blur(16px);
//                 -webkit-backdrop-filter: blur(16px);
//                 border-radius: 32px !important;
//                 z-index: 999999;
//                 box-shadow: 0 30px 80px rgba(0,0,0,0.8), 0 0 0 1px rgba(255,255,255,0.08) inset !important;
//                 display: flex;
//                 flex-direction: column;
//                 overflow: hidden;
//                 opacity: 0;
//                 visibility: hidden;
//                 pointer-events: none;
//                 transform: translateY(40px) scale(0.95);
//                 transform-origin: bottom right;
//                 transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
//                 font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
//             }

//             #classic-chatbot-panel.cc-open {
//                 opacity: 1;
//                 visibility: visible;
//                 pointer-events: auto;
//                 transform: translateY(0) scale(1);
//             }
            
//             /* Header */
//             .cc-head {
//                 background: transparent !important;
//                 color: #ececec !important;
//                 padding: 20px 24px;
//                 display: flex;
//                 align-items: center;
//                 justify-content: space-between;
//                 flex-shrink: 0;
//                 border-bottom: 1px solid rgba(255,255,255,0.05) !important;
//             }

//             .cc-title {
//                 font-size: 16px;
//                 font-weight: 600;
//                 display: flex;
//                 flex-direction: column;
//             }

//             .cc-status {
//                 font-size: 11px;
//                 font-weight: 500;
//                 color: rgba(255,255,255,0.6);
//                 margin-top: 2px;
//             }
            
//             .cc-actions {
//                 display: flex;
//                 gap: 12px;
//             }

//             .cc-icon-btn {
//                 background: transparent;
//                 border: none;
//                 color: #ececec;
//                 width: 32px;
//                 height: 32px;
//                 border-radius: 50%;
//                 cursor: pointer;
//                 transition: all 0.2s;
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//             }

//             .cc-icon-btn:hover {
//                 background: rgba(255,255,255,0.1);
//             }

//             /* Model Selector */
//             #classic-chatbot-model-select {
//                 display: block; 
//                 background: rgba(255, 255, 255, 0.08);
//                 color: #ececec;
//                 border: 1px solid rgba(255, 255, 255, 0.15);
//                 border-radius: 12px;
//                 padding: 4px 8px;
//                 font-size: 11px;
//                 outline: none;
//                 cursor: pointer;
//                 transition: all 0.2s;
//                 backdrop-filter: blur(4px);
//             }
//             #classic-chatbot-model-select:hover {
//                 background: rgba(255, 255, 255, 0.15);
//             }
//             #classic-chatbot-model-select option {
//                 background: #212121;
//                 color: #ececec;
//             }

//             /* Chat Body */
//             #classic-chatbot-body {
//                 flex: 1;
//                 padding: 24px 24px 0 24px;
//                 overflow-y: auto;
//                 scroll-behavior: smooth;
//             }

//             .cc-bot-msg,
//             .cc-user-msg {
//                 margin-bottom: 24px;
//                 font-size: 15px;
//                 line-height: 1.6;
//                 word-wrap: break-word;
//                 animation: ccMsgIn 0.3s ease forwards;
//             }
            
//             .cc-bot-msg {
//                 background: transparent !important;
//                 color: #ececec !important;
//                 padding: 0 !important;
//                 border-radius: 0 !important;
//                 box-shadow: none !important;
//                 border: none !important;
//                 max-width: 95%;
//             }

//             .cc-user-msg {
//                 background: rgba(47, 47, 47, 0.6) !important;
//                 color: #ececec !important;
//                 padding: 12px 18px !important;
//                 border-radius: 20px !important;
//                 border-bottom-right-radius: 4px !important;
//                 margin-left: auto;
//                 max-width: 80%;
//                 width: fit-content;
//                 box-shadow: none !important;
//                 border: 1px solid rgba(255,255,255,0.05) !important;
//             }

//             .cc-sys-msg {
//                 text-align: center;
//                 color: rgba(255,255,255,0.5);
//                 font-size: 12px;
//                 margin-bottom: 24px;
//                 font-weight: 500;
//                 animation: ccMsgIn 0.3s ease forwards;
//             }
            
//             /* Quick Actions */
//             .cc-foot-wrapper {
//                 padding: 10px 16px 20px 16px;
//                 background: transparent;
//                 flex-shrink: 0;
//             }

//             .cc-quick {
//                 display: flex;
//                 gap: 8px;
//                 overflow-x: auto;
//                 padding-bottom: 12px;
//                 scrollbar-width: none;
//             }
//             .cc-quick::-webkit-scrollbar { display: none; }

//             .cc-quick button {
//                 flex-shrink: 0;
//                 background: rgba(47, 47, 47, 0.6) !important;
//                 border: 1px solid rgba(255,255,255,0.1) !important;
//                 color: #ececec !important;
//                 border-radius: 20px !important;
//                 padding: 8px 14px !important;
//                 font-size: 13px !important;
//                 font-weight: 500 !important;
//                 cursor: pointer;
//                 transition: background 0.2s;
//                 backdrop-filter: blur(4px);
//             }

//             .cc-quick button:hover {
//                 background: rgba(63, 63, 63, 0.8) !important;
//             }

//             /* Floating Island Input */
//             .cc-input-container {
//                 background: rgba(47, 47, 47, 0.5);
//                 border: 1px solid rgba(255,255,255,0.08);
//                 backdrop-filter: blur(12px);
//                 -webkit-backdrop-filter: blur(12px);
//                 border-radius: 26px;
//                 padding: 12px 6px 6px 16px;
//                 display: flex;
//                 flex-direction: column;
//                 gap: 12px;
//             }

//             #classic-chatbot-input {
//                 width: 100%;
//                 background: transparent !important;
//                 border: none !important;
//                 color: #ececec !important;
//                 font-size: 16px !important;
//                 outline: none !important;
//                 padding-right: 12px;
//                 font-family: inherit;
//                 box-shadow: none !important;
//             }
//             #classic-chatbot-input::placeholder {
//                 color: rgba(255,255,255,0.4) !important;
//             }

//             /* Tools Toolbar */
//             .cc-input-toolbar {
//                 display: flex;
//                 justify-content: space-between;
//                 align-items: center;
//             }

//             .cc-tools-left {
//                 display: flex;
//                 gap: 6px;
//             }

//             .cc-tool-btn {
//                 background: transparent;
//                 border: 1px solid rgba(255,255,255,0.15);
//                 color: #ececec;
//                 width: 32px;
//                 height: 32px;
//                 border-radius: 50%;
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//                 cursor: pointer;
//                 transition: all 0.2s ease;
//             }
//             .cc-tool-btn:hover { background: rgba(255,255,255,0.1); }
//             .cc-tool-btn svg { width: 16px; height: 16px; opacity: 0.8; }

//             /* ACTIVE & RECORDING STATES */
//             .cc-tool-active {
//                 background: rgba(255, 255, 255, 0.9) !important;
//                 color: #000000 !important;
//                 border-color: transparent !important;
//             }
//             .cc-tool-active svg { opacity: 1; }
            
//             .cc-tool-recording {
//                 background: #ef4444 !important;
//                 color: #ffffff !important;
//                 border-color: transparent !important;
//                 animation: pulseRecord 1.5s infinite;
//             }
//             @keyframes pulseRecord {
//                 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
//                 70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
//                 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
//             }

//             .cc-tools-right {
//                 display: flex;
//                 gap: 6px;
//                 align-items: center;
//             }

//             #classic-chatbot-send {
//                 width: 34px;
//                 height: 34px;
//                 border-radius: 50%;
//                 border: none;
//                 background: rgba(255, 255, 255, 0.9) !important;
//                 color: #000000 !important;
//                 cursor: pointer;
//                 transition: transform 0.2s;
//                 display: flex;
//                 align-items: center;
//                 justify-content: center;
//                 margin-right: 4px;
//             }

//             #classic-chatbot-send:hover {
//                 transform: scale(1.05);
//                 background: #ffffff !important;
//             }
//             #classic-chatbot-send svg { width: 20px; height: 20px; }

//             /* Empty State */
//             .cc-empty-state {
//                 height: 100%;
//                 display: flex;
//                 flex-direction: column;
//                 align-items: center;
//                 justify-content: center;
//                 opacity: 1;
//             }
//             .cc-empty-title {
//                 font-size: 28px;
//                 font-weight: 600;
//                 color: rgba(255,255,255,0.9);
//                 text-align: center;
//             }

//             /* Toast Notification */
//             #cc-toast {
//                 position: absolute;
//                 bottom: 100px;
//                 left: 50%;
//                 transform: translateX(-50%);
//                 background: rgba(255, 255, 255, 0.9);
//                 color: #000;
//                 padding: 6px 14px;
//                 border-radius: 20px;
//                 font-size: 12px;
//                 font-weight: 600;
//                 pointer-events: none;
//                 opacity: 0;
//                 transition: opacity 0.3s ease;
//                 z-index: 1000;
//                 box-shadow: 0 4px 10px rgba(0,0,0,0.3);
//             }
//             #cc-toast.show { opacity: 1; }

//             /* Typing Indicator */
//             .cc-typing { display: flex; gap: 4px; padding: 12px 0; }
//             .cc-typing span {
//                 width: 8px; height: 8px; border-radius: 50%;
//                 background: #ececec; opacity: 0.5;
//                 animation: ccTypingBounce 1.4s infinite ease-in-out both;
//             }
//             .cc-typing span:nth-child(1) { animation-delay: -0.32s; }
//             .cc-typing span:nth-child(2) { animation-delay: -0.16s; }
//             @keyframes ccTypingBounce {
//                 0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
//                 40% { transform: scale(1); opacity: 1; }
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
//             statusEl.innerHTML = `${ctx.doctype} Mode`;
//             quickDiv.innerHTML = `
//                 <button type="button" data-q="Is ${ctx.doctype} form ke mandatory fields kya hain?">Missing Fields?</button>
//                 <button type="button" data-q="Current form ka error theek karo">Fix Error</button>
//                 <button type="button" data-q="${ctx.doctype} ke top 5 records dikhao">Top Records</button>
//             `;
//         } else {
//             statusEl.innerHTML = `Direct ERP Data`;
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
        
//         var oldLauncher = document.getElementById("classic-chatbot-launcher");
//         if (oldLauncher) oldLauncher.remove();
//         var oldPanel = document.getElementById("classic-chatbot-panel");
//         if (oldPanel) oldPanel.remove();

//         injectStyle();

//         var launcher = document.createElement("button");
//         launcher.id = "classic-chatbot-launcher";
//         launcher.innerHTML = `<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;

//         var panel = document.createElement("div");
//         panel.id = "classic-chatbot-panel";

//         panel.innerHTML = `
//             <div class="cc-head">
//                 <div style="display: flex; align-items: center; gap: 12px;">
//                     <div class="cc-title">
//                         <div>AI Agent</div>
//                         <div class="cc-status" id="cc-context-status">Direct ERP Data</div>
//                     </div>
//                     <select id="classic-chatbot-model-select">
//                         <option value="auto" selected>Auto</option>
//                         <option value="groq">Groq</option>
//                         <option value="local">Local</option>
//                     </select>
//                 </div>
//                 <div class="cc-actions">
//                     <button class="cc-icon-btn" id="classic-chatbot-refresh" title="Clear Chat">
//                         <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"></path><path d="M21 3v5h-5"></path></svg>
//                     </button>
//                     <button class="cc-icon-btn" id="classic-chatbot-close" title="Close">
//                         <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
//                     </button>
//                 </div>
//             </div>

//             <div id="classic-chatbot-body">
//                 <div class="cc-empty-state">
//                     <div class="cc-empty-title">What can I help with?</div>
//                 </div>
//             </div>

//             <div class="cc-foot-wrapper">
//                 <div class="cc-quick"></div>
//                 <div class="cc-input-container">
//                     <input id="classic-chatbot-input" placeholder="Ask anything" autocomplete="off" />
                    
//                     <div class="cc-input-toolbar">
//                         <div class="cc-tools-left">
//                             <button class="cc-tool-btn" id="cc-btn-attach" type="button" title="Attach File"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg></button>
//                             <button class="cc-tool-btn" id="cc-btn-web" type="button" title="Toggle Web Search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></button>
//                             <button class="cc-tool-btn" id="cc-btn-reason" type="button" title="Deep Reasoning Mode"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A6 6 0 1 0 7.5 11.5c.76.76 1.23 1.52 1.41 2.5h6.18z"></path></svg></button>
//                             <button class="cc-tool-btn" id="cc-btn-live" type="button" title="Sync ERP Context"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2"></circle><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48 0a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"></path></svg></button>
//                             <button class="cc-tool-btn" id="cc-btn-mic" type="button" title="Voice to Text"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg></button>
                            
//                             <!-- Hidden File Input -->
//                             <input type="file" id="cc-hidden-file" style="display:none;" />
//                         </div>
                        
//                         <div class="cc-tools-right">
//                             <button id="classic-chatbot-send" type="button">
//                                 <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
//                             </button>
//                         </div>
//                     </div>
//                 </div>
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

//                     if (body && ctx.doctype && !body.innerHTML.includes(`Mapsd to ${ctx.doctype}`)) {
//                         var emptyState = body.querySelector(".cc-empty-state");
//                         if(emptyState) emptyState.remove();

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
//         }, 300);
//     }

//     function addUserMessage(text) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;
        
//         var emptyState = body.querySelector(".cc-empty-state");
//         if(emptyState) emptyState.remove();

//         body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + "</div>");
//         body.scrollTop = body.scrollHeight;
//     }

//     function addBotMessage(text, rawHTML) {
//         var body = document.getElementById("classic-chatbot-body");
//         if (!body) return;

//         var emptyState = body.querySelector(".cc-empty-state");
//         if(emptyState) emptyState.remove();

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
//         var rawMsg = quickText || (input ? input.value.trim() : "");

//         if (!rawMsg) return;
//         if (input) input.value = "";

//         addUserMessage(rawMsg);
//         showTyping();

//         var ctx = getContext();

//         // Include UI Tool States contextually before sending
//         var finalQuestion = rawMsg;
//         if (webSearchActive) finalQuestion = "[Web Search Mode] " + finalQuestion;
//         if (reasoningActive) finalQuestion = "[Deep Reasoning] " + finalQuestion;

//         if (last_error && rawMsg.toLowerCase().includes("error")) {
//             finalQuestion += "\n(Recent UI Error Logged: " + last_error + ")";
//             last_error = "";
//         }

//         var safeDocData = {};

//         if (ctx.doc) {
//             Object.keys(ctx.doc).forEach(function (key) {
//                 if (key.startsWith("_")) return;
//                 var val = ctx.doc[key];

//                 if (val === null || val === undefined || val === "") return;

//                 if (Array.isArray(val)) {
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
//         var preferredModel = modelSelect ? modelSelect.value : "auto";

//         var args = {
//             question: finalQuestion, // Sending modified question
//             doctype: ctx.doctype,
//             docname: ctx.docname,
//             doc: JSON.stringify(safeDocData),
//             route: JSON.stringify(ctx.route || []),
//             preferred_model: preferredModel,
//             history: JSON.stringify(chat_history.slice(-6))
//         };

//         function renderBotResponse(m) {
//             hideTyping();

//             var answer = "Server ne answer generate nahi kiya.";
//             var badge = "";

//             if (m) {
//                 if (m.answer) {
//                     answer = m.answer;
//                 }

//                 if (m.model_used) {
//                     var tools = Array.isArray(m.tools_used) && m.tools_used.length
//                         ? " · " + esc(m.tools_used.join(", "))
//                         : "";
//                     badge = `<div style="font-size: 11px; color: rgba(255,255,255,0.4); margin-top: 12px; font-weight: 500;">${esc(m.model_used)}${tools}</div>`;
//                 }
//             }

//             addBotMessage(answer, badge);

//             chat_history.push({ role: "user", content: rawMsg });
//             chat_history.push({ role: "assistant", content: answer });
//             if (chat_history.length > 12) chat_history = chat_history.slice(-12);
//         }

//         function showFailure() {
//             hideTyping();
//             addBotMessage("⚠️ API Server disconnect ho gaya. Kripya check karein.");
//         }

//         frappe.call({
//             method: "classic_chatbot.api.agent.ask",
//             args: args,
//             callback: function (r) {
//                 renderBotResponse(r && r.message);
//             },
//             error: showFailure
//         });
//     }

//     // --- EVENT LISTENERS ---
//     document.addEventListener("click", function (e) {
//         var launcher = e.target.closest("#classic-chatbot-launcher");
//         var close = e.target.closest("#classic-chatbot-close");
//         var refresh = e.target.closest("#classic-chatbot-refresh");
//         var send = e.target.closest("#classic-chatbot-send");
//         var quick = e.target.closest(".cc-quick button");
        
//         // Toolbar Tools
//         var btnAttach = e.target.closest("#cc-btn-attach");
//         var btnWeb = e.target.closest("#cc-btn-web");
//         var btnReason = e.target.closest("#cc-btn-reason");
//         var btnLive = e.target.closest("#cc-btn-live");
//         var btnMic = e.target.closest("#cc-btn-mic");

//         if (launcher) {
//             e.preventDefault();
//             openBot();
//         } else if (close) {
//             e.preventDefault();
//             closeBot();
//         } else if (refresh) {
//             e.preventDefault();
//             var body = document.getElementById("classic-chatbot-body");
//             chat_history = [];
//             if (body) {
//                 body.innerHTML = `
//                 <div class="cc-empty-state">
//                     <div class="cc-empty-title">What can I help with?</div>
//                 </div>`;
//             }
//             showToast("Chat Cleared");
//         } else if (send) {
//             e.preventDefault();
//             sendMessage();
//         } else if (quick) {
//             e.preventDefault();
//             sendMessage(quick.getAttribute("data-q"));
//         } 
        
//         // Tool Functions
//         else if (btnAttach) {
//             e.preventDefault();
//             document.getElementById("cc-hidden-file").click();
//         } else if (btnWeb) {
//             e.preventDefault();
//             webSearchActive = !webSearchActive;
//             btnWeb.classList.toggle("cc-tool-active", webSearchActive);
//             showToast(webSearchActive ? "Web Search: Enabled" : "Web Search: Disabled");
//         } else if (btnReason) {
//             e.preventDefault();
//             reasoningActive = !reasoningActive;
//             btnReason.classList.toggle("cc-tool-active", reasoningActive);
//             showToast(reasoningActive ? "Reasoning Mode: ON" : "Reasoning Mode: OFF");
//         } else if (btnLive) {
//             e.preventDefault();
//             updateContextUI();
//             showToast("Context Synced!");
//         } else if (btnMic) {
//             e.preventDefault();
//             startDictation(btnMic);
//         }
//     });

//     // File Input Listener
//     document.addEventListener("change", function(e) {
//         if(e.target && e.target.id === "cc-hidden-file") {
//             if(e.target.files && e.target.files.length > 0) {
//                 var fileName = e.target.files[0].name;
//                 var input = document.getElementById("classic-chatbot-input");
//                 if (input) {
//                     input.value = "[Attached: " + fileName + "] " + input.value;
//                     input.focus();
//                 }
//                 showToast("File Attached");
//                 e.target.value = ""; 
//             }
//         }
//     });

//     document.addEventListener("keydown", function (e) {
//         if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
//             e.preventDefault();
//             sendMessage();
//         }
//     });

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
    "use strict";

    console.log(
        "[Classic Chatbot] Loading Local AI Chatbot"
    );

    var lastError = "";
    var chatHistory = [];

    var webSearchActive = false;
    var reasoningActive = false;

    function escapeHtml(value) {
        if (
            value === undefined ||
            value === null
        ) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function parseMarkdown(escapedText) {
    var html = String(
        escapedText || ""
    );

    /*
     * Code blocks ko temporarily placeholders me convert karo,
     * taki later markdown replacements code content ko alter na karein.
     */
    var codeBlocks = [];

    html = html.replace(
        /```(?:[a-zA-Z0-9_+-]+)?\s*([\s\S]*?)```/g,
        function (match, code) {
            var placeholder =
                "@@CLASSIC_CODE_BLOCK_" +
                codeBlocks.length +
                "@@";

            codeBlocks.push(
                '<pre class="cc-code-block">' +
                    "<code>" +
                    code.trim() +
                    "</code>" +
                "</pre>"
            );

            return placeholder;
        }
    );

    /*
     * Markdown tables.
     * Input pehle hi escapeHtml se sanitized hai.
     */
    html = html.replace(
        /(?:^\|.*\|[ \t]*$(?:\r?\n|$))+/gm,
        function (tableText) {
            var rows = tableText
                .trim()
                .split(/\r?\n/);

            if (!rows.length) {
                return tableText;
            }

            var tableHtml =
                '<div class="cc-table-wrapper">' +
                '<table class="cc-table">' +
                "<tbody>";

            var visibleRowIndex = 0;

            rows.forEach(function (row) {
                var normalized =
                    row.trim();

                /*
                 * Markdown separator:
                 * | --- | --- |
                 */
                if (
                    /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(
                        normalized
                    )
                ) {
                    return;
                }

                var columns = normalized
                    .replace(/^\|/, "")
                    .replace(/\|$/, "")
                    .split("|");

                if (!columns.length) {
                    return;
                }

                tableHtml += "<tr>";

                columns.forEach(
                    function (column) {
                        var tag =
                            visibleRowIndex === 0
                                ? "th"
                                : "td";

                        tableHtml +=
                            "<" +
                            tag +
                            ">" +
                            column.trim() +
                            "</" +
                            tag +
                            ">";
                    }
                );

                tableHtml += "</tr>";
                visibleRowIndex += 1;
            });

            tableHtml +=
                "</tbody>" +
                "</table>" +
                "</div>";

            return tableHtml;
        }
    );

    /*
     * Inline code.
     */
    html = html.replace(
        /`([^`\n]+)`/g,
        '<code class="cc-inline-code">$1</code>'
    );

    /*
     * Bold text.
     */
    html = html.replace(
        /\*\*([^*\n]+)\*\*/g,
        "<strong>$1</strong>"
    );

    /*
     * Basic unordered lists.
     */
    html = html.replace(
        /(?:^(?:-|\*)\s+.+$(?:\r?\n|$))+/gm,
        function (listText) {
            var items = listText
                .trim()
                .split(/\r?\n/)
                .filter(Boolean);

            var listHtml = "<ul>";

            items.forEach(function (item) {
                var content = item.replace(
                    /^(?:-|\*)\s+/,
                    ""
                );

                listHtml +=
                    "<li>" +
                    content +
                    "</li>";
            });

            listHtml += "</ul>";

            return listHtml;
        }
    );

    /*
     * Basic numbered lists.
     */
    html = html.replace(
        /(?:^\d+\.\s+.+$(?:\r?\n|$))+/gm,
        function (listText) {
            var items = listText
                .trim()
                .split(/\r?\n/)
                .filter(Boolean);

            var listHtml = "<ol>";

            items.forEach(function (item) {
                var content = item.replace(
                    /^\d+\.\s+/,
                    ""
                );

                listHtml +=
                    "<li>" +
                    content +
                    "</li>";
            });

            listHtml += "</ol>";

            return listHtml;
        }
    );

    /*
     * Remaining new lines.
     */
    html = html.replace(
        /\r?\n/g,
        "<br>"
    );

    /*
     * Restore safe code blocks.
     */
    codeBlocks.forEach(
        function (codeBlock, index) {
            var placeholder =
                "@@CLASSIC_CODE_BLOCK_" +
                index +
                "@@";

            html = html.replace(
                placeholder,
                codeBlock
            );
        }
    );

    return html;
}

    function getContext() {
        var route = [];

        try {
            route = frappe.get_route
                ? frappe.get_route()
                : [];
        } catch (error) {
            console.error(
                "[Classic Chatbot] Route error",
                error
            );
        }

        var context = {
            route: route,
            doctype: null,
            docname: null,
            doc: null
        };

        if (
            route &&
            route[0] === "Form"
        ) {
            context.doctype = route[1];
            context.docname = route[2];

            if (
                window.cur_frm &&
                cur_frm.doc &&
                cur_frm.doc.doctype ===
                    context.doctype
            ) {
                context.doc = cur_frm.doc;
            }
        }

        if (
            route &&
            route[0] === "List"
        ) {
            context.doctype = route[1];
        }

        return context;
    }

    function isLoggedIn() {
        if (
            window.frappe &&
            frappe.session &&
            frappe.session.user
        ) {
            return (
                frappe.session.user !== "Guest"
            );
        }

        var match =
            document.cookie.match(
                /(?:^|;\s*)user_id=([^;]*)/
            );

        var user =
            match
                ? decodeURIComponent(match[1])
                : "";

        return Boolean(
            user &&
            user !== "Guest"
        );
    }

    function showToast(text) {
        var panel =
            document.getElementById(
                "classic-chatbot-panel"
            );

        if (!panel) {
            return;
        }

        var toast =
            document.getElementById(
                "classic-chatbot-toast"
            );

        if (!toast) {
            toast =
                document.createElement("div");

            toast.id =
                "classic-chatbot-toast";

            panel.appendChild(toast);
        }

        toast.textContent = text;
        toast.classList.add("cc-show");

        setTimeout(function () {
            toast.classList.remove(
                "cc-show"
            );
        }, 2200);
    }

    function startDictation(button) {
        var SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            showToast(
                "Microphone browser mein supported nahi hai."
            );

            return;
        }

        var recognition =
            new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart =
            function () {
                button.classList.add(
                    "cc-recording"
                );

                showToast(
                    "Listening..."
                );
            };

        recognition.onresult =
            function (event) {
                var transcript =
                    event.results[0][0]
                        .transcript;

                var input =
                    document.getElementById(
                        "classic-chatbot-input"
                    );

                if (input) {
                    input.value =
                        (
                            input.value +
                            " " +
                            transcript
                        ).trim();

                    input.focus();
                }
            };

        recognition.onerror =
            function (event) {
                button.classList.remove(
                    "cc-recording"
                );

                showToast(
                    "Mic error: " +
                    event.error
                );
            };

        recognition.onend =
            function () {
                button.classList.remove(
                    "cc-recording"
                );
            };

        recognition.start();
    }

    function injectStyles() {
        if (
            document.getElementById(
                "classic-chatbot-style"
            )
        ) {
            return;
        }

        var style =
            document.createElement("style");

        style.id =
            "classic-chatbot-style";

        style.textContent = `
            #classic-chatbot-launcher {
                position: fixed;
                right: 28px;
                bottom: 28px;
                width: 58px;
                height: 58px;
                border: none;
                border-radius: 50%;
                background: #ffffff;
                color: #171717;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                z-index: 999999;
                box-shadow:
                    0 14px 35px rgba(0,0,0,.28);
                transition:
                    transform .2s ease,
                    opacity .2s ease;
            }

            #classic-chatbot-launcher:hover {
                transform: scale(1.06);
            }

            #classic-chatbot-launcher.cc-hidden {
                opacity: 0;
                pointer-events: none;
                transform: scale(.7);
            }

            #classic-chatbot-panel {
                position: fixed;
                right: 28px;
                bottom: 105px;
                width: 420px;
                height: 700px;
                max-height: calc(100vh - 130px);
                max-width: calc(100vw - 40px);
                border-radius: 24px;
                background:
                    rgba(28,28,28,.95);
                color: #ececec;
                z-index: 999999;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                box-shadow:
                    0 24px 75px rgba(0,0,0,.45);
                opacity: 0;
                visibility: hidden;
                pointer-events: none;
                transform:
                    translateY(20px)
                    scale(.96);
                transform-origin:
                    bottom right;
                transition:
                    opacity .25s ease,
                    transform .25s ease,
                    visibility .25s ease;
                font-family:
                    Inter,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }

            #classic-chatbot-panel.cc-open {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
                transform:
                    translateY(0)
                    scale(1);
            }

            .cc-header {
                padding: 17px 18px;
                border-bottom:
                    1px solid rgba(255,255,255,.08);
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-shrink: 0;
            }

            .cc-header-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .cc-title {
                font-size: 16px;
                font-weight: 700;
                color: #ffffff;
            }

            .cc-context {
                margin-top: 2px;
                font-size: 11px;
                color:
                    rgba(255,255,255,.55);
            }

            #classic-chatbot-model-select {
                background:
                    rgba(255,255,255,.08);
                color: #ececec;
                border:
                    1px solid rgba(255,255,255,.14);
                border-radius: 9px;
                padding: 5px 8px;
                font-size: 11px;
                outline: none;
                cursor: pointer;
            }

            #classic-chatbot-model-select option {
                background: #202020;
                color: #ffffff;
            }

            .cc-header-actions {
                display: flex;
                gap: 5px;
            }

            .cc-icon-button {
                width: 34px;
                height: 34px;
                border: none;
                border-radius: 50%;
                background: transparent;
                color: #ececec;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }

            .cc-icon-button:hover {
                background:
                    rgba(255,255,255,.09);
            }

            #classic-chatbot-body {
                flex: 1;
                overflow-y: auto;
                padding: 20px 20px 8px;
                scroll-behavior: smooth;
            }

            .cc-empty-state {
                height: 100%;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }

            .cc-empty-title {
                font-size: 26px;
                font-weight: 700;
                color: #ffffff;
            }

            .cc-empty-subtitle {
                margin-top: 8px;
                color:
                    rgba(255,255,255,.48);
                font-size: 13px;
            }

            .cc-message {
                margin-bottom: 18px;
                font-size: 14px;
                line-height: 1.55;
                word-break: break-word;
            }

            .cc-user-message {
                margin-left: auto;
                max-width: 82%;
                width: fit-content;
                padding: 11px 15px;
                border-radius:
                    18px 18px 4px 18px;
                background:
                    rgba(255,255,255,.1);
                color: #ffffff;
            }

            .cc-bot-message {
                max-width: 96%;
                color: #ececec;
            }

            .cc-system-message {
                text-align: center;
                margin: 8px 0 18px;
                color:
                    rgba(255,255,255,.45);
                font-size: 11px;
            }

            .cc-model-badge {
                margin-top: 9px;
                color:
                    rgba(255,255,255,.38);
                font-size: 10px;
            }

            .cc-code-block {
                margin: 10px 0;
                padding: 13px;
                border-radius: 10px;
                background: #111111;
                border:
                    1px solid rgba(255,255,255,.09);
                color: #e4e4e4;
                overflow-x: auto;
                font-size: 12px;
                line-height: 1.5;
            }

            .cc-inline-code {
                padding: 2px 5px;
                border-radius: 5px;
                background:
                    rgba(255,255,255,.1);
                color: #ffb15c;
                font-size: 12px;
            }

            .cc-table-wrapper {
                overflow-x: auto;
                margin: 10px 0;
            }

            .cc-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }

            .cc-table th,
            .cc-table td {
                border:
                    1px solid rgba(255,255,255,.1);
                padding: 8px;
                text-align: left;
            }

            .cc-table th {
                background:
                    rgba(255,255,255,.08);
            }

            .cc-footer {
                padding: 8px 14px 16px;
                flex-shrink: 0;
            }

            .cc-quick-actions {
                display: flex;
                gap: 7px;
                padding-bottom: 10px;
                overflow-x: auto;
            }

            .cc-quick-actions button {
                flex: 0 0 auto;
                border:
                    1px solid rgba(255,255,255,.12);
                background:
                    rgba(255,255,255,.06);
                color: #ececec;
                border-radius: 18px;
                padding: 7px 11px;
                font-size: 11px;
                cursor: pointer;
            }

            .cc-quick-actions button:hover {
                background:
                    rgba(255,255,255,.12);
            }

            .cc-input-box {
                padding: 11px 7px 7px 14px;
                border:
                    1px solid rgba(255,255,255,.1);
                border-radius: 22px;
                background:
                    rgba(255,255,255,.075);
            }

            #classic-chatbot-input {
                width: 100%;
                border: none;
                outline: none;
                box-shadow: none;
                background: transparent;
                color: #ffffff;
                font-size: 14px;
                padding: 2px 7px 9px 0;
            }

            #classic-chatbot-input::placeholder {
                color:
                    rgba(255,255,255,.4);
            }

            .cc-input-toolbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .cc-tools {
                display: flex;
                gap: 5px;
            }

            .cc-tool-button {
                width: 31px;
                height: 31px;
                border-radius: 50%;
                border:
                    1px solid rgba(255,255,255,.12);
                background: transparent;
                color: #ececec;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }

            .cc-tool-button:hover {
                background:
                    rgba(255,255,255,.09);
            }

            .cc-tool-button.cc-active {
                background: #ffffff;
                color: #111111;
            }

            .cc-tool-button.cc-recording {
                background: #d92d20;
                color: #ffffff;
                animation:
                    ccRecordingPulse
                    1.3s infinite;
            }

            #classic-chatbot-send {
                width: 34px;
                height: 34px;
                border: none;
                border-radius: 50%;
                background: #ffffff;
                color: #111111;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }

            #classic-chatbot-send:hover {
                transform: scale(1.04);
            }

            .cc-typing {
                display: flex;
                gap: 4px;
                padding: 8px 0;
            }

            .cc-typing span {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background:
                    rgba(255,255,255,.65);
                animation:
                    ccTypingBounce
                    1.2s infinite ease-in-out;
            }

            .cc-typing span:nth-child(2) {
                animation-delay: .15s;
            }

            .cc-typing span:nth-child(3) {
                animation-delay: .3s;
            }

            #classic-chatbot-toast {
                position: absolute;
                left: 50%;
                bottom: 95px;
                transform:
                    translateX(-50%)
                    translateY(8px);
                opacity: 0;
                pointer-events: none;
                padding: 7px 12px;
                border-radius: 18px;
                background: #ffffff;
                color: #111111;
                font-size: 11px;
                font-weight: 600;
                transition:
                    opacity .2s ease,
                    transform .2s ease;
                z-index: 10;
                white-space: nowrap;
            }

            #classic-chatbot-toast.cc-show {
                opacity: 1;
                transform:
                    translateX(-50%)
                    translateY(0);
            }

            @keyframes ccTypingBounce {
                0%,
                70%,
                100% {
                    transform: translateY(0);
                    opacity: .45;
                }

                35% {
                    transform: translateY(-4px);
                    opacity: 1;
                }
            }

            @keyframes ccRecordingPulse {
                0% {
                    box-shadow:
                        0 0 0 0
                        rgba(217,45,32,.5);
                }

                70% {
                    box-shadow:
                        0 0 0 8px
                        rgba(217,45,32,0);
                }

                100% {
                    box-shadow:
                        0 0 0 0
                        rgba(217,45,32,0);
                }
            }

            @media (max-width: 600px) {
                #classic-chatbot-panel {
                    left: 10px;
                    right: 10px;
                    bottom: 85px;
                    width: auto;
                    height:
                        calc(100vh - 105px);
                    max-height:
                        calc(100vh - 105px);
                    border-radius: 18px;
                }

                #classic-chatbot-launcher {
                    right: 18px;
                    bottom: 18px;
                }
            }
        `;

        document.head.appendChild(style);
    }

    function updateContextUI() {
        var context = getContext();

        var statusElement =
            document.getElementById(
                "classic-chatbot-context"
            );

        var quickContainer =
            document.querySelector(
                ".cc-quick-actions"
            );

        if (
            !statusElement ||
            !quickContainer
        ) {
            return;
        }

        if (context.doctype) {
            statusElement.textContent =
                context.doctype + " Mode";

            quickContainer.innerHTML =
                '<button type="button" ' +
                'data-question="Current form ko validate karo">' +
                    "Check Form" +
                "</button>" +

                '<button type="button" ' +
                'data-question="Current form mein kya galat hai?">' +
                    "Find Errors" +
                "</button>" +

                '<button type="button" ' +
                'data-question="' +
                    escapeHtml(context.doctype) +
                    ' ke top 5 records dikhao">' +
                    "Top Records" +
                "</button>";
        } else {
            statusElement.textContent =
                "Direct ERP Data";

            quickContainer.innerHTML =
                '<button type="button" ' +
                'data-question="Pending Purchase Orders dikhao">' +
                    "Pending POs" +
                "</button>" +

                '<button type="button" ' +
                'data-question="Low stock items dikhao">' +
                    "Low Stock" +
                "</button>" +

                '<button type="button" ' +
                'data-question="ERPNext manufacturing process explain karo">' +
                    "Manufacturing" +
                "</button>";
        }
    }

    function mountBot() {
        if (!isLoggedIn()) {
            return;
        }

        var existingLauncher =
            document.getElementById(
                "classic-chatbot-launcher"
            );

        var existingPanel =
            document.getElementById(
                "classic-chatbot-panel"
            );

        if (existingLauncher) {
            existingLauncher.remove();
        }

        if (existingPanel) {
            existingPanel.remove();
        }

        injectStyles();

        var launcher =
            document.createElement("button");

        launcher.id =
            "classic-chatbot-launcher";

        launcher.type = "button";

        launcher.title =
            "Open Classic AI Chatbot";

        launcher.innerHTML = `
            <svg
                width="27"
                height="27"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                ></path>
            </svg>
        `;

        var panel =
            document.createElement("div");

        panel.id =
            "classic-chatbot-panel";

        panel.innerHTML = `
            <div class="cc-header">
                <div class="cc-header-left">
                    <div>
                        <div class="cc-title">
                            Classic AI Agent
                        </div>

                        <div
                            class="cc-context"
                            id="classic-chatbot-context"
                        >
                            Direct ERP Data
                        </div>
                    </div>

                    <select
                        id="classic-chatbot-model-select"
                        title="Select AI Model"
                    >
                        <option
                            value="local"
                            selected
                        >
                            Local
                        </option>

                        <option value="auto">
                            Auto
                        </option>

                        <option value="groq">
                            Groq
                        </option>
                    </select>
                </div>

                <div class="cc-header-actions">
                    <button
                        type="button"
                        class="cc-icon-button"
                        id="classic-chatbot-clear"
                        title="Clear Chat"
                    >
                        <svg
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path
                                d="M21 12a9 9 0 1 1-9-9c2.5 0 4.9 1 6.7 2.7L21 8"
                            ></path>

                            <path
                                d="M21 3v5h-5"
                            ></path>
                        </svg>
                    </button>

                    <button
                        type="button"
                        class="cc-icon-button"
                        id="classic-chatbot-close"
                        title="Close"
                    >
                        <svg
                            width="21"
                            height="21"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <line
                                x1="18"
                                y1="6"
                                x2="6"
                                y2="18"
                            ></line>

                            <line
                                x1="6"
                                y1="6"
                                x2="18"
                                y2="18"
                            ></line>
                        </svg>
                    </button>
                </div>
            </div>

            <div id="classic-chatbot-body">
                <div class="cc-empty-state">
                    <div class="cc-empty-title">
                        What can I help with?
                    </div>

                    <div class="cc-empty-subtitle">
                        Ask about the current form or ERP data.
                    </div>
                </div>
            </div>

            <div class="cc-footer">
                <div class="cc-quick-actions"></div>

                <div class="cc-input-box">
                    <input
                        type="text"
                        id="classic-chatbot-input"
                        placeholder="Ask anything about ERP..."
                        autocomplete="off"
                    >

                    <div class="cc-input-toolbar">
                        <div class="cc-tools">
                            <button
                                type="button"
                                class="cc-tool-button"
                                id="classic-chatbot-attach"
                                title="Attach File"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <line
                                        x1="12"
                                        y1="5"
                                        x2="12"
                                        y2="19"
                                    ></line>

                                    <line
                                        x1="5"
                                        y1="12"
                                        x2="19"
                                        y2="12"
                                    ></line>
                                </svg>
                            </button>

                            <button
                                type="button"
                                class="cc-tool-button"
                                id="classic-chatbot-web"
                                title="Web Search"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <circle
                                        cx="12"
                                        cy="12"
                                        r="10"
                                    ></circle>

                                    <line
                                        x1="2"
                                        y1="12"
                                        x2="22"
                                        y2="12"
                                    ></line>

                                    <path
                                        d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
                                    ></path>
                                </svg>
                            </button>

                            <button
                                type="button"
                                class="cc-tool-button"
                                id="classic-chatbot-reasoning"
                                title="Reasoning Mode"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path
                                        d="M9 18h6"
                                    ></path>

                                    <path
                                        d="M10 22h4"
                                    ></path>

                                    <path
                                        d="M15.1 14c.2-1 .6-1.7 1.4-2.5A6 6 0 1 0 7.5 11.5c.8.8 1.2 1.5 1.4 2.5h6.2z"
                                    ></path>
                                </svg>
                            </button>

                            <button
                                type="button"
                                class="cc-tool-button"
                                id="classic-chatbot-sync"
                                title="Sync Current Context"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <circle
                                        cx="12"
                                        cy="12"
                                        r="2"
                                    ></circle>

                                    <path
                                        d="M16.2 7.8a6 6 0 0 1 0 8.5"
                                    ></path>

                                    <path
                                        d="M7.8 16.2a6 6 0 0 1 0-8.5"
                                    ></path>
                                </svg>
                            </button>

                            <button
                                type="button"
                                class="cc-tool-button"
                                id="classic-chatbot-mic"
                                title="Voice Input"
                            >
                                <svg
                                    width="16"
                                    height="16"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path
                                        d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"
                                    ></path>

                                    <path
                                        d="M19 10v2a7 7 0 0 1-14 0v-2"
                                    ></path>

                                    <line
                                        x1="12"
                                        y1="19"
                                        x2="12"
                                        y2="23"
                                    ></line>
                                </svg>
                            </button>

                            <input
                                type="file"
                                id="classic-chatbot-file-input"
                                style="display:none"
                            >
                        </div>

                        <button
                            type="button"
                            id="classic-chatbot-send"
                            title="Send"
                        >
                            <svg
                                width="19"
                                height="19"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="3"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <line
                                    x1="12"
                                    y1="19"
                                    x2="12"
                                    y2="5"
                                ></line>

                                <polyline
                                    points="5 12 12 5 19 12"
                                ></polyline>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(
            launcher
        );

        document.body.appendChild(
            panel
        );

        updateContextUI();

        if (
            window.frappe &&
            frappe.router &&
            frappe.router.on
        ) {
            frappe.router.on(
                "change",
                function () {
                    setTimeout(
                        updateContextUI,
                        500
                    );
                }
            );
        }
    }

    function openBot() {
        var launcher =
            document.getElementById(
                "classic-chatbot-launcher"
            );

        var panel =
            document.getElementById(
                "classic-chatbot-panel"
            );

        if (
            !launcher ||
            !panel
        ) {
            return;
        }

        launcher.classList.add(
            "cc-hidden"
        );

        panel.classList.add(
            "cc-open"
        );

        updateContextUI();

        setTimeout(function () {
            var input =
                document.getElementById(
                    "classic-chatbot-input"
                );

            if (input) {
                input.focus();
            }
        }, 100);
    }

    function closeBot() {
        var launcher =
            document.getElementById(
                "classic-chatbot-launcher"
            );

        var panel =
            document.getElementById(
                "classic-chatbot-panel"
            );

        if (panel) {
            panel.classList.remove(
                "cc-open"
            );
        }

        setTimeout(function () {
            if (launcher) {
                launcher.classList.remove(
                    "cc-hidden"
                );
            }
        }, 200);
    }

    function clearChat() {
        chatHistory = [];

        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (!body) {
            return;
        }

        body.innerHTML = `
            <div class="cc-empty-state">
                <div class="cc-empty-title">
                    What can I help with?
                </div>

                <div class="cc-empty-subtitle">
                    Ask about the current form or ERP data.
                </div>
            </div>
        `;

        showToast(
            "Chat cleared"
        );
    }

    function removeEmptyState() {
        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (!body) {
            return;
        }

        var emptyState =
            body.querySelector(
                ".cc-empty-state"
            );

        if (emptyState) {
            emptyState.remove();
        }
    }

    function scrollChatToBottom() {
        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (body) {
            body.scrollTop =
                body.scrollHeight;
        }
    }

    function addUserMessage(text) {
        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (!body) {
            return;
        }

        removeEmptyState();

        body.insertAdjacentHTML(
            "beforeend",
            '<div class="cc-message cc-user-message">' +
                escapeHtml(text) +
            "</div>"
        );

        scrollChatToBottom();
    }

    function addBotMessage(
    text,
    modelBadge
) {
    var body =
        document.getElementById(
            "classic-chatbot-body"
        );

    if (!body) {
        return;
    }

    removeEmptyState();

    /*
     * Pehle complete model response escape karo.
     * parseMarkdown sirf limited safe markup generate karega.
     */
    var escapedText =
        escapeHtml(text || "");

    var html =
        parseMarkdown(escapedText);

    if (modelBadge) {
        html +=
            '<div class="cc-model-badge">' +
                escapeHtml(modelBadge) +
            "</div>";
    }

    body.insertAdjacentHTML(
        "beforeend",
        '<div class="cc-message cc-bot-message">' +
            html +
        "</div>"
    );

    scrollChatToBottom();
}

    function addSystemMessage(text) {
        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (!body) {
            return;
        }

        removeEmptyState();

        body.insertAdjacentHTML(
            "beforeend",
            '<div class="cc-system-message">' +
                escapeHtml(text) +
            "</div>"
        );

        scrollChatToBottom();
    }

    function showTyping() {
        var body =
            document.getElementById(
                "classic-chatbot-body"
            );

        if (
            !body ||
            document.getElementById(
                "classic-chatbot-typing"
            )
        ) {
            return;
        }

        removeEmptyState();

        body.insertAdjacentHTML(
            "beforeend",
            '<div id="classic-chatbot-typing" ' +
            'class="cc-message cc-bot-message">' +

                '<div class="cc-typing">' +
                    "<span></span>" +
                    "<span></span>" +
                    "<span></span>" +
                "</div>" +

            "</div>"
        );

        scrollChatToBottom();
    }

    function hideTyping() {
        var typing =
            document.getElementById(
                "classic-chatbot-typing"
            );

        if (typing) {
            typing.remove();
        }
    }

    function cleanDocumentData(documentData) {
        var output = {};

        if (!documentData) {
            return output;
        }

        Object.keys(
            documentData
        ).forEach(
            function (key) {
                if (
                    key.indexOf("_") === 0
                ) {
                    return;
                }

                var value =
                    documentData[key];

                if (
                    value === null ||
                    value === undefined ||
                    value === ""
                ) {
                    return;
                }

                if (Array.isArray(value)) {
                    var rows =
                        value.slice(0, 20)
                            .map(function (row) {
                                if (
                                    !row ||
                                    typeof row !== "object"
                                ) {
                                    return row;
                                }

                                var cleanRow = {};

                                Object.keys(row)
                                    .forEach(
                                        function (rowKey) {
                                            if (
                                                rowKey.indexOf(
                                                    "_"
                                                ) === 0
                                            ) {
                                                return;
                                            }

                                            if (
                                                [
                                                    "name",
                                                    "owner",
                                                    "creation",
                                                    "modified",
                                                    "modified_by",
                                                    "docstatus",
                                                    "doctype",
                                                    "parent",
                                                    "parentfield",
                                                    "parenttype"
                                                ].indexOf(
                                                    rowKey
                                                ) !== -1
                                            ) {
                                                return;
                                            }

                                            var rowValue =
                                                row[rowKey];

                                            if (
                                                rowValue === null ||
                                                rowValue === undefined ||
                                                rowValue === "" ||
                                                typeof rowValue === "object"
                                            ) {
                                                return;
                                            }

                                            cleanRow[
                                                rowKey
                                            ] = rowValue;
                                        }
                                    );

                                return cleanRow;
                            });

                    if (rows.length) {
                        output[key] = rows;
                    }

                    return;
                }

                if (
                    typeof value !== "object"
                ) {
                    output[key] = value;
                }
            }
        );

        return output;
    }

    function sendMessage(
        providedText
    ) {
        var input =
            document.getElementById(
                "classic-chatbot-input"
            );

        var rawMessage =
            providedText ||
            (
                input
                    ? input.value.trim()
                    : ""
            );

        if (!rawMessage) {
            return;
        }

        if (input) {
            input.value = "";
        }

        addUserMessage(
            rawMessage
        );

        showTyping();

        var context =
            getContext();

        var finalQuestion =
            rawMessage;

        if (webSearchActive) {
            finalQuestion =
                "[Web Search Mode] " +
                finalQuestion;
        }

        if (reasoningActive) {
            finalQuestion =
                "[Deep Reasoning Mode] " +
                finalQuestion;
        }

        if (
            lastError &&
            rawMessage
                .toLowerCase()
                .indexOf("error") !== -1
        ) {
            finalQuestion +=
                "\nRecent browser error: " +
                lastError;

            lastError = "";
        }

        var documentData =
            cleanDocumentData(
                context.doc
            );

        var modelSelect =
            document.getElementById(
                "classic-chatbot-model-select"
            );

        var selectedModel =
            modelSelect
                ? modelSelect.value
                : "local";

        frappe.call({
            method:
                "classic_chatbot.api.agent.ask",

            args: {
                question:
                    finalQuestion,

                doctype:
                    context.doctype,

                docname:
                    context.docname,

                doc:
                    JSON.stringify(
                        documentData
                    ),

                route:
                    JSON.stringify(
                        context.route || []
                    ),

                preferred_model:
                    selectedModel,

                history:
                    JSON.stringify(
                        chatHistory.slice(-8)
                    )
            },

            callback: function (response) {
                hideTyping();

                var result =
                    response &&
                    response.message
                        ? response.message
                        : {};

                var answer =
                    result.answer ||
                    "Server ne answer generate nahi kiya.";

                var tools =
                    Array.isArray(
                        result.tools_used
                    )
                        ? result.tools_used
                        : [];

                var badgeParts = [];

                if (result.model_used) {
                    badgeParts.push(
                        escapeHtml(
                            result.model_used
                        )
                    );
                }

                if (tools.length) {
                    badgeParts.push(
                        escapeHtml(
                            tools.join(", ")
                        )
                    );
                }

                addBotMessage(
                    answer,
                    badgeParts.join(" · ")
                );

                chatHistory.push({
                    role: "user",
                    content: rawMessage
                });

                chatHistory.push({
                    role: "assistant",
                    content: answer
                });

                if (
                    chatHistory.length > 16
                ) {
                    chatHistory =
                        chatHistory.slice(-16);
                }
            },

            error: function (error) {
                hideTyping();

                console.error(
                    "[Classic Chatbot] API error",
                    error
                );

                addBotMessage(
                    "Backend API connect nahi ho rahi. " +
                    "Ollama aur Frappe logs check karo."
                );
            }
        });
    }

    document.addEventListener(
        "click",
        function (event) {
            var launcher =
                event.target.closest(
                    "#classic-chatbot-launcher"
                );

            var close =
                event.target.closest(
                    "#classic-chatbot-close"
                );

            var clear =
                event.target.closest(
                    "#classic-chatbot-clear"
                );

            var send =
                event.target.closest(
                    "#classic-chatbot-send"
                );

            var quick =
                event.target.closest(
                    ".cc-quick-actions button"
                );

            var attach =
                event.target.closest(
                    "#classic-chatbot-attach"
                );

            var web =
                event.target.closest(
                    "#classic-chatbot-web"
                );

            var reasoning =
                event.target.closest(
                    "#classic-chatbot-reasoning"
                );

            var sync =
                event.target.closest(
                    "#classic-chatbot-sync"
                );

            var mic =
                event.target.closest(
                    "#classic-chatbot-mic"
                );

            if (launcher) {
                event.preventDefault();
                openBot();
                return;
            }

            if (close) {
                event.preventDefault();
                closeBot();
                return;
            }

            if (clear) {
                event.preventDefault();
                clearChat();
                return;
            }

            if (send) {
                event.preventDefault();
                sendMessage();
                return;
            }

            if (quick) {
                event.preventDefault();

                sendMessage(
                    quick.getAttribute(
                        "data-question"
                    )
                );

                return;
            }

            if (attach) {
                event.preventDefault();

                var fileInput =
                    document.getElementById(
                        "classic-chatbot-file-input"
                    );

                if (fileInput) {
                    fileInput.click();
                }

                return;
            }

            if (web) {
                event.preventDefault();

                webSearchActive =
                    !webSearchActive;

                web.classList.toggle(
                    "cc-active",
                    webSearchActive
                );

                showToast(
                    webSearchActive
                        ? "Web search enabled"
                        : "Web search disabled"
                );

                return;
            }

            if (reasoning) {
                event.preventDefault();

                reasoningActive =
                    !reasoningActive;

                reasoning.classList.toggle(
                    "cc-active",
                    reasoningActive
                );

                showToast(
                    reasoningActive
                        ? "Reasoning mode enabled"
                        : "Reasoning mode disabled"
                );

                return;
            }

            if (sync) {
                event.preventDefault();

                updateContextUI();

                addSystemMessage(
                    "Current ERP context synced."
                );

                showToast(
                    "Context synced"
                );

                return;
            }

            if (mic) {
                event.preventDefault();

                startDictation(mic);
            }
        }
    );

    document.addEventListener(
        "change",
        function (event) {
            if (
                !event.target ||
                event.target.id !==
                    "classic-chatbot-file-input"
            ) {
                return;
            }

            var files =
                event.target.files || [];

            if (!files.length) {
                return;
            }

            var file =
                files[0];

            var input =
                document.getElementById(
                    "classic-chatbot-input"
                );

            if (input) {
                input.value =
                    (
                        "[Attached file: " +
                        file.name +
                        "] " +
                        input.value
                    ).trim();

                input.focus();
            }

            showToast(
                "File selected: " +
                file.name
            );

            event.target.value = "";
        }
    );

    document.addEventListener(
        "keydown",
        function (event) {
            if (
                event.target &&
                event.target.id ===
                    "classic-chatbot-input" &&
                event.key === "Enter"
            ) {
                event.preventDefault();
                sendMessage();
            }
        }
    );

    window.addEventListener(
        "error",
        function (event) {
            lastError =
                event.message || "";
        }
    );

    window.addEventListener(
        "unhandledrejection",
        function (event) {
            lastError =
                event.reason
                    ? String(event.reason)
                    : "";
        }
    );

    function initialize() {
        mountBot();

        console.log(
            "[Classic Chatbot] UI loaded successfully"
        );
    }

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            initialize
        );
    } else {
        initialize();
    }
})();




























/* ============================================================
   REMOVE ONLY LEGACY FORM VALIDATION AVATAR
   New AI validator and chatbot will continue working.
   ============================================================ */

(function removeLegacyFormValidationAvatar() {
    "use strict";

    var LEGACY_SELECTORS = [
        "#classic-error-avatar",
        "#classic-validation-avatar",
        "#classic-form-validation-avatar",
        ".classic-error-avatar",
        ".classic-validation-avatar",
        ".classic-form-validation-avatar",
        ".cea-avatar",
        ".cea-wrapper",
        ".classic-avatar-wrapper"
    ];

    function removeBySelector() {
        LEGACY_SELECTORS.forEach(function (selector) {
            document
                .querySelectorAll(selector)
                .forEach(function (element) {
                    /*
                     * New validator ko remove nahi karna.
                     */
                    if (
                        element.id ===
                        "classic-ai-validation-avatar"
                    ) {
                        return;
                    }

                    element.remove();
                });
        });
    }

    function removeByContent() {
        document
            .querySelectorAll(
                "body > div, body > section"
            )
            .forEach(function (element) {
                if (
                    !element ||
                    element.id ===
                        "classic-ai-validation-avatar" ||
                    element.id ===
                        "classic-chatbot-panel" ||
                    element.id ===
                        "classic-chatbot-launcher"
                ) {
                    return;
                }

                var text = String(
                    element.innerText || ""
                ).trim();

                var containsOldHeading =
                    text.indexOf(
                        "FORM VALIDATION"
                    ) !== -1;

                var containsOldButtons =
                    text.indexOf(
                        "Show Field"
                    ) !== -1 &&
                    (
                        text.indexOf(
                            "Ask Chatbot"
                        ) !== -1 ||
                        text.indexOf(
                            "Ask AI"
                        ) !== -1
                    );

                if (
                    containsOldHeading &&
                    containsOldButtons
                ) {
                    element.remove();
                }
            });
    }

    function removeLegacyAvatar() {
        removeBySelector();
        removeByContent();
    }

    /*
     * Remove immediately.
     */
    removeLegacyAvatar();

    /*
     * Old JavaScript may recreate the avatar after form refresh.
     * Observer removes only that legacy avatar again.
     */
    var observer = new MutationObserver(
        function () {
            removeLegacyAvatar();
        }
    );

    function startObserver() {
        if (!document.body) {
            setTimeout(
                startObserver,
                200
            );
            return;
        }

        observer.observe(
            document.body,
            {
                childList: true,
                subtree: true
            }
        );

        removeLegacyAvatar();
    }

    startObserver();

    /*
     * Also remove after Frappe route/form changes.
     */
    document.addEventListener(
        "form-refresh",
        function () {
            setTimeout(
                removeLegacyAvatar,
                100
            );
        }
    );

    if (
        window.frappe &&
        frappe.router &&
        frappe.router.on
    ) {
        frappe.router.on(
            "change",
            function () {
                setTimeout(
                    removeLegacyAvatar,
                    300
                );
            }
        );
    }

    window.removeLegacyFormValidationAvatar =
        removeLegacyAvatar;
})();