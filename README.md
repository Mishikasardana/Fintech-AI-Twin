# Fintech AI Twin
## Introduction

Fintech AI Twin is a cutting-edge platform that empowers users to create intelligent digital twins for financial technology applications. It leverages state-of-the-art artificial intelligence and data analytics to simulate, analyze, and optimize financial processes in real-time environments. Designed for both developers and business users, the platform bridges the gap between AI technology and fintech operations, enabling smarter decisions and enhanced automation.

## Overview

Fintech AI Twin is a full-stack platform that provides:

### Transparent AI Decisions

Users receive explainable loan decisions including SHAP-based reasoning.

### Verifiable Receipts

Every AI decision generates a tamper-proof receipt anchored using:

### Merkle Trees

### ZK-Proof (simulated)

### Hash verification

### Personal AI Twin

Users can edit their data, fix wrong assumptions, and update the system.

### What-If Analysis

Users try alternate values to see how they can get approved.

### Governance Dashboard

## Admin-only area for:

### Audit incidents

### Appeals

### Model behaviour

### Real-time risk overview

### Built for Banks, Fintechs & Regulators

Implements transparency, fairness, user empowerment, and auditability — aligned with EU AI Act and RBI guidelines.

## Project Structure
### Backend

api/

main.py – All endpoints

receipts.db – Stored receipts

action_logs.db – Logged decisions

incidents.db – Audit incidents

Other engine modules

### Frontend

components/ – React UI components

screens/ – Page components

App.tsx – Main application

index.tsx – Entry file

package.json – Project config


## Tech Stack
### Backend

FastAPI

Python 3.10+

SQLite

SHAP

APScheduler

Custom ZK-Proof simulator

Merkle Tree anchoring

### Frontend

React + Vite

TypeScript

TailwindCSS

Axios

### Backend Setup
1. Create virtual environment
cd api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Start backend
uvicorn api.main:app --reload --port 8000

### Frontend Setup
npm install
npm run dev


Runs at: http://localhost:5173

### API Security

Add to .env:

API_KEY=supersecretadminkey


Include in header:

x-api-key: supersecretadminkey


### Admin-only endpoints:

/audit/run
/governance/overview
/zk/prove
/receipts/merkle
/appeal/*

### Key API Endpoints
Generate Decision

1. POST /decision

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

7. Overview

GET /governance/overview

{
  "models": ["demo-v1"],
  "incidents_count": 3,
  "pending_appeals": 1,
  "latest_receipts": 41
}

## Installation
### Clone
git clone https://github.com/Mishikasardana/Fintech-AI-Twin.git
cd Fintech-AI-Twin

### Setup virtual environment
python3 -m venv venv
source venv/bin/activate

### Install dependencies
pip install -r requirements.txt

### Usage Scenarios

Create and manage AI twins

Real-time financial simulations

What-if modeling

Audit & explainability

Receipt generation

Fintech API integrations

Configuration

### Example .env:

API_KEY=supersecretadminkey
DATABASE_URL=sqlite:///receipts.db
LOG_LEVEL=info

### Contributing

Fork the repository

Create feature branch

Commit changes

Push and open a pull request

# License

MIT License. See LICENSE for details.
