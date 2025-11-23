import sqlite3
import os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "consent.db")
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS consents (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT,
      feature TEXT,
      allowed INTEGER,
      expiry TEXT,
      signature TEXT,
      updated_at TEXT
    );
    """)
    conn.commit()
    conn.close()

init_db()

def update_consent(user_id, feature, allowed=True, expiry=None, signature=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO consents (user_id,feature,allowed,expiry,signature,updated_at) VALUES (?,?,?,?,?,?)",
              (user_id, feature, 1 if allowed else 0, expiry or "", signature or "", datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return True

def get_user_consents(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT feature,allowed,expiry,updated_at FROM consents WHERE user_id=? ORDER BY updated_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"feature":r[0],"allowed":bool(r[1]),"expiry":r[2],"updated_at":r[3]} for r in rows]
