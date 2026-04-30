# CLAUDE.md — Purchase & Inventory System

## Project Overview

Mini ERP system จำลอง business workflow ของ Odoo Purchase & Inventory module
สร้างเพื่อทำความเข้าใจ ERP logic ก่อนนำไปต่อยอดบน Odoo จริง

---

## Tech Stack

- **Backend:** Python 3.x, Flask
- **ORM:** SQLAlchemy + Flask-Migrate
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Architecture:** MVC

---

## Project Structure

```
purchase-inventory-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py        ← Flask app factory + db init
│   │   ├── models/            ← SQLAlchemy models (M)
│   │   ├── controllers/       ← Request handlers (C)
│   │   ├── routes/            ← API endpoint definitions
│   │   └── services/          ← Business logic
│   │       ├── purchase_order_service.py  ← State machine
│   │       └── stock_service.py           ← Atomic transaction
│   ├── migrations/            ← Flask-Migrate files (อย่าแก้มือ)
│   ├── database/
│   │   └── schema.sql         ← Reference schema (ไม่ได้ใช้ run จริง)
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
├── frontend/
│   ├── pages/                 ← HTML files
│   ├── css/
│   └── js/                    ← fetch calls ไปหา backend API
└── docs/
    ├── workflow.md
    └── api.md
```

---

## Architecture Rules

- **Models** — เฉพาะ SQLAlchemy class definitions และ relationships ห้ามมี business logic
- **Controllers** — รับ request, เรียก service, return response เท่านั้น
- **Services** — business logic ทั้งหมดอยู่ที่นี่ โดยเฉพาะ state machine และ atomic transaction
- **Routes** — กำหนด endpoint และผูกกับ controller เท่านั้น

---

## Coding Conventions

- ชื่อไฟล์: `snake_case` เช่น `purchase_order.py`
- ชื่อ class: `PascalCase` เช่น `PurchaseOrder`
- ชื่อ function: `snake_case` เช่น `confirm_purchase_order()`
- ชื่อ table: `snake_case` plural เช่น `purchase_orders`
- API response format ทุกตัวต้องมี `success` และ `data` หรือ `message`

```python
# Success
{"success": True, "data": {...}}

# Error
{"success": False, "message": "error description"}
```

---

## Business Rules (สำคัญมาก)

### PO State Machine

```
draft → confirmed → received → done
draft → cancelled
confirmed → cancelled
```

- ห้าม skip state เช่น draft → received ตรงๆ ไม่ได้
- ห้ามแก้ไข line items เมื่อ status ไม่ใช่ draft
- ทุก state action ต้อง validate status ก่อนเสมอ

### Atomic Transaction (ตอน Receive)

เมื่อกด receive ต้องทำใน transaction เดียวเท่านั้น:

1. อัปเดต PO status → received
2. สร้าง stock_movement record (type: in)
3. อัปเดต inventory on_hand_qty

ถ้า step ใด fail → rollback ทั้งหมด ห้ามทำแยกกัน

### Low Stock Check

หลังอัปเดต inventory ให้เช็คว่า `on_hand_qty < min_qty`
ถ้าใช่ให้ flag สินค้านั้นใน response

---

## Common Commands

```bash
# รัน backend server
cd backend
flask --app run run --debug

# สร้าง migration หลังแก้ไข model
flask --app run db migrate -m "description"
flask --app run db upgrade

# ย้อน migration
flask --app run db downgrade
```

---

## Database

- **6 tables:** products, suppliers, purchase_orders, purchase_order_lines, inventory, stock_movements
- `stock_movements` เป็น immutable log ห้ามแก้ไขหลังสร้าง
- `purchase_order_lines.unit_price` คือ snapshot ราคา ณ วันสั่งซื้อ ไม่ใช่ราคาปัจจุบัน
- `inventory` เก็บแค่ยอดปัจจุบัน ประวัติทั้งหมดอยู่ใน `stock_movements`

---

## References

- Workflow diagram: `docs/workflow.md`
- API documentation: `docs/api.md`
- Schema reference: `backend/database/schema.sql`
