// Form validation, loading spinner, and dynamic animations
document.addEventListener('DOMContentLoaded', () => {
    // Registration password match
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm_password').value;
            if (password !== confirm) {
                e.preventDefault();
                alert('❌ Passwords do not match!');
            }
        });
    }

    // Prediction form – show spinner on submit
    const predForm = document.getElementById('predictionForm');
    if (predForm) {
        predForm.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner"></span> Predicting...';
            btn.disabled = true;

            // Optional: restore if error (but page will reload anyway)
            // This is just for UX during submit
        });
    }

    // Animate risk meter if result exists
    const riskBar = document.querySelector('.risk-bar');
    if (riskBar) {
        const width = riskBar.style.width;
        riskBar.style.width = '0%';
        setTimeout(() => {
            riskBar.style.width = width;
        }, 100);
    }

    // Add hover effect on stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'scale(1.05)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'scale(1)';
        });
    });
});



// Close flash messages when clicking the X button
document.querySelectorAll('.alert').forEach(alert => {
    // Create close button if not already present
    if (!alert.querySelector('.alert-close')) {
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'alert-close';
        closeBtn.setAttribute('aria-label', 'Close');
        closeBtn.onclick = () => alert.remove();
        alert.appendChild(closeBtn);
    }
});