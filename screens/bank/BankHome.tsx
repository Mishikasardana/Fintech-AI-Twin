import React, { useEffect, useState } from "react";

interface AuditResult {
  audit_result: string;
  data: any;
}

const BankHome: React.FC = () => {
  const [audit, setAudit] = useState<AuditResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
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
        setAudit(data);
      } catch (err) {
        console.error("Audit error", err);
      } finally {
        setLoading(false);
      }
    };

    runAudit();
  }, []);

  return (
    <div className="p-6 text-white space-y-6">
      <h1 className="text-3xl font-bold">Bank Dashboard</h1>
      <p className="text-brand-text-secondary">
        High-level view of model performance, audits and system health.
      </p>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">Latest Audit Status</h2>
          <p className="text-2xl">
            {loading
              ? "Running..."
              : audit
              ? audit.audit_result
              : "No data yet"}
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">Models Active</h2>
          <p className="text-2xl">3</p>
          <p className="text-sm text-gray-400 mt-1">
            Demo count – wired for UI exploration.
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">Incidents (24h)</h2>
          <p className="text-2xl">0</p>
          <p className="text-sm text-gray-400 mt-1">
            Audit endpoint currently returns “no issues detected ✅”.
          </p>
        </div>
      </div>
    </div>
  );
};

export default BankHome;
