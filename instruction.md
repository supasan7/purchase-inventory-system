# Project Setup Instruction

## Objective

สร้าง folder structure เปล่าสำหรับโปรเจค purchase-inventory-system
แยก frontend และ backend ออกจากกันชัดเจนตาม best practice

---

## Folder Structure ที่ต้องสร้าง

```
purchase-inventory-system/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   └── database/
├── frontend/
│   ├── pages/
│   ├── css/
│   └── js/
└── docs/
```

---

## Steps

### 1. สร้าง folders ทั้งหมด

```bash
mkdir -p backend/app/controllers
mkdir -p backend/app/models
mkdir -p backend/app/routes
mkdir -p backend/app/services
mkdir -p backend/database
mkdir -p frontend/pages
mkdir -p frontend/css
mkdir -p frontend/js
mkdir -p docs
```

### 2. สร้าง .gitkeep ใน folder เปล่าทุก folder

เพราะ Git ไม่ track folder เปล่า ต้องมีไฟล์อยู่ข้างใน

```bash
touch backend/app/controllers/.gitkeep
touch backend/app/models/.gitkeep
touch backend/app/routes/.gitkeep
touch backend/app/services/.gitkeep
touch backend/database/.gitkeep
touch frontend/pages/.gitkeep
touch frontend/css/.gitkeep
touch frontend/js/.gitkeep
```

### 3. ย้าย workflow.md ไปไว้ใน docs/

```bash
mv docs/workflow.md docs/workflow.md 2>/dev/null || true
```

### 4. Push ขึ้น GitHub

```bash
git add .
git commit -m "feat: initialize project folder structure"
git push origin main
```

---

## หมายเหตุ

- อย่าสร้างไฟล์อื่นนอกจากที่ระบุ
- อย่าแก้ไข README.md หรือ workflow.md ที่มีอยู่แล้ว
- ทำแค่ folder structure เปล่าเท่านั้น
