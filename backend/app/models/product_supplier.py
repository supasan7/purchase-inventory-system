from app import db
from datetime import datetime

class ProductSupplier(db.Model):
    __tablename__ = 'product_suppliers'

    id            = db.Column(db.Integer, primary_key=True)
    product_id    = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    supplier_id   = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='RESTRICT'), nullable=False)
    price         = db.Column(db.Numeric(12, 2), nullable=False)
    min_order_qty = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    is_preferred  = db.Column(db.Boolean, nullable=False, default=False)
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('product_id', 'supplier_id', name='uq_product_supplier'),
        db.CheckConstraint('price >= 0',         name='chk_ps_price'),
        db.CheckConstraint('min_order_qty >= 0', name='chk_ps_min_order_qty'),
    )
