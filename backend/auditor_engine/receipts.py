# receipts_module.py
# Place this file in your project, e.g. auditor_engine/receipts.py
# This module implements AI Receipt creation and retrieval.

import os
import sqlite3
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

# path to the action logs DB (same as your main.py uses)
DB_ACTIONS = os.path.join(os.path.dirname(__file__), "..", "action_logs.db")

# Initialize receipts table inside the same DB used for action logs
def init_receipts_table():
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS receipts (
            id TEXT PRIMARY KEY,
            action_row_id INTEGER,
            user_id TEXT,
            receipt_json TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_receipts_table()


# Helper: read action log by row id
def get_action_by_rowid(rowid: int) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    r = c.execute("SELECT id, user_id, inputs, output, explanation, model_version, created_at, hash FROM action_logs WHERE id = ?", (rowid,)).fetchone()
    conn.close()
    if not r:
        return None
    # map columns
    return {
        "rowid": r[0],
        "user_id": r[1],
        "inputs": json.loads(r[2]) if r[2] else {},
        "output": json.loads(r[3]) if r[3] else {},
        "explanation": r[4],
        "model_version": r[5],
        "created_at": r[6],
        "hash": r[7]
    }


# Create a receipt dict from an action log row
def build_receipt_from_action(action: Dict[str, Any]) -> Dict[str, Any]:
    receipt_id = str(uuid.uuid4())
    action_id = f"a_{action['rowid']}"

    # Simple reasons extraction: use explanation text or top attribution keys
    reasons = []
    if action.get("explanation"):
        # keep the explanation short as the major reason(s)
        reasons.append(action["explanation"].split('\n')[0])
    else:
        reasons.append("Model decision summary not available")

    # used_data: infer from inputs keys
    used_data = list(action.get("inputs", {}).keys())

    # simple alternatives: try to produce user-friendly hints (demo)
    alternatives = []
    out = action.get("output", {})
    if out.get("decision") == "denied":
        alternatives = ["Add a co-signer", "Increase downpayment", "Correct income estimate in AI Twin"]
    else:
        alternatives = ["No action needed"]

    receipt = {
        "receipt_id": receipt_id,
        "action_id": action_id,
        "summary": f"Decision: {out.get('decision', 'unknown')}",
        "reasons": reasons,
        "used_data": used_data,
        "alternatives": alternatives,
        # audit anchor placeholder (fill with real merkle anchor later)
        "audit_anchor": None,
        "zk_proof_meta": None,
        "created_at": datetime.utcnow().isoformat()
    }

    return receipt


# Persist receipt into receipts table
def save_receipt(rowid: int, receipt: Dict[str, Any]):
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO receipts (id, action_row_id, user_id, receipt_json, created_at) VALUES (?,?,?,?,?)",
              (receipt["receipt_id"], rowid, receipt.get("user_id", ""), json.dumps(receipt), receipt.get("created_at")))
    conn.commit()
    conn.close()


# Public: generate receipt for a given action row id (if not exists)
def generate_receipt_for_action(rowid: int) -> Dict[str, Any]:
    action = get_action_by_rowid(rowid)
    if not action:
        raise ValueError("action not found")

    # check if receipt already exists
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    existing = c.execute("SELECT receipt_json FROM receipts WHERE action_row_id = ?", (rowid,)).fetchone()
    conn.close()

    if existing:
        return json.loads(existing[0])

    receipt = build_receipt_from_action(action)
    # attach metadata
    receipt["user_id"] = action.get("user_id")

    # Save
    save_receipt(rowid, receipt)
    return receipt


# Public: fetch receipts for a user
def get_receipts_for_user(user_id: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_ACTIONS)
    c = conn.cursor()
    rows = c.execute("SELECT receipt_json FROM receipts WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    out = []
    for r in rows:
        try:
            out.append(json.loads(r[0]))
        except Exception:
            continue
    return out


# Small helper: attach a merkle anchor using verifiable.merkle if available
try:
    from verifiable.merkle import merkle_root
    def attach_anchor_to_receipt(receipt: Dict[str, Any]):
        # collect last 32 hashes from action_logs and compute root
        conn = sqlite3.connect(DB_ACTIONS)
        rows = conn.execute("SELECT hash FROM action_logs ORDER BY created_at DESC LIMIT 32").fetchall()
        conn.close()
        leaves = [bytes(r[0], "utf-8") for r in rows]
        root = merkle_root(leaves) if leaves else None
        receipt["audit_anchor"] = {"merkle_root": root}
        return receipt
except Exception:
    def attach_anchor_to_receipt(receipt: Dict[str, Any]):
        # noop
        receipt["audit_anchor"] = None
        return receipt


# Example: endpoint snippets (to add to your FastAPI app)
#
# from auditor_engine.receipts import generate_receipt_for_action, get_receipts_for_user, attach_anchor_to_receipt
#
# @app.post("/receipts/generate/{action_rowid}")
# def api_generate_receipt(action_rowid: int):
#     r = generate_receipt_for_action(action_rowid)
#     r = attach_anchor_to_receipt(r)
#     return r
#
# @app.get("/receipts/{user_id}")
# def api_get_receipts(user_id: str):
#     return {"receipts": get_receipts_for_user(user_id)}
