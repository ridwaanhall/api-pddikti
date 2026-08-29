/* Web playground.
 *
 * Execution deliberately goes through POST /web/execute with the typed values in the
 * request body: nothing the user types is ever placed in a URL, so it stays out of the
 * address bar, the browser's network log, and server access logs. The code snippets do
 * show the real public URL, because that is what a caller needs in order to use the API.
 */
(() => {
    "use strict";

    const config = JSON.parse(document.getElementById("playground-config").textContent);
    const API_BASE = config.publicApiBaseUrl;

    /* ------------------------------------------------------------------ helpers */

    const parseJson = (text) => {
        try {
            return JSON.parse(text);
        } catch {
            return undefined;
        }
    };

    const formatBytes = (n) =>
        n < 1024
            ? n + " B"
            : n < 1048576
              ? (n / 1024).toFixed(1) + " KB"
              : (n / 1048576).toFixed(2) + " MB";

    const isImageUrl = (value) =>
        typeof value === "string" &&
        /^https?:\/\/\S+\.(png|jpe?g|gif|webp|svg)(\?\S*)?$/i.test(value);

    const isUrl = (value) => typeof value === "string" && /^https?:\/\/\S+$/i.test(value);

    const prettyKey = (key) => key.replace(/[_-]+/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

    /* --------------------------------------------------------------- request build */

    function collectFields(form) {
        const params = {};
        const missing = [];

        form.querySelectorAll("[data-param-name]").forEach((field) => {
            const name = field.dataset.paramName;
            const value = (field.value || "").trim();
            if (!value) {
                if (field.dataset.paramIn === "path") missing.push(name);
                return;
            }
            params[name] = value;
        });

        return { params, missing };
    }

    function readBody(form) {
        const field = form.querySelector("[data-request-body]");
        if (!field || !field.value.trim()) return { body: null, error: null };
        const parsed = parseJson(field.value.trim());
        if (parsed === undefined) return { body: null, error: "Request body must be valid JSON." };
        return { body: parsed, error: null };
    }

    /** The public URL a third party would call. Used for snippets only, never for fetch. */
    function publicUrl(form, params) {
        let path = form.dataset.apiPath.replace(/^\/api/, "");
        const query = new URLSearchParams();

        form.querySelectorAll("[data-param-name]").forEach((field) => {
            const name = field.dataset.paramName;
            const value = params[name];
            if (!value) return;
            if (field.dataset.paramIn === "path") {
                path = path.replace("{" + name + "}", encodeURIComponent(value));
            } else {
                query.append(name, value);
            }
        });

        const qs = query.toString();
        return API_BASE + path + (qs ? "?" + qs : "");
    }

    /* -------------------------------------------------------------------- snippets */

    function buildSnippet(language, method, url, body) {
        const bodyText = body ? JSON.stringify(body, null, 4) : null;

        if (language === "python") {
            return [
                "import requests",
                "",
                ...(bodyText ? ["payload = " + bodyText, ""] : []),
                'url = "' + url + '"',
                'headers = {"accept": "application/json"}',
                'response = requests.request("' +
                    method +
                    '", url, headers=headers' +
                    (bodyText ? ", json=payload" : "") +
                    ")",
                "print(response.json())",
            ].join("\n");
        }

        if (language === "javascript") {
            return [
                ...(bodyText ? ["const payload = " + bodyText + ";", ""] : []),
                'const response = await fetch("' + url + '", {',
                '    method: "' + method + '",',
                '    headers: { accept: "application/json"' +
                    (bodyText ? ', "content-type": "application/json"' : "") +
                    " },",
                ...(bodyText ? ["    body: JSON.stringify(payload),"] : []),
                "});",
                "const data = await response.json();",
                "console.log(data);",
            ].join("\n");
        }

        if (language === "php") {
            return [
                "<?php",
                '$ch = curl_init("' + url + '");',
                'curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "' + method + '");',
                "curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);",
                'curl_setopt($ch, CURLOPT_HTTPHEADER, ["accept: application/json"]);',
                "$response = curl_exec($ch);",
                "curl_close($ch);",
                "echo $response;",
            ].join("\n");
        }

        return [
            "curl -X '" + method + "' \\",
            "    '" + url + "' \\",
            "    -H 'accept: application/json'" + (bodyText ? " \\" : ""),
            ...(bodyText
                ? ["    -H 'content-type: application/json' \\", "    -d '" + JSON.stringify(body) + "'"]
                : []),
        ].join("\n");
    }

    /* ------------------------------------------------------------- readable render */

    function valueNode(value) {
        if (value === null || value === undefined) {
            const span = document.createElement("span");
            span.className = "italic text-zinc-600";
            span.textContent = "null";
            return span;
        }

        if (typeof value === "boolean") {
            const span = document.createElement("span");
            span.className =
                "text-[11px] uppercase tracking-wider " +
                (value ? "text-emerald-400" : "text-rose-400");
            span.textContent = String(value);
            return span;
        }

        if (isImageUrl(value)) {
            const img = document.createElement("img");
            img.src = value;
            img.loading = "lazy";
            img.alt = "";
            img.className = "max-h-24 border border-zinc-800 bg-black/30 p-1";
            return img;
        }

        if (isUrl(value)) {
            const link = document.createElement("a");
            link.href = value;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.className =
                "break-all text-gold-500 underline decoration-gold-500/30 hover:text-gold-400";
            link.textContent = value;
            return link;
        }

        if (Array.isArray(value) || typeof value === "object") return renderReadable(value);

        const span = document.createElement("span");
        span.className = "break-words text-zinc-300";
        span.textContent = String(value);
        return span;
    }

    /** Arrays of uniform objects become real tables; everything else becomes key/value rows. */
    function renderReadable(data) {
        if (Array.isArray(data)) {
            if (data.length === 0) {
                const empty = document.createElement("p");
                empty.className = "text-xs italic text-zinc-600";
                empty.textContent = "Empty list";
                return empty;
            }

            const allObjects = data.every(
                (item) => item && typeof item === "object" && !Array.isArray(item),
            );

            if (allObjects) {
                const columns = [];
                data.forEach((item) =>
                    Object.keys(item).forEach((key) => {
                        if (!columns.includes(key)) columns.push(key);
                    }),
                );

                const wrap = document.createElement("div");
                wrap.className = "overflow-x-auto";
                const table = document.createElement("table");
                table.className = "w-full border-collapse text-left text-xs";

                const thead = document.createElement("thead");
                const headRow = document.createElement("tr");
                columns.forEach((key) => {
                    const th = document.createElement("th");
                    th.className =
                        "whitespace-nowrap border-b border-zinc-800 px-3 py-2 text-[10px] font-semibold uppercase tracking-[0.15em] text-zinc-500";
                    th.textContent = prettyKey(key);
                    headRow.appendChild(th);
                });
                thead.appendChild(headRow);
                table.appendChild(thead);

                const tbody = document.createElement("tbody");
                data.forEach((item) => {
                    const row = document.createElement("tr");
                    row.className = "border-b border-zinc-900/80 align-top hover:bg-zinc-900/30";
                    columns.forEach((key) => {
                        const td = document.createElement("td");
                        td.className = "max-w-xs px-3 py-2";
                        td.appendChild(valueNode(item[key]));
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);
                wrap.appendChild(table);
                return wrap;
            }

            const list = document.createElement("div");
            list.className = "grid gap-2";
            data.forEach((item, index) => {
                const row = document.createElement("div");
                row.className = "border-l border-zinc-800 pl-3";
                const label = document.createElement("p");
                label.className = "text-[10px] uppercase tracking-wider text-zinc-600";
                label.textContent = "#" + (index + 1);
                row.appendChild(label);
                row.appendChild(valueNode(item));
                list.appendChild(row);
            });
            return list;
        }

        if (data && typeof data === "object") {
            const grid = document.createElement("div");
            grid.className = "grid gap-px bg-zinc-900";
            Object.entries(data).forEach(([key, value]) => {
                const row = document.createElement("div");
                row.className =
                    "grid gap-1 bg-[#0c0c0e] px-3 py-2 sm:grid-cols-[220px_1fr] sm:gap-4";
                const label = document.createElement("p");
                label.className =
                    "text-[10px] font-semibold uppercase tracking-[0.15em] text-zinc-500";
                label.textContent = prettyKey(key);
                const cell = document.createElement("div");
                cell.className = "text-xs";
                cell.appendChild(valueNode(value));
                row.appendChild(label);
                row.appendChild(cell);
                grid.appendChild(row);
            });
            return grid;
        }

        return valueNode(data);
    }

    /* ------------------------------------------------------------ card state */

    const cardOf = (element) => element.closest("[data-endpoint-card]");
    const partOf = (card, name) => card.querySelector('[data-part="' + name + '"]');

    function setStatus(card, code, meta) {
        const chip = partOf(card, "status");
        chip.hidden = false;
        chip.textContent = code;
        const tone =
            typeof code !== "number"
                ? "border-zinc-700 text-zinc-400"
                : code < 300
                  ? "border-emerald-600/40 bg-emerald-500/10 text-emerald-400"
                  : code < 500
                    ? "border-amber-600/40 bg-amber-500/10 text-amber-400"
                    : "border-rose-600/40 bg-rose-500/10 text-rose-400";
        chip.className =
            "border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider " + tone;
        partOf(card, "meta").textContent = meta || "";
    }

    function showTab(card, tab) {
        card.querySelectorAll("[data-tab]").forEach((button) => {
            const active = button.dataset.tab === tab;
            button.classList.toggle("text-gold-500", active);
            button.classList.toggle("border-gold-500", active);
            button.classList.toggle("text-zinc-500", !active);
            button.classList.toggle("border-transparent", !active);
        });
        card.querySelectorAll("[data-panel]").forEach((panel) => {
            panel.hidden = panel.dataset.panel !== tab;
        });
    }

    function refreshSnippet(card) {
        const form = partOf(card, "form");
        const language = partOf(card, "language").value;
        const { params } = collectFields(form);
        const { body } = readBody(form);
        partOf(card, "snippet").textContent = buildSnippet(
            language,
            form.dataset.method,
            publicUrl(form, params),
            body,
        );
    }

    /* -------------------------------------------------------------------- execute */

    async function execute(card) {
        const form = partOf(card, "form");
        const button = partOf(card, "submit");
        const rawBox = partOf(card, "raw");
        const readableBox = partOf(card, "readable");
        const errorBox = partOf(card, "error");

        errorBox.hidden = true;
        errorBox.textContent = "";

        const { params, missing } = collectFields(form);
        if (missing.length) {
            errorBox.hidden = false;
            errorBox.textContent =
                "Fill required parameter" + (missing.length > 1 ? "s" : "") + ": " + missing.join(", ");
            return;
        }

        const { body, error: bodyError } = readBody(form);
        if (bodyError) {
            errorBox.hidden = false;
            errorBox.textContent = bodyError;
            return;
        }

        button.disabled = true;
        button.textContent = "Executing";
        const startedAt = performance.now();

        try {
            const response = await fetch("/web/execute", {
                method: "POST",
                headers: { "content-type": "application/json", accept: "application/json" },
                body: JSON.stringify({
                    operation_id: form.dataset.operationId,
                    group: form.dataset.group,
                    params: params,
                    body: body,
                }),
            });

            const elapsed = Math.round(performance.now() - startedAt);
            const contentType = response.headers.get("content-type") || "";
            readableBox.replaceChildren();

            if (contentType.startsWith("image/")) {
                const blob = await response.blob();
                const img = document.createElement("img");
                img.src = URL.createObjectURL(blob);
                img.alt = "Response image";
                img.className = "max-h-64 border border-zinc-800 bg-black/40 p-2";
                readableBox.appendChild(img);
                rawBox.textContent = "<binary " + contentType + ", " + formatBytes(blob.size) + ">";
                setStatus(
                    card,
                    response.status,
                    elapsed + " ms · " + formatBytes(blob.size) + " · " + contentType,
                );
            } else {
                const text = await response.text();
                const parsed = parseJson(text);
                rawBox.textContent = parsed === undefined ? text : JSON.stringify(parsed, null, 2);
                const readableSource =
                    parsed === undefined ? text : parsed && parsed.data !== undefined ? parsed.data : parsed;
                readableBox.appendChild(renderReadable(readableSource));
                setStatus(
                    card,
                    response.status,
                    elapsed + " ms · " + formatBytes(new Blob([text]).size),
                );
            }

            showTab(card, "readable");
        } catch (error) {
            errorBox.hidden = false;
            errorBox.textContent = error instanceof Error ? error.message : "Request failed.";
            setStatus(card, "ERR", "");
        } finally {
            button.disabled = false;
            button.textContent = "Execute";
        }
    }

    /* ------------------------------------------------------- wiring (delegated) */

    document.addEventListener("submit", (event) => {
        const form = event.target.closest('[data-part="form"]');
        if (!form) return;
        event.preventDefault();
        execute(cardOf(form));
    });

    document.addEventListener("input", (event) => {
        if (event.target.matches("[data-endpoint-filter]")) {
            const term = event.target.value.trim().toLowerCase();
            document.querySelectorAll("[data-sidebar-entry]").forEach((entry) => {
                entry.hidden = Boolean(term) && !entry.dataset.sidebarEntry.includes(term);
            });
            return;
        }
        const card = cardOf(event.target);
        if (card && event.target.matches("[data-param-name], [data-request-body]")) {
            refreshSnippet(card);
        }
    });

    document.addEventListener("change", (event) => {
        if (event.target.matches('[data-part="language"]')) refreshSnippet(cardOf(event.target));
    });

    document.addEventListener("click", async (event) => {
        const tabButton = event.target.closest("[data-tab]");
        if (tabButton) {
            showTab(cardOf(tabButton), tabButton.dataset.tab);
            return;
        }

        const copyButton = event.target.closest("[data-copy]");
        if (!copyButton) return;
        const source = partOf(cardOf(copyButton), copyButton.dataset.copy);
        try {
            await navigator.clipboard.writeText(source.textContent || "");
            const original = copyButton.textContent;
            copyButton.textContent = "Copied";
            setTimeout(() => {
                copyButton.textContent = original;
            }, 1500);
        } catch {
            /* clipboard unavailable (insecure context) -- nothing useful to do */
        }
    });

    document.querySelectorAll("[data-endpoint-card]").forEach((card) => {
        refreshSnippet(card);
        showTab(card, "readable");
    });
})();
