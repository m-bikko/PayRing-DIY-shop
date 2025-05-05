from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models.user import User
from app.models.product import KitType, RingType, RingSize
from app.models.order import Order, OrderItem
from app.models.database import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Auth routes
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

# Dashboard
@admin_bp.route('/')
@login_required
def dashboard():
    # Count statistics
    orders_count = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    kits_count = KitType.query.count()
    ring_types_count = RingType.query.count()
    ring_sizes_count = RingSize.query.count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          orders_count=orders_count,
                          pending_orders=pending_orders,
                          kits_count=kits_count,
                          ring_types_count=ring_types_count,
                          ring_sizes_count=ring_sizes_count,
                          recent_orders=recent_orders)

# Orders management
@admin_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))

# Kit Types management
@admin_bp.route('/kit-types')
@login_required
def kit_types():
    kits = KitType.query.all()
    return render_template('admin/kit_types.html', kits=kits)

@admin_bp.route('/kit-types/add', methods=['GET', 'POST'])
@login_required
def add_kit_type():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        
        if not name or not description or not price:
            flash('All fields are required', 'error')
            return redirect(url_for('admin.add_kit_type'))
        
        try:
            price = float(price)
        except ValueError:
            flash('Price must be a number', 'error')
            return redirect(url_for('admin.add_kit_type'))
        
        kit = KitType(
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )
        
        db.session.add(kit)
        db.session.commit()
        
        flash('Kit type added successfully', 'success')
        return redirect(url_for('admin.kit_types'))
    
    return render_template('admin/add_kit_type.html')

@admin_bp.route('/kit-types/<int:kit_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_kit_type(kit_id):
    kit = KitType.query.get_or_404(kit_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        
        if not name or not description or not price:
            flash('All fields are required', 'error')
            return redirect(url_for('admin.edit_kit_type', kit_id=kit_id))
        
        try:
            price = float(price)
        except ValueError:
            flash('Price must be a number', 'error')
            return redirect(url_for('admin.edit_kit_type', kit_id=kit_id))
        
        kit.name = name
        kit.description = description
        kit.price = price
        kit.image_url = image_url
        
        db.session.commit()
        
        flash('Kit type updated successfully', 'success')
        return redirect(url_for('admin.kit_types'))
    
    return render_template('admin/edit_kit_type.html', kit=kit)

@admin_bp.route('/kit-types/<int:kit_id>/delete', methods=['POST'])
@login_required
def delete_kit_type(kit_id):
    kit = KitType.query.get_or_404(kit_id)
    
    # Check if kit is used in any order
    order_items = OrderItem.query.filter_by(kit_type_id=kit_id).first()
    if order_items:
        flash('Cannot delete kit type because it is used in orders', 'error')
        return redirect(url_for('admin.kit_types'))
    
    db.session.delete(kit)
    db.session.commit()
    
    flash('Kit type deleted successfully', 'success')
    return redirect(url_for('admin.kit_types'))

# Ring Types management
@admin_bp.route('/ring-types')
@login_required
def ring_types():
    rings = RingType.query.all()
    return render_template('admin/ring_types.html', rings=rings)

@admin_bp.route('/ring-types/add', methods=['GET', 'POST'])
@login_required
def add_ring_type():
    if request.method == 'POST':
        name = request.form.get('name')
        image_url = request.form.get('image_url')
        
        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('admin.add_ring_type'))
        
        ring = RingType(
            name=name,
            image_url=image_url
        )
        
        db.session.add(ring)
        db.session.commit()
        
        flash('Ring type added successfully', 'success')
        return redirect(url_for('admin.ring_types'))
    
    return render_template('admin/add_ring_type.html')

@admin_bp.route('/ring-types/<int:ring_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ring_type(ring_id):
    ring = RingType.query.get_or_404(ring_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        image_url = request.form.get('image_url')
        
        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('admin.edit_ring_type', ring_id=ring_id))
        
        ring.name = name
        ring.image_url = image_url
        
        db.session.commit()
        
        flash('Ring type updated successfully', 'success')
        return redirect(url_for('admin.ring_types'))
    
    return render_template('admin/edit_ring_type.html', ring=ring)

@admin_bp.route('/ring-types/<int:ring_id>/delete', methods=['POST'])
@login_required
def delete_ring_type(ring_id):
    ring = RingType.query.get_or_404(ring_id)
    
    # Check if ring type is used in any order
    order_items = OrderItem.query.filter_by(ring_type_id=ring_id).first()
    if order_items:
        flash('Cannot delete ring type because it is used in orders', 'error')
        return redirect(url_for('admin.ring_types'))
    
    db.session.delete(ring)
    db.session.commit()
    
    flash('Ring type deleted successfully', 'success')
    return redirect(url_for('admin.ring_types'))

# Ring Sizes management
@admin_bp.route('/ring-sizes')
@login_required
def ring_sizes():
    sizes = RingSize.query.all()
    return render_template('admin/ring_sizes.html', sizes=sizes)

@admin_bp.route('/ring-sizes/add', methods=['GET', 'POST'])
@login_required
def add_ring_size():
    if request.method == 'POST':
        size = request.form.get('size')
        
        if not size:
            flash('Size is required', 'error')
            return redirect(url_for('admin.add_ring_size'))
        
        ring_size = RingSize(size=size)
        
        db.session.add(ring_size)
        db.session.commit()
        
        flash('Ring size added successfully', 'success')
        return redirect(url_for('admin.ring_sizes'))
    
    return render_template('admin/add_ring_size.html')

@admin_bp.route('/ring-sizes/<int:size_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ring_size(size_id):
    ring_size = RingSize.query.get_or_404(size_id)
    
    if request.method == 'POST':
        size = request.form.get('size')
        
        if not size:
            flash('Size is required', 'error')
            return redirect(url_for('admin.edit_ring_size', size_id=size_id))
        
        ring_size.size = size
        
        db.session.commit()
        
        flash('Ring size updated successfully', 'success')
        return redirect(url_for('admin.ring_sizes'))
    
    return render_template('admin/edit_ring_size.html', ring_size=ring_size)

@admin_bp.route('/ring-sizes/<int:size_id>/delete', methods=['POST'])
@login_required
def delete_ring_size(size_id):
    ring_size = RingSize.query.get_or_404(size_id)
    
    # Check if ring size is used in any order
    order_items = OrderItem.query.filter_by(ring_size_id=size_id).first()
    if order_items:
        flash('Cannot delete ring size because it is used in orders', 'error')
        return redirect(url_for('admin.ring_sizes'))
    
    db.session.delete(ring_size)
    db.session.commit()
    
    flash('Ring size deleted successfully', 'success')
    return redirect(url_for('admin.ring_sizes'))