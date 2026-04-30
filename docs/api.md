# API Documentation

Base URL: `http://localhost:5000/api`

Response format ทุก endpoint:

```json
// Success
{ "success": true, "data": {...} }

// Error
{ "success": false, "message": "error description" }
```

---

## 1. Products

### GET /products

ดึงสินค้าทั้งหมด

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "กระดาษ A4",
      "unit": "รีม",
      "unit_price": 120.0,
      "min_qty": 10.0,
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

---

### GET /products/:id

ดึงสินค้าตาม id

**Response**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "กระดาษ A4",
    "unit": "รีม",
    "unit_price": 120.0,
    "min_qty": 10.0
  }
}
```

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Product not found |

---

### POST /products

เพิ่มสินค้าใหม่

**Request Body**

```json
{
  "name": "กระดาษ A4",
  "unit": "รีม",
  "unit_price": 120.0,
  "min_qty": 10.0
}
```

**Validation**

- `name` — required
- `unit_price` — required, >= 0
- `min_qty` — required, >= 0

**Response** `201 Created`

```json
{
  "success": true,
  "data": { "id": 1, "name": "กระดาษ A4", ... }
}
```

**Error Cases**
| Status | Message |
|--------|---------|
| 400 | name is required |
| 400 | unit_price must be >= 0 |

---

### PUT /products/:id

แก้ไขสินค้า

**Request Body** (ส่งแค่ field ที่ต้องการแก้)

```json
{
  "unit_price": 150.0
}
```

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Product not found |
| 400 | Cannot delete product with existing purchase orders |

---

### DELETE /products/:id

ลบสินค้า (ลบได้เฉพาะที่ไม่มีใน PO ใดๆ)

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Product not found |
| 400 | Cannot delete product linked to purchase orders |

---

## 2. Suppliers

### GET /suppliers

ดึงซัพพลายเออร์ทั้งหมด

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "บริษัท ออฟฟิศมาร์ท จำกัด",
      "phone": "02-xxx-xxxx",
      "email": "contact@officemart.com",
      "address": "กรุงเทพฯ"
    }
  ]
}
```

---

### GET /suppliers/:id

ดึงซัพพลายเออร์ตาม id

---

### POST /suppliers

เพิ่มซัพพลายเออร์ใหม่

**Request Body**

```json
{
  "name": "บริษัท ออฟฟิศมาร์ท จำกัด",
  "phone": "02-xxx-xxxx",
  "email": "contact@officemart.com",
  "address": "กรุงเทพฯ"
}
```

**Validation**

- `name` — required, unique

**Error Cases**
| Status | Message |
|--------|---------|
| 400 | name is required |
| 400 | Supplier name already exists |

---

### PUT /suppliers/:id

แก้ไขซัพพลายเออร์

---

### DELETE /suppliers/:id

ลบซัพพลายเออร์ (ลบได้เฉพาะที่ไม่มีใน PO ใดๆ)

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Supplier not found |
| 400 | Cannot delete supplier linked to purchase orders |

---

## 3. Purchase Orders

### GET /purchase/orders

ดึง PO ทั้งหมด

**Query Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | filter by status (draft, confirmed, received, done, cancelled) |

**Example:** `GET /purchase/orders?status=draft`

**Response**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "supplier": { "id": 1, "name": "ออฟฟิศมาร์ท" },
      "status": "draft",
      "order_date": "2024-01-01",
      "total_amount": 8200.0,
      "line_count": 3
    }
  ]
}
```

---

### GET /purchase/orders/:id

ดึง PO พร้อม line items ทั้งหมด

**Response**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "supplier": { "id": 1, "name": "ออฟฟิศมาร์ท" },
    "status": "draft",
    "order_date": "2024-01-01",
    "received_date": null,
    "note": null,
    "total_amount": 8200.0,
    "lines": [
      {
        "id": 1,
        "product": { "id": 1, "name": "กระดาษ A4", "unit": "รีม" },
        "qty": 50,
        "unit_price": 120.0,
        "subtotal": 6000.0
      }
    ]
  }
}
```

---

### POST /purchase/orders

สร้าง PO ใหม่ (status เริ่มต้นเป็น draft เสมอ)

**Request Body**

```json
{
  "supplier_id": 1,
  "note": "หมายเหตุ (optional)",
  "lines": [
    { "product_id": 1, "qty": 50, "unit_price": 120.0 },
    { "product_id": 2, "qty": 100, "unit_price": 15.0 }
  ]
}
```

