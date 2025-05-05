from app.models.database import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=True)
    shipping_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, processing, shipped, delivered, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    kit_type_id = db.Column(db.Integer, db.ForeignKey('kit_type.id'), nullable=False)
    ring_type_id = db.Column(db.Integer, db.ForeignKey('ring_type.id'), nullable=False)
    ring_size_id = db.Column(db.Integer, db.ForeignKey('ring_size.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationships
    kit_type = db.relationship('KitType')
    ring_type = db.relationship('RingType')
    ring_size = db.relationship('RingSize')
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'