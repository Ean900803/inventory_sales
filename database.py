import hashlib
import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import DB_CONFIG


SCHEMA_SQL = """
CREATE TABLE employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  cellphone CHAR(10) NOT NULL,
  address VARCHAR(100),
  lv TINYINT NOT NULL DEFAULT 1,
  resigned_date TIMESTAMP NULL,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(64) NOT NULL
);

CREATE TABLE categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  deleted_at TIMESTAMP NULL
);

CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  category_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  cellphone CHAR(10),
  address VARCHAR(100),
  note TEXT
);

CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  ordered_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending', 'confirmed', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  cost DECIMAL(10,2) NOT NULL,
  discount DECIMAL(5,2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
"""


@contextmanager
def get_connection(transaction=False):
    # 加上DictCursot 確保取値時可以使用col name做為key取value，而非tuple
    conn = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)
    try:
        yield conn # 每次透過with取得連線併使用這邊的try catch
        if transaction:
            conn.commit()
    except Exception as e:
        if transaction:
            conn.rollback()
        raise e
    finally:
        conn.close()


def test_connection():
    """啟動時測試DB連線"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return True
    except Exception as e:
        print(f"DB連線失敗:{e}")
        return False


def _hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


def setup_database(config):
    """確保資料庫與 schema 存在；首次初始化會塞一筆 admin。

    回傳 True：本次有跑初始化（建表 + seed admin）
    回傳 False：DB 跟 tables 都已就緒，沒做事
    """
    db_name = config["database"]
    server_only = {k: v for k, v in config.items() if k != "database"}

    # 1. 確認資料庫存在；不存在就建立
    conn = pymysql.connect(**server_only)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES LIKE %s", (db_name,))
            db_exists = cur.fetchone() is not None
        if not db_exists:
            with conn.cursor() as cur:
                cur.execute(
                    f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            conn.commit()
    finally:
        conn.close()

    # 2. 切到該 DB，檢查 employees 表是否存在；缺就跑 schema + seed admin
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES LIKE 'employees'")
            tables_ready = cur.fetchone() is not None
        if tables_ready:
            return False

        with conn.cursor() as cur:
            for stmt in SCHEMA_SQL.split(";"):
                stmt = stmt.strip()
                if stmt:
                    cur.execute(stmt)
            cur.execute(
                "INSERT INTO employees (name, cellphone, lv, username, password) "
                "VALUES (%s, %s, %s, %s, %s)",
                ("管理員", "0000000000", 9, "admin", _hash_password("admin")),
            )
        conn.commit()
        return True
    finally:
        conn.close()
