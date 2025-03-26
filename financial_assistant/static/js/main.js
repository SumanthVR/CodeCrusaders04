document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userMessageInput = document.getElementById("user-message");
    const sendButton = document.getElementById("send-button");
    const questionButtons = document.querySelectorAll(".question-btn");
    const loadingIndicator = document.getElementById("loading");

    // Smooth scrolling for nav links
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: "smooth" });
        });
    });

    // Event listener for quick question buttons
    questionButtons.forEach(button => {
        button.addEventListener("click", function () {
            userMessageInput.value = this.getAttribute("data-question");
            userMessageInput.focus();
        });
    });

    // Function to send user message
    sendButton.addEventListener("click", async function () {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        appendMessage("You", userMessage);
        userMessageInput.value = "";

        try {
            loadingIndicator.style.display = "block"; // Show loading

            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage("FinWise", data.response);
        } catch (error) {
            appendMessage("FinWise", "⚠️ Oops! Something went wrong. Please try again.");
        } finally {
            loadingIndicator.style.display = "none"; // Hide loading
        }
    });

    // Function to append chat messages
    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", sender === "You" ? "user" : "bot");
        messageElement.innerHTML = `<div class="message-content"><strong>${sender}:</strong> ${message}</div>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
    //added code from here
      
        function sendMessage() {
            const inputField = document.getElementById("user-input");
            const chatBox = document.getElementById("chat-box");
            const userMessage = inputField.value;
            
            if (userMessage.trim() === "") return;
            
            const userDiv = document.createElement("div");
            userDiv.textContent = "You: " + userMessage;
            chatBox.appendChild(userDiv);
            inputField.value = "";
            
            fetch("https://your-backend-api.com/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                const botDiv = document.createElement("div");
                botDiv.textContent = "Bot: " + data.reply;
                chatBox.appendChild(botDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(error => console.error("Error:", error));
        }

        function checkAnswer(selected) {
            const feedback = document.getElementById("quiz-feedback");
            if (selected === 'a') {
                feedback.textContent = "Correct! A budget helps track expenses and manage finances effectively.";
                feedback.style.color = "green";
            } else {
                feedback.textContent = "Incorrect. The correct answer is A. A budget helps track expenses.";
                feedback.style.color = "red";
            }
        }
  
    }
});
