(function () {
    console.log("[Classic Chatbot] Force Loading ChatGPT Dark UI (Transparent) + Functional Tools 🌙");

    var last_error = "";
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
                        <option value="auto" selected>Auto</option>
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

    function sendMessage(quickText) {
        var input = document.getElementById("classic-chatbot-input");
        var rawMsg = quickText || (input ? input.value.trim() : "");

        if (!rawMsg) return;
        if (input) input.value = "";

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
        var preferredModel = modelSelect ? modelSelect.value : "auto";

        var args = {
            question: finalQuestion, // Sending modified question
            doctype: ctx.doctype,
            docname: ctx.docname,
            doc: JSON.stringify(safeDocData),
            route: JSON.stringify(ctx.route || []),
            preferred_model: preferredModel,
            history: JSON.stringify(chat_history.slice(-6))
        };

        function renderBotResponse(m) {
            hideTyping();

            var answer = "Server ne answer generate nahi kiya.";
            var badge = "";

            if (m) {
                if (m.answer) {
                    answer = m.answer;
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

        frappe.call({
            method: "classic_chatbot.api.agent.ask",
            args: args,
            callback: function (r) {
                renderBotResponse(r && r.message);
            },
            error: showFailure
        });
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
























