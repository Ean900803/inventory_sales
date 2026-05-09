import os
from dotenv import load_dotenv

load_dotenv()

# 啟動時 ConnectionDialog 會以這份 DB_CONFIG 作為預設值；使用者輸入後再 update 回來
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "pw"),
    "database": os.getenv("DB_NAME", "inventory_sales"),
    "charset": "utf8mb4",
}
