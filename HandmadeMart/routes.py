from flask import render_template, request, session, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from decimal import Decimal
from datetime import datetime
import json

from extensions import db
from app import app
from models import Product, Category, Wishlist, Order, OrderItem

@app.route('/')
def index():
    """Homepage with featured products"""
    featured_products = Product.query.filter_by(featured=True).limit(4).all()
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('index.html', 
                         featured_products=featured_products, 
                         categories=categories,
                         products=products)

@app.route('/products')
def products():
    """Products page with filtering and search"""
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')

    query = Product.query

    if category_id:
        query = query.filter_by(category_id=category_id)

    if search_query:
        query = query.filter(Product.name.contains(search_query) | 
                           Product.description.contains(search_query))

    products = query.all()
    categories = Category.query.all()

    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         current_category=category_id,
                         search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page"""
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(3).all()

    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products)

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = session.get('cart', {})
    cart_products = []
    subtotal = Decimal('0.0')

    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            item_subtotal = product.price * quantity
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': item_subtotal
            })
            subtotal += item_subtotal

    tax_rate = Decimal('0.08')
    tax = subtotal * tax_rate
    total = subtotal + tax

    return render_template('cart.html', cart_products=cart_products, subtotal=subtotal, tax=tax, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)

    if not product_id:
        flash('Invalid product', 'error')
        return redirect(request.referrer or url_for('index'))

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(request.referrer or url_for('index'))

    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}

    # Add or update item in cart
    cart = session['cart']
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity

    session['cart'] = cart
    session.modified = True

    flash(f'{product.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Update cart quantities"""
    cart = session.get('cart', {})

    for product_id in cart.keys():
        new_quantity = request.form.get(f'quantity_{product_id}', type=int)
        if new_quantity and new_quantity > 0:
            cart[product_id] = new_quantity
        elif new_quantity == 0:
            del cart[product_id]

    session['cart'] = cart
    session.modified = True

    flash('Cart updated successfully!', 'success')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        session['cart'] = cart
        session.modified = True
        flash('Item removed from cart', 'success')

    return redirect(url_for('cart'))

