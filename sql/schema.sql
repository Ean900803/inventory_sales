USE inventory_sales;
-- 員工
CREATE TABLE employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  cellphone CHAR(10) NOT NULL,
  address VARCHAR(100),
  lv TINYINT NOT NULL DEFAULT 1 COMMENT '權限等級：1=一般員工, 9=管理員',
  resigned_date TIMESTAMP NULL,
  INDEX idx_resigned (resigned_date)
);

-- 商品類別
CREATE TABLE categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  deleted_at TIMESTAMP NULL,
  deleted_by INT NULL,
  FOREIGN KEY (deleted_by) REFERENCES employees(id)
);

-- 單位
CREATE TABLE units (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(10) NOT NULL UNIQUE
);

-- 商品
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  category_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description TEXT,
  base_unit_id INT NOT NULL COMMENT '基準單位，所有庫存運算的基礎',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INT NOT NULL,
  deleted_at TIMESTAMP NULL,
  deleted_by INT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id),
  FOREIGN KEY (base_unit_id) REFERENCES units(id),
  FOREIGN KEY (created_by) REFERENCES employees(id),
  FOREIGN KEY (deleted_by) REFERENCES employees(id),
  INDEX idx_category (category_id),
  INDEX idx_deleted (deleted_at)
);

-- 商品單位定價（含歷程）
CREATE TABLE product_unit (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  unit_id INT NOT NULL,
  conversion_rate INT NOT NULL COMMENT '此單位 = 幾個基準單位',
  price DECIMAL(10,2) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INT NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (unit_id) REFERENCES units(id),
  FOREIGN KEY (created_by) REFERENCES employees(id),
  INDEX idx_active_lookup (product_id, unit_id, status)
);

-- 客戶
CREATE TABLE customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  cellphone CHAR(10),
  address VARCHAR(100),
  note TEXT
);

-- 訂單主檔
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  ordered_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending', 'confirmed', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
  deleted_at TIMESTAMP NULL,
  deleted_by INT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (deleted_by) REFERENCES employees(id),
  INDEX idx_customer (customer_id),
  INDEX idx_date (ordered_date)
);

-- 訂單明細（不開放編輯，只能新增/刪除）
CREATE TABLE order_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  unit_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL COMMENT '成交當下單價',
  cost DECIMAL(10,2) NOT NULL COMMENT '成交當下成本',
  conversion_rate INT NOT NULL COMMENT '成交當下換算比例',
  discount DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '折扣率，0~1之間',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by INT NOT NULL,
  deleted_at TIMESTAMP NULL,
  deleted_by INT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (unit_id) REFERENCES units(id),
  FOREIGN KEY (created_by) REFERENCES employees(id),
  FOREIGN KEY (deleted_by) REFERENCES employees(id),
  INDEX idx_order (order_id),
  INDEX idx_product (product_id)
);

-- 進貨／庫存
CREATE TABLE stocks (
  id INT PRIMARY KEY AUTO_INCREMENT,
  product_id INT NOT NULL,
  unit_id INT NOT NULL COMMENT '進貨時使用的單位',
  quantity INT NOT NULL COMMENT '進貨數量',
  quantity_remaining INT NOT NULL COMMENT '剩餘基準單位數',
  unit_cost DECIMAL(10,2) NOT NULL COMMENT '此批次每個基準單位的成本',
  restocked_date DATE NOT NULL,
  restocked_by INT NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (unit_id) REFERENCES units(id),
  FOREIGN KEY (restocked_by) REFERENCES employees(id),
  INDEX idx_fifo_lookup (product_id, restocked_date, quantity_remaining)
);