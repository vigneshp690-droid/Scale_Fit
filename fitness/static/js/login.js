/**
 * ScaleFit Login Page - JavaScript
 */

// Toggle Password Visibility
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        passwordInput.type = 'password';
        toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// Validate Mobile Number Format
function validateMobileNumber(mobile) {
    return /^\d{10}$/.test(mobile);
}

// Real-time validation feedback
document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById('username_mobile');
    const usernameCheck = document.getElementById('usernameCheck');
    const loginForm = document.getElementById('loginForm');

    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            const value = this.value.trim();
            
            if (value.length === 0) {
                usernameCheck.innerHTML = '';
            } else if (validateMobileNumber(value)) {
                usernameCheck.innerHTML = '<i class="fas fa-check-circle" style="color: #4CAF50;"></i>';
            } else if (/^[a-zA-Z0-9_]{3,}$/.test(value)) {
                usernameCheck.innerHTML = '<i class="fas fa-check-circle" style="color: #4CAF50;"></i>';
            } else if (value.length < 3) {
                usernameCheck.innerHTML = '<i class="fas fa-exclamation-circle" style="color: #ff9800;"></i>';
            } else {
                usernameCheck.innerHTML = '';
            }
        });
    }

    // Form validation on submit
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = usernameInput.value.trim();
            const password = document.getElementById('password').value;

            if (!username) {
                e.preventDefault();
                showValidationError('Please enter your username or mobile number');
                return;
            }

            if (!password) {
                e.preventDefault();
                showValidationError('Please enter your password');
                return;
            }

            // Check if username is mobile and validate format
            if (/^\d+$/.test(username)) {
                if (!validateMobileNumber(username)) {
                    e.preventDefault();
                    showValidationError('Mobile number must be exactly 10 digits');
                    return;
                }
            }

            // Show loading state
            const submitBtn = loginForm.querySelector('.btn-submit');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Signing in...</span>';

            // Reset button after timeout if needed
            setTimeout(() => {
                if (submitBtn.disabled) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            }, 10000);
        });
    }
});

// Show validation error as alert
function showValidationError(message) {
    const loginForm = document.getElementById('loginForm');
    
    // Remove existing validation alerts
    const existingAlert = loginForm.querySelector('.validation-alert');
    if (existingAlert) {
        existingAlert.remove();
    }

    // Create and insert new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-error validation-alert';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
        <button type="button" class="close-alert" onclick="this.parentElement.remove();">
            <i class="fas fa-times"></i>
        </button>
    `;

    const messagesContainer = loginForm.querySelector('.messages-container');
    if (messagesContainer) {
        messagesContainer.insertAdjacentElement('afterbegin', alertDiv);
    } else {
        loginForm.insertAdjacentElement('afterbegin', alertDiv);
    }

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.style.animation = 'slideOutAlert 0.3s ease-out';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

// Add animation for alert exit
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutAlert {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(-20px);
        }
    }

    .validation-alert {
        animation: slideInAlert 0.4s ease-out;
    }
`;
document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Enter key to submit form
    if (e.key === 'Enter') {
        const loginForm = document.getElementById('loginForm');
        if (loginForm && document.activeElement !== document.querySelector('.btn-submit')) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    }

    // Ctrl+Shift+D to toggle "Remember me"
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        const rememberMe = document.querySelector('input[name="remember_me"]');
        if (rememberMe) {
            rememberMe.checked = !rememberMe.checked;
        }
    }
});

// Auto-dismiss alerts after 5 seconds
window.addEventListener('load', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOutAlert 0.3s ease-out';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
});
