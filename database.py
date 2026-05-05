import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from config import DB_CONFIG

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