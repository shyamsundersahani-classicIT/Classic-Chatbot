(function () {
    console.log("[Classic Chatbot v2] Loaded");

    var VERSION = "classic-chatbot-v2";
    var last_error = "";

    function removeOldBot() {
        var oldLauncher = document.getElementById("classic-chatbot-launcher");
        var oldPanel = document.getElementById("classic-chatbot-panel");
        var oldStyle = document.getElementById("classic-chatbot-style-v2");

        if (oldLauncher) oldLauncher.remove();
        if (oldPanel) oldPanel.remove();
        if (oldStyle) oldStyle.remove();
    }

    function escapeHtml(text) {
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

        try {
            route = window.frappe && frappe.get_route ? frappe.get_route() : [];
        } catch (e) {
            route = [];
        }

        var ctx = {
            route: route,
            doctype: null,
            docname: null,
            doc: null
        };

        if (route && route[0] === "Form") {
            ctx.doctype = route[1];
            ctx.docname = route[2];

            if (window.cur_frm && cur_frm.doc) {
                ctx.doc = cur_frm.doc;
            }
        }

        if (route && route[0] === "List") {
            ctx.doctype = route[1];
        }

        return ctx;
    }

    function injectStyle() {
        var style = document.createElement("style");
        style.id = "classic-chatbot-style-v2";

        style.innerHTML = `
            #classic-chatbot-launcher {
                position: fixed;
                right: 28px;
                bottom: 28px;
                width: 72px;
                height: 72px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #4f46e5, #8b5cf6, #c084fc);
                color: white;
                font-size: 34px;
                z-index: 999999;
                cursor: pointer;
                box-shadow: 0 18px 45px rgba(124, 77, 255, 0.45);
                opacity: 1;
                transform: scale(1);
                transition: opacity 0.25s ease, transform 0.28s ease, box-shadow 0.25s ease;
                animation: classicBotPulse 2.2s infinite;
            }

            #classic-chatbot-launcher:hover {
                transform: scale(1.08) rotate(4deg);
                box-shadow: 0 22px 55px rgba(124, 77, 255, 0.65);
            }

            #classic-chatbot-launcher.cc-hide {
                opacity: 0;
                pointer-events: none;
                transform: scale(0.45) rotate(18deg);
            }

            #classic-chatbot-panel {
                position: fixed;
                right: 24px;
                bottom: 24px;
                width: 430px;
                height: 650px;
                background: white;
                border-radius: 30px;
                z-index: 999999;
                overflow: hidden;
                box-shadow: 0 30px 90px rgba(15, 23, 42, 0.28);
                font-family: Inter, Arial, sans-serif;

                opacity: 0;
                visibility: hidden;
                pointer-events: none;
                transform: translateY(50px) scale(0.78);
                transform-origin: bottom right;

                transition:
                    opacity 0.38s ease,
                    visibility 0.38s ease,
                    transform 0.55s cubic-bezier(0.16, 1, 0.3, 1);
            }

            #classic-chatbot-panel.cc-open {
                opacity: 1;
                visibility: visible;
                pointer-events: auto;
                transform: translateY(0) scale(1);
            }

            .cc-header {
                height: 110px;
                background: linear-gradient(135deg, #4f46e5, #8b5cf6, #c084fc);
                color: white;
                display: flex;
                align-items: center;
                padding: 18px 20px;
                gap: 14px;
            }

            .cc-avatar {
                width: 58px;
                height: 58px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.95);
                color: #6d28d9;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                box-shadow: 0 8px 25px rgba(255, 255, 255, 0.25);
                animation: classicBotFloat 2.8s ease-in-out infinite;
            }

            .cc-title {
                font-size: 24px;
                font-weight: 800;
                line-height: 1.1;
            }

            .cc-status {
                margin-top: 7px;
                display: flex;
                align-items: center;
                gap: 7px;
                font-size: 14px;
                font-weight: 500;
            }

            .cc-status-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: white;
                box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.18);
                animation: classicStatusBlink 1.5s infinite;
            }

            #classic-chatbot-close {
                margin-left: auto;
                width: 42px;
                height: 42px;
                border-radius: 50%;
                border: none;
                background: rgba(255, 255, 255, 0.25);
                color: white;
                font-size: 28px;
                line-height: 1;
                cursor: pointer;
                transition: transform 0.22s ease, background 0.22s ease;
            }

            #classic-chatbot-close:hover {
                background: rgba(255, 255, 255, 0.35);
                transform: rotate(90deg) scale(1.05);
            }

            #classic-chatbot-body {
                height: 415px;
                padding: 22px;
                background: linear-gradient(180deg, #f8f9ff, #eef2ff);
                overflow-y: auto;
                scroll-behavior: smooth;
            }

            .cc-row {
                display: flex;
                gap: 9px;
                margin-bottom: 14px;
                animation: classicMessageIn 0.25s ease;
            }

            .cc-mini-avatar {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: white;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                flex-shrink: 0;
            }

            .cc-bot-msg {
                max-width: 82%;
                background: white;
                padding: 14px 16px;
                border-radius: 18px 18px 18px 6px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
                color: #263248;
                font-size: 14px;
                line-height: 1.55;
            }

            .cc-user-msg {
                max-width: 82%;
                margin-left: auto;
                margin-bottom: 14px;
                background: linear-gradient(135deg, #5b3df5, #a855f7);
                color: white;
                padding: 14px 16px;
                border-radius: 18px 18px 6px 18px;
                box-shadow: 0 8px 24px rgba(124, 77, 255, 0.22);
                font-size: 14px;
                line-height: 1.55;
                animation: classicMessageIn 0.25s ease;
            }

            .cc-quick {
                display: flex;
                gap: 8px;
                padding: 10px 16px;
                background: white;
                border-top: 1px solid #eee;
            }

            .cc-quick button {
                border: 1px solid #ddd6fe;
                background: #faf5ff;
                color: #5b21b6;
                border-radius: 20px;
                padding: 7px 11px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .cc-quick button:hover {
                background: #ede9fe;
                transform: translateY(-1px);
            }

            .cc-footer {
                height: 82px;
                padding: 14px 18px;
                display: flex;
                gap: 10px;
                align-items: center;
                background: white;
                border-top: 1px solid #eee;
            }

            #classic-chatbot-input {
                flex: 1;
                height: 48px;
                border: 1px solid #ddd;
                border-radius: 24px;
                padding: 0 16px;
                outline: none;
                font-size: 14px;
                transition: border 0.2s ease, box-shadow 0.2s ease;
            }

            #classic-chatbot-input:focus {
                border-color: #8b5cf6;
                box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.12);
            }

            #classic-chatbot-send {
                border: none;
                background: linear-gradient(135deg, #5b3df5, #a855f7);
                color: white;
                border-radius: 50%;
                width: 52px;
                height: 52px;
                font-size: 22px;
                cursor: pointer;
                transition: transform 0.18s ease, box-shadow 0.18s ease;
                box-shadow: 0 8px 22px rgba(124, 77, 255, 0.28);
            }

            #classic-chatbot-send:hover {
                transform: scale(1.08);
                box-shadow: 0 12px 28px rgba(124, 77, 255, 0.42);
            }

            #classic-chatbot-send:active {
                transform: scale(0.94);
            }

            .cc-typing {
                display: inline-flex;
                gap: 4px;
                align-items: center;
            }

            .cc-typing span {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #8b5cf6;
                animation: classicTyping 1s infinite ease-in-out;
            }

            .cc-typing span:nth-child(2) {
                animation-delay: 0.15s;
            }

            .cc-typing span:nth-child(3) {
                animation-delay: 0.3s;
            }

            @keyframes classicBotPulse {
                0% {
                    box-shadow: 0 0 0 0 rgba(124,77,255,0.42), 0 18px 45px rgba(124,77,255,0.45);
                }
                70% {
                    box-shadow: 0 0 0 14px rgba(124,77,255,0), 0 18px 45px rgba(124,77,255,0.45);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(124,77,255,0), 0 18px 45px rgba(124,77,255,0.45);
                }
            }

            @keyframes classicBotFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }

            @keyframes classicStatusBlink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.55; }
            }

            @keyframes classicMessageIn {
                from {
                    opacity: 0;
                    transform: translateY(8px) scale(0.98);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            @keyframes classicTyping {
                0%, 80%, 100% {
                    transform: scale(0.6);
                    opacity: 0.45;
                }
                40% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
        `;

        document.head.appendChild(style);
    }

    function botMessage(text) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;

        body.insertAdjacentHTML(
            "beforeend",
            '<div class="cc-row">' +
                '<div class="cc-mini-avatar">🤖</div>' +
                '<div class="cc-bot-msg">' + escapeHtml(text).replace(/\n/g, "<br>") + '</div>' +
            '</div>'
        );

        body.scrollTop = body.scrollHeight;
    }

    function userMessage(text) {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;

        body.insertAdjacentHTML(
            "beforeend",
            '<div class="cc-user-msg">' + escapeHtml(text) + '</div>'
        );

        body.scrollTop = body.scrollHeight;
    }

    function showTyping() {
        var body = document.getElementById("classic-chatbot-body");
        if (!body) return;
        if (document.getElementById("classic-chatbot-typing")) return;

        body.insertAdjacentHTML(
            "beforeend",
            '<div class="cc-row" id="classic-chatbot-typing">' +
                '<div class="cc-mini-avatar">🤖</div>' +
                '<div class="cc-bot-msg">' +
                    '<span class="cc-typing"><span></span><span></span><span></span></span>' +
                '</div>' +
            '</div>'
        );

        body.scrollTop = body.scrollHeight;
    }

    function hideTyping() {
        var typing = document.getElementById("classic-chatbot-typing");
        if (typing) typing.remove();
    }

    function sendMessage(quickText) {
        console.log("[Classic Chatbot v2] Send clicked");

        var input = document.getElementById("classic-chatbot-input");
        var msg = quickText || (input ? input.value.trim() : "");

        if (!msg) {
            console.log("[Classic Chatbot v2] Empty message");
            return;
        }

        if (input) input.value = "";

        userMessage(msg);
        showTyping();

        var ctx = getContext();

        if (!window.frappe || !frappe.call) {
            setTimeout(function () {
                hideTyping();
                botMessage("Frappe API available nahi hai. Page reload karo.");
            }, 400);
            return;
        }

        frappe.call({
            method: "classic_chatbot.api.agent.ask",
            args: {
                question: msg,
                doctype: ctx.doctype,
                docname: ctx.docname,
                doc: JSON.stringify(ctx.doc || {}),
                route: JSON.stringify(ctx.route || []),
                error: last_error || ""
            },
            callback: function (r) {
                hideTyping();

                var answer = "No response received.";
                if (r && r.message && r.message.answer) {
                    answer = r.message.answer;
                }

                botMessage(answer);
            },
            error: function (err) {
                hideTyping();
                console.error("[Classic Chatbot v2] API Error", err);
                botMessage("API error aa gaya. Bench terminal ya browser console me error check karo.");
            }
        });
    }

    function mount() {
        removeOldBot();
        injectStyle();

        var launcher = document.createElement("button");
        launcher.id = "classic-chatbot-launcher";
        launcher.type = "button";
        launcher.innerHTML = "🤖";

        var panel = document.createElement("div");
        panel.id = "classic-chatbot-panel";

        panel.innerHTML =
            '<div class="cc-header">' +
                '<div class="cc-avatar">🤖</div>' +
                '<div>' +
                    '<div class="cc-title">Classic Chatbot</div>' +
                    '<div class="cc-status"><span class="cc-status-dot"></span>Agent Mode</div>' +
                '</div>' +
                '<button id="classic-chatbot-close" type="button">×</button>' +
            '</div>' +
            '<div id="classic-chatbot-body">' +
                '<div class="cc-row">' +
                    '<div class="cc-mini-avatar">🤖</div>' +
                    '<div class="cc-bot-msg">Hello 👋 Main Classic Chatbot hoon.<br>Main ERPNext DocType, fields aur errors analyze karke help karunga.</div>' +
                '</div>' +
            '</div>' +
            '<div class="cc-quick">' +
                '<button type="button" data-q="current form me kya missing hai?">Missing?</button>' +
                '<button type="button" data-q="is form ke mandatory fields kya hain?">Mandatory</button>' +
                '<button type="button" data-q="is error ka solution batao">Error Fix</button>' +
            '</div>' +
            '<div class="cc-footer">' +
                '<input id="classic-chatbot-input" placeholder="Ask ERPNext issue..." />' +
                '<button id="classic-chatbot-send" type="button">➤</button>' +
            '</div>';

        document.body.appendChild(launcher);
        document.body.appendChild(panel);

        launcher.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();

            console.log("[Classic Chatbot v2] Open clicked");

            launcher.classList.add("cc-hide");

            requestAnimationFrame(function () {
                panel.classList.add("cc-open");
            });

            setTimeout(function () {
                var input = document.getElementById("classic-chatbot-input");
                if (input) input.focus();
            }, 350);
        });

        document.getElementById("classic-chatbot-close").addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();

            console.log("[Classic Chatbot v2] Close clicked");

            panel.classList.remove("cc-open");

            setTimeout(function () {
                launcher.classList.remove("cc-hide");
            }, 260);
        });

        document.getElementById("classic-chatbot-send").addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            sendMessage();
        });

        document.getElementById("classic-chatbot-input").addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });

        panel.querySelectorAll(".cc-quick button").forEach(function (button) {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();
                sendMessage(button.getAttribute("data-q"));
            });
        });
    }

    window.addEventListener("error", function (event) {
        last_error = event.message || "";
    });

    window.addEventListener("unhandledrejection", function (event) {
        last_error = event.reason ? String(event.reason) : "";
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", mount);
    } else {
        mount();
    }

    setTimeout(mount, 800);

    window.ClassicChatbotV2 = {
        remount: mount,
        sendMessage: sendMessage
    };
})();