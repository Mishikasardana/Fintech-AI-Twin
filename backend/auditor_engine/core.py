import pandas as pd
import sqlite3
import os
import uuid
from datetime import datetime
from auditor_engine.fairness.parity import statistical_parity
from auditor_engine.drift.monitor import detect_drift

DB = os.path.join(os.path.dirname(__file__), "incidents.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
      id TEXT PRIMARY KEY,
      test TEXT,
      value REAL,
      severity TEXT,
      created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

def log_incident(test, value, severity="MEDIUM"):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    iid = str(uuid.uuid4())
    c.execute("INSERT INTO incidents (id,test,value,severity,created_at) VALUES (?,?,?,?,?)",
              (iid, test, float(value), severity, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return iid

class EthicalAIAuditor:
    def __init__(self, fairness_threshold=0.1, drift_threshold=0.5):
        self.fairness_threshold = fairness_threshold
        self.drift_threshold = drift_threshold

    def run_audit(self, df: pd.DataFrame, sensitive_col=None, label_col="decision"):
        results = {"incidents": []}
        if sensitive_col is None:
            # try to pick a plausible sensitive column
            candidates = [c for c in df.columns if c.lower() in ("region","gender","race")]
            sensitive_col = candidates[0] if candidates else None
        if sensitive_col and sensitive_col in df.columns:
            sp = statistical_parity(df, sensitive_col, label_col)
            if pd.notnull(sp) and abs(sp) > self.fairness_threshold:
                iid = log_incident("statistical_parity", sp, "HIGH")
                results["incidents"].append({"id": iid, "test": "statistical_parity", "value": sp})
        drift_score = detect_drift(df)
        if drift_score > self.drift_threshold:
            iid = log_incident("drift", drift_score, "MEDIUM")
            results["incidents"].append({"id": iid, "test": "drift", "value": drift_score})
        return results
