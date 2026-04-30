# Instruction: Setup Flask-Migrate + SQLAlchemy

## Objective

ติดตั้งและ setup Flask-Migrate + SQLAlchemy สำหรับโปรเจค purchase-inventory-system
โดยแปลง schema.sql ที่ออกแบบไว้เป็น SQLAlchemy models แล้วสร้าง migration files

---

## Context

- Framework: Flask (Python)
- Database: PostgreSQL
- Architecture: MVC
- โปรเจคอยู่ที่ folder: `backend/`

---

## Step 1: ติดตั้ง dependencies

เพิ่มใน `backend/requirements.txt`

```
Flask
Flask-SQLAlchemy
Flask-Migrate
psycopg2-binary
python-dotenv
```

รัน:

```bash
cd backend
pip install -r requirements.txt
```

---

## Step 2: สร้าง config.py

สร้างไฟล์ `backend/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## Step 3: สร้าง .env.example

สร้างไฟล์ `backend/.env.example`

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=purchase_inventory
DB_USER=postgres
DB_PASSWORD=yourpassword
```

---

## Step 4: สร้าง app/**init**.py

สร้างไฟล์ `backend/app/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import product, supplier, purchase_order, purchase_order_line, inventory, stock_movement

    return app
```

---

## Step 5: สร้าง SQLAlchemy Models

### `backend/app/models/product.py`

```python
from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False)
    unit        = db.Column(db.String(50), nullable=False, default='pcs')
    unit_price  = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    min_qty     = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    po_lines        = db.relationship('PurchaseOrderLine', backref='product', lazy=True)
    inventory       = db.relationship('Inventory', backref='product', uselist=False)
    stock_movements = db.relationship('StockMovement', backref='product', lazy=True)

    __table_args__ = (
        db.CheckConstraint('unit_price >= 0', name='chk_products_unit_price'),
        db.CheckConstraint('min_qty >= 0',    name='chk_products_min_qty'),
    )
```

### `backend/app/models/supplier.py`

```python
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
```

### `backend/app/models/purchase_order.py`

```python
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
```

### `backend/app/models/purchase_order_line.py`

```python
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
        db.CheckConstraint('qty > 0',        name='chk_pol_qty'),
        db.CheckConstraint('unit_price >= 0', name='chk_pol_unit_price'),
    )
```

### `backend/app/models/inventory.py`

```python
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
```

### `backend/app/models/stock_movement.py`

```python
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
        db.CheckConstraint('qty > 0', name='chk_sm_qty'),
    )
```

---

## Step 6: สร้าง run.py

สร้างไฟล์ `backend/run.py`

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Step 7: รัน Migration

```bash
cd backend

# copy .env.example เป็น .env แล้วแก้ค่า DB
cp .env.example .env

# สร้าง migrations folder
flask --app run db init

# สร้าง migration file จาก models
flask --app run db migrate -m "initial schema"

# สร้าง table จริงใน database
flask --app run db upgrade
```

---

## Expected Result

หลังรัน `flask db upgrade` แล้ว database จะมี table ครบ 6 ตาราง:

- `products`
- `suppliers`
- `purchase_orders`
- `purchase_order_lines`
- `inventory`
- `stock_movements`

และมี folder `backend/migrations/` พร้อม migration files

---

## หมายเหตุ

- อย่าแก้ไขไฟล์ใน `migrations/versions/` ด้วยมือ
- ทุกครั้งที่แก้ไข model ให้รัน `flask db migrate` แล้วตามด้วย `flask db upgrade`
- ห้าม commit ไฟล์ `.env` ขึ้น GitHub
