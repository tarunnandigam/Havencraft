// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart
    updateCartDisplay();

    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, parseInt(quantity));
        });
    });

    // Add to cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const productId = formData.get('product_id');
            const quantity = formData.get('quantity') || 1;
            addToCart(productId, parseInt(quantity));
        });
    });

    // Quantity update buttons in cart
    const updateButtons = document.querySelectorAll('.update-quantity');
    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const action = this.dataset.action;
            const quantityInput = document.querySelector(`input[name="quantity_${productId}"]`);

            if (quantityInput) {
                let currentQuantity = parseInt(quantityInput.value);

                if (action === 'increase') {
                    quantityInput.value = currentQuantity + 1;
                } else if (action === 'decrease' && currentQuantity > 1) {
                    quantityInput.value = currentQuantity - 1;
                }

                // Auto-update cart
                updateCartQuantity(productId, parseInt(quantityInput.value));
            }
        });
    });

    // Remove from cart buttons
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            removeFromCart(productId);
        });
    });
});

function addToCart(productId, quantity = 1) {
    // Show loading state
    const button = document.querySelector(`[data-product-id="${productId}"]`);
    if (button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
        button.disabled = true;
    }

    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${productId}&quantity=${quantity}`
    })
    .then(response => {
        if (response.ok) {
            // Update cart display
            updateCartDisplay();
            showNotification('Product added to cart!', 'success');
        } else {
            showNotification('Failed to add product to cart', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'error');
    })
    .finally(() => {
        // Restore button state
        if (button) {
            button.innerHTML = '<i class="fas fa-cart-plus me-2"></i>Add to Cart';
            button.disabled = false;
        }
    });
}

function updateCartQuantity(productId, quantity) {
    const formData = new FormData();
    formData.append(`quantity_${productId}`, quantity);

    fetch('/update_cart', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            location.reload(); // Reload to update totals
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeFromCart(productId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        fetch(`/remove_from_cart/${productId}`)
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function updateCartDisplay() {
    fetch('/api/cart')
    .then(response => response.json())
    .then(cart => {
        const totalItems = Object.values(cart).reduce((sum, quantity) => sum + quantity, 0);
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(element => {
            element.textContent = totalItems;
            element.style.display = totalItems > 0 ? 'inline' : 'none';
        });
    })
    .catch(error => {
        console.error('Error updating cart display:', error);
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Wishlist functionality
function toggleWishlist(productId) {
    fetch(`/toggle_wishlist/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const wishlistBtn = document.querySelector(`[data-wishlist-product-id="${productId}"]`);
            if (wishlistBtn) {
                const icon = wishlistBtn.querySelector('i');
                if (data.action === 'added') {
                    icon.className = 'fas fa-heart';
                    wishlistBtn.classList.add('text-danger');
                } else {
                    icon.className = 'far fa-heart';
                    wishlistBtn.classList.remove('text-danger');
                }
            }
            showNotification(
                data.action === 'added' ? 'Added to wishlist!' : 'Removed from wishlist!',
                'success'
            );
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Please log in to use wishlist', 'error');
    });
}