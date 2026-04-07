// KtulueBot chat page — vanilla JavaScript, no framework, no build step.

(function () {
    "use strict";

    const SESSION_KEY = "kchatbot_session_id";

    // --- Session ID (per-tab via sessionStorage) ---

    function getOrCreateSessionId() {
        let id = sessionStorage.getItem(SESSION_KEY);
        if (!id) {
            id = crypto.randomUUID();
            sessionStorage.setItem(SESSION_KEY, id);
        }
        return id;
    }

    const sessionId = getOrCreateSessionId();

    // --- DOM references ---

    const messagesEl = document.getElementById("chat-messages");
    const formEl = document.getElementById("chat-form");
    const inputEl = document.getElementById("chat-input");
    const sendBtn = document.getElementById("chat-send");

    // --- Rendering helpers ---

    function appendMessage(role, text) {
        const div = document.createElement("div");
        div.className = "message " + role;
        div.textContent = text;
        messagesEl.appendChild(div);
        return div;
    }

    function appendTypingIndicator() {
        const div = document.createElement("div");
        div.className = "message bot typing-bubble";
        div.innerHTML =
            '<div class="typing-indicator">' +
            '<span></span><span></span><span></span>' +
            '</div>';
        messagesEl.appendChild(div);
        return div;
    }

    function setInputEnabled(enabled) {
        inputEl.disabled = !enabled;
        sendBtn.disabled = !enabled;
        if (enabled) {
            inputEl.focus();
        }
    }

    // --- SSE parsing for fetch streams ---
    // Each event arrives as: "data: {json}\n\n"

    async function readSseStream(response, onEvent) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            let sepIndex;
            while ((sepIndex = buffer.indexOf("\n\n")) !== -1) {
                const rawEvent = buffer.slice(0, sepIndex);
                buffer = buffer.slice(sepIndex + 2);
                const dataLine = rawEvent
                    .split("\n")
                    .find((line) => line.startsWith("data: "));
                if (!dataLine) continue;
                const jsonStr = dataLine.slice("data: ".length);
                try {
                    const evt = JSON.parse(jsonStr);
                    onEvent(evt);
                } catch (err) {
                    console.error("Bad SSE payload:", jsonStr, err);
                }
            }
        }
    }

    // --- Sending a message ---

    async function sendMessage(text) {
        appendMessage("user", text);
        setInputEnabled(false);

        const typingBubble = appendTypingIndicator();
        let botBubble = null;

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: text,
                }),
            });

            if (!response.ok) {
                typingBubble.remove();
                appendMessage(
                    "bot",
                    "My brain just buffered. Hydrate while I reboot."
                );
                return;
            }

            await readSseStream(response, (evt) => {
                if (evt.type === "token") {
                    if (botBubble === null) {
                        typingBubble.remove();
                        botBubble = appendMessage("bot", "");
                    }
                    botBubble.textContent += evt.text;
                } else if (evt.type === "error") {
                    if (botBubble) {
                        botBubble.remove();
                        botBubble = null;
                    }
                    typingBubble.remove();
                    appendMessage("bot", evt.text);
                }
            });
        } catch (err) {
            console.error("Chat request failed:", err);
            typingBubble.remove();
            if (botBubble) {
                botBubble.remove();
            }
            appendMessage(
                "bot",
                "Connection's choppier than my Wi-Fi during a stream. Try that one again?"
            );
        } finally {
            setInputEnabled(true);
        }
    }

    // --- Wire up the form ---

    formEl.addEventListener("submit", function (e) {
        e.preventDefault();
        const text = inputEl.value.trim();
        if (!text) return;
        inputEl.value = "";
        sendMessage(text);
    });

    // --- Initial greeting (no API call) ---

    appendMessage(
        "bot",
        "Hey, I'm KtulueBot — Josh in chatbot form. Ask me about streaming, projects, board games, or just say hi. And drink some water while you're at it."
    );

    inputEl.focus();
})();
