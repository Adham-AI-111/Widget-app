// Flash Messages JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash messages
    initFlashMessages();
});

function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add auto-hide functionality
        autoHideMessage(message);
        
        // Add click to dismiss functionality
        message.addEventListener('click', function(e) {
            if (e.target.classList.contains('flash-close')) {
                return; // Don't trigger if clicking the close button
            }
            dismissMessage(message);
        });
        
        // Add keyboard support
        message.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                dismissMessage(message);
            }
        });
        
        // Make message focusable
        message.setAttribute('tabindex', '0');
    });
}

function autoHideMessage(message) {
    // Auto-hide after 5 seconds for success and info messages
    const messageType = message.className;
    if (messageType.includes('flash-success') || messageType.includes('flash-info')) {
        setTimeout(() => {
            dismissMessage(message);
        }, 5000);
    }
    
    // Auto-hide after 8 seconds for warning messages
    if (messageType.includes('flash-warning')) {
        setTimeout(() => {
            dismissMessage(message);
        }, 8000);
    }
    
    // Error messages don't auto-hide - user must dismiss them
}

function dismissMessage(message) {
    // Add removing class for animation
    message.classList.add('removing');
    
    // Remove message after animation completes
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300);
}

// Function to create and show a new flash message
function showFlashMessage(message, type = 'info') {
    const container = document.querySelector('.flash-messages-container');
    if (!container) return;
    
    const messageElement = document.createElement('div');
    messageElement.className = `flash-message flash-${type}`;
    
    const icon = getIconForType(type);
    
    messageElement.innerHTML = `
        <div class="flash-content">
            <span class="flash-icon">${icon}</span>
            <span class="flash-text">${message}</span>
        </div>
        <button class="flash-close" onclick="dismissMessage(this.parentElement)">×</button>
    `;
    
    container.appendChild(messageElement);
    
    // Initialize the new message
    initFlashMessages();
}

function getIconForType(type) {
    const icons = {
        'success': '✅',
        'error': '⚠️',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    return icons[type] || icons['info'];
}

// Global function to show flash messages from anywhere
window.showFlashMessage = showFlashMessage;
window.dismissMessage = dismissMessage; 