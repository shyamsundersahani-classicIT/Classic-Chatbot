(function () {
    "use strict";

    var VALIDATION_METHOD =
    "classic_chatbot.api.validation.validate_current_form";
    
    var TARGET_VALIDATION_DOCTYPE =
    "Contact";

    var VALIDATION_LAYOUT_TYPES = {
        "Section Break": true,
        "Column Break": true,
        "Tab Break": true,
        "HTML": true,
        "Button": true,
        "Image": true,
        "Fold": true,
        "Heading": true
    };

    function escapeHtml(value) {
        return String(value === undefined || value === null ? "" : value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function isFormAvailable() {
        return Boolean(
            window.frappe &&
            frappe.ui &&
            frappe.ui.form &&
            frappe.ui.form.Form
        );
    }

    function cleanValue(value, depth) {
        depth = depth || 0;

        if (depth > 5) {
            return undefined;
        }

        if (
            value === null ||
            value === undefined ||
            typeof value === "string" ||
            typeof value === "number" ||
            typeof value === "boolean"
        ) {
            return value;
        }

        if (Array.isArray(value)) {
            return value.slice(0, 100).map(function (row) {
                return cleanValue(row, depth + 1);
            });
        }

        if (typeof value === "object") {
            var output = {};

            Object.keys(value).forEach(function (key) {
                if (key.indexOf("__") === 0) {
                    return;
                }

                if (
                    key === "_liked_by" ||
                    key === "_comments"
                ) {
                    return;
                }

                var cleaned = cleanValue(
                    value[key],
                    depth + 1
                );

                if (cleaned !== undefined) {
                    output[key] = cleaned;
                }
            });

            return output;
        }

        return String(value);
    }

    function getFieldState(frm) {
        var requiredFields = [];
        var visibleFields = [];

        Object.keys(frm.fields_dict || {}).forEach(
            function (fieldname) {
                var field = frm.fields_dict[fieldname];

                if (!field || !field.df) {
                    return;
                }

                if (
                    VALIDATION_LAYOUT_TYPES[
                        field.df.fieldtype
                    ]
                ) {
                    return;
                }

                var wrapper =
                    field.$wrapper ||
                    $(field.wrapper || []);

                var hiddenByDependency = Boolean(
                    field.df.hidden ||
                    field.disp_status === "None" ||
                    (
                        wrapper.length &&
                        (
                            wrapper.hasClass("hide-control") ||
                            wrapper.hasClass("hidden")
                        )
                    )
                );

                var visible = !hiddenByDependency;

                if (visible) {
                    visibleFields.push(fieldname);
                }

                if (
                    visible &&
                    field.df.reqd
                ) {
                    requiredFields.push(fieldname);
                }
            }
        );

        return {
            required_fields: requiredFields,
            visible_fields: visibleFields
        };
    }

   function requestValidation(frm, runAI) {
    /*
     * AI validation currently sirf Contact DocType ke liye enabled hai.
     * Kisi aur DocType par backend API call nahi hogi.
     */
    if (
        !frm ||
        !frm.doctype ||
        frm.doctype !== TARGET_VALIDATION_DOCTYPE
    ) {
        return Promise.resolve({
            ok: true,
            skipped: true,
            skip_reason:
                "AI validation is enabled only for Contact.",
            doctype:
                frm && frm.doctype
                    ? frm.doctype
                    : null,
            docname:
                frm && frm.docname
                    ? frm.docname
                    : null,
            issue_count: 0,
            blocking_issue_count: 0,
            first_issue: null,
            issues: [],
            warnings: [],
            model_used: "Validation skipped",
            ai_error: null,
            ai_cached: false
        });
    }

    var state = getFieldState(frm);

    var payload = cleanValue(
        frm.doc || {},
        0
    ) || {};

    return new Promise(function (resolve, reject) {
        frappe.call({
            method: VALIDATION_METHOD,

            args: {
                doctype: frm.doctype,
                docname: frm.docname,

                doc: JSON.stringify(
                    payload
                ),

                required_fields: JSON.stringify(
                    state.required_fields
                ),

                visible_fields: JSON.stringify(
                    state.visible_fields
                ),

                run_ai:
                    runAI === false
                        ? 0
                        : 1
            },

            callback: function (response) {
                var result =
                    response &&
                    response.message
                        ? response.message
                        : {
                            ok: true,
                            skipped: false,
                            issue_count: 0,
                            blocking_issue_count: 0,
                            first_issue: null,
                            issues: [],
                            warnings: [],
                            ai_error: null,
                            ai_cached: false
                        };

                /*
                 * Backend se issues/warnings arrays na aayein
                 * to safe empty arrays set kar do.
                 */
                if (!Array.isArray(result.issues)) {
                    result.issues = [];
                }

                if (!Array.isArray(result.warnings)) {
                    result.warnings = [];
                }

                resolve(result);
            },

            error: function (error) {
                console.error(
                    "[Classic AI Validator Request Error]",
                    error
                );

                reject(
                    error ||
                    new Error(
                        "Contact AI validation request failed."
                    )
                );
            }
        });
    });
}

    function injectValidationStyle() {
        if (
            document.getElementById(
                "classic-ai-validation-style"
            )
        ) {
            return;
        }

        var style = document.createElement("style");

        style.id =
            "classic-ai-validation-style";

        style.textContent = [
            "#classic-ai-validation-avatar{position:fixed;left:20px;bottom:20px;width:340px;max-width:calc(100vw - 40px);z-index:1000001;background:#fff;border:1px solid #d1d8dd;border-radius:16px;box-shadow:0 16px 45px rgba(0,0,0,.22);font-family:Inter,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;overflow:hidden;animation:classicAiIn .22s ease-out}",

            "#classic-ai-validation-avatar.classic-ai-warning{border-color:#f0ad4e}",

            ".classic-ai-avatar-head{display:flex;gap:12px;align-items:flex-start;padding:15px 16px 10px}",

            ".classic-ai-avatar-icon{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#ffe8e8;color:#c92a2a;font-size:20px;flex:0 0 38px}",

            ".classic-ai-warning .classic-ai-avatar-icon{background:#fff3cd;color:#8a5a00}",

            ".classic-ai-avatar-title{font-size:14px;font-weight:700;color:#1f272e;margin-top:1px}",

            ".classic-ai-avatar-model{font-size:11px;color:#7c858d;margin-top:2px}",

            ".classic-ai-avatar-close{margin-left:auto;border:0;background:transparent;font-size:20px;line-height:20px;color:#7c858d;cursor:pointer}",

            ".classic-ai-avatar-body{padding:0 16px 12px;max-height:220px;overflow:auto}",

            ".classic-ai-avatar-issue{padding:9px 10px;border-radius:10px;background:#f8f9fa;margin-top:7px;color:#36414c;font-size:12px;line-height:1.45;cursor:pointer}",

            ".classic-ai-avatar-issue:hover{background:#eef1f4}",

            ".classic-ai-avatar-expected{display:block;color:#6c7680;margin-top:3px}",

            ".classic-ai-avatar-actions{display:flex;gap:8px;padding:10px 16px 15px;border-top:1px solid #eef1f4}",

            ".classic-ai-avatar-actions button{border:1px solid #d1d8dd;border-radius:8px;padding:7px 11px;background:#fff;color:#36414c;font-size:12px;cursor:pointer}",

            ".classic-ai-avatar-actions .classic-ai-primary{background:#171717;color:#fff;border-color:#171717}",

            ".classic-ai-field-error{outline:2px solid #e03131!important;outline-offset:2px;border-radius:6px;transition:outline .2s ease}",

            "@keyframes classicAiIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}",

            "@media(max-width:600px){#classic-ai-validation-avatar{left:10px;right:10px;bottom:10px;width:auto;max-width:none}}"
        ].join("");

        document.head.appendChild(style);
    }

    function clearFieldHighlights(frm) {
        if (!frm || !frm.wrapper) {
            return;
        }

        $(frm.wrapper)
            .find(".classic-ai-field-error")
            .removeClass(
                "classic-ai-field-error"
            );
    }

    function focusParentField(
        frm,
        fieldname
    ) {
        var field =
            frm.fields_dict &&
            frm.fields_dict[fieldname];

        if (!field) {
            return false;
        }

        try {
            if (frm.scroll_to_field) {
                frm.scroll_to_field(fieldname);
            }

            if (
                field.$wrapper &&
                field.$wrapper.length
            ) {
                field.$wrapper.addClass(
                    "classic-ai-field-error"
                );
            }

            if (field.set_focus) {
                setTimeout(function () {
                    field.set_focus();
                }, 180);
            }

            return true;
        } catch (error) {
            console.error(
                "[Classic AI] Field focus error",
                error
            );

            return false;
        }
    }

    function focusChildField(
        frm,
        issue
    ) {
        var tableField =
            frm.fields_dict &&
            frm.fields_dict[
                issue.fieldname
            ];

        if (
            !tableField ||
            !tableField.grid
        ) {
            return focusParentField(
                frm,
                issue.fieldname
            );
        }

        try {
            if (tableField.$wrapper) {
                tableField.$wrapper.addClass(
                    "classic-ai-field-error"
                );
            }

            if (frm.scroll_to_field) {
                frm.scroll_to_field(
                    issue.fieldname
                );
            }

            var rowIndex = Number(
                issue.row_index || 0
            );

            var gridRow =
                rowIndex > 0
                    ? tableField.grid.grid_rows[
                        rowIndex - 1
                    ]
                    : null;

            if (!gridRow) {
                return true;
            }

            if (gridRow.toggle_view) {
                gridRow.toggle_view(true);
            }

            setTimeout(function () {
                try {
                    var childField =
                        gridRow.columns &&
                        gridRow.columns[
                            issue.child_fieldname
                        ];

                    if (
                        childField &&
                        childField.field_area
                    ) {
                        $(childField.field_area)
                            .addClass(
                                "classic-ai-field-error"
                            );

                        $(childField.field_area)
                            .find(
                                ":input:visible:first"
                            )
                            .trigger("focus");
                    } else if (gridRow.row) {
                        $(gridRow.row)
                            .addClass(
                                "classic-ai-field-error"
                            );
                    }
                } catch (error) {
                    console.error(
                        "[Classic AI] Child focus error",
                        error
                    );
                }
            }, 220);

            return true;
        } catch (error) {
            console.error(
                "[Classic AI] Child table error",
                error
            );

            return focusParentField(
                frm,
                issue.fieldname
            );
        }
    }

    function focusIssue(frm, issue) {
        if (!frm || !issue) {
            return;
        }

        clearFieldHighlights(frm);

        if (issue.child_fieldname) {
            focusChildField(
                frm,
                issue
            );
        } else if (issue.fieldname) {
            focusParentField(
                frm,
                issue.fieldname
            );
        }
    }

    function closeValidationAvatar() {
        var avatar =
            document.getElementById(
                "classic-ai-validation-avatar"
            );

        if (avatar) {
            avatar.remove();
        }
    }

    function openChatbotWithIssue(issue) {
        var launcher =
            document.getElementById(
                "classic-chatbot-launcher"
            );

        if (launcher) {
            launcher.click();
        }

        setTimeout(function () {
            var input =
                document.getElementById(
                    "classic-chatbot-input"
                );

            if (!input) {
                return;
            }

            input.value = issue
                ? (
                    "Is validation issue ko explain " +
                    "karke correct value batao: " +
                    issue.message
                )
                : (
                    "Current form ke validation " +
                    "issues explain karo"
                );

            input.focus();
        }, 250);
    }

    function showValidationAvatar(
        frm,
        result
    ) {
        injectValidationStyle();
        closeValidationAvatar();

        var issues =
            (
                result &&
                result.issues
            ) || [];

        if (!issues.length) {
            return;
        }

        var blocking =
            Number(
                result.blocking_issue_count ||
                0
            ) > 0;

        var avatar =
            document.createElement("div");

        avatar.id =
            "classic-ai-validation-avatar";

        if (!blocking) {
            avatar.classList.add(
                "classic-ai-warning"
            );
        }

        var shownIssues =
            issues.slice(0, 6);

        var issueHtml =
            shownIssues.map(
                function (issue, index) {
                    var rowText =
                        issue.row_index
                            ? (
                                " · Row " +
                                issue.row_index
                            )
                            : "";

                    var expected =
                        issue.expected
                            ? (
                                '<span class="' +
                                'classic-ai-avatar-expected">' +
                                "Expected: " +
                                escapeHtml(
                                    issue.expected
                                ) +
                                "</span>"
                            )
                            : "";

                    return (
                        '<div class="' +
                        'classic-ai-avatar-issue" ' +
                        'data-index="' +
                        index +
                        '">' +

                        "<b>" +
                        escapeHtml(
                            issue.label ||
                            issue.fieldname ||
                            "Field"
                        ) +
                        escapeHtml(rowText) +
                        "</b><br>" +

                        escapeHtml(
                            issue.message ||
                            "Please check this value."
                        ) +

                        expected +

                        "</div>"
                    );
                }
            ).join("");

        avatar.innerHTML =
            '<div class="classic-ai-avatar-head">' +

                '<div class="classic-ai-avatar-icon">' +
                    (
                        blocking
                            ? "!"
                            : "i"
                    ) +
                "</div>" +

                "<div>" +

                    '<div class="classic-ai-avatar-title">' +

                        (
                            blocking
                                ? (
                                    "AI found " +
                                    Number(
                                        result.blocking_issue_count ||
                                        issues.length
                                    ) +
                                    " blocking issue(s)"
                                )
                                : "AI validation warning"
                        ) +

                    "</div>" +

                    '<div class="classic-ai-avatar-model">' +

                        escapeHtml(
                            result.model_used ||
                            "Classic Chatbot Validator"
                        ) +

                        (
                            result.ai_cached
                                ? " · cached"
                                : ""
                        ) +

                    "</div>" +

                "</div>" +

                '<button type="button" ' +
                'class="classic-ai-avatar-close" ' +
                'title="Close">×</button>' +

            "</div>" +

            '<div class="classic-ai-avatar-body">' +
                issueHtml +
            "</div>" +

            '<div class="classic-ai-avatar-actions">' +

                '<button type="button" ' +
                'class="classic-ai-primary" ' +
                'data-action="focus">' +
                    "Go to Field" +
                "</button>" +

                '<button type="button" ' +
                'data-action="chat">' +
                    "Ask AI" +
                "</button>" +

                '<button type="button" ' +
                'data-action="close">' +
                    "Close" +
                "</button>" +

            "</div>";

        document.body.appendChild(avatar);

        avatar.addEventListener(
            "click",
            function (event) {
                var issueNode =
                    event.target.closest(
                        ".classic-ai-avatar-issue"
                    );

                if (issueNode) {
                    var issueIndex =
                        Number(
                            issueNode.getAttribute(
                                "data-index"
                            ) || 0
                        );

                    focusIssue(
                        frm,
                        shownIssues[issueIndex]
                    );

                    return;
                }

                var close =
                    event.target.closest(
                        ".classic-ai-avatar-close"
                    );

                var actionButton =
                    event.target.closest(
                        "[data-action]"
                    );

                if (close) {
                    closeValidationAvatar();
                    return;
                }

                if (!actionButton) {
                    return;
                }

                var action =
                    actionButton.getAttribute(
                        "data-action"
                    );

                if (action === "focus") {
                    focusIssue(
                        frm,
                        shownIssues[0]
                    );
                } else if (action === "chat") {
                    openChatbotWithIssue(
                        shownIssues[0]
                    );
                } else if (action === "close") {
                    closeValidationAvatar();
                }
            }
        );

        focusIssue(
            frm,
            shownIssues[0]
        );
    }

    function validateCurrentForm(
        frm,
        options
    ) {
        options = options || {};

        if (
            !frm ||
            !frm.doc ||
            !frm.doctype
        ) {
            return Promise.resolve({
                ok: true,
                issues: []
            });
        }

        if (
            options.showProgress !== false &&
            frappe.show_alert
        ) {
            frappe.show_alert(
                {
                    message: __(
                        "AI is checking the current form..."
                    ),
                    indicator: "blue"
                },
                3
            );
        }

        return requestValidation(
            frm,
            options.runAI !== false
        ).then(function (result) {
            if (
                !result.ok ||
                (
                    result.issues &&
                    result.issues.length
                ) ||
                result.ai_error
            ) {
                showValidationAvatar(
                    frm,
                    result
                );
            } else {
                closeValidationAvatar();
                clearFieldHighlights(frm);

                if (
                    options.successMessage !== false &&
                    frappe.show_alert
                ) {
                    frappe.show_alert(
                        {
                            message: __(
                                "AI validation passed."
                            ),
                            indicator: "green"
                        },
                        3
                    );
                }
            }

            return result;
        });
    }

   function shouldValidateForm(frm) {
    if (
        !frm ||
        !frm.doc ||
        !frm.doctype
    ) {
        return false;
    }

    if (
        frm.doctype !==
        TARGET_VALIDATION_DOCTYPE
    ) {
        return false;
    }

    if (
        frm.meta &&
        frm.meta.istable
    ) {
        return false;
    }

    return true;
}

    function installSaveGuard() {
        if (!isFormAvailable()) {
            setTimeout(
                installSaveGuard,
                500
            );

            return;
        }

        var Form =
            frappe.ui.form.Form;

        if (
            Form.prototype
                .__classic_ai_save_guard_installed
        ) {
            return;
        }

        Form.prototype
            .__classic_ai_save_guard_installed =
            true;

        var originalSave =
            Form.prototype.save;

        Form.prototype.save = function () {
            var frm = this;
            var originalArguments = arguments;

            if (!shouldValidateForm(frm)) {
                return originalSave.apply(
                    frm,
                    originalArguments
                );
            }

            if (
                frm.__classic_ai_validation_running
            ) {
                return (
                    frm
                        .__classic_ai_validation_running
                );
            }

            frm.__classic_ai_validation_running =
                validateCurrentForm(
                    frm,
                    {
                        runAI: true,
                        showProgress: true,
                        successMessage: false
                    }
                )
                    .then(function (result) {
                        if (!result.ok) {
                            frappe.validated = false;

                            var validationError =
                                new Error(
                                    "Classic AI validation failed."
                                );

                            validationError
                                .classic_ai_result =
                                result;

                            return Promise.reject(
                                validationError
                            );
                        }

                        return originalSave.apply(
                            frm,
                            originalArguments
                        );
                    })
                    .catch(function (error) {
                        if (
                            error &&
                            error.classic_ai_result
                        ) {
                            return Promise.reject(
                                error
                            );
                        }

                        console.error(
                            "[Classic AI Validator]",
                            error
                        );

                        return originalSave.apply(
                            frm,
                            originalArguments
                        );
                    })
                    .finally(function () {
                        frm
                            .__classic_ai_validation_running =
                            null;
                    });

            return (
                frm
                    .__classic_ai_validation_running
            );
        };
    }




    function exposeManualValidation() {
    window
        .classic_chatbot_validate_current_form =
        function () {
            if (!window.cur_frm) {
                frappe.msgprint(
                    __(
                        "Please open a Contact form first."
                    )
                );

                return Promise.resolve({
                    ok: true,
                    issues: []
                });
            }

            if (
                cur_frm.doctype !==
                TARGET_VALIDATION_DOCTYPE
            ) {
                frappe.msgprint(
                    __(
                        "AI validation is currently enabled only for Contact."
                    )
                );

                return Promise.resolve({
                    ok: true,
                    skipped: true,
                    issues: []
                });
            }

            return validateCurrentForm(
                window.cur_frm,
                {
                    runAI: true,
                    showProgress: true,
                    successMessage: true
                }
            );
        };

    $(document).off(
        "form-refresh.classic-ai-validator"
    );

    $(document).on(
        "form-refresh.classic-ai-validator",
        function (event, frm) {
            if (
                !frm ||
                !frm.page ||
                frm.doctype !==
                    TARGET_VALIDATION_DOCTYPE ||
                frm
                    .__classic_ai_check_button_added
            ) {
                return;
            }

            frm
                .__classic_ai_check_button_added =
                true;

            try {
                frm.page.add_menu_item(
                    __(
                        "Check Contact with Local AI"
                    ),
                    function () {
                        validateCurrentForm(
                            frm,
                            {
                                runAI: true,
                                showProgress: true,
                                successMessage: true
                            }
                        );
                    }
                );

            } catch (error) {
                console.error(
                    "[Classic AI] Menu error",
                    error
                );
            }
        }
    );
}

    











    function initialize() {
        injectValidationStyle();
        installSaveGuard();
        exposeManualValidation();

        console.log(
            "[Classic AI Validator] Loaded successfully."
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