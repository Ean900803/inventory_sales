from database import get_connection


class Category:
    @staticmethod
    def get_all():
        """進到類別管理時載入的 table（含已停用）"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM categories")
                return cur.fetchall()

    @staticmethod
    def get_active():
        """建立商品時只能選啟用的類別"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM categories WHERE deleted_at IS NULL")
                return cur.fetchall()

    @staticmethod
    def create(name):
        """建立類別"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
                return cur.lastrowid

    @staticmethod
    def update(category_id, name):
        """編輯類別"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE categories SET name = %s WHERE id = %s",
                    (name, category_id),
                )

    @staticmethod
    def disable(category_id):
        """停用類別"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE categories SET deleted_at = NOW() WHERE id = %s",
                    (category_id,),
                )

    @staticmethod
    def restore(category_id):
        """復原類別"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE categories SET deleted_at = NULL WHERE id = %s",
                    (category_id,),
                )
