import React, { useState } from "react";

export default function WhatIfSimulator() {
  const [incomeChange, setIncomeChange] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runSimulation = async () => {
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/what-if", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": import.meta.env.VITE_API_KEY,
      },
      body: JSON.stringify({
        income_change: Number(incomeChange),
      }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-6">What-If Simulator</h1>

      <div className="bg-gray-800 p-6 rounded-xl space-y-4 w-96">
        <label>
          <span>Income Change ($)</span>
          <input
            type="number"
            className="mt-2 p-2 rounded bg-gray-700 w-full"
            value={incomeChange}
            onChange={(e) => setIncomeChange(e.target.value)}
          />
        </label>

        <button
          onClick={runSimulation}
          className="bg-blue-600 px-4 py-2 rounded w-full"
          disabled={loading}
        >
          {loading ? "Running..." : "Run Simulation"}
        </button>

        {result && (
          <div className="mt-4 bg-gray-700 p-4 rounded">
            <h3 className="font-semibold mb-2">Result</h3>
            <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
