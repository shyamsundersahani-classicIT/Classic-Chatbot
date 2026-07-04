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



(function () {
    console.log("[Classic Chatbot v8.0] Loaded with Premium UI, Markdown & Smart Automation");

    var last_error = "";

    function esc(text) {
        if (text === undefined || text === null) return "";
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // --- ADVANCED MARKDOWN PARSER (For Tables, Bold, Code) ---
    function parseMarkdown(text) {
        let html = text;
        
        // 1. Code Blocks
        html = html.replace(/```([\s\S]*?)```/g, '<pre style="background:#1e293b; color:#e2e8f0; padding:12px; border-radius:8px; overflow-x:auto; font-size:12px; margin: 10px 0;"><code>$1</code></pre>');
        // 2. Inline Code
        html = html.replace(/`([^`]+)`/g, '<code style="background:#f1f5f9; color:#e11d48; padding:2px 6px; border-radius:4px; font-size:13px; font-weight:600;">$1</code>');
        // 3. Bold Text
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // 4. Tables (Critical for ERP Data)
        html = html.replace(/(?:\|.*?\|[\r\n]+)+/g, function(match) {
            let rows = match.trim().split('\n');
            let table = '<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; margin:10px 0; font-size:13px; border-radius:8px; overflow:hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05);"><tbody>';
            rows.forEach((row, i) => {
                if (row.includes('---')) return; // Skip separator line
                let cols = row.split('|').filter(c => c.trim() !== '');
                table += '<tr>';
                cols.forEach(col => {
                    let cell = i === 0 ? 'th' : 'td';
                    let style = i === 0 ? 'border:1px solid #e2e8f0; padding:10px; background:#f8fafc; text-align:left; color:#334155;' : 'border:1px solid #e2e8f0; padding:10px; color:#475569;';
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
        try { route = frappe.get_route ? frappe.get_route() : []; } catch (e) {}
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

    function injectStyle() {
        if (document.getElementById("classic-chatbot-style-v8")) return;
        var style = document.createElement("style");
        style.id = "classic-chatbot-style-v8";
        style.innerHTML = `
            /* Custom Scrollbar for Premium Feel */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

            #classic-chatbot-launcher { position: fixed; right: 28px; bottom: 28px; width: 64px; height: 64px; border-radius: 50%; border: none; background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; font-size: 28px; z-index: 999999; cursor: pointer; box-shadow: 0 12px 30px rgba(79,70,229,.4); transition: all .3s cubic-bezier(0.4, 0, 0.2, 1); display: flex; align-items: center; justify-content: center; }
            #classic-chatbot-launcher:hover { transform: translateY(-5px) scale(1.05); box-shadow: 0 20px 40px rgba(79,70,229,.5); }
            #classic-chatbot-launcher.cc-hide { opacity: 0; pointer-events: none; transform: scale(.5) translateY(20px); }
            
            #classic-chatbot-panel { position: fixed; right: 28px; bottom: 105px; width: 420px; height: 650px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5); border-radius: 24px; z-index: 999999; box-shadow: 0 25px 80px rgba(0,0,0,.15); display: flex; flex-direction: column; overflow: hidden; opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(40px) scale(.95); transform-origin: bottom right; transition: all .4s cubic-bezier(0.16, 1, 0.3, 1); }
            #classic-chatbot-panel.cc-open { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0) scale(1); }
            
            .cc-head { background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; padding: 20px; position: relative; flex-shrink: 0; }
            .cc-title { font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
            .cc-status { font-size: 12px; font-weight: 500; opacity: 0.9; margin-top: 4px; display: flex; align-items: center; gap: 6px; }
            .cc-status-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #22c55e; }
            
            .cc-actions { position: absolute; right: 15px; top: 15px; display: flex; gap: 8px; }
            .cc-icon-btn { background: rgba(255,255,255,0.2); border: none; color: white; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; transition: all .2s ease; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
            .cc-icon-btn:hover { background: rgba(255,255,255,0.4); transform: scale(1.1); }
            
            #classic-chatbot-model-select { margin-top: 12px; background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 8px; padding: 6px 10px; font-size: 12px; width: 100%; outline: none; cursor: pointer; }
            #classic-chatbot-model-select option { color: #333; }

            #classic-chatbot-body { flex: 1; padding: 20px; overflow-y: auto; scroll-behavior: smooth; background: #f8fafc; }
            .cc-bot-msg, .cc-user-msg { padding: 12px 16px; border-radius: 16px; margin-bottom: 16px; font-size: 14px; line-height: 1.5; word-wrap: break-word; animation: ccMsgIn .3s ease forwards; opacity: 0; transform: translateY(10px); }
            
            .cc-bot-msg { background: white; color: #334155; border: 1px solid #e2e8f0; border-bottom-left-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); max-width: 90%; }
            .cc-user-msg { background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; border-bottom-right-radius: 4px; box-shadow: 0 4px 15px rgba(79,70,229,0.2); margin-left: auto; max-width: 85%; }
            .cc-sys-msg { text-align: center; color: #64748b; font-size: 12px; margin-bottom: 16px; font-weight: 500; animation: ccMsgIn .3s ease forwards; }
            
            /* Quick Actions (Smart Chips) */
            .cc-quick-wrap { padding: 12px 15px; background: white; border-top: 1px solid #e2e8f0; flex-shrink: 0; }
            .cc-quick { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; }
            .cc-quick button { flex-shrink: 0; background: #f1f5f9; border: 1px solid #cbd5e1; color: #475569; border-radius: 16px; padding: 6px 14px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
            .cc-quick button:hover { background: #e0e7ff; border-color: #818cf8; color: #4f46e5; }
            
            .cc-foot { padding: 15px; background: white; border-top: 1px solid #e2e8f0; display: flex; gap: 10px; align-items: center; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px;}
            #classic-chatbot-input { flex: 1; height: 44px; border: 1px solid #cbd5e1; border-radius: 22px; padding: 0 16px; font-size: 14px; transition: all 0.2s; outline: none; background: #f8fafc; }
            #classic-chatbot-input:focus { border-color: #818cf8; background: white; box-shadow: 0 0 0 3px rgba(79,70,229,0.1); }
            #classic-chatbot-send { width: 44px; height: 44px; border-radius: 50%; border: none; background: #4f46e5; color: white; font-size: 18px; cursor: pointer; transition: all .2s; display: flex; align-items: center; justify-content: center; }
            #classic-chatbot-send:hover { background: #4338ca; transform: scale(1.05); }
            
            .cc-typing { display: flex; gap: 4px; padding: 4px 0; }
            .cc-typing span { width: 6px; height: 6px; border-radius: 50%; background: #94a3b8; animation: ccTyping 1.4s infinite ease-in-out both; }
            .cc-typing span:nth-child(1) { animation-delay: -0.32s; }
            .cc-typing span:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes ccMsgIn { to { opacity: 1; transform: translateY(0); } }
            @keyframes ccTyping { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
        `;
        document.head.appendChild(style);
    }

    function updateContextUI() {
        var ctx = getContext();
        var statusEl = document.getElementById("cc-context-status");
        var quickDiv = document.querySelector(".cc-quick");
        
        if (!statusEl || !quickDiv) return;

        if (ctx.doctype) {
            statusEl.innerHTML = `<span class="cc-status-dot"></span> Active on: <b>${ctx.doctype}</b>`;
            // AUTOMATION: Smart buttons based on Route
            quickDiv.innerHTML = `
                <button type="button" data-q="Is ${ctx.doctype} form ke mandatory fields kya hain?">Missing Fields?</button>
                <button type="button" data-q="Ye ${ctx.doctype} ERP me kya kaam aata hai?">What is this?</button>
                <button type="button" data-q="Is DocType ke liye ek custom script likh do">Write Script</button>
            `;
        } else {
            statusEl.innerHTML = `<span class="cc-status-dot"></span> Online & Ready`;
            quickDiv.innerHTML = `
                <button type="button" data-q="Manufacturing me kya features hain?">Manufacturing</button>
                <button type="button" data-q="Pukhraj / Sapphire ki stock valuation kaise hoti hai?">Stock Value</button>
                <button type="button" data-q="Mujhe Frappe custom script likhni hai">Code Help</button>
            `;
        }
    }

    function mountBot() {
        if (document.getElementById("classic-chatbot-launcher")) return;
        injectStyle();

        var launcher = document.createElement("button");
        launcher.id = "classic-chatbot-launcher";
        launcher.innerHTML = `<svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path></svg>`;

        var panel = document.createElement("div");
        panel.id = "classic-chatbot-panel";

        panel.innerHTML = `
            <div class="cc-head">
                <div class="cc-actions">
                    <button class="cc-icon-btn" id="classic-chatbot-refresh" title="Clear Chat">🔄</button>
                    <button class="cc-icon-btn" id="classic-chatbot-close" title="Close">✕</button>
                </div>
                <div class="cc-title">🤖 Classic AI Agent</div>
                <div class="cc-status" id="cc-context-status"><span class="cc-status-dot"></span> Online & Ready</div>
                <select id="classic-chatbot-model-select" title="Routing Engine">
                    <option value="auto">⚡ Multi-Agent Auto Router</option>
                    <option value="claude">💻 Coder (Claude 3.5)</option>
                    <option value="gpt">📊 Consultant (GPT-4o)</option>
                </select>
            </div>
            <div id="classic-chatbot-body">
                <div class="cc-bot-msg">Hello, User's me apki kya sahayta kar skta hun </div>
            </div>
            <div class="cc-quick-wrap"><div class="cc-quick"></div></div>
            <div class="cc-foot">
                <input id="classic-chatbot-input" placeholder="Ask anything about Frappe/ERPNext..." autocomplete="off" />
                <button id="classic-chatbot-send" type="button">➤</button>
            </div>
        `;

        document.body.appendChild(launcher);
        document.body.appendChild(panel);
        updateContextUI();

        // SMART AUTOMATION: Update buttons & greet when changing screens
        if (window.frappe && frappe.router) {
            frappe.router.on('change', function() {
                setTimeout(function() { 
                    updateContextUI();
                    var ctx = getContext();
                    var body = document.getElementById("classic-chatbot-body");
                    if (body && ctx.doctype && !body.innerHTML.includes(`Switched to <b>${ctx.doctype}</b>`)) {
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
        setTimeout(() => { document.getElementById("classic-chatbot-input").focus(); }, 100);
        updateContextUI(); // Refresh state on open
    }

    function closeBot() {
        document.getElementById("classic-chatbot-panel").classList.remove("cc-open");
        setTimeout(() => { document.getElementById("classic-chatbot-launcher").classList.remove("cc-hide"); }, 200);
    }

    function addUserMessage(text) {
        var body = document.getElementById("classic-chatbot-body");
        body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + '</div>');
        body.scrollTop = body.scrollHeight;
    }

    function addBotMessage(text, rawHTML) {
        var body = document.getElementById("classic-chatbot-body");
        // Apply Markdown Parsing!
        var finalHTML = parseMarkdown(esc(text));
        if (rawHTML) finalHTML += rawHTML;
        
        body.insertAdjacentHTML("beforeend", '<div class="cc-bot-msg">' + finalHTML + '</div>');
        body.scrollTop = body.scrollHeight;
    }

    function showTyping() {
        var body = document.getElementById("classic-chatbot-body");
        if (document.getElementById("classic-chatbot-typing")) return;
        body.insertAdjacentHTML("beforeend", '<div id="classic-chatbot-typing" class="cc-bot-msg"><div class="cc-typing"><span></span><span></span><span></span></div></div>');
        body.scrollTop = body.scrollHeight;
    }

    function hideTyping() {
        var t = document.getElementById("classic-chatbot-typing");
        if (t) t.remove();
    }

    function sendMessage(quickText) {
        var input = document.getElementById("classic-chatbot-input");
        var msg = quickText || (input ? input.value.trim() : "");
        if (!msg) return;
        if (input) input.value = "";

        addUserMessage(msg);
        showTyping();

        var ctx = getContext();

        // AUTOMATION: Catch UI errors before sending
        if (last_error && msg.toLowerCase().includes("error")) {
            msg += "\n(Recent UI Error Logged: " + last_error + ")";
            last_error = ""; // Clear after sending
        }

        var safeDocData = {};
        if (ctx.doc) {
            Object.keys(ctx.doc).forEach(function(key) {
                if (!key.startsWith("_") && typeof ctx.doc[key] !== "object") {
                    safeDocData[key] = ctx.doc[key];
                }
            });
        }

        frappe.call({
            method: "classic_chatbot.api.agent.ask", 
            args: {
                question: msg,
                doctype: ctx.doctype,
                docname: ctx.docname,
                doc: JSON.stringify(safeDocData), 
                route: JSON.stringify(ctx.route || []),
                preferred_model: document.getElementById("classic-chatbot-model-select").value 
            },
            callback: function (r) {
                hideTyping();
                var answer = "Server ne answer generate nahi kiya.";
                var badge = ""; 
                if (r && r.message) {
                    if (r.message.answer) answer = r.message.answer;
                    if (r.message.model_used) {
                        badge = `<div style="font-size: 10px; color: #64748b; margin-top: 8px; text-align: right; border-top: 1px solid #e2e8f0; padding-top: 6px;">Served by: <b>${r.message.model_used}</b></div>`;
                    }
                }
                addBotMessage(answer, badge);
            },
            error: function () {
                hideTyping();
                addBotMessage("⚠️ API Server disconnect ho gaya. Kripya apna internet ya terminal check karein.");
            }
        });
    }

    document.addEventListener("click", function (e) {
        var launcher = e.target.closest("#classic-chatbot-launcher");
        var close = e.target.closest("#classic-chatbot-close");
        var refresh = e.target.closest("#classic-chatbot-refresh");
        var send = e.target.closest("#classic-chatbot-send");
        var quick = e.target.closest(".cc-quick button");

        if (launcher) { e.preventDefault(); openBot(); }
        else if (close) { e.preventDefault(); closeBot(); }
        else if (refresh) {
            e.preventDefault();
            document.getElementById("classic-chatbot-body").innerHTML = '<div class="cc-sys-msg">Memory Cleared ✨</div><div class="cc-bot-msg">Chat refresh ho gayi hai. Naya sawal poocho.</div>';
        }
        else if (send) { e.preventDefault(); sendMessage(); }
        else if (quick) { e.preventDefault(); sendMessage(quick.getAttribute("data-q")); }
    });

    document.addEventListener("keydown", function (e) {
        if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
            e.preventDefault(); sendMessage();
        }
    });

    // Auto-capture UI Errors silently
    window.addEventListener("error", function (e) { last_error = e.message || ""; });
    window.addEventListener("unhandledrejection", function (e) { last_error = e.reason ? String(e.reason) : ""; });

    if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", mountBot); } 
    else { mountBot(); }
})();