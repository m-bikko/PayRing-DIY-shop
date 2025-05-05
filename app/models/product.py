from app.models.database import db
from datetime import datetime

class KitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    rings = db.relationship('RingType', secondary='kit_ring_association', backref='kits')
    
    def __repr__(self):
        return f'<KitType {self.name}>'

class RingType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RingType {self.name}>'

class RingSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RingSize {self.size}>'

# Association table for kit types and ring types
kit_ring_association = db.Table('kit_ring_association',
    db.Column('kit_id', db.Integer, db.ForeignKey('kit_type.id'), primary_key=True),
    db.Column('ring_id', db.Integer, db.ForeignKey('ring_type.id'), primary_key=True)
)