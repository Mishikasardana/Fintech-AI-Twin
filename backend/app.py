# #what-if
{
  "income": 25000,
  "age": 24,
  "credit_score": 580,
  "spending_ratio": 0.65
}
# #decision
{
  "user_id": "user123",
  "income": 25000,
  "age": 24,
  "credit_score": 580,
  "spending_ratio": 0.65
}

# #explain
{
  "user_id": "user123",
  "income": 25000,
  "age": 24,
  "credit_score": 580,
  "spending_ratio": 0.65,
  "include_llm": True
}
# #consent/update
{
  "user_id": "user123",
  "feature": "credit_model_use",
  "allowed": True,
  "expiry": "2025-12-31"
}
# #audit/run
{
  "user_id": "user123",
  "model_version": "demo-v1",
  "input": {
    "income": 25000,
    "age": 24,
    "credit_score": 580,
    "spending_ratio": 0.65
  }
}
# #receipts/generate/1
{
  "receipt_id": "r_1_1732300100",
  "action_id": 1,
  "user_id": "user123",
  "summary": "Loan decision: Approved",
  "reasons": [
    "Your income contributed positively",
    "Your credit score supported approval",
    "Your spending ratio had mild negative influence"
  ],
  "used_data": {
    "income": 55000,
    "age": 29,
    "credit_score": 680,
    "spending_ratio": 0.42
  },
  "alternatives": [
    "Increase credit score to 650",
    "Reduce spending ratio below 40%",
    "Increase income by ₹10,000"
  ],
  "audit_anchor": {
    "merkle_root": "a8bc...f091",
    "batch_timestamp": "2025-11-22T15:25:33.125Z"
  },
  "timestamp": "2025-11-22T15:20:40Z"
}

# #twin/user123
{
  "income_est": 65000,
  "risk_score": 0.41,
  "spending_traits": ["mostly_saver"],
  "annotations": [
    {
      "by": "user",
      "text": "My income increased recently",
      "ts": "2025-11-22T19:20:30Z"
    }
  ]
}

# #appeal/user123
{
  "action_id": 12,
  "message": "I believe the loan was denied because my salary was not updated."
}


# #zk/verify
{
  "receipt": {
    "receipt_id": "r_1_1700000000",
    "action_id": 1,
    "user_id": "user123",
    "summary": "Loan decision: denied",
    "reasons": ["Low savings-to-income ratio"],
    "used_data": { "income": 25000, "credit_score": 580 },
    "alternatives": ["Increase credit score to 650"],
    "audit_anchor": { "merkle_root": "abc123..." },
    "timestamp": "2025-11-22T12:34:00Z"
  },
  "proof": {
    "proof_id": "zk_1700000000",
    "hash": "d83a9f39...",  
    "valid": True
  }
}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sqlite3
import json
from datetime import datetime

# ===== ENV SETUP =====
load_dotenv()
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(name="x-api-key")

def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return key

# ===== DATABASE =====
DB_PATH = "action_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            user_id TEXT,
            payload TEXT,
            result TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Create table at startup
init_db()

def save_action(endpoint: str, user_id: str, payload: dict, result: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO action_logs (endpoint, user_id, payload, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        endpoint,
        user_id,
        json.dumps(payload),
        json.dumps(result),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

# ===== FASTAPI APP =====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Fusion backend running"}

# ===== ENDPOINTS =====

@app.post("/chat")
def chat(payload: dict, _ = Depends(verify_api_key)):
    result = {"reply": f"You said: {payload.get('message')}"}
    save_action("/chat", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.post("/what-if")
def what_if(payload: dict):
    result = {
        "prediction_change": "Demo response",
        "input_received": payload
    }
    save_action("/what-if", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.post("/decision")
def decision(payload: dict):
    result = {"status": "decision logged", "data": payload}
    save_action("/decision", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.post("/explain")
def explain(payload: dict):
    result = {
        "explanation": "Mock explanation",
        "input_received": payload
    }
    save_action("/explain", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.post("/consent/update")
def consent_update(payload: dict):
    result = {"status": "consent updated", "data": payload}
    save_action("/consent/update", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.post("/audit/run")
def audit_run(payload: dict):
    result = {"audit_result": "no issues detected", "data": payload}
    save_action("/audit/run", payload.get("user_id", "anonymous"), payload, result)
    return result

@app.get("/receipts/generate/{receipt_id}")
def receipts(receipt_id: int):
    result = {
        "receipt_id": receipt_id,
        "status": "receipt generated"
    }
    save_action("/receipts/generate", str(receipt_id), {}, result)
    return result

@app.get("/twin/{user_id}")
def twin(user_id: str):
    result = {
        "user_id": user_id,
        "twin": {
            "income_est": 65000,
            "risk_score": 0.41
        }
    }
    save_action("/twin", user_id, {}, result)
    return result

@app.post("/appeal/{user_id}")
def appeal(user_id: str, payload: dict):
    result = {"status": "appeal submitted", "user_id": user_id}
    save_action("/appeal", user_id, payload, result)
    return result

@app.post("/zk/verify")
def zk_verify(payload: dict):
    result = {"zk_valid": True, "data": payload}
    save_action("/zk/verify", payload.get("user_id", "anonymous"), payload, result)
    return result

# ===== LOG VIEWER =====
@app.get("/logs")
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, endpoint, user_id, payload, result, timestamp
        FROM action_logs ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "endpoint": row[1],
            "user_id": row[2],
            "payload": json.loads(row[3]) if row[3] else {},
            "result": json.loads(row[4]) if row[4] else {},
            "timestamp": row[5]
        })

    return {"logs": logs}

