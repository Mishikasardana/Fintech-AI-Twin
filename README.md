Fintech AI Twin
Introduction

Fintech AI Twin is a cutting-edge platform that empowers users to create intelligent digital twins for financial technology applications. It leverages state-of-the-art artificial intelligence and data analytics to simulate, analyze, and optimize financial processes in real-time environments. Designed for both developers and business users, the platform bridges the gap between AI technology and fintech operations, enabling smarter decisions and enhanced automation.

Overview

Fintech AI Twin is a full-stack platform that provides:

Transparent AI Decisions

Users receive explainable loan decisions including SHAP-based reasoning.

Verifiable Receipts

Every AI decision generates a tamper-proof receipt anchored using:

Merkle Trees

ZK-Proof (simulated)

Hash verification

Personal AI Twin

Users can edit their data, fix wrong assumptions, and update the system.

What-If Analysis

Users try alternate values to see how they can get approved.

Governance Dashboard

Admin-only area for:

Audit incidents

Appeals

Model behaviour

Real-time risk overview

Built for Banks, Fintechs & Regulators

Implements transparency, fairness, user empowerment, and auditability — aligned with EU AI Act and RBI guidelines.

Project Structure
backend/
│── api/                         → FastAPI backend
│     ├── main.py                → All endpoints
│     ├── receipts.db            → Stored receipts
│     ├── action_logs.db         → Logged decisions
│     ├── incidents.db           → Audit incidents
│     ├── ...other engine modules
│
├── components/                  → React UI Components
├── screens/                     → Frontend screens/pages
├── backend/venv/                → Python environment (ignored)
├── App.tsx
├── index.tsx
├── package.json
└── README.md

Tech Stack
Backend

FastAPI

Python 3.10+

SQLite

SHAP

APScheduler

Custom ZK-Proof Simulator

Custom Merkle Tree Anchoring

Frontend

React + Vite

TypeScript

Tailwind (optional)

Axios

Backend Setup (FastAPI)
1. Create virtual environment
cd api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Start backend
uvicorn api.main:app --reload --port 8000

Frontend Setup (React)
npm install
npm run dev


Runs on: http://localhost:5173

API Security (Admin API Key)

Add to .env:

API_KEY=supersecretadminkey


Include in request headers:

x-api-key: supersecretadminkey


Protected admin endpoints:

/audit/run
/governance/overview
/zk/prove
/receipts/merkle
/appeal/*

Key API Endpoints
1. Generate Decision

POST /decision

{
  "user_id": "user123",
  "income": 55000,
  "age": 28,
  "credit_score": 680,
  "spending_ratio": 0.42
}

2. Generate Receipt

POST /receipts/generate/{action_id}

{
  "receipt_id": "r_1_17000000",
  "audit_anchor": {
    "merkle_root": "abc123..."
  }
}

3. ZK Proof

POST /zk/prove

{
  "receipt_id": "r_1_17000000",
  "leaf_hash": "d83a9f...",
  "merkle_root": "abc123..."
}

4. What-If Analysis

POST /what-if

5. AI Twin
POST /twin/{user_id}
GET  /twin/{user_id}

6. Appeals

POST /appeal/{user_id}

{
  "action_id": 1,
  "message": "My salary has changed, decision incorrect."
}

7. Governance Dashboard

GET /governance/overview

{
  "models": ["demo-v1"],
  "incidents_count": 3,
  "pending_appeals": 1,
  "latest_receipts": 41
}

Installation
Clone the repository
git clone https://github.com/Mishikasardana/Fintech-AI-Twin.git
cd Fintech-AI-Twin

Setup virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt


Open browser: http://localhost:8000

Usage Scenarios

Creating & managing AI twins

Real-time financial simulations

What-if modeling for loan approvals

Generating tamper-proof decision receipts

Auditing AI behaviour

Integrating with fintech APIs

Anomaly detection & automated responses

Configuration

Use environment variables for customization:

API_KEY=supersecretadminkey
DATABASE_URL=sqlite:///receipts.db
LOG_LEVEL=info

Contributing

Fork the repo

Create a branch

Commit your changes

Push and open a pull request

License

This project is licensed under the MIT License.
