// Main JavaScript file for E-Commerce Store
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize cart functionality
    initializeCart();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize image lazy loading
    initializeLazyLoading();
    
    // Initialize scroll to top
    initializeScrollToTop();
});

// Cart functionality
function initializeCart() {
    // Update cart badge on page load
    updateCartBadge();
    
    // Add to cart form handling
    const addToCartForms = document.querySelectorAll('form[action*="add_to_cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
            submitBtn.disabled = true;
            
            // Reset after 2 seconds (form will submit normally)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    });
    
    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 100;
            const value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
                showToast('Minimum quantity is ' + min, 'warning');
            } else if (value > max) {
                this.value = max;
                showToast('Maximum quantity is ' + max, 'warning');
            }
        });
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        // Add search suggestions (simple implementation)
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if (query.length > 2) {
                // Here you could implement search suggestions
                // For now, we'll just validate the input
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
            }
        });
    }
    
    // Category filter handling
    const categorySelect = document.querySelector('select[name="category"]');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            // Auto-submit form when category changes
            if (this.value !== '') {
                this.closest('form').submit();
            }
        });
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showToast('Please fill in all required fields correctly', 'error');
            }
            form.classList.add('was-validated');
        });
    });
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.setCustomValidity('Please enter a valid email address');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                if (this.value) this.classList.add('is-valid');
            }
        });
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Kenyan phone formatting (+254 XXX XXX XXX)
            let value = this.value.replace(/\D/g, '');
            if (value.startsWith('254')) {
                value = value.substring(3); // Remove 254 prefix
            } else if (value.startsWith('0')) {
                value = value.substring(1); // Remove leading 0
            }
            
            if (value.length >= 6) {
                value = '+254 ' + value.replace(/(\d{3})(\d{3})(\d{3})/, '$1 $2 $3');
            } else if (value.length >= 3) {
                value = '+254 ' + value.replace(/(\d{3})(\d{0,3})/, '$1 $2');
            } else if (value.length > 0) {
                value = '+254 ' + value;
            }
            this.value = value;
        });
    });
}

// Image lazy loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Scroll to top functionality
function initializeScrollToTop() {
    // Create scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollBtn.className = 'btn btn-primary scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
    `;
    document.body.appendChild(scrollBtn);
    
    // Show/hide scroll button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
    
    // Scroll to top on click
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Utility functions
function updateCartBadge() {
    // This would typically fetch cart count from server
    // For now, we'll use the value from the template
    const cartBadge = document.querySelector('.navbar .badge');
    if (cartBadge && cartBadge.textContent === '0') {
        cartBadge.style.display = 'none';
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 1060; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// Product image error handling
function handleImageError(img) {
    img.style.display = 'none';
    const placeholder = img.parentNode.querySelector('.image-placeholder');
    if (placeholder) {
        placeholder.style.display = 'flex';
    }
}

// Price formatting
function formatPrice(price) {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency',
        currency: 'KES',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(price);
}

// Local storage helpers
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
        console.warn('LocalStorage not available');
    }
}

function getFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.warn('LocalStorage not available');
        return null;
    }
}

// Product quick view functionality
function openQuickView(productId) {
    // This would fetch product details and show in modal
    showToast('Quick view coming soon!', 'info');
}

// Wishlist functionality (future enhancement)
function toggleWishlist(productId) {
    showToast('Wishlist feature coming soon!', 'info');
}

// Compare products functionality (future enhancement)
function addToCompare(productId) {
    showToast('Compare feature coming soon!', 'info');
}

// Admin specific functions
if (window.location.pathname.includes('/admin')) {
    document.addEventListener('DOMContentLoaded', function() {
        initializeAdminFeatures();
    });
}

function initializeAdminFeatures() {
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-save functionality for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Save to localStorage as draft
                const formData = new FormData(form);
                const formObject = {};
                formData.forEach((value, key) => {
                    formObject[key] = value;
                });
                saveToLocalStorage('draft_' + form.action, formObject);
            });
        });
    });
}

// Export functions for global use
window.ecommerceApp = {
    showToast,
    formatPrice,
    handleImageError,
    openQuickView,
    toggleWishlist,
    addToCompare
};
