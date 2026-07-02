(function () {
    console.log("[Classic Chatbot v6.1] Loaded with Dynamic SPA Context Fix");

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

    function getContext() {
        var route = [];
        try { route = frappe.get_route ? frappe.get_route() : []; } catch (e) {}
        var ctx = { route: route, doctype: null, docname: null, doc: null };
        
        if (route && route[0] === "Form") {
            ctx.doctype = route[1];
            ctx.docname = route[2];
            // FIX: Ensure cur_frm is perfectly synced with the current route
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
        if (document.getElementById("classic-chatbot-style-v6")) return;
        var style = document.createElement("style");
        style.id = "classic-chatbot-style-v6";
        style.innerHTML = `
            #classic-chatbot-launcher { position: fixed; right: 28px; bottom: 28px; width: 72px; height: 72px; border-radius: 50%; border: none; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; font-size: 32px; z-index: 999999; cursor: pointer; box-shadow: 0 18px 45px rgba(124,77,255,.45); transition: transform .3s ease; animation: ccPulse 2s infinite; }
            #classic-chatbot-launcher:hover { transform: scale(1.08) rotate(4deg); }
            #classic-chatbot-launcher.cc-hide { opacity: 0; pointer-events: none; transform: scale(.35) rotate(15deg); }
            #classic-chatbot-panel { position: fixed; right: 24px; bottom: 24px; width: 430px; height: 650px; background: white; border-radius: 30px; z-index: 999999; box-shadow: 0 30px 90px rgba(0,0,0,.28); overflow: hidden; opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(55px) scale(.78); transform-origin: bottom right; transition: all .35s ease; }
            #classic-chatbot-panel.cc-open { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0) scale(1); }
            
            .cc-head { height: 110px; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; padding: 20px; font-size: 24px; font-weight: 800; position: relative; }
            
            #classic-chatbot-close { float: right; border: none; background: rgba(255,255,255,.25); color: white; border-radius: 50%; width: 36px; height: 36px; font-size: 22px; cursor: pointer; transition: transform .25s ease; margin-left: 8px; }
            #classic-chatbot-close:hover { transform: rotate(90deg); }
            
            #classic-chatbot-refresh { float: right; border: none; background: rgba(255,255,255,.25); color: white; border-radius: 50%; width: 36px; height: 36px; font-size: 16px; cursor: pointer; transition: transform .4s ease; margin-left: 8px; }
            #classic-chatbot-refresh:hover { transform: rotate(-180deg); background: rgba(255,255,255,.4); }

            #classic-chatbot-model-select { float: right; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.4); border-radius: 12px; padding: 6px 10px; font-size: 12px; font-weight: 600; outline: none; cursor: pointer; appearance: none; -webkit-appearance: none; }
            #classic-chatbot-model-select option { color: #333; font-weight: 500; }
            #classic-chatbot-model-select:hover { background: rgba(255,255,255,0.3); }

            #classic-chatbot-body { height: 410px; padding: 20px; background: linear-gradient(180deg,#f8f9ff,#eef2ff); overflow-y: auto; scroll-behavior: smooth; }
            .cc-bot-msg { background: white; padding: 14px 16px; border-radius: 18px; box-shadow: 0 8px 24px rgba(0,0,0,.08); margin-bottom: 12px; color: #263248; line-height: 1.5; animation: ccMsgIn .25s ease; word-wrap: break-word;}
            .cc-user-msg { background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; padding: 14px 16px; border-radius: 18px; margin-left: auto; margin-bottom: 12px; max-width: 82%; line-height: 1.5; animation: ccMsgIn .25s ease; word-wrap: break-word;}
            .cc-sys-msg { background: #eef2ff; color: #4f46e5; border-left: 4px solid #4f46e5; padding: 10px; font-size: 13px; margin-bottom: 12px; border-radius: 8px; animation: ccMsgIn .25s ease; }
            .cc-quick { display: flex; gap: 8px; padding: 10px 16px; background: white; border-top: 1px solid #eee; }
            .cc-quick button { border: 1px solid #ddd6fe; background: #faf5ff; color: #5b21b6; border-radius: 20px; padding: 7px 11px; font-size: 12px; cursor: pointer; }
            .cc-foot { padding: 15px; display: flex; gap: 10px; border-top: 1px solid #eee; background: white; }
            #classic-chatbot-input { flex: 1; height: 48px; border: 1px solid #ddd; border-radius: 24px; padding: 0 16px; outline: none; }
            #classic-chatbot-input:focus { border-color: #8b5cf6; box-shadow: 0 0 0 4px rgba(139,92,246,.12); }
            #classic-chatbot-send { width: 52px; height: 52px; border-radius: 50%; border: none; background: linear-gradient(135deg,#5b3df5,#b36cff); color: white; font-size: 22px; cursor: pointer; transition: transform .2s ease; }
            #classic-chatbot-send:hover { transform: scale(1.08); }
            .cc-typing span { display: inline-block; width: 7px; height: 7px; margin: 0 2px; border-radius: 50%; background: #8b5cf6; animation: ccTyping 1s infinite ease-in-out; }
            .cc-typing span:nth-child(2) { animation-delay: .15s; }
            .cc-typing span:nth-child(3) { animation-delay: .3s; }
            @keyframes ccPulse { 0% { box-shadow: 0 0 0 0 rgba(124,77,255,.42); } 70% { box-shadow: 0 0 0 14px rgba(124,77,255,0); } 100% { box-shadow: 0 0 0 0 rgba(124,77,255,0); } }
            @keyframes ccMsgIn { from { opacity: 0; transform: translateY(8px) scale(.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
            @keyframes ccTyping { 0%,80%,100% { transform: scale(.6); opacity: .45; } 40% { transform: scale(1); opacity: 1; } }
        `;
        document.head.appendChild(style);
    }

    function mountBot() {
        if (document.getElementById("classic-chatbot-launcher")) return;
        injectStyle();

        var launcher = document.createElement("button");
        launcher.id = "classic-chatbot-launcher";
        launcher.type = "button";
        launcher.innerHTML = "🤖";

        var panel = document.createElement("div");
        panel.id = "classic-chatbot-panel";

        panel.innerHTML =
            '<div class="cc-head">' +
                '🤖 Classic Chatbot' +
                '<button id="classic-chatbot-close" type="button" title="Close">×</button>' +
                '<button id="classic-chatbot-refresh" type="button" title="Clear Chat">🔄</button>' +
                '<select id="classic-chatbot-model-select" title="Switch Model">' +
                    '<option value="auto">🤖 Auto (Local First)</option>' +
                    '<option value="groq">☁️ Groq (Fast & Paid)</option>' +
                    '<option value="local">🖥️ Local (Strict Free)</option>' +
                '</select>' +
                '<div style="font-size:14px;font-weight:400;margin-top:6px;">● Agent Mode</div>' +
            '</div>' +
            '<div id="classic-chatbot-body">' +
                '<div class="cc-bot-msg">Hello 👋 Model Switcher active hai. Kaise help karu?</div>' +
            '</div>' +
            '<div class="cc-quick">' +
                '<button type="button" data-q="current form me kya missing hai?">Missing?</button>' +
                '<button type="button" data-q="is form ke mandatory fields kya hain?">Mandatory</button>' +
                '<button type="button" data-q="is error ka solution batao">Error Fix</button>' +
            '</div>' +
            '<div class="cc-foot">' +
                '<input id="classic-chatbot-input" placeholder="Ask ERPNext issue..." autocomplete="off" />' +
                '<button id="classic-chatbot-send" type="button">➤</button>' +
            '</div>';

        document.body.appendChild(launcher);
        document.body.appendChild(panel);

        // NAYA FIX: Frappe SPA Route Change Listener
        if (window.frappe && frappe.router) {
            frappe.router.on('change', function() {
                setTimeout(function() { // Halka sa delay taaki route puri tarah set ho jaye
                    var newCtx = getContext();
                    var body = document.getElementById("classic-chatbot-body");
                    if (body && newCtx.doctype) {
                        body.insertAdjacentHTML("beforeend", `<div class="cc-sys-msg">🔄 Switched to <b>${newCtx.doctype}</b>. Chatbot context is updated.</div>`);
                        body.scrollTop = body.scrollHeight;
                    }
                }, 500);
            });
        }
    }

    function openBot() {
        var launcher = document.getElementById("classic-chatbot-launcher");
        var panel = document.getElementById("classic-chatbot-panel");
        if (!launcher || !panel) return;
        launcher.classList.add("cc-hide");
        requestAnimationFrame(function () { panel.classList.add("cc-open"); });
        setTimeout(function () {
            var input = document.getElementById("classic-chatbot-input");
            if (input) input.focus();
        }, 350);
    }

    function closeBot() {
        var launcher = document.getElementById("classic-chatbot-launcher");
        var panel = document.getElementById("classic-chatbot-panel");
        if (!launcher || !panel) return;
        panel.classList.remove("cc-open");
        setTimeout(function () { launcher.classList.remove("cc-hide"); }, 260);
    }

    function addUserMessage(text) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;
        body.insertAdjacentHTML("beforeend", '<div class="cc-user-msg">' + esc(text) + '</div>');
        body.scrollTop = body.scrollHeight;
    }

    function addBotMessage(text, rawHTML) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;
        
        // Syntax fix: Removed double backslash for newlines
        var finalHTML = esc(text).replace(/\n/g, "<br>");
        if (rawHTML) {
            finalHTML += rawHTML;
        }
        
        body.insertAdjacentHTML("beforeend", '<div class="cc-bot-msg">' + finalHTML + '</div>');
        body.scrollTop = body.scrollHeight;
    }

    function showTyping() {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;
        if (document.getElementById("classic-chatbot-typing")) return;
        body.insertAdjacentHTML(
            "beforeend",
            '<div id="classic-chatbot-typing" class="cc-bot-msg"><span class="cc-typing"><span></span><span></span><span></span></span></div>'
        );
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

        var modelSelect = document.getElementById("classic-chatbot-model-select");
        var preferredModel = modelSelect ? modelSelect.value : "auto";

        addUserMessage(msg);
        showTyping();

        var ctx = getContext();

        if (!window.frappe || !frappe.call) {
            setTimeout(function () {
                hideTyping();
                addBotMessage("Frappe API available nahi hai.");
            }, 400);
            return;
        }

        // NAYA FIX: Dynamic form data copying taaki bot pura form samajh sake
        var safeDocData = {};
        if (ctx.doc) {
            Object.keys(ctx.doc).forEach(function(key) {
                // Ignore heavy objects/arrays aur internal metadata (jo '_' se shuru hote hain)
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
                error: last_error || "",
                preferred_model: preferredModel 
            },
            callback: function (r) {
                hideTyping();
                var answer = "Message sent, but no response received.";
                var modelBadge = ""; 

                if (r && r.message) {
                    if (r.message.answer) answer = r.message.answer;
                    if (r.message.model_used) {
                        var badgeColor = r.message.model_used.includes("Groq") ? "#f59e0b" : "#10b981";
                        modelBadge = `<div style="font-size: 10px; color: ${badgeColor}; margin-top: 8px; text-align: right; font-weight: 700; border-top: 1px solid #eee; padding-top: 4px;">${r.message.model_used}</div>`;
                    }
                }
                addBotMessage(answer, modelBadge);
            },
            error: function (err) {
                hideTyping();
                addBotMessage("API error aa gaya. Bench terminal check karo.");
            }
        });
    }

    document.addEventListener("click", function (e) {
        var launcher = e.target.closest("#classic-chatbot-launcher");
        var close = e.target.closest("#classic-chatbot-close");
        var refresh = e.target.closest("#classic-chatbot-refresh");
        var send = e.target.closest("#classic-chatbot-send");
        var quick = e.target.closest(".cc-quick button");

        if (launcher) { e.preventDefault(); e.stopPropagation(); openBot(); return; }
        if (close) { e.preventDefault(); e.stopPropagation(); closeBot(); return; }
        if (refresh) {
            e.preventDefault(); e.stopPropagation();
            var body = document.getElementById("classic-chatbot-body");
            if (body) body.innerHTML = '<div class="cc-bot-msg">Chat refresh ho gayi hai 🔄<br>Naya sawal poocho.</div>';
            return;
        }
        if (send) { e.preventDefault(); e.stopPropagation(); sendMessage(); return; }
        if (quick) { e.preventDefault(); e.stopPropagation(); sendMessage(quick.getAttribute("data-q")); return; }
    }, true);

    document.addEventListener("keydown", function (e) {
        if (e.target && e.target.id === "classic-chatbot-input" && e.key === "Enter") {
            e.preventDefault(); sendMessage();
        }
    }, true);

    window.addEventListener("error", function (event) { last_error = event.message || ""; });
    window.addEventListener("unhandledrejection", function (event) { last_error = event.reason ? String(event.reason) : ""; });

    if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", mountBot); } 
    else { mountBot(); }
    setTimeout(mountBot, 1000);
})();