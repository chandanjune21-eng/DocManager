import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "documents.db")


def get_connection():
    print("Using DB PATH:", DB_PATH)
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True) 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        path TEXT,
        thumbnail_path TEXT,
        tags TEXT,
        description TEXT,
        upload_date TEXT,
        lecture_date TEXT,
        total_pages INTEGER               
    )    
    ''')

    # Safe migrations
    try:
        cursor.execute("ALTER TABLE documents ADD COLUMN upload_date TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE documents ADD COLUMN lecture_date TEXT")
    except sqlite3.OperationalError:
        pass
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_visits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        page_number INTEGER,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_visits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        timestamp TEXT
    )                          
    """)

    conn.commit()
    print("DB operation successful")
    conn.close()
    