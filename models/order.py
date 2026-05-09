from database import get_connection


ORDER_STATUSES = ["pending", "confirmed", "completed", "cancelled"]
STATUS_LABELS = {
    "pending":   "待確認",
    "confirmed": "已確認",
    "completed": "已完成",
    "cancelled": "已取消",
}


class Order:
    @staticmethod
    def get_all():
        """訂單列表，含客戶名與總額（計算折扣）"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        o.id,
                        o.ordered_date,
                        o.status,
                        c.name AS customer_name,
                        COALESCE(
                            SUM(r.price * r.quantity * (1 - r.discount / 100)),
                            0
                        ) AS total
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    LEFT JOIN order_records r
                        ON o.id = r.order_id AND r.deleted_at IS NULL
                    WHERE o.deleted_at IS NULL
                    GROUP BY o.id, o.ordered_date, o.status, c.name
                    ORDER BY o.ordered_date DESC
                """)
                return cur.fetchall()

    @staticmethod
    def get_with_records(order_id):
        """單筆訂單+明細(records)"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT o.*, c.name AS customer_name
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    WHERE o.id = %s
                """, (order_id,))
                order = cur.fetchone()
                if order is None:
                    return None, []
                cur.execute("""
                    SELECT r.*, p.name AS product_name
                    FROM order_records r
                    JOIN products p ON r.product_id = p.id
                    WHERE r.order_id = %s AND r.deleted_at IS NULL
                """, (order_id,))
                records = cur.fetchall()
                return order, records

    @staticmethod
    def create(customer_id, records):
        """records: [{product_id, quantity, price, cost, discount}, ...]"""
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO orders (customer_id) VALUES (%s)",
                    (customer_id,),
                )
                order_id = cur.lastrowid
                for r in records:
                    cur.execute("""
                        INSERT INTO order_records
                            (order_id, product_id, quantity, price, cost, discount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        order_id, r["product_id"], r["quantity"],
                        r["price"], r["cost"], r["discount"],
                    ))
                return order_id

    @staticmethod
    def update_status(order_id, status):
        if status not in ORDER_STATUSES:
            raise ValueError(f"unknown status: {status}")
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE orders SET status = %s WHERE id = %s",
                    (status, order_id),
                )

    @staticmethod
    def cancel(order_id):
        Order.update_status(order_id, "cancelled")
