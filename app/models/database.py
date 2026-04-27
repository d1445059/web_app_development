import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')

def get_db_connection():
    """建立並回傳一個與 SQLite 資料庫的連線"""
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將查詢結果轉換為字典形式，方便用鍵值取資料
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫，基於 database/schema.sql 建立資料表"""
    if not os.path.exists(SCHEMA_PATH):
        print("Schema file not found. Database initialization skipped.")
        return
    with get_db_connection() as conn:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
