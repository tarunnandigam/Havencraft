// Main JavaScript functionality for Artisan Marketplace

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize image lazy loading
    initializeLazyLoading();
    
    // Initialize product filtering
    initializeProductFiltering();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize animations
    initializeAnimations();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Lazy loading for images
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

// Product filtering functionality
function initializeProductFiltering() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter products
            productCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Enhanced search functionality
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const searchForm = document.querySelector('form[action*="products"]');
    
    if (searchInput && searchForm) {
        let searchTimeout;
        
        // Auto-submit search after typing stops
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    searchForm.submit();
                }
            }, 500);
        });
        
        // Clear search functionality
        const clearButton = document.createElement('button');
        clearButton.type = 'button';
        clearButton.className = 'btn btn-outline-secondary btn-sm ms-1';
        clearButton.innerHTML = '<i class="fas fa-times"></i>';
        clearButton.title = 'Clear search';
        
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            searchForm.submit();
        });
        
        if (searchInput.value) {
            searchInput.parentNode.appendChild(clearButton);
        }
    }
}

// Animation initialization
function initializeAnimations() {
    // Fade in animation for cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = `${Math.random() * 0.3}s`;
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.card, .product-card').forEach(card => {
        cardObserver.observe(card);
    });
}

// Product gallery functionality
function initializeProductGallery() {
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.gallery-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Update main image
                mainImage.src = this.src;
                
                // Update active thumbnail
                thumbnails.forEach(thumb => thumb.classList.remove('active'));
                this.classList.add('active');
                
                // Add loading effect
                mainImage.style.opacity = '0.5';
                setTimeout(() => {
                    mainImage.style.opacity = '1';
                }, 200);
            });
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
            }
            form.classList.add('was-validated');
        });
    });
}

// Loading states for buttons
function initializeLoadingStates() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = form.querySelector('.btn[type="submit"]');
            if (button) {
                button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
                button.disabled = true;
            }
        });
    });
}

// Utility functions
const Utils = {
    // Format price
    formatPrice(price) {
        return `$${parseFloat(price).toFixed(2)}`;
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show notification
    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 100px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    },
    
    // Animate element
    animateElement(element, animation) {
        element.classList.add(animation);
        element.addEventListener('animationend', () => {
            element.classList.remove(animation);
        }, { once: true });
    }
};

// Global error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // You could send this to an error reporting service
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log(`Page load time: ${perfData.loadEventEnd - perfData.loadEventStart}ms`);
        }, 0);
    });
}

// Add CSS for animations
const animationCSS = `
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;

// Inject animation CSS
if (!document.getElementById('animation-styles')) {
    const style = document.createElement('style');
    style.id = 'animation-styles';
    style.textContent = animationCSS;
    document.head.appendChild(style);
}

// Initialize gallery when on product detail page
if (window.location.pathname.includes('/product/')) {
    document.addEventListener('DOMContentLoaded', initializeProductGallery);
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
    initializeLoadingStates();
});
