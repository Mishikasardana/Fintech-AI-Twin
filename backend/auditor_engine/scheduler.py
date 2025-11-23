import sqlite3, json, pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from auditor_engine.core import EthicalAIAuditor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTION_DB = os.path.join(BASE_DIR, "..", "api", "action_logs.db")
INCIDENT_DB = os.path.join(BASE_DIR, "incidents.db")

auditor = EthicalAIAuditor()

def run_fairness_audit():
    conn = sqlite3.connect(ACTION_DB)
    rows = conn.execute("SELECT inputs, output FROM action_logs").fetchall()
    conn.close()

    if not rows:
        return

    # Prepare DF
    data = []
    for i, (inp, out) in enumerate(rows):
        inp_json = json.loads(inp)
        out_json = json.loads(out)
        inp_json["decision"] = out_json["decision"]
        data.append(inp_json)

    df = pd.DataFrame(data)

    result = auditor.run_audit(df, sensitive_col=None)

    # Save incidents
    conn = sqlite3.connect(INCIDENT_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test TEXT,
            value REAL,
            severity TEXT,
            created_at TEXT
        )
    """)

    for r in result.get("incidents", []):
        c.execute("""
            INSERT INTO incidents(test, value, severity, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            r["test"], r["value"], r["severity"], datetime.utcnow().isoformat()
        ))

    conn.commit()
    conn.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_fairness_audit, "interval", minutes=30)
    scheduler.start()