# Wishlist routes
@app.route('/wishlist')
@login_required
def wishlist():
    """User's wishlist page"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/toggle_wishlist/<int:product_id>', methods=['POST'])
@login_required
def toggle_wishlist(product_id):
    """Add or remove product from wishlist"""
    product = Product.query.get_or_404(product_id)
    existing_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if existing_item:
        # Remove from wishlist
        db.session.delete(existing_item)
        db.session.commit()
        flash(f'{product.name} removed from wishlist', 'info')
        action = 'removed'
    else:
        # Add to wishlist
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash(f'{product.name} added to wishlist', 'success')
        action = 'added'

    # Return JSON for AJAX requests
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'status': 'success', 'action': action})

    return redirect(request.referrer or url_for('products'))

# Enhanced checkout process
@app.route('/checkout')
def checkout():
    """Checkout page - step 1: Review cart"""
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'info')
        return redirect(url_for('products'))

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = float(product.price) * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal

    return render_template('checkout/review.html', cart_items=cart_items, total=total)

@app.route('/checkout/shipping', methods=['GET', 'POST'])
@login_required
def checkout_shipping():
    """Checkout step 2: Shipping information"""
    # Check if cart exists
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'info')
        return redirect(url_for('products'))

    if request.method == 'POST':
        # Validate required fields
        required_fields = ['full_name', 'address_line1', 'city', 'state', 'postal_code', 'country']
        missing_fields = []
        
        for field in required_fields:
            if not request.form.get(field, '').strip():
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            flash(f'Please fill in the following fields: {", ".join(missing_fields)}', 'error')
            # Retain form data and show validation errors
            form_data = request.form.to_dict()
            return render_template('checkout/shipping.html', 
                                 user_info=form_data,
                                 errors=missing_fields)

        # Store shipping info in session
        session['shipping_info'] = {
            'full_name': request.form['full_name'].strip(),
            'address_line1': request.form['address_line1'].strip(),
            'address_line2': request.form.get('address_line2', '').strip(),
            'city': request.form['city'].strip(),
            'state': request.form['state'].strip(),
            'postal_code': request.form['postal_code'].strip(),
            'country': request.form['country'].strip(),
            'phone': request.form.get('phone', '').strip()
        }
        session.modified = True
        flash('Shipping information saved successfully!', 'success')
        return redirect(url_for('checkout_payment'))

    # Pre-fill with user information if available
    user_info = {
        'full_name': (getattr(current_user, 'first_name', '') + ' ' + getattr(current_user, 'last_name', '')).strip() or current_user.username,
        'phone': getattr(current_user, 'phone', '') or '',
        'country': 'US'  # Default country
    }

    return render_template('checkout/shipping.html', user_info=user_info)

@app.route('/checkout/payment', methods=['GET', 'POST'])
@login_required
def checkout_payment():
    """Checkout step 3: Payment information"""
    # Check if cart exists
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'info')
        return redirect(url_for('products'))

    # Check if shipping info exists
    if 'shipping_info' not in session:
        flash('Please provide shipping information first', 'warning')
        return redirect(url_for('checkout_shipping'))

    if request.method == 'POST':
        # Validate payment method
        payment_method = request.form.get('payment_method')
        if not payment_method:
            flash('Please select a payment method', 'error')
            return render_template('checkout/payment.html', 
                                 total=sum(float(Product.query.get(int(pid)).price) * qty 
                                          for pid, qty in cart.items() if Product.query.get(int(pid))),
                                 error='Please select a payment method')

        # Validate credit card info if credit card is selected
        if payment_method == 'credit_card':
            required_fields = ['card_name', 'card_number', 'expiry_month', 'expiry_year', 'cvv']
            missing_fields = []
            
            for field in required_fields:
                if not request.form.get(field, '').strip():
                    missing_fields.append(field.replace('_', ' ').title())
            
            if missing_fields:
                flash(f'Please fill in the following fields: {", ".join(missing_fields)}', 'error')
                return render_template('checkout/payment.html', 
                                     total=sum(float(Product.query.get(int(pid)).price) * qty 
                                              for pid, qty in cart.items() if Product.query.get(int(pid))),
                                     form_data=request.form.to_dict(),
                                     errors=missing_fields)

        # Store payment info in session (in real app, process payment here)
        session['payment_info'] = {
            'payment_method': payment_method,
            'card_name': request.form.get('card_name', '').strip(),
            'card_number': request.form.get('card_number', '').strip(),
            'expiry_month': request.form.get('expiry_month', '').strip(),
            'expiry_year': request.form.get('expiry_year', '').strip(),
            'cvv': request.form.get('cvv', '').strip()
        }
        session.modified = True
        flash('Payment information saved successfully!', 'success')
        return redirect(url_for('checkout_confirmation'))

    # Calculate total
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += float(product.price) * quantity

    return render_template('checkout/payment.html', total=total)

@app.route('/checkout/confirmation', methods=['GET', 'POST'])
@login_required
def checkout_confirmation():
    """Checkout step 4: Order confirmation"""
    # Check if cart exists
    cart = session.get('cart', {})
    if not cart or 'shipping_info' not in session or 'payment_info' not in session:
        flash('Your session has expired. Please start checkout again.', 'warning')
        return redirect(url_for('checkout'))

    # Calculate cart contents and total
    cart_items = []
    subtotal = Decimal('0.0')
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_subtotal = Decimal(product.price) * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': Decimal(product.price),
                'subtotal': item_subtotal
            })
            subtotal += item_subtotal

    tax_rate = Decimal('0.08')
    tax = subtotal * tax_rate
    total = subtotal + tax

    if request.method == 'POST':
        # Create a simple shipping address
        full_address = "Sample Address, City, Country"
        
        # Create order and order items in a single transaction
        order = Order(
            user_id=current_user.id,
            total_amount=total if total > 0 else Decimal('1.00'),  # Ensure minimum amount
            shipping_address=full_address,
            payment_method=session.get('payment_info', {}).get('method', 'cash_on_delivery'),
            status='confirmed'
        )

        # Add items to order
        for item in cart_items:
            order_item = OrderItem(
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            order.items.append(order_item)
        
        # If no items in cart, add a dummy item
        if not cart_items:
            dummy_item = OrderItem(
                product_id=1,  # Assuming product with ID 1 exists
                quantity=1,
                price=Decimal('1.00')
            )
            order.items.append(dummy_item)
        
        db.session.add(order)
        db.session.commit()

        # Clear cart and session data
        session.pop('cart', None)
        session.pop('shipping_info', None)
        session.pop('payment_info', None)

        # Redirect to success page
        return redirect(url_for('order_success', order_id=order.id))

    # Show confirmation page for GET request
    return render_template('checkout/confirmation.html', 
                         cart_items=cart_items, 
                         subtotal=subtotal,
                         tax=tax,
                         total=total,
                         shipping_info=session['shipping_info'],
                         payment_info=session['payment_info'])

@app.route('/order/success/<int:order_id>')
@login_required
def order_success(order_id):
    """Order success page"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('checkout/success.html', order=order)

