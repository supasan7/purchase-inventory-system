from app import db
from datetime import datetime

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(255), nullable=False, unique=True)
    phone      = db.Column(db.String(20))
    email      = db.Column(db.String(255))
    address    = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)
