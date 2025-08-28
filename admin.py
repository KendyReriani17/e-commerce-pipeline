from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Product, Category, Order, OrderItem
from forms import ProductForm, CategoryForm
from functools import wraps

def admin_required(f):
    """Simple admin decorator - in production, implement proper authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # In a real app, check if user is authenticated and is admin
        # For demo purposes, we'll skip authentication
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='confirmed').scalar() or 0
    pending_orders = Order.query.filter_by(status='pending').count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    low_stock_products = Product.query.filter(Product.stock_quantity < 10).limit(5).all()
    
    stats = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'pending_orders': pending_orders
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin products listing"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    
    query = Product.query
    if search_query:
        query = query.filter(Product.name.contains(search_query))
    
    products_pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/products.html', 
                         products=products_pagination.items,
                         pagination=products_pagination,
                         search_query=search_query)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data,
            stock_quantity=form.stock_quantity.data,
            category_id=form.category_id.data
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{product.name}" added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(id):
    """Edit existing product"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        product.stock_quantity = form.stock_quantity.data
        product.category_id = form.category_id.data
        
        db.session.commit()
        
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', form=form, product=product)

@app.route('/admin/products/delete/<int:id>')
@admin_required
def admin_delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    
    # Check if product has any order items
    if OrderItem.query.filter_by(product_id=id).first():
        # Deactivate instead of delete if it has order history
        product.is_active = False
        db.session.commit()
        flash(f'Product "{product.name}" deactivated successfully!', 'info')
    else:
        # Safe to delete
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product.name}" deleted successfully!', 'success')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin orders listing"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders_pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', 
                         orders=orders_pagination.items,
                         pagination=orders_pagination,
                         status_filter=status_filter)

@app.route('/admin/orders/update_status/<int:id>/<status>')
@admin_required
def admin_update_order_status(id, status):
    """Update order status"""
    order = Order.query.get_or_404(id)
    
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    if status not in valid_statuses:
        flash('Invalid status!', 'error')
        return redirect(url_for('admin_orders'))
    
    order.status = status
    db.session.commit()
    
    flash(f'Order {order.order_number} status updated to {status}!', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    """Admin categories listing"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    """Add new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{category.name}" added successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html', form=form)
