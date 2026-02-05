// function to handle sending messages
async function sendMessage() {
    // 1. Get the input element and chat container
    const inputField = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const message = inputField.value.trim(); // Get text and remove extra spaces

    // 2. Do nothing if message is empty
    if (!message) return;

    // 3. Add User Message to Chat
    appendMessage(message, 'user-message');
    inputField.value = ''; // Clear the input field

    // 4. Send message to the backend (app.py)
    try {
        // Show a temporary "Thinking..." message
        const loadingId = 'loading-' + Date.now();
        appendMessage('Thinking...', 'bot-message', loadingId);

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove "Thinking..." message
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) loadingElement.remove();

        // 5. Add Bot Response to Chat
        if (data.reply) {
            appendMessage(data.reply, 'bot-message');
        } else if (data.error) {
            appendMessage('Error: ' + data.error, 'bot-message');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage('Error converting to server.', 'bot-message');
    }
}

// Helper function to add messages to the HTML
function appendMessage(text, className, id = null) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');

    // Set the class (user-message or bot-message)
    messageDiv.className = `message ${className}`;

    // Set the text content
    messageDiv.innerText = text;

    // Add ID if provided (for removing loading indicators)
    if (id) messageDiv.id = id;

    // Add to the container
    chatContainer.appendChild(messageDiv);

    // Auto-scroll to the bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Allow sending with 'Enter' key
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
