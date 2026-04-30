from app import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id          = db.Column(db.Integer, primary_key=True)
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, unique=True)
    on_hand_qty = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint('on_hand_qty >= 0', name='chk_inv_on_hand_qty'),
    )
