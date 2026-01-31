document.addEventListener("DOMContentLoaded", () => {
    const chatTrigger = document.querySelector(".chat-bot");
    const chatbotContainer = document.getElementById("chatbot-container");
    const closeBtn = document.getElementById("chatbot-close");
    const input = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send");
    const messages = document.getElementById("chatbot-messages");

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

    const clearBtn = document.getElementById("chatbot-clear");
    clearBtn.addEventListener("click", () => {
        messages.innerHTML = ""; // clear chat messages
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

        appendMessage("Searching...", "bot");

        try {
            const res = await fetch("http://localhost:5000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query })
            });

            const data = await res.json();
            document.querySelectorAll(".bot").forEach(el => el.remove());

            if (data.results.length === 0) {
                appendMessage("No valid info found 🤷‍♂️", "bot");
            } else {
                const buttonGroup = document.createElement("div");
                buttonGroup.className = "answer-buttons";

                function showButtons() {
                    buttonGroup.innerHTML = ""; // Clear previous content
                    data.results.slice(0, 5).forEach((r, i) => {
                        const btn = document.createElement("button");
                        btn.textContent = `Answer ${i + 1}`;
                        btn.className = "response-button";
                        btn.onclick = () => showAnswer(i);
                        buttonGroup.appendChild(btn);
                    });
                    messages.appendChild(buttonGroup);
                    messages.scrollTop = messages.scrollHeight;
                }

                function showAnswer(index) {
                    buttonGroup.innerHTML = "";

                    const answer = data.results[index];
                    appendMessage(`🔎 Answer ${index + 1} (Confidence: ${answer.score.toFixed(2)}):\n${answer.text}`, "bot");

                    const backBtn = document.createElement("button");
                    backBtn.textContent = "⬅️ Back to options";
                    backBtn.className = "back-button";
                    backBtn.onclick = () => {
                        const bubbles = document.querySelectorAll('.chat-bubble.bot:last-of-type');
                        if (bubbles.length) bubbles[bubbles.length - 1].remove(); // Remove last answer
                        showButtons();
                    };
                    buttonGroup.appendChild(backBtn);

                    messages.appendChild(buttonGroup);
                    messages.scrollTop = messages.scrollHeight;
                }

                showButtons();

                messages.appendChild(buttonGroup);
                messages.scrollTop = messages.scrollHeight;
            }
        } catch (err) {
            appendMessage("❌ Failed to fetch response.", "bot");
        }
    }
});
