import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import DB_CONFIG

@contextmanager
def get_connection():
    conn = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)
    try:
        yield conn
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