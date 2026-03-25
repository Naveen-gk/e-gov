document.addEventListener("DOMContentLoaded", () => {
    const chatTrigger = document.querySelector(".chat-bot");
    const chatbotContainer = document.getElementById("chatbot-container");
    const closeBtn = document.getElementById("chatbot-close");
    const input = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send");
    const messages = document.getElementById("chatbot-messages");
    const clearBtn = document.getElementById("chatbot-clear");

    chatTrigger.addEventListener("click", () => {
        chatbotContainer.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        chatbotContainer.style.display = "none";
    });

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    clearBtn.addEventListener("click", () => {
        messages.innerHTML = "";
    });

    function appendMessage(content, from = "user") {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${from}`;
        bubble.textContent = content;
        messages.appendChild(bubble);
        messages.scrollTop = messages.scrollHeight;
    }

    async function sendMessage() {
        const query = input.value.trim();
        if (!query) return;

        appendMessage(query, "user");
        input.value = "";

        const typing = document.createElement("div");
        typing.className = "chat-bubble bot";
        typing.textContent = "Typing...";
        messages.appendChild(typing);

        try {
            const res = await fetch("/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });

            const data = await res.json();

            typing.remove();

            appendMessage(data.reply, "bot");

        } catch (err) {
            typing.remove();
            appendMessage("Failed to fetch response.", "bot");
        }
    }
});