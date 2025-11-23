import os
import sqlite3
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

# ------------------------------
# External service imports
# ------------------------------
from explain_service.explain import compute_shap_attributions, nl_explanation, get_model
from what_if_engine.engine import WhatIfEngine
from auditor_engine.core import EthicalAIAuditor
from consent.policy import update_consent, get_user_consents
from verifiable.merkle import merkle_root, sha256
from auditor_engine.twin import save_twin, get_twin
from auditor_engine.appeals import create_appeal, list_appeals
from auditor_engine.zk import generate_zk_proof


# ============================================================
# APP INIT
# ============================================================
app = FastAPI(title="Fusion Demo API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # api/
DB_ACTIONS = os.path.join(BASE_DIR, "action_logs.db")
RECEIPTS_DB = os.path.join(BASE_DIR, "receipts.db")
INCIDENTS_DB = os.path.join(BASE_DIR, "incidents.db")


# ============================================================
# INIT DATABASES
# ============================================================
def init_actions_db():
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            inputs TEXT,
            output TEXT,
            explanation TEXT,
            model_version TEXT,
            created_at TEXT,
            hash TEXT
        )
    """)
    conn.commit()
    conn.close()


def init_receipts_db():
    conn = sqlite3.connect(RECEIPTS_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_rowid INTEGER,
            user_id TEXT,
            summary TEXT,
            reasons TEXT,
            used_data TEXT,
            alternatives TEXT,
            audit_anchor TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def init_incidents_db():
    conn = sqlite3.connect(INCIDENTS_DB)
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
    conn.commit()
    conn.close()


init_actions_db()
init_receipts_db()
init_incidents_db()


# ============================================================
# MODEL + SERVICES
# ============================================================
MODEL = get_model()
WHATIF = WhatIfEngine(MODEL)
AUDITOR = EthicalAIAuditor()


# ============================================================
# REQUEST MODELS
# ============================================================
class InputData(BaseModel):
    income: float
    age: int
    credit_score: float
    spending_ratio: float


class DecisionInput(InputData):
    user_id: str = "anonymous"


class ExplainInput(InputData):
    user_id: str = "anonymous"


class ConsentUpdate(BaseModel):
    user_id: str
    feature: str
    allowed: bool
    expiry: str | None = None


class Appeal(BaseModel):
    message: str
    action_id: int


# ============================================================
# RECEIPT HELPERS
# ============================================================
def generate_receipt_for_action(action_rowid: int):
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    row = c.execute(
        "SELECT user_id, inputs, output, explanation, created_at FROM action_logs WHERE id=?",
        (action_rowid,)
    ).fetchone()
    conn.close()

    if not row:
        return None

    user_id, inputs_json, output_json, explanation, ts = row

    inputs = json.loads(inputs_json)
    output = json.loads(output_json)
    reasons = [s.strip() for s in explanation.split(".") if s.strip()]

    alternatives = [
        "Increase credit score to 650",
        "Reduce spending ratio below 40%",
        "Increase income by ₹10,000"
    ]

    receipt = {
        "receipt_id": f"r_{action_rowid}_{int(datetime.utcnow().timestamp())}",
        "action_id": action_rowid,
        "user_id": user_id,
        "summary": f"Loan decision: {output['decision']}",
        "reasons": reasons,
        "used_data": inputs,
        "alternatives": alternatives,
        "audit_anchor": None,
        "timestamp": ts
    }

    # Save to DB
    conn = sqlite3.connect(RECEIPTS_DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO receipts(action_rowid, user_id, summary, reasons, used_data,
                             alternatives, audit_anchor, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action_rowid,
        user_id,
        receipt["summary"],
        json.dumps(reasons),
        json.dumps(inputs),
        json.dumps(alternatives),
        None,
        ts
    ))
    conn.commit()
    conn.close()

    return receipt


def attach_anchor_to_receipt(receipt: dict):
    leaf = sha256(json.dumps(receipt, sort_keys=True).encode())
    root = merkle_root([leaf])

    receipt["audit_anchor"] = {
        "merkle_root": root,
        "batch_timestamp": datetime.utcnow().isoformat()
    }
    return receipt


def get_receipts_for_user(user_id: str):
    conn = sqlite3.connect(RECEIPTS_DB)
    c = conn.cursor()
    rows = c.execute(
        "SELECT id, action_rowid, summary, timestamp FROM receipts WHERE user_id=?",
        (user_id,)
    ).fetchall()
    conn.close()

    return [
        {
            "receipt_id": f"r_{r[0]}",
            "action_id": r[1],
            "summary": r[2],
            "timestamp": r[3]
        }
        for r in rows
    ]


# ============================================================
# ====================== API ROUTES ==========================
# ============================================================

# ------------------ DECISION ------------------
@app.post("/decision")
def decision(req: DecisionInput):
    features = {k: req.dict()[k] for k in MODEL.feature_names}

    pred = MODEL.predict(pd.DataFrame([features]))[0]
    atts = compute_shap_attributions(features)
    preview = nl_explanation(atts, context={"user_id": req.user_id})

    action = {
        "user_id": req.user_id,
        "inputs": features,
        "output": {"decision": pred},
        "explanation": preview,
        "model_version": "demo-v1",
        "created_at": datetime.utcnow().isoformat()
    }

    h = sha256(json.dumps(action, sort_keys=True).encode())

    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    c.execute("""
        INSERT INTO action_logs(user_id, inputs, output, explanation, model_version, created_at, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        req.user_id,
        json.dumps(features),
        json.dumps(action["output"]),
        preview,
        "demo-v1",
        action["created_at"],
        h
    ))
    conn.commit()
    conn.close()

    return {"decision": pred, "explanation_preview": preview, "attributions": atts}


