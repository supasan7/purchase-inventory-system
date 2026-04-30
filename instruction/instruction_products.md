# Instruction: Products Module

## Objective

สร้าง Products module ให้ครบทั้ง Backend และ Frontend
อ้างอิง CLAUDE.md สำหรับ architecture rules และ coding conventions

---

## Context

- Framework: Flask (Python)
- ORM: SQLAlchemy (model มีอยู่แล้วที่ `app/models/product.py`)
- Architecture: MVC
- API Base URL: `http://localhost:5000/api`

---

## Backend

### Step 1: สร้าง `backend/app/services/product_service.py`

Business logic ทั้งหมดอยู่ที่นี่

```python
from app import db
from app.models.product import Product
from app.models.purchase_order_line import PurchaseOrderLine

def get_all_products():
    return Product.query.order_by(Product.name).all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def create_product(data):
    # Validate required fields
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

    # ตรวจว่ามีอยู่ใน PO ไหม
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
```

---

### Step 2: สร้าง `backend/app/controllers/product_controller.py`

รับ request จาก route แล้วเรียก service

```python
from flask import request, jsonify
from app.services import product_service

def get_all():
    products = product_service.get_all_products()
    return jsonify({
        'success': True,
        'data': [product_service.serialize_product(p) for p in products]
    })

def get_one(product_id):
    product = product_service.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    return jsonify({'success': True, 'data': product_service.serialize_product(product)})

def create():
    try:
        data = request.get_json()
        product = product_service.create_product(data)
        return jsonify({'success': True, 'data': product_service.serialize_product(product)}), 201
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def update(product_id):
    try:
        data = request.get_json()
        product = product_service.update_product(product_id, data)
        return jsonify({'success': True, 'data': product_service.serialize_product(product)})
    except LookupError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def delete(product_id):
    try:
        product_service.delete_product(product_id)
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except LookupError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
```

---

### Step 3: สร้าง `backend/app/routes/product_routes.py`

ผูก URL กับ controller

```python
from flask import Blueprint
from app.controllers import product_controller

product_bp = Blueprint('products', __name__)

product_bp.route('/', methods=['GET'])(product_controller.get_all)
product_bp.route('/<int:product_id>', methods=['GET'])(product_controller.get_one)
product_bp.route('/', methods=['POST'])(product_controller.create)
product_bp.route('/<int:product_id>', methods=['PUT'])(product_controller.update)
product_bp.route('/<int:product_id>', methods=['DELETE'])(product_controller.delete)
```

---

### Step 4: ลงทะเบียน Blueprint ใน `backend/app/__init__.py`

เพิ่ม code นี้ใน `create_app()` ก่อน `return app`

```python
from app.routes.product_routes import product_bp
app.register_blueprint(product_bp, url_prefix='/api/products')
```

---

## Frontend

### Step 5: สร้าง `frontend/js/products.js`

fetch calls ทั้งหมดสำหรับ Products

```javascript
const API_URL = "http://localhost:5000/api/products";

async function fetchProducts() {
  const res = await fetch(API_URL);
  const json = await res.json();
  return json.data;
}

async function createProduct(data) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

async function updateProduct(id, data) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

async function deleteProduct(id) {
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  return await res.json();
}
```

---

### Step 6: สร้าง `frontend/pages/products.html`

หน้า Products management ที่มี:

- ตารางแสดงสินค้าทั้งหมด (id, name, unit, unit_price, min_qty)
- ปุ่ม Add Product เปิด form เพิ่มสินค้า
- ปุ่ม Edit และ Delete ในแต่ละแถว
- Form input: name (required), unit, unit_price, min_qty
- แสดง error message เมื่อ API return error
- โหลดข้อมูลใหม่อัตโนมัติหลัง create/update/delete สำเร็จ

---

## Testing

หลังสร้างเสร็จ ทดสอบด้วย curl หรือ browser:

```bash
# ทดสอบ GET ทั้งหมด
curl http://localhost:5000/api/products

# ทดสอบ POST สร้างสินค้าใหม่
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "กระดาษ A4", "unit": "รีม", "unit_price": 120, "min_qty": 10}'

# ทดสอบ DELETE ที่ไม่มีใน PO
curl -X DELETE http://localhost:5000/api/products/1
```

---

## Expected Result

- `GET /api/products` → return list of products
- `POST /api/products` → create product, return 201
- `PUT /api/products/:id` → update product
- `DELETE /api/products/:id` → ลบได้เฉพาะที่ไม่มีใน PO
- หน้า products.html แสดงตารางและ form ได้ถูกต้อง

---

## หมายเหตุ

- อย่าเขียน business logic ใน controller ให้อยู่ใน service เท่านั้น
- ทุก endpoint ต้อง return format `{"success": true/false, "data"/"message": ...}`
- อ้างอิง `docs/api.md` สำหรับ request/response format ละเอียด
