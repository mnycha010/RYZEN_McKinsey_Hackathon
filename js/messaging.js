document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const adminMessageInput = document.getElementById('adminMessage');
    const sendButton = document.getElementById('sendBtn');
    const checkboxes = document.querySelectorAll('.user-checkbox');
    const checkboxItems = document.querySelectorAll('.checkbox-item');

    // Function to check if send button should be enabled
    function checkSendButtonState() {
        const hasSelectedUsers = Array.from(checkboxes).some(checkbox => checkbox.checked);
        const hasMessage = adminMessageInput.value.trim().length > 0;
        
        sendButton.disabled = !(hasSelectedUsers && hasMessage);
    }

    // Function to handle sending messages
    function sendMessage() {
        const messageText = adminMessageInput.value.trim();
        if (!messageText) return;

        // Get all checked checkboxes
        const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        
        selectedCheckboxes.forEach(checkbox => {
            const userId = checkbox.value;
            const messageDisplay = document.getElementById(`message-display-${userId}`);
            
            if (messageDisplay) {
                // Create new message element
                const messageElement = document.createElement('div');
                messageElement.className = 'message-item message-admin';
                messageElement.textContent = `Admin: ${messageText}`;
                messageElement.style.animation = 'fadeInUp 0.4s ease';
                
                // Add message to display
                messageDisplay.appendChild(messageElement);
                
                // Scroll to bottom
                messageDisplay.scrollTop = messageDisplay.scrollHeight;
            }
            
            // Uncheck the checkbox and remove selection style
            checkbox.checked = false;
            checkbox.parentElement.classList.remove('selected');
        });

        // Clear message input and update button state
        adminMessageInput.value = '';
        checkSendButtonState();
    }

    // Add event listeners to checkboxes for visual feedback
    checkboxes.forEach((checkbox, index) => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                checkboxItems[index].classList.add('selected');
            } else {
                checkboxItems[index].classList.remove('selected');
            }
            checkSendButtonState();
        });
    });

    // Add event listener to message input
    adminMessageInput.addEventListener('input', checkSendButtonState);

    // Add event listener to send button
    sendButton.addEventListener('click', sendMessage);

    // Allow sending with Enter key (but allow Shift+Enter for new line)
    adminMessageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendButton.disabled) {
                sendMessage();
            }
        }
    });

    // Initialize button state
    checkSendButtonState();
});