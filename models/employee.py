import hashlib
from database import get_connection


def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


class Employee:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM employees WHERE resigned_date IS NULL")
                return cursor.fetchall()

    @staticmethod
    def get_by_id(emp_id):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
                return cursor.fetchone()

    @staticmethod
    def create(name, cellphone, address=None, lv=1):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO employees (name, cellphone, address, lv) VALUES (%s, %s, %s, %s)",
                    (name, cellphone, address, lv),
                )
                return cursor.lastrowid

    @staticmethod
    def update(emp_id, name, cellphone, address=None, lv=1):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE employees SET name=%s, cellphone=%s, address=%s, lv=%s WHERE id=%s",
                    (name, cellphone, address, lv, emp_id),
                )

    @staticmethod
    def get_by_credentials(username, password):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM employees WHERE username = %s AND password = %s AND resigned_date IS NULL",
                    (username, _hash(password)),
                )
                return cursor.fetchone()

    @staticmethod
    def resign(emp_id):
        with get_connection(transaction=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE employees SET resigned_date = NOW() WHERE id = %s",
                    (emp_id,),
                )
