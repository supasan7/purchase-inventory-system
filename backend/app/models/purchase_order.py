from app import db
from datetime import datetime, date

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'

    id            = db.Column(db.Integer, primary_key=True)
    supplier_id   = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='RESTRICT'), nullable=False)
    status        = db.Column(db.String(20), nullable=False, default='draft')
    order_date    = db.Column(db.Date, nullable=False, default=date.today)
    received_date = db.Column(db.Date)
    note          = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    lines           = db.relationship('PurchaseOrderLine', backref='purchase_order', lazy=True, cascade='all, delete-orphan')
    stock_movements = db.relationship('StockMovement', backref='purchase_order', lazy=True)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('draft','confirmed','received','done','cancelled')",
            name='chk_po_status'
        ),
    )
