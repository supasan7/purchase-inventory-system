from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(255), nullable=False)
    unit       = db.Column(db.String(50), nullable=False, default='pcs')
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    min_qty    = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    po_lines        = db.relationship('PurchaseOrderLine', backref='product', lazy=True)
    inventory       = db.relationship('Inventory', backref='product', uselist=False)
    stock_movements = db.relationship('StockMovement', backref='product', lazy=True)

    __table_args__ = (
        db.CheckConstraint('unit_price >= 0', name='chk_products_unit_price'),
        db.CheckConstraint('min_qty >= 0',    name='chk_products_min_qty'),
    )