**Validation**

- `supplier_id` — required, must exist
- `lines` — required, อย่างน้อย 1 รายการ
- `lines[].qty` — required, > 0
- `lines[].unit_price` — required, >= 0

**Error Cases**
| Status | Message |
|--------|---------|
| 400 | supplier_id is required |
| 404 | Supplier not found |
| 400 | lines must have at least 1 item |
| 400 | qty must be > 0 |

---

### PUT /purchase/orders/:id

แก้ไข PO (เฉพาะ status = draft เท่านั้น)

**Request Body**

```json
{
  "note": "แก้ไขหมายเหตุ",
  "lines": [{ "product_id": 1, "qty": 60, "unit_price": 120.0 }]
}
```

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Purchase order not found |
| 400 | Cannot edit purchase order with status: confirmed |

---

### PATCH /purchase/orders/:id/confirm

เปลี่ยน status: draft → confirmed

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Purchase order not found |
| 400 | Only draft orders can be confirmed |

---

### PATCH /purchase/orders/:id/receive

เปลี่ยน status: confirmed → received
พร้อม trigger atomic transaction (stock_movement + inventory)

**Request Body** (optional)

```json
{
  "note": "รับสินค้าครบแล้ว"
}
```

**Atomic Transaction**

1. อัปเดต PO status → received + บันทึก received_date
2. สร้าง stock_movement (type: in) ต่อ 1 line item
3. อัปเดต inventory on_hand_qty ต่อ 1 product

**Response**

```json
{
  "success": true,
  "data": {
    "po_id": 1,
    "status": "received",
    "low_stock_alerts": [
      { "product_id": 2, "name": "ปากกา", "on_hand_qty": 5, "min_qty": 20 }
    ]
  }
}
```

**Error Cases**
| Status | Message |
|--------|---------|
| 404 | Purchase order not found |
| 400 | Only confirmed orders can be received |
| 500 | Transaction failed, rolled back |

---

### PATCH /purchase/orders/:id/done

เปลี่ยน status: received → done

**Error Cases**
| Status | Message |
|--------|---------|
| 400 | Only received orders can be marked as done |

---

### PATCH /purchase/orders/:id/cancel

ยกเลิก PO (ทำได้จาก draft หรือ confirmed เท่านั้น)

**Error Cases**
| Status | Message |
|--------|---------|
| 400 | Cannot cancel order with status: received |

---

## 4. Inventory

### GET /inventory

ดูสต็อกสินค้าทั้งหมด

**Response**

```json
{
  "success": true,
  "data": [
    {
      "product_id": 1,
      "product_name": "กระดาษ A4",
      "unit": "รีม",
      "on_hand_qty": 50.0,
      "min_qty": 10.0,
      "is_low_stock": false
    }
  ]
}
```

---

### GET /inventory/low-stock

ดูสินค้าที่ on_hand_qty < min_qty

**Response**

```json
{
  "success": true,
  "data": [
    {
      "product_id": 2,
      "product_name": "ปากกาลูกลื่น",
      "on_hand_qty": 5.0,
      "min_qty": 20.0,
      "shortage": 15.0
    }
  ]
}
```

---

### GET /inventory/:product_id/movements

ดูประวัติการเคลื่อนไหวสต็อกของสินค้า

**Query Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | filter by type (in, out, adjustment) |

**Response**

```json
{
  "success": true,
  "data": {
    "product": { "id": 1, "name": "กระดาษ A4" },
    "on_hand_qty": 50.0,
    "movements": [
      {
        "id": 1,
        "type": "in",
        "qty": 50.0,
        "po_id": 1,
        "note": "รับสินค้าจาก PO #1",
        "created_at": "2024-01-01T10:00:00"
      }
    ]
  }
}
```

---

## 5. Dashboard

### GET /dashboard/summary

ดึงข้อมูล KPI สรุปภาพรวมระบบ

**Response**

```json
{
  "success": true,
  "data": {
    "purchase_orders": {
      "total": 10,
      "draft": 2,
      "confirmed": 3,
      "received": 1,
      "done": 3,
      "cancelled": 1
    },
    "inventory": {
      "total_products": 20,
      "low_stock_count": 3
    },
    "total_purchase_value": 125000.0
  }
}
```
