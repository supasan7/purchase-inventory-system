from app import db
from datetime import datetime

class PurchaseOrderLine(db.Model):
    __tablename__ = 'purchase_order_lines'

    id         = db.Column(db.Integer, primary_key=True)
    po_id      = db.Column(db.Integer, db.ForeignKey('purchase_orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    qty        = db.Column(db.Numeric(12, 2), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint('qty > 0',         name='chk_pol_qty'),
        db.CheckConstraint('unit_price >= 0', name='chk_pol_unit_price'),
    )
