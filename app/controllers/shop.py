from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from app.models.product import KitType, RingType, RingSize
from app.models.order import Order, OrderItem
from app.models.database import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def shop_index():
    kits = KitType.query.all()
    return render_template('shop/index.html', kits=kits)

@shop_bp.route('/kit/<int:kit_id>')
def kit_detail(kit_id):
    kit = KitType.query.get_or_404(kit_id)
    ring_types = RingType.query.all()
    ring_sizes = RingSize.query.all()
    return render_template('shop/kit_detail.html', kit=kit, ring_types=ring_types, ring_sizes=ring_sizes)

@shop_bp.route('/api/kit/<int:kit_id>')
def api_kit_detail(kit_id):
    kit = KitType.query.get_or_404(kit_id)
    return jsonify({
        'id': kit.id,
        'name': kit.name,
        'description': kit.description,
        'price': kit.price,
        'image_url': kit.image_url
    })

@shop_bp.route('/api/ring-types')
def api_ring_types():
    ring_types = RingType.query.all()
    return jsonify([{
        'id': ring.id,
        'name': ring.name,
        'image_url': ring.image_url
    } for ring in ring_types])

@shop_bp.route('/api/ring-sizes')
def api_ring_sizes():
    ring_sizes = RingSize.query.all()
    return jsonify([{
        'id': size.id,
        'size': size.size
    } for size in ring_sizes])

@shop_bp.route('/order', methods=['POST'])
def create_order():
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate customer data
        customer_name = data.get('customerName')
        customer_email = data.get('customerEmail')
        customer_phone = data.get('customerPhone')
        shipping_address = data.get('shippingAddress')
        
        if not customer_name or not customer_email or not shipping_address:
            return jsonify({'error': 'Missing required customer information'}), 400
        
        # Validate order items
        items = data.get('items')
        if not items or not isinstance(items, list) or len(items) == 0:
            return jsonify({'error': 'No items in order'}), 400
        
        # Create order
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            total_amount=0,  # Will calculate below
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID without committing
        
        total_amount = 0
        
        # Process order items
        for item in items:
            kit_type_id = item.get('kitTypeId')
            ring_type_id = item.get('ringTypeId')
            ring_size_id = item.get('ringSizeId')
            quantity = item.get('quantity', 1)
            
            # Validate item data
            if not kit_type_id or not ring_type_id or not ring_size_id:
                db.session.rollback()
                return jsonify({'error': 'Missing required item information'}), 400
            
            # Verify products exist
            kit = KitType.query.get(kit_type_id)
            ring_type = RingType.query.get(ring_type_id)
            ring_size = RingSize.query.get(ring_size_id)
            
            if not kit or not ring_type or not ring_size:
                db.session.rollback()
                return jsonify({'error': 'Invalid product selection'}), 400
            
            # Create order item
            order_item = OrderItem(
                order_id=order.id,
                kit_type_id=kit_type_id,
                ring_type_id=ring_type_id,
                ring_size_id=ring_size_id,
                quantity=quantity,
                price=kit.price
            )
            
            db.session.add(order_item)
            
            # Update total amount
            total_amount += kit.price * quantity
        
        # Update order total
        order.total_amount = total_amount
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'orderId': order.id,
            'message': 'Order placed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('shop/order_confirmation.html', order=order)