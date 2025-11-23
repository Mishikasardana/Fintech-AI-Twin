import React, { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

const APITester: React.FC = () => {
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const callAPI = async (endpoint: string, payload?: any) => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: payload ? "POST" : "GET",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": import.meta.env.VITE_API_KEY,
        },
        body: payload ? JSON.stringify(payload) : undefined,
      });

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: err.toString() });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 text-white space-y-4">
      <h1 className="text-3xl font-semibold">API Tester</h1>

      <div className="grid gap-3 md:grid-cols-2">

        <button
          onClick={() =>
            callAPI("/what-if", {
              income: 25000,
              age: 24,
              credit_score: 580,
              spending_ratio: 0.65,
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test WHAT-IF
        </button>

        <button
          onClick={() =>
            callAPI("/decision", {
              user_id: "user123",
              income: 25000,
              age: 24,
              credit_score: 580,
              spending_ratio: 0.65,
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test DECISION
        </button>

        <button
          onClick={() =>
            callAPI("/explain", {
              user_id: "user123",
              income: 25000,
              age: 24,
              credit_score: 580,
              spending_ratio: 0.65,
              include_llm: true,
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test EXPLAIN
        </button>

        <button
          onClick={() =>
            callAPI("/consent/update", {
              user_id: "user123",
              feature: "credit_model_use",
              allowed: true,
              expiry: "2025-12-31",
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test CONSENT UPDATE
        </button>

        <button
          onClick={() =>
            callAPI("/audit/run", {
              user_id: "user123",
              model_version: "demo-v1",
              input: {
                income: 25000,
                age: 24,
                credit_score: 580,
                spending_ratio: 0.65,
              },
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test AUDIT
        </button>

        <button
          onClick={() => callAPI("/receipts/generate/1")}
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test RECEIPT
        </button>

        <button
          onClick={() => callAPI("/twin/user123")}
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test TWIN DATA
        </button>

        <button
          onClick={() =>
            callAPI("/appeal/user123", {
              action_id: 12,
              message:
                "I believe the loan was denied because my salary was not updated.",
            })
          }
          className="bg-blue-600 px-4 py-2 rounded"
        >
          Test APPEAL
        </button>
      </div>

      <div className="bg-gray-900 rounded p-4 mt-4 max-h-80 overflow-auto">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <pre>{JSON.stringify(response, null, 2)}</pre>
        )}
      </div>
    </div>
  );
};

export default APITester;
