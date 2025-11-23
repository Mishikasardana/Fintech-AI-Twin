# auditor_engine/twin.py
import sqlite3, os, json
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(__file__))
DB = os.path.join(BASE, "twin.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS twin (
            user_id TEXT PRIMARY KEY,
            twin_json TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_twin(user_id: str, twin: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO twin(user_id, twin_json, updated_at)
        VALUES (?, ?, ?)
    """, (user_id, json.dumps(twin), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_twin(user_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    row = c.execute("SELECT twin_json FROM twin WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return {"user_id": user_id, "twin": {}}
    return json.loads(row[0])
