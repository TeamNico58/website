document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const referrerAlert = document.getElementById('referrer-alert');
    const keySection = document.getElementById('key-section');
    const generateSection = document.getElementById('generate-section');
    const generateBtn = document.getElementById('generate-btn');
    const keyDisplay = document.getElementById('key-display');
    const copyBtn = document.getElementById('copy-btn');
    const revokeBtn = document.getElementById('revoke-btn');
    const timeRemaining = document.getElementById('time-remaining');

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Check if referrer is from Linkvertise
    function isValidReferrer() {
        const referrer = document.referrer;
        // For testing purposes, also allow direct access (empty referrer) or localhost
        if (!referrer || referrer.includes('localhost')) {
            console.log('Development mode: skipping referrer check');
            return true;
        }
        
        return referrer.includes('linkvertise.com');
    }

    // Generate a random key
    function generateKey() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const keyLength = 24;
        let key = '';
        
        for (let i = 0; i < keyLength; i++) {
            key += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        
        return key;
    }

    // Save key to localStorage with expiration
    function saveKey(key) {
        const now = new Date();
        const expiration = new Date(now.getTime() + 24 * 60 * 60 * 1000); // 24 hours
        
        const keyData = {
            key: key,
            expiration: expiration.getTime()
        };
        
        localStorage.setItem('secureKey', JSON.stringify(keyData));
        return keyData;
    }

    // Get key from localStorage
    function getKey() {
        const keyDataStr = localStorage.getItem('secureKey');
        if (!keyDataStr) return null;
        
        const keyData = JSON.parse(keyDataStr);
        const now = new Date().getTime();
        
        // Check if key has expired
        if (now > keyData.expiration) {
            localStorage.removeItem('secureKey');
            return null;
        }
        
        return keyData;
    }

    // Copy key to clipboard
    function copyToClipboard() {
        keyDisplay.select();
        document.execCommand('copy');
        
        // Update tooltip text
        const tooltip = bootstrap.Tooltip.getInstance(copyBtn);
        if (tooltip) {
            copyBtn.setAttribute('data-bs-original-title', 'Copied!');
            tooltip.show();
            
            // Reset tooltip after 2 seconds
            setTimeout(() => {
                copyBtn.setAttribute('data-bs-original-title', 'Copy to clipboard');
                tooltip.hide();
            }, 2000);
        }
    }

    // Format time remaining
    function formatTimeRemaining(expirationMs) {
        const now = new Date().getTime();
        const diff = expirationMs - now;
        
        if (diff <= 0) return 'Expired';
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        return `Expires in ${hours}h ${minutes}m`;
    }

    // Update the UI based on key status
    function updateUI() {
        const keyData = getKey();
        
        if (keyData) {
            // We have a valid key
            keyDisplay.value = keyData.key;
            timeRemaining.textContent = formatTimeRemaining(keyData.expiration);
            
            keySection.classList.remove('d-none');
            generateSection.classList.add('d-none');
            
            // Set up a timer to update the "time remaining" text
            updateExpirationTimer(keyData.expiration);
        } else {
            // No valid key
            keySection.classList.add('d-none');
            generateSection.classList.remove('d-none');
        }
    }

    // Update expiration timer
    let timerInterval;
    function updateExpirationTimer(expirationMs) {
        // Clear any existing timer
        if (timerInterval) clearInterval(timerInterval);
        
        // Update immediately
        timeRemaining.textContent = formatTimeRemaining(expirationMs);
        
        // Set interval to update every minute
        timerInterval = setInterval(() => {
            const now = new Date().getTime();
            
            if (now > expirationMs) {
                // Key has expired
                clearInterval(timerInterval);
                localStorage.removeItem('secureKey');
                updateUI();
            } else {
                timeRemaining.textContent = formatTimeRemaining(expirationMs);
            }
        }, 60000); // Update every minute
    }

    // Event listeners
    generateBtn.addEventListener('click', function() {
        const newKey = generateKey();
        const keyData = saveKey(newKey);
        updateUI();
    });

    copyBtn.addEventListener('click', copyToClipboard);

    revokeBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to revoke this key? This action cannot be undone.')) {
            localStorage.removeItem('secureKey');
            updateUI();
        }
    });

    // Initial setup
    if (!isValidReferrer()) {
        referrerAlert.classList.remove('d-none');
        keySection.classList.add('d-none');
        generateSection.classList.add('d-none');
    } else {
        referrerAlert.classList.add('d-none');
        updateUI();
    }
});
