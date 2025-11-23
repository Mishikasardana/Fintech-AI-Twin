import React, { useState } from "react";

interface AuditLog {
  id: number;
  result: string;
  ts: string;
}

const AuditIncidents: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(false);

  const runAudit = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/audit/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": import.meta.env.VITE_API_KEY,
        },
        body: JSON.stringify({
          user_id: "user123",
          model_version: "demo-v1",
          input: {
            income: 25000,
            age: 24,
            credit_score: 580,
            spending_ratio: 0.65,
          },
        }),
      });
      const data = await res.json();
      const ts = new Date().toISOString();
      setLogs(prev => [
        { id: prev.length + 1, result: data.audit_result, ts },
        ...prev,
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 text-white space-y-4">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-3xl font-bold">Audit Incidents</h1>
          <p className="text-brand-text-secondary">
            Run audits and review the latest results.
          </p>
        </div>
        <button
          onClick={runAudit}
          className="bg-blue-600 px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Running..." : "Run Audit"}
        </button>
      </div>

      <div className="bg-gray-900 rounded-xl p-4">
        {logs.length === 0 ? (
          <p className="text-sm text-gray-400">
            No audits run yet. Click “Run Audit” to start.
          </p>
        ) : (
          <ul className="space-y-2 text-sm">
            {logs.map((log) => (
              <li
                key={log.id}
                className="flex justify-between border-b border-gray-800 pb-2"
              >
                <span>{log.result}</span>
                <span className="text-gray-400">{log.ts}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default AuditIncidents;
