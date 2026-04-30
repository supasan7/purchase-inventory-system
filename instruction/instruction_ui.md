# Instruction: Mock UI Implementation

## Objective

สร้าง Frontend ให้มี layout และ design ตาม Mock UI ที่กำหนด
ประกอบด้วย Sidebar + Topbar + Content area ครอบคลุมทุก module

---

## File Structure ที่ต้องสร้าง

```
frontend/
├── css/
│   └── style.css          ← shared styles ทั้งระบบ
├── pages/
│   ├── index.html         ← entry point (redirect ไป dashboard)
│   ├── dashboard.html
│   ├── products.html      ← มีอยู่แล้ว ให้ปรับ layout ใหม่
│   ├── suppliers.html
│   ├── purchase_orders.html
│   └── inventory.html
└── js/
    ├── products.js        ← มีอยู่แล้ว
    └── (module อื่นๆ ทำทีหลัง)
```

---

## Layout Structure

ทุกหน้าใช้ layout เดียวกัน:

```
┌─────────────────────────────────────┐
│  Sidebar (180px) │  Main Content    │
│                  │  ┌─ Topbar ────┐ │
│  Mini ERP        │  │ Title  [btn]│ │
│  ─────────────   │  └────────────┘ │
│  • Dashboard     │  ┌─ Content ───┐ │
│  • Products      │  │             │ │
│  • Suppliers     │  │             │ │
│  • Purchase      │  └────────────┘ │
│  • Inventory     │                  │
└─────────────────────────────────────┘
```

---

## Step 1: สร้าง `frontend/css/style.css`

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --sidebar-width: 180px;
  --topbar-height: 48px;
  --color-primary: #1a1a1a;
  --color-secondary: #f5f5f3;
  --color-border: rgba(0, 0, 0, 0.12);
  --color-text: #1a1a1a;
  --color-text-muted: #6b6b68;
  --color-text-hint: #9a9a96;
  --color-white: #ffffff;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 13px;
  color: var(--color-text);
  background: var(--color-white);
  height: 100vh;
  display: flex;
  overflow: hidden;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  border-right: 0.5px solid var(--color-border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-logo {
  padding: 14px 16px;
  font-size: 14px;
  font-weight: 500;
  border-bottom: 0.5px solid var(--color-border);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 12px;
  text-decoration: none;
  transition: background 0.1s;
}

.nav-item:hover {
  background: var(--color-secondary);
}

.nav-item.active {
  background: var(--color-secondary);
  color: var(--color-text);
  font-weight: 500;
}

.nav-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ── Main ── */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── Topbar ── */
.topbar {
  height: var(--topbar-height);
  padding: 0 20px;
  border-bottom: 0.5px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.page-title {
  font-size: 15px;
  font-weight: 500;
}

/* ── Content ── */
.content {
  flex: 1;
  padding: 16px 20px;
  overflow-y: auto;
}

/* ── Buttons ── */
.btn {
  padding: 6px 12px;
  border-radius: var(--radius-md);
  border: 0.5px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  cursor: pointer;
  font-size: 12px;
  transition: background 0.1s;
}

.btn:hover {
  background: var(--color-secondary);
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-white);
  border-color: transparent;
}

.btn-primary:hover {
  opacity: 0.85;
}

.btn-sm {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  color: var(--color-text-muted);
}

/* ── KPI Cards ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.kpi {
  background: var(--color-secondary);
  border-radius: var(--radius-md);
  padding: 12px 14px;
}

.kpi-label {
  font-size: 11px;
  color: var(--color-text-hint);
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 22px;
  font-weight: 500;
}

.kpi-sub {
  font-size: 11px;
  color: var(--color-text-hint);
  margin-top: 2px;
}

/* ── Alert ── */
.alert-warning {
  background: #faeeda;
  border: 0.5px solid #ef9f27;
  border-radius: var(--radius-md);
  padding: 10px 14px;
  margin-bottom: 14px;
  font-size: 12px;
  color: #633806;
}

/* ── Section Header ── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.section-title {
  font-size: 13px;
  font-weight: 500;
}

/* ── Table ── */
.table-wrap {
  border: 0.5px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

th {
  text-align: left;
  padding: 8px 12px;
  background: var(--color-secondary);
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 11px;
  border-bottom: 0.5px solid var(--color-border);
}

td {
  padding: 8px 12px;
  border-bottom: 0.5px solid var(--color-border);
}

tr:last-child td {
  border-bottom: none;
}
tr:hover td {
  background: var(--color-secondary);
}

/* ── Badges ── */
.badge {
  display: inline-block;
  font-size: 10px;
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: 500;
}

.badge-gray {
  background: #f1efe8;
  color: #444441;
}
.badge-amber {
  background: #faeeda;
  color: #633806;
}
.badge-blue {
  background: #e6f1fb;
  color: #0c447c;
}
.badge-green {
  background: #eaf3de;
  color: #27500a;
}
.badge-red {
  background: #fcebeb;
  color: #791f1f;
}
.badge-warning {
  background: #faeeda;
  color: #633806;
}

/* ── Form ── */
.form-group {
  margin-bottom: 12px;
}

.form-label {
  display: block;
  font-size: 11px;
  color: var(--color-text-muted);
  margin-bottom: 4px;
}

input,
select,
textarea {
  width: 100%;
  padding: 7px 10px;
  border-radius: var(--radius-md);
  border: 0.5px solid var(--color-border);
  background: var(--color-white);
  color: var(--color-text);
  font-size: 12px;
}

input:focus,
select:focus {
  outline: none;
  border-color: #888;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 12px;
}

/* ── Modal ── */
.modal-overlay {
  display: none;
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-overlay.open {
  display: flex;
}

.modal {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 0.5px solid var(--color-border);
  padding: 20px;
  width: 420px;
}

.modal-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}

/* ── Empty State ── */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--color-text-hint);
  font-size: 12px;
}

