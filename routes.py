from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import Product, Category, Order, OrderItem
from forms import AddToCartForm, CheckoutForm
from utils import generate_order_number, calculate_cart_total, get_cart_item_count
from sqlalchemy import or_

@app.route('/')
def index():
    """Homepage with featured products"""
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', products=featured_products, categories=categories)

@app.route('/products')
def products():
    """Product listing page with search and filtering"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    sort_by = request.args.get('sort', 'name')
    
    # Base query
    query = Product.query.filter_by(is_active=True)
    
    # Apply search filter
    if search_query:
        query = query.filter(or_(
            Product.name.contains(search_query),
            Product.description.contains(search_query)
        ))
    
    # Apply category filter
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Apply sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Product.name.asc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    
    # Paginate results
    products_pagination = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('products.html', 
                         products=products_pagination.items,
                         pagination=products_pagination,
                         categories=categories,
                         search_query=search_query,
                         selected_category=category_id,
                         sort_by=sort_by)

@app.route('/product/<int:id>')
def product_detail(id):
    """Product detail page"""
    product = Product.query.get_or_404(id)
    form = AddToCartForm()
    form.product_id.data = product.id
    
    # Get related products from same category
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    return render_template('product_detail.html', 
                         product=product, 
                         form=form, 
                         related_products=related_products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    form = AddToCartForm()
    if form.validate_on_submit():
        product_id = int(form.product_id.data)
        quantity = form.quantity.data
        
        product = Product.query.get_or_404(product_id)
        
        # Check stock availability
        if quantity > product.stock_quantity:
            flash(f'Sorry, only {product.stock_quantity} items available in stock.', 'error')
            return redirect(url_for('product_detail', id=product_id))
        
        # Initialize cart in session if not exists
        if 'cart' not in session:
            session['cart'] = []
        
        cart = session['cart']
        
        # Check if product already in cart
        item_found = False
        for item in cart:
            if item['product_id'] == product_id:
                # Update quantity if product already in cart
                new_quantity = item['quantity'] + quantity
                if new_quantity > product.stock_quantity:
                    flash(f'Cannot add more items. Maximum available: {product.stock_quantity}', 'error')
                    return redirect(url_for('product_detail', id=product_id))
                item['quantity'] = new_quantity
                item_found = True
                break
        
        if not item_found:
            # Add new item to cart
            cart.append({
                'product_id': product_id,
                'name': product.name,
                'price': float(product.price),
                'quantity': quantity,
                'image_url': product.image_url
            })
        
        session['cart'] = cart
        session.modified = True
        
        flash(f'{quantity} x {product.name} added to cart!', 'success')
        return redirect(url_for('product_detail', id=product_id))
    
    flash('Error adding product to cart.', 'error')
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = session.get('cart', [])
    total = calculate_cart_total(cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update cart item quantity"""
    quantity = int(request.form.get('quantity', 0))
    
    if 'cart' in session:
        cart = session['cart']
        for i, item in enumerate(cart):
            if item['product_id'] == product_id:
                if quantity <= 0:
                    # Remove item from cart
                    cart.pop(i)
                    flash('Item removed from cart.', 'info')
                else:
                    # Check stock availability
                    product = Product.query.get(product_id)
                    if quantity > product.stock_quantity:
                        flash(f'Only {product.stock_quantity} items available.', 'error')
                        return redirect(url_for('cart'))
                    
                    # Update quantity
                    item['quantity'] = quantity
                    flash('Cart updated successfully.', 'success')
                break
        
        session['cart'] = cart
        session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    if 'cart' in session:
        cart = session['cart']
        cart = [item for item in cart if item['product_id'] != product_id]
        session['cart'] = cart
        session.modified = True
        flash('Item removed from cart.', 'info')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    cart_items = session.get('cart', [])
    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('products'))
    
    form = CheckoutForm()
    total = calculate_cart_total(cart_items)
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            order_number=generate_order_number(),
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            shipping_address=form.shipping_address.data,
            total_amount=total,
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for item in cart_items:
            product = Product.query.get(item['product_id'])
            
            # Check stock availability one more time
            if item['quantity'] > product.stock_quantity:
                db.session.rollback()
                flash(f'Insufficient stock for {product.name}. Please update your cart.', 'error')
                return redirect(url_for('cart'))
            
            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            product.stock_quantity -= item['quantity']
        
        db.session.commit()
        
        # Clear cart
        session['cart'] = []
        session.modified = True
        
        flash(f'Order {order.order_number} placed successfully!', 'success')
        return redirect(url_for('order_success', order_number=order.order_number))
    
    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)

@app.route('/order_success/<order_number>')
def order_success(order_number):
    """Order success page"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('order_success.html', order=order)

@app.route('/orders')
def orders():
    """Orders listing for customers (simplified version)"""
    # In a real app, this would be protected by user authentication
    page = request.args.get('page', 1, type=int)
    orders_pagination = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('orders.html', orders=orders_pagination.items, pagination=orders_pagination)

# Context processor to make cart info available in all templates
@app.context_processor
def inject_cart_info():
    cart_items = session.get('cart', [])
    return {
        'cart_item_count': get_cart_item_count(cart_items),
        'cart_total': calculate_cart_total(cart_items)
    }

# API endpoints for AJAX requests
@app.route('/api/products')
def api_products():
    """API endpoint for products"""
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': float(p.price),
        'stock_quantity': p.stock_quantity,
        'category_id': p.category_id,
        'image_url': p.image_url
    } for p in products])

@app.route('/api/categories')
def api_categories():
    """API endpoint for categories"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

@app.route('/api/orders')
def api_orders():
    """API endpoint for orders"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': o.id,
        'order_number': o.order_number,
        'customer_name': o.customer_name,
        'total_amount': float(o.total_amount),
        'status': o.status,
        'created_at': o.created_at.isoformat()
    } for o in orders])
