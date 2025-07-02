from flask import render_template, request, session, redirect, url_for, flash, jsonify
from app import app, db
from models import Product, Category
import json

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
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = float(product.price) * quantity
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart.html', cart_products=cart_products, total=total)

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

@app.route('/checkout')
def checkout():
    """Checkout page (simplified for MVP)"""
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    # For MVP, just clear the cart and show success
    session['cart'] = {}
    session.modified = True
    flash('Order placed successfully! Thank you for your purchase.', 'success')
    return redirect(url_for('index'))

@app.context_processor
def inject_cart_count():
    """Inject cart item count into all templates"""
    cart = session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0
    return {'cart_count': cart_count}