/* ── Misc ── */
.text-danger {
  color: #e24b4a;
}
.text-warning {
  color: #ba7517;
}
.text-success {
  color: #3b6d11;
}
.text-muted {
  color: var(--color-text-muted);
}
.flex-gap {
  display: flex;
  gap: 8px;
  align-items: center;
}
```

---

## Step 2: สร้าง HTML template สำหรับทุกหน้า

ทุกหน้าใช้ HTML structure เดียวกัน เปลี่ยนแค่ `<title>`, active nav item และ content ข้างใน

### Template base (ใช้กับทุกหน้า):

```html
<!DOCTYPE html>
<html lang="th">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PAGE_TITLE — Mini ERP</title>
    <link rel="stylesheet" href="../css/style.css" />
  </head>
  <body>
    <aside class="sidebar">
      <div class="sidebar-logo">Mini ERP</div>
      <a href="dashboard.html" class="nav-item PAGE_ACTIVE_DASHBOARD">
        <span class="nav-dot" style="background:#7F77DD"></span> Dashboard
      </a>
      <a href="products.html" class="nav-item PAGE_ACTIVE_PRODUCTS">
        <span class="nav-dot" style="background:#1D9E75"></span> Products
      </a>
      <a href="suppliers.html" class="nav-item PAGE_ACTIVE_SUPPLIERS">
        <span class="nav-dot" style="background:#1D9E75"></span> Suppliers
      </a>
      <a href="purchase_orders.html" class="nav-item PAGE_ACTIVE_PURCHASE">
        <span class="nav-dot" style="background:#BA7517"></span> Purchase Orders
      </a>
      <a href="inventory.html" class="nav-item PAGE_ACTIVE_INVENTORY">
        <span class="nav-dot" style="background:#378ADD"></span> Inventory
      </a>
    </aside>

    <div class="main">
      <div class="topbar">
        <span class="page-title">PAGE_TITLE</span>
        <div class="flex-gap">
          <!-- action buttons ของแต่ละหน้า -->
        </div>
      </div>
      <div class="content">
        <!-- content ของแต่ละหน้า -->
      </div>
    </div>

    <script src="../js/PAGE_JS.js"></script>
  </body>
</html>
```

---

## Step 3: สร้างแต่ละหน้าตาม Mock UI

### `dashboard.html`

- KPI grid 4 ช่อง: PO ทั้งหมด, รอรับสินค้า, ยอดสั่งซื้อรวม, สินค้าใกล้หมด
- Alert box แสดงชื่อสินค้า low stock (ซ่อนถ้าไม่มี)
- ตาราง PO ล่าสุด: columns = PO #, Supplier, วันที่, ยอดรวม, Status

### `products.html` (ปรับจากที่มีอยู่)

- Section header: "สินค้าทั้งหมด (N รายการ)" + ปุ่ม "+ เพิ่มสินค้า"
- ตาราง: columns = ชื่อสินค้า, หน่วย, ราคา/หน่วย, Min qty, Actions
- Actions ต่อแถว: ปุ่ม "แก้ไข" + "ลบ"
- Modal form: name (required), unit, unit_price, min_qty

### `suppliers.html`

- Section header: "ซัพพลายเออร์ทั้งหมด (N รายการ)" + ปุ่ม "+ เพิ่มซัพพลายเออร์"
- ตาราง: columns = ชื่อบริษัท, เบอร์โทร, อีเมล, Actions
- Modal form: name (required), phone, email, address

### `purchase_orders.html`

- Section header: filter dropdown (ทุก status / draft / confirmed / ...) + ปุ่ม "+ สร้าง PO"
- ตาราง: columns = PO #, Supplier, วันที่สั่ง, ยอดรวม, Status, Actions
- Actions เปลี่ยนตาม status:
  - draft → ดู, Confirm, ยกเลิก
  - confirmed → ดู, รับสินค้า, ยกเลิก
  - received → ดู, Done
  - done/cancelled → ดู

### `inventory.html`

- Section header: "สต็อกสินค้า" + ปุ่ม warning "สินค้าใกล้หมด N รายการ"
- ตาราง: columns = สินค้า, หน่วย, คงเหลือ, Min qty, สถานะ, Actions
- สถานะ: badge-green "ปกติ" หรือ badge-red "ต่ำกว่า min"
- Actions: ปุ่ม "ประวัติ" เปิด modal แสดง stock movements

---

## Step 4: เชื่อม CSS กับไฟล์ products.js ที่มีอยู่แล้ว

ตรวจสอบว่า `products.html` ที่ปรับใหม่:

- `<link rel="stylesheet" href="../css/style.css">` อยู่ใน `<head>`
- `<script src="../js/products.js">` อยู่ก่อน `</body>`
- class names ใน HTML ตรงกับ CSS ที่เขียน

---

## Expected Result

- ทุกหน้ามี sidebar + topbar + content เหมือนกัน
- กดเมนูซ้ายแล้วไปหน้าที่ถูกต้องได้
- active nav item highlight ถูกหน้า
- หน้า products.html ทำงานได้จริงกับ API เดิม
- หน้าอื่นแสดง UI ได้ถูกต้อง (ยังไม่ต้องเชื่อม API)

---

## หมายเหตุ

- ใช้ `<a href="...">` สำหรับ navigation ไม่ใช่ JavaScript
- Modal ให้ใช้ CSS class `modal-overlay` + `modal-overlay.open`
- อย่าใช้ framework ภายนอก ทุกอย่าง vanilla CSS + JS เท่านั้น
- สี badge ให้อิงจาก PO status: gray=draft, amber=confirmed, blue=received, green=done, red=cancelled
