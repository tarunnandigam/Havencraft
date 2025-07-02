// Cart functionality for Artisan Marketplace
class Cart {
    constructor() {
        this.items = this.loadCart();
        this.updateCartUI();
        this.bindEvents();
    }

    // Load cart from sessionStorage and sync with server
    loadCart() {
        try {
            // Load from sessionStorage as fallback
            const cart = sessionStorage.getItem('cart');
            return cart ? JSON.parse(cart) : {};
        } catch (error) {
            console.error('Error loading cart:', error);
            return {};
        }
    }

    // Sync cart with server
    async syncWithServer() {
        try {
            const response = await fetch('/api/cart');
            if (response.ok) {
                const serverCart = await response.json();
                this.items = serverCart;
                this.saveCart();
                this.updateCartUI();
            }
        } catch (error) {
            console.error('Error syncing cart with server:', error);
        }
    }

    // Save cart to sessionStorage
    saveCart() {
        try {
            sessionStorage.setItem('cart', JSON.stringify(this.items));
        } catch (error) {
            console.error('Error saving cart:', error);
        }
    }

    // Add item to cart
    async addItem(productId, quantity = 1) {
        try {
            const formData = new FormData();
            formData.append('product_id', productId);
            formData.append('quantity', quantity);

            const response = await fetch('/add_to_cart', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Update local cart after successful server update
                if (this.items[productId]) {
                    this.items[productId] += quantity;
                } else {
                    this.items[productId] = quantity;
                }
                this.saveCart();
                this.updateCartUI();
                this.showCartNotification('Item added to cart!', 'success');
            } else {
                this.showCartNotification('Failed to add item to cart', 'error');
            }
        } catch (error) {
            console.error('Error adding item to cart:', error);
            this.showCartNotification('Failed to add item to cart', 'error');
        }
    }

    // Remove item from cart
    async removeItem(productId) {
        try {
            const response = await fetch(`/remove_from_cart/${productId}`);

            if (response.ok) {
                // Update local cart after successful server update
                if (this.items[productId]) {
                    delete this.items[productId];
                    this.saveCart();
                    this.updateCartUI();
                    this.showCartNotification('Item removed from cart', 'warning');
                }
            } else {
                this.showCartNotification('Failed to remove item from cart', 'error');
            }
        } catch (error) {
            console.error('Error removing item from cart:', error);
            this.showCartNotification('Failed to remove item from cart', 'error');
        }
    }

    // Update item quantity
    updateQuantity(productId, quantity) {
        if (quantity <= 0) {
            this.removeItem(productId);
        } else {
            this.items[productId] = quantity;
            this.saveCart();
            this.updateCartUI();
        }
    }

    // Get total item count
    getTotalCount() {
        return Object.values(this.items).reduce((total, quantity) => total + quantity, 0);
    }

    // Update cart UI elements
    updateCartUI() {
        const cartCount = this.getTotalCount();
        const cartBadges = document.querySelectorAll('.cart-count, .badge');

        cartBadges.forEach(badge => {
            if (badge.classList.contains('cart-count') || badge.closest('.btn')) {
                if (cartCount > 0) {
                    badge.textContent = cartCount;
                    badge.style.display = 'inline';
                } else {
                    badge.style.display = 'none';
                }
            }
        });

        // Update cart icon animation
        const cartIcon = document.querySelector('.fa-shopping-cart');
        if (cartIcon && cartCount > 0) {
            cartIcon.classList.add('cart-bounce');
            setTimeout(() => cartIcon.classList.remove('cart-bounce'), 300);
        }
    }

    // Show cart notification
    showCartNotification(message, type = 'success') {
        // Create notification element
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

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    // Bind events
    bindEvents() {
        // Add to cart form submissions
        document.addEventListener('submit', (e) => {
            if (e.target.classList.contains('add-to-cart-form') || e.target.action?.includes('add_to_cart')) {
                e.preventDefault();
                const formData = new FormData(e.target);
                const productId = formData.get('product_id');
                const quantity = parseInt(formData.get('quantity') || 1);

                if (productId) {
                    this.addItem(productId, quantity);
                }
            }
        });

        // Add to cart buttons with data attributes
        document.addEventListener('click', (e) => {
            if (e.target.matches('.add-to-cart, .add-to-cart *')) {
                const button = e.target.closest('.add-to-cart') || e.target;
                const productId = button.dataset.productId;
                const quantity = parseInt(button.dataset.quantity || 1);

                if (productId) {
                    e.preventDefault();
                    this.addItem(productId, quantity);
                }
            }
        });

        // Quantity change events in cart
        document.addEventListener('change', (e) => {
            if (e.target.matches('input[name^="quantity_"]')) {
                const productId = e.target.name.replace('quantity_', '');
                const quantity = parseInt(e.target.value);
                this.updateQuantity(productId, quantity);
            }
        });

        // Quick quantity buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.qty-decrease')) {
                const input = e.target.nextElementSibling;
                const currentValue = parseInt(input.value);
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    input.dispatchEvent(new Event('change'));
                }
            }

            if (e.target.matches('.qty-increase')) {
                const input = e.target.previousElementSibling;
                const currentValue = parseInt(input.value);
                const maxValue = parseInt(input.max) || 999;
                if (currentValue < maxValue) {
                    input.value = currentValue + 1;
                    input.dispatchEvent(new Event('change'));
                }
            }
        });
    }
}

// Cart animation CSS
const cartAnimationCSS = `
    .cart-bounce {
        animation: cartBounce 0.3s ease-in-out;
    }
    
    @keyframes cartBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .cart-item-enter {
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = cartAnimationCSS;
document.head.appendChild(style);

// Initialize cart when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    window.cart = new Cart();
    await window.cart.syncWithServer();
});

// Quantity control functions for cart page
function increaseQuantity(productId, maxQty) {
    const input = document.getElementById(`qty_${productId}`);
    const currentValue = parseInt(input.value);
    if (currentValue < maxQty) {
        input.value = currentValue + 1;
    }
}

function decreaseQuantity(productId) {
    const input = document.getElementById(`qty_${productId}`);
    const currentValue = parseInt(input.value);
    if (currentValue > 1) {
        input.value = currentValue - 1;
    }
}

// Enhanced cart functionality for product pages
async function addToCartWithAnimation(productId, quantity = 1) {
    if (window.cart) {
        // Add visual feedback
        const button = event.target;
        const originalText = button.innerHTML;
        
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Adding...';
        button.disabled = true;
        
        try {
            await window.cart.addItem(productId, quantity);
            
            button.innerHTML = '<i class="fas fa-check me-1"></i>Added!';
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.disabled = false;
            }, 1500);
        } catch (error) {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }
}

// Cart persistence across page loads
window.addEventListener('beforeunload', () => {
    if (window.cart) {
        window.cart.saveCart();
    }
});