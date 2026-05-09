from database import get_connection


class Customer:
    @staticmethod
    def get_all():
        """取得客戶清單"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customers")
                return cur.fetchall()

    @staticmethod
    def get_by_id(customer_id):
        """取得特定客戶資訊"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
                return cur.fetchone()

    @staticmethod
    def create(name, cellphone, address, note):
        """建立客戶"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customers (name, cellphone, address, note) VALUES (%s, %s, %s, %s)",
                    (name, cellphone, address, note),
                )
                return cur.lastrowid

    @staticmethod
    def update(customer_id, name, cellphone, address, note):
        """更新客戶"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE customers SET name=%s, cellphone=%s, address=%s, note=%s WHERE id=%s",
                    (name, cellphone, address, note, customer_id),
                )
