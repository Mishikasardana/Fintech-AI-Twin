import React, { useEffect, useState } from "react";

export default function AITwinEditor() {
  const [twin, setTwin] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/twin/123", {
      headers: {
        "x-api-key": import.meta.env.VITE_API_KEY,
      },
    })
      .then(res => res.json())
      .then(data => {
        setTwin(data.twin);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-white p-6">Loading...</p>;

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-6">AI Twin Editor</h1>

      <div className="bg-gray-800 p-6 rounded-xl space-y-4">
        <label className="block">
          <span>Income Estimate</span>
          <input
            className="mt-2 p-2 rounded bg-gray-700 w-full"
            type="number"
            value={twin.income_est}
            onChange={(e) =>
              setTwin({ ...twin, income_est: Number(e.target.value) })
            }
          />
        </label>

        <label className="block">
          <span>Risk Score</span>
          <input
            className="mt-2 p-2 rounded bg-gray-700 w-full"
            type="number"
            step="0.01"
            value={twin.risk_score}
            onChange={(e) =>
              setTwin({ ...twin, risk_score: Number(e.target.value) })
            }
          />
        </label>

        <button
          className="mt-6 bg-blue-600 px-4 py-2 rounded"
          onClick={() => {
            fetch("http://127.0.0.1:8000/decision", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "x-api-key": import.meta.env.VITE_API_KEY,
              },
              body: JSON.stringify(twin),
            });
            alert("✅ Updated successfully!");
          }}
        >
          Save Changes
        </button>
      </div>
    </div>
  );
}
