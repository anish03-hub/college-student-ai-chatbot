// Initialize Lucide icons
lucide.createIcons();

const chatMessages = document.getElementById('chat-messages');
const msgInput = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');

// Handle Send
async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text) return;

    // Add User Message
    appendMessage(text, 'user');
    msgInput.value = '';
    
    // Show Typing Indicator
    const typingId = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        
        // Remove Typing Indicator
        removeTypingIndicator(typingId);
        
        if (data.ok) {
            appendMessage(data.response, 'bot');
        } else {
            appendMessage("Sorry, I'm having trouble connecting to the server.", 'bot');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        appendMessage("An error occurred. Please try again.", 'bot');
    }
}

function appendMessage(text, role) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const group = document.createElement('div');
    group.className = `message-group ${role}-group`;
    
    const row = document.createElement('div');
    row.className = `message-row ${role}-row`;
    
    let avatarHtml = '';
    if (role === 'bot') {
        avatarHtml = `<div class="msg-avatar"><i data-lucide="bot" size="18"></i></div>`;
    }
    
    const metaHtml = `
        <div class="msg-meta">
            ${time}
            ${role === 'user' ? '<span class="check-icons"><i data-lucide="check-check" size="14"></i></span>' : ''}
        </div>
    `;
    
    // Format bold text and lists if present
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    row.innerHTML = `
        ${avatarHtml}
        <div class="bubble ${role}-bubble">
            ${formattedText}
        </div>
    `;
    
    group.appendChild(row);
    const metaDiv = document.createElement('div');
    metaDiv.innerHTML = metaHtml;
    group.appendChild(metaDiv.firstElementChild);
    
    chatMessages.appendChild(group);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Re-run Lucide to render new icons
    lucide.createIcons();
}

function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const group = document.createElement('div');
    group.className = 'message-group bot-group';
    group.id = id;
    
    group.innerHTML = `
        <div class="message-row bot-row">
            <div class="msg-avatar"><i data-lucide="bot" size="18"></i></div>
            <div class="bubble bot-bubble">
                <div class="typing">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(group);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    lucide.createIcons();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

async function clearChat() {
    if (confirm("Are you sure you want to clear the conversation?")) {
        await fetch('/clear', { method: 'POST' });
        chatMessages.innerHTML = '';
        appendMessage('Hi! How can I help you today?', 'bot');
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
msgInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Focus input on load
window.addEventListener('load', () => msgInput.focus());
