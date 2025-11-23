import sqlite3, os, json
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(__file__))
DB = os.path.join(BASE, "appeals.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS appeals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        action_id INTEGER,
        message TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

def create_appeal(user_id, action_id, message):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    INSERT INTO appeals(user_id, action_id, message, status, created_at)
    VALUES (?,?,?,?,?)
    """,(user_id, action_id, message, "pending", datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_appeals(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM appeals WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return rows
