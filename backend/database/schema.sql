-- ============================================================
-- Purchase & Inventory System — Database Schema (Reference)
-- ============================================================
-- NOTE: Schema นี้เป็น reference เท่านั้น
-- ปัจจุบัน database ถูก managed โดย SQLAlchemy + Flask-Migrate
-- ดู models จริงได้ที่ backend/app/models/
--
-- ลำดับการสร้าง table สำคัญมาก เพราะมี foreign key dependencies
-- products, suppliers → purchase_orders → purchase_order_lines
--                                       → stock_movements
-- products → inventory
-- products → stock_movements

-- ============================================================
-- 1. PRODUCTS
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL          PRIMARY KEY,
    name        VARCHAR(255)    NOT NULL,
    unit        VARCHAR(50)     NOT NULL    DEFAULT 'pcs',
    unit_price  NUMERIC(12,2)   NOT NULL    DEFAULT 0,
    min_qty     NUMERIC(12,2)   NOT NULL    DEFAULT 0,
    created_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),

    CONSTRAINT chk_products_unit_price  CHECK (unit_price >= 0),
    CONSTRAINT chk_products_min_qty     CHECK (min_qty >= 0)
);

-- ============================================================
-- 2. SUPPLIERS
-- ============================================================
CREATE TABLE IF NOT EXISTS suppliers (
    id          SERIAL          PRIMARY KEY,
    name        VARCHAR(255)    NOT NULL    UNIQUE,
    phone       VARCHAR(20),
    email       VARCHAR(255),
    address     TEXT,
    created_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL    DEFAULT NOW()
);

-- ============================================================
-- 3. PURCHASE ORDERS
-- ============================================================
CREATE TABLE IF NOT EXISTS purchase_orders (
    id              SERIAL          PRIMARY KEY,
    supplier_id     INTEGER         NOT NULL,
    status          VARCHAR(20)     NOT NULL    DEFAULT 'draft',
    order_date      DATE            NOT NULL    DEFAULT CURRENT_DATE,
    received_date   DATE,
    note            TEXT,
    created_at      TIMESTAMP       NOT NULL    DEFAULT NOW(),
    updated_at      TIMESTAMP       NOT NULL    DEFAULT NOW(),

    CONSTRAINT fk_po_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_po_status
        CHECK (status IN ('draft', 'confirmed', 'received', 'done', 'cancelled'))
);

-- ============================================================
-- 4. PURCHASE ORDER LINES
-- ============================================================
CREATE TABLE IF NOT EXISTS purchase_order_lines (
    id          SERIAL          PRIMARY KEY,
    po_id       INTEGER         NOT NULL,
    product_id  INTEGER         NOT NULL,
    qty         NUMERIC(12,2)   NOT NULL,
    unit_price  NUMERIC(12,2)   NOT NULL,
    created_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),

    CONSTRAINT fk_pol_po
        FOREIGN KEY (po_id)
        REFERENCES purchase_orders(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pol_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_pol_qty         CHECK (qty > 0),
    CONSTRAINT chk_pol_unit_price  CHECK (unit_price >= 0)
);

-- ============================================================
-- 5. INVENTORY
-- ============================================================
CREATE TABLE IF NOT EXISTS inventory (
    id          SERIAL          PRIMARY KEY,
    product_id  INTEGER         NOT NULL    UNIQUE,
    on_hand_qty NUMERIC(12,2)   NOT NULL    DEFAULT 0,
    updated_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),

    CONSTRAINT fk_inv_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_inv_on_hand_qty CHECK (on_hand_qty >= 0)
);

-- ============================================================
-- 6. STOCK MOVEMENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS stock_movements (
    id          SERIAL          PRIMARY KEY,
    product_id  INTEGER         NOT NULL,
    po_id       INTEGER,
    type        VARCHAR(20)     NOT NULL,
    qty         NUMERIC(12,2)   NOT NULL,
    note        TEXT,
    created_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),

    CONSTRAINT fk_sm_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_sm_po
        FOREIGN KEY (po_id)
        REFERENCES purchase_orders(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_sm_type  CHECK (type IN ('in', 'out', 'adjustment')),
    CONSTRAINT chk_sm_qty   CHECK (qty > 0)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_po_status        ON purchase_orders(status);
CREATE INDEX IF NOT EXISTS idx_po_supplier      ON purchase_orders(supplier_id);
CREATE INDEX IF NOT EXISTS idx_pol_po           ON purchase_order_lines(po_id);
CREATE INDEX IF NOT EXISTS idx_pol_product      ON purchase_order_lines(product_id);
CREATE INDEX IF NOT EXISTS idx_sm_product       ON stock_movements(product_id);
CREATE INDEX IF NOT EXISTS idx_sm_po            ON stock_movements(po_id);
CREATE INDEX IF NOT EXISTS idx_sm_type          ON stock_movements(type);
CREATE INDEX IF NOT EXISTS idx_inv_product      ON inventory(product_id);