# ------------------ EXPLAIN ------------------
@app.post("/explain")
def explain(req: ExplainInput):
    features = {k: req.dict()[k] for k in MODEL.feature_names}
    atts = compute_shap_attributions(features)
    text = nl_explanation(atts, context={"user_id": req.user_id})
    return {"explanation": text, "attributions": atts}


# ------------------ WHAT-IF ------------------
@app.post("/what-if")
def what_if_api(req: InputData):
    cf = WHATIF.search_counterfactuals(req.dict())
    return {"input": req.dict(), "counterfactuals": cf, "model_version": "demo-v1"}


# ------------------ CONSENT ------------------
@app.post("/consent/update")
def consent_update_api(req: ConsentUpdate):
    update_consent(req.user_id, req.feature, req.allowed, req.expiry)
    return {"status": "ok"}


@app.get("/consent/{user_id}")
def fetch_consent(user_id: str):
    return get_user_consents(user_id)


# ------------------ AUDIT ------------------
@app.post("/audit/run")
def audit_run():
    conn = sqlite3.connect(DB_ACTIONS)
    rows = conn.execute("SELECT inputs, output FROM action_logs").fetchall()
    conn.close()

    if not rows:
        raise HTTPException(400, "no logs")

    df = []
    for inputs_json, output_json in rows:
        inp = json.loads(inputs_json)
        out = json.loads(output_json)
        inp["decision"] = out["decision"]
        df.append(inp)

    df_pd = pd.DataFrame(df)
    return AUDITOR.run_audit(df_pd, sensitive_col=None)


@app.get("/audit/incidents")
def audit_incidents():
    conn = sqlite3.connect(INCIDENTS_DB)
    rows = conn.execute("SELECT id, test, value, severity, created_at FROM incidents").fetchall()
    conn.close()

    return {"incidents": [
        {"id": r[0], "test": r[1], "value": r[2], "severity": r[3], "created_at": r[4]}
        for r in rows
    ]}


# ------------------ RECEIPTS ------------------
@app.post("/receipts/generate/{action_rowid}")
def api_generate_receipt(action_rowid: int):
    r = generate_receipt_for_action(action_rowid)
    if not r:
        raise HTTPException(404, "action not found")
    return attach_anchor_to_receipt(r)


@app.get("/receipts/{user_id}")
def api_get_receipts(user_id: str):
    return {"receipts": get_receipts_for_user(user_id)}


@app.get("/receipts/merkle")
def receipts_merkle():
    conn = sqlite3.connect(DB_ACTIONS)
    rows = conn.execute("SELECT hash FROM action_logs").fetchall()
    conn.close()

    leaves = [r[0].encode() for r in rows]
    return {"merkle_root": merkle_root(leaves)}


# ------------------ AI TWIN ------------------
@app.get("/twin/{user_id}")
def get_user_twin_route(user_id: str):
    return get_twin(user_id)


@app.post("/twin/{user_id}")
def update_user_twin_route(user_id: str, body: dict):
    save_twin(user_id, body)
    return {"status": "ok", "updated": body}


# ------------------ APPEALS ------------------
@app.post("/appeal/{user_id}")
def appeal_api(user_id: str, req: Appeal):
    create_appeal(user_id, req.action_id, req.message)
    return {"status": "submitted"}


@app.get("/appeal/{user_id}")
def get_appeals_api(user_id: str):
    return {"appeals": list_appeals(user_id)}


# ------------------ ZK PROOF ------------------
@app.post("/zk/prove")
def zk_prove(body: dict):
    return generate_zk_proof(body)


# ------------------ GOV OVERVIEW ------------------
@app.get("/governance/overview")
def gov_overview():
    return {
        "models": ["demo-v1"],
        "incidents_count": len(get_receipts_for_user("*")),
        "pending_appeals": len(list_appeals("*")),
        "latest_receipts": len(get_receipts_for_user("*"))
    }


# ------------------ MOCK BANK ------------------
@app.get("/bank/user-balance/{user_id}")
def mock_bank_balance(user_id: str):
    return {"balance": 42000, "currency": "INR"}


# ------------------ DEBUG ------------------
@app.get("/debug/actions")
def debug_actions():
    conn = sqlite3.connect(DB_ACTIONS)
    rows = conn.execute("SELECT id, user_id, created_at FROM action_logs").fetchall()
    conn.close()
    return {"actions": rows}

# --- ZK Verification endpoint (paste into main.py) ---
from fastapi import Body

@app.post("/zk/verify")
def zk_verify(payload: dict = Body(...)):
    """
    Expected payload:
    {
      "receipt": { ... },             # the receipt JSON returned by /receipts/generate
      "proof": { "proof_id":"..", "hash":"..", "valid": True, "proof_meta": {...} }
    }
    """
    receipt = payload.get("receipt")
    proof = payload.get("proof")

    if not receipt:
        raise HTTPException(status_code=400, detail="missing receipt")

    # Remove any anchor fields when computing canonical leaf (so it's deterministic)
    receipt_clone = dict(receipt)
    # If receipt contains an anchor, remove it for leaf calculation (we verify it separately)
    receipt_clone.pop("audit_anchor", None)
    # Sort keys for deterministic serialization
    serialized = json.dumps(receipt_clone, sort_keys=True).encode()

    # compute leaf and compare to proof hash (if provided)
    leaf_hash = sha256(serialized)

    verification = {
        "leaf_hash": leaf_hash,
        "leaf_ok": False,
        "merkle_root_ok": False,
        "proof_ok": False,
        "details": {}
    }

    # Check proof hash matches leaf
    if proof and proof.get("hash") == leaf_hash:
        verification["proof_ok"] = proof.get("valid", False)
    else:
        # still allow verification when proof not provided but anchor is present
        verification["proof_ok"] = False

    # If receipt contained an audit_anchor, check merkle root matches recomputed root
    audit_anchor = receipt.get("audit_anchor")
    if audit_anchor and audit_anchor.get("merkle_root"):
        # For demo we assume the merkle root was produced over [leaf] (single-leaf batch)
        recomputed_root = merkle_root([leaf_hash.encode()])
        verification["merkle_root"] = audit_anchor.get("merkle_root")
        verification["recomputed_root"] = recomputed_root
        verification["merkle_root_ok"] = (recomputed_root == audit_anchor.get("merkle_root"))
    else:
        verification["merkle_root"] = None
        verification["recomputed_root"] = merkle_root([leaf_hash.encode()])  # value for debugging

    verification["leaf_ok"] = True  # leaf is always derivable
    verification["details"]["receipt_id"] = receipt.get("receipt_id")
    verification["details"]["timestamp"] = receipt.get("timestamp")

    # Final verdict: require proof_ok AND merkle_root_ok (if anchor present). If anchor absent, rely on proof_ok.
    if audit_anchor:
        verified = verification["proof_ok"] and verification["merkle_root_ok"]
    else:
        verified = verification["proof_ok"]

    return {"verified": bool(verified), "verification": verification}
from auditor_engine.scheduler import start_scheduler
start_scheduler()