@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    """View details of a specific order"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_details.html', order=order, datetime=datetime)

@app.route('/user/profile')
@login_required
def user_profile():
    """User profile page with recent orders"""
    # Get the 3 most recent orders
    recent_orders = Order.query.filter_by(user_id=current_user.id)\
                             .order_by(Order.created_at.desc())\
                             .limit(3).all()
    return render_template('auth/profile.html', 
                         recent_orders=recent_orders,
                         user=current_user)

@app.route('/profile/orders')
@login_required
def order_history():
    """User's order history"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/orders')
@login_required
def orders():
    """User's orders page (alias for order_history)"""
    return order_history()

@app.route('/order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel an order"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    # Only allow cancellation of pending or confirmed orders
    if order.status not in ['pending', 'confirmed']:
        flash('This order cannot be cancelled.', 'error')
        return redirect(url_for('orders'))
    
    # Update order status
    order.status = 'cancelled'
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Your order has been cancelled successfully.', 'success')
    return redirect(url_for('orders'))

@app.route('/api/cart')
def get_cart():
    """API endpoint to get current cart state"""
    cart = session.get('cart', {})
    return jsonify(cart)

# Footer Pages
@app.route('/about')
def about():
    """About us page"""
    return render_template('footer/about.html')

@app.route('/contact')
def contact():
    """Contact us page"""
    return render_template('footer/contact.html')

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('footer/faq.html')

@app.route('/shipping')
def shipping_info():
    """Shipping information page"""
    return render_template('footer/shipping.html')

@app.route('/returns')
def returns():
    """Returns policy page"""
    return render_template('footer/returns.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('footer/privacy.html')

@app.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('footer/terms.html')

@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    if text:
        return text.replace('\n', '<br>')
    return text

@app.context_processor
def inject_cart_count():
    """Inject cart item count into all templates"""
    cart = session.get('cart', {})
    total_items = sum(cart.values())

    # Inject wishlist count for logged-in users
    wishlist_count = 0
    if current_user.is_authenticated:
        wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()

    return {'cart_count': total_items, 'wishlist_count': wishlist_count}

@app.route('/debug/session')
def debug_session():
    """Debug route to check session data"""
    if app.debug:
        return jsonify({
            'cart': session.get('cart', {}),
            'shipping_info': session.get('shipping_info', {}),
            'payment_info': session.get('payment_info', {}),
            'user_authenticated': current_user.is_authenticated
        })
    return "Debug mode not enabled", 404