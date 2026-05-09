from database import get_connection


class Product:
    @staticmethod
    def get_all():
        """含已停用，table 顯示用"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.*, c.name AS category_name
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                """)
                return cur.fetchall()

    @staticmethod
    def get_active():
        """建單時可選的商品"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, price, cost
                    FROM products
                    WHERE deleted_at IS NULL
                """)
                return cur.fetchall()

    @staticmethod
    def get_by_id(product_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                return cur.fetchone()

    @staticmethod
    def create(category_id, name, description, price, cost):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO products (category_id, name, description, price, cost) VALUES (%s, %s, %s, %s, %s)",
                    (category_id, name, description, price, cost),
                )
                return cur.lastrowid

    @staticmethod
    def update(product_id, category_id, name, description, price, cost):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE products SET category_id=%s, name=%s, description=%s, price=%s, cost=%s WHERE id=%s",
                    (category_id, name, description, price, cost, product_id),
                )

    @staticmethod
    def disable(product_id):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE products SET deleted_at = NOW() WHERE id = %s",
                    (product_id,),
                )

    @staticmethod
    def restore(product_id):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE products SET deleted_at = NULL WHERE id = %s",
                    (product_id,),
                )
