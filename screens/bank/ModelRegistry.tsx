import React, { useState } from "react";

interface ModelInfo {
  id: string;
  name: string;
  version: string;
  status: "active" | "paused";
}

const initialModels: ModelInfo[] = [
  { id: "credit-risk", name: "Credit Risk Model", version: "v1.0", status: "active" },
  { id: "fraud-det", name: "Fraud Detection", version: "v0.9", status: "paused" },
  { id: "offer-engine", name: "Offer Recommender", version: "v0.5", status: "active" },
];

const ModelRegistry: React.FC = () => {
  const [models, setModels] = useState<ModelInfo[]>(initialModels);
  const [message, setMessage] = useState<string | null>(null);

  const toggleStatus = async (model: ModelInfo) => {
    const newStatus = model.status === "active" ? "paused" : "active";

    // hit backend just to log this decision
    try {
      const res = await fetch("http://127.0.0.1:8000/decision", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": import.meta.env.VITE_API_KEY,
        },
        body: JSON.stringify({
          model_id: model.id,
          action: newStatus,
        }),
      });
      await res.json();
      setModels(prev =>
        prev.map(m =>
          m.id === model.id ? { ...m, status: newStatus } : m
        )
      );
      setMessage(`Updated ${model.name} → ${newStatus}`);
      setTimeout(() => setMessage(null), 2500);
    } catch (err) {
      console.error(err);
      setMessage("Failed to update model status");
      setTimeout(() => setMessage(null), 2500);
    }
  };

  return (
    <div className="p-6 text-white space-y-4">
      <h1 className="text-3xl font-bold mb-2">Model Registry</h1>
      <p className="text-brand-text-secondary mb-4">
        View and control models powering AI decisions.
      </p>

      {message && (
        <div className="bg-gray-800 border border-gray-600 rounded-md px-3 py-2 text-sm">
          {message}
        </div>
      )}

      <div className="bg-gray-900 rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-800">
            <tr>
              <th className="px-4 py-3">Model</th>
              <th className="px-4 py-3">Version</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {models.map((m) => (
              <tr key={m.id} className="border-t border-gray-800">
                <td className="px-4 py-3">{m.name}</td>
                <td className="px-4 py-3">{m.version}</td>
                <td className="px-4 py-3 capitalize">{m.status}</td>
                <td className="px-4 py-3 text-right">
                  <button
                    onClick={() => toggleStatus(m)}
                    className="px-3 py-1 rounded bg-blue-600 text-xs"
                  >
                    {m.status === "active" ? "Pause" : "Activate"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelRegistry;
