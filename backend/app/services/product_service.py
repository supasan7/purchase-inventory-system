from app import db
from app.models.product import Product
from app.models.purchase_order_line import PurchaseOrderLine

def get_all_products():
    return Product.query.order_by(Product.name).all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def create_product(data):
    if not data.get('name'):
        raise ValueError('name is required')
    if data.get('unit_price', 0) < 0:
        raise ValueError('unit_price must be >= 0')
    if data.get('min_qty', 0) < 0:
        raise ValueError('min_qty must be >= 0')

    product = Product(
        name=data['name'],
        unit=data.get('unit', 'pcs'),
        unit_price=data.get('unit_price', 0),
        min_qty=data.get('min_qty', 0)
    )
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, data):
    product = Product.query.get(product_id)
    if not product:
        raise LookupError('Product not found')

    if 'name' in data and not data['name']:
        raise ValueError('name cannot be empty')
    if 'unit_price' in data and data['unit_price'] < 0:
        raise ValueError('unit_price must be >= 0')
    if 'min_qty' in data and data['min_qty'] < 0:
        raise ValueError('min_qty must be >= 0')

    if 'name' in data:
        product.name = data['name']
    if 'unit' in data:
        product.unit = data['unit']
    if 'unit_price' in data:
        product.unit_price = data['unit_price']
    if 'min_qty' in data:
        product.min_qty = data['min_qty']

    db.session.commit()
    return product

def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        raise LookupError('Product not found')

    in_use = PurchaseOrderLine.query.filter_by(product_id=product_id).first()
    if in_use:
        raise ValueError('Cannot delete product linked to purchase orders')

    db.session.delete(product)
    db.session.commit()

def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'unit': product.unit,
        'unit_price': float(product.unit_price),
        'min_qty': float(product.min_qty),
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat()
    }
