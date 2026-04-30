# Workflow Documentation

ระบบ Purchase & Inventory Management จำลอง business workflow ของ Odoo ERP
ประกอบด้วย 5 module หลักที่ทำงานเชื่อมกันผ่าน Core Database

---

## 1. Business Flow Overview

ภาพรวมการทำงานของทุก module ตั้งแต่ต้นจนจบ

```mermaid
flowchart TD
    A([Start]) --> B[Product Management]
    A --> C[Supplier Management]

    B --> D[สร้าง Purchase Order\nstatus: draft]
    C --> D

    D --> E{PO Action?}
    E -->|confirm| F[Confirmed PO\nlock การแก้ไข]
    E -->|cancel| CA([Cancelled])

    F --> G{PO Action?}
    G -->|cancel| CA
    G -->|receive| H[Received PO\nบันทึกวันรับ + qty จริง]

    H --> I[/Atomic Transaction/]
    I --> J[สร้าง Stock Movement\ntype: in]
    I --> K[อัปเดต Inventory\non_hand_qty + qty]

    J --> L{qty < min_qty?}
    K --> L
    L -->|yes| M[⚠ Low Stock Alert]
    L -->|no| N[Done PO]
    M --> N

    N --> O([Dashboard\nKPI & Summary])

    style F fill:#FAEEDA,stroke:#854F0B,color:#412402
    style H fill:#E6F1FB,stroke:#185FA5,color:#042C53
    style I fill:#EEEDFE,stroke:#534AB7,color:#26215C
    style J fill:#EEEDFE,stroke:#534AB7,color:#26215C
    style K fill:#EAF3DE,stroke:#3B6D11,color:#173404
    style CA fill:#FCEBEB,stroke:#A32D2D,color:#501313
    style N fill:#EAF3DE,stroke:#3B6D11,color:#173404
    style M fill:#FAEEDA,stroke:#854F0B,color:#412402
```

---

## 2. Purchase Order — State Machine

แสดงสถานะทั้งหมดของ PO และเงื่อนไขการเปลี่ยนสถานะ

```mermaid
stateDiagram-v2
    [*] --> Draft : สร้าง PO ใหม่

    Draft --> Confirmed : confirm()\nมี line items อย่างน้อย 1 รายการ
    Draft --> Cancelled : cancel()

    Confirmed --> Received : receive()\nบันทึกวันรับ + qty จริง
    Confirmed --> Cancelled : cancel()

    Received --> Done : done()\nตรวจสอบครบถ้วน

    Cancelled --> [*]
    Done --> [*]

    note right of Draft
        แก้ไขได้ทุกอย่าง
        เพิ่ม/ลบ line items ได้
        ยังไม่มีผลต่อ stock
    end note

    note right of Confirmed
        lock การแก้ไข
        ส่ง PO ให้ supplier ได้
        ยังไม่มีผลต่อ stock
    end note

    note right of Received
        stock เพิ่มขึ้นทันที
        สร้าง stock_movement อัตโนมัติ
        เช็ค low stock alert
    end note
```

---

## 3. Atomic Transaction — เมื่อรับสินค้า

เมื่อกด receive ระบบต้องทำ 3 อย่างนี้พร้อมกันใน transaction เดียว
ถ้า step ใด fail จะ rollback ทั้งหมด

```mermaid
sequenceDiagram
    actor User
    participant PO as Purchase Order
    participant DB as Database Transaction
    participant SM as Stock Movement
    participant INV as Inventory

    User->>PO: PATCH /orders/:id/receive
    PO->>DB: BEGIN TRANSACTION

    DB->>PO: UPDATE status = 'received'
    DB->>SM: INSERT stock_movement (type: in)
    DB->>INV: UPDATE on_hand_qty + qty

    alt ทุก step สำเร็จ
        DB->>PO: COMMIT
        PO->>User: 200 OK
    else มี step ใด fail
        DB->>PO: ROLLBACK
        PO->>User: 500 Error
    end
```

---

## 4. Module Relationships

ความสัมพันธ์ระหว่าง module และ database tables

```mermaid
erDiagram
    PRODUCTS ||--o{ PURCHASE_ORDER_LINES : "อยู่ใน"
    PRODUCTS ||--|| INVENTORY : "ติดตามสต็อก"
    PRODUCTS ||--o{ STOCK_MOVEMENTS : "บันทึกการเคลื่อนไหว"

    SUPPLIERS ||--o{ PURCHASE_ORDERS : "ออก PO ให้"

    PURCHASE_ORDERS ||--o{ PURCHASE_ORDER_LINES : "มี"
    PURCHASE_ORDERS ||--o{ STOCK_MOVEMENTS : "trigger"

    PRODUCTS {
        int id PK
        string name
        string unit
        decimal unit_price
        decimal min_qty
    }

    SUPPLIERS {
        int id PK
        string name
        string phone
        string email
        string address
    }

    PURCHASE_ORDERS {
        int id PK
        int supplier_id FK
        string status
        date order_date
        date received_date
    }

    PURCHASE_ORDER_LINES {
        int id PK
        int po_id FK
        int product_id FK
        decimal qty
        decimal unit_price
    }

    INVENTORY {
        int id PK
        int product_id FK
        decimal on_hand_qty
    }

    STOCK_MOVEMENTS {
        int id PK
        int product_id FK
        int po_id FK
        string type
        decimal qty
    }
```

---

## 5. API Flow Summary

สรุป endpoint หลักของแต่ละ module

```mermaid
flowchart LR
    subgraph Product["Product Management"]
        P1[GET /products]
        P2[POST /products]
        P3[PUT /products/:id]
        P4[DELETE /products/:id]
    end

    subgraph Supplier["Supplier Management"]
        S1[GET /suppliers]
        S2[POST /suppliers]
        S3[PUT /suppliers/:id]
    end

    subgraph PO["Purchase Order"]
        PO1[POST /purchase/orders]
        PO2[PATCH /orders/:id/confirm]
        PO3[PATCH /orders/:id/receive]
        PO4[PATCH /orders/:id/cancel]
    end

    subgraph Inv["Inventory"]
        I1[GET /inventory]
        I2[GET /inventory/low-stock]
        I3[GET /inventory/:id/movements]
    end

    Product --> PO
    Supplier --> PO
    PO -->|receive trigger| Inv
```
