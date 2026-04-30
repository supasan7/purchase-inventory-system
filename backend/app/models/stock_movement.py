from app import db
from datetime import datetime

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'

    id         = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    po_id      = db.Column(db.Integer, db.ForeignKey('purchase_orders.id', ondelete='SET NULL'), nullable=True)
    type       = db.Column(db.String(20), nullable=False)
    qty        = db.Column(db.Numeric(12, 2), nullable=False)
    note       = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("type IN ('in','out','adjustment')", name='chk_sm_type'),
        db.CheckConstraint('qty > 0',                          name='chk_sm_qty'),
    )
