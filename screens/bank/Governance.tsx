import React, { useState } from "react";

interface PolicyState {
  human_in_loop: boolean;
  allow_auto_approve: boolean;
  enable_explanations: boolean;
}

const Governance: React.FC = () => {
  const [policy, setPolicy] = useState<PolicyState>({
    human_in_loop: true,
    allow_auto_approve: false,
    enable_explanations: true,
  });

  const [message, setMessage] = useState<string | null>(null);

  const toggle = (key: keyof PolicyState) => {
    setPolicy(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const saveGovernance = async () => {
    try {
      // use consent/update just to log settings in backend
      const payloads = Object.entries(policy).map(([k, v]) => ({
        user_id: "admin",
        feature: `policy_${k}`,
        allowed: v,
        expiry: "2025-12-31",
      }));

      await Promise.all(
        payloads.map(p =>
          fetch("http://127.0.0.1:8000/consent/update", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "x-api-key": import.meta.env.VITE_API_KEY,
            },
            body: JSON.stringify(p),
          })
        )
      );

      setMessage("✅ Governance settings saved");
      setTimeout(() => setMessage(null), 2500);
    } catch (err) {
      console.error(err);
      setMessage("Failed to save settings");
      setTimeout(() => setMessage(null), 2500);
    }
  };

  return (
    <div className="p-6 text-white space-y-4">
      <h1 className="text-3xl font-bold mb-2">Governance Center</h1>
      <p className="text-brand-text-secondary mb-4">
        Configure human oversight, auto-approval and explanations.
      </p>

      {message && (
        <div className="bg-gray-800 border border-gray-600 rounded-md px-3 py-2 text-sm">
          {message}
        </div>
      )}

      <div className="bg-gray-900 rounded-xl p-6 space-y-4 w-full md:w-[480px]">
        <label className="flex items-center justify-between">
          <span>Human-in-the-loop required for high-risk loans</span>
          <input
            type="checkbox"
            checked={policy.human_in_loop}
            onChange={() => toggle("human_in_loop")}
          />
        </label>

        <label className="flex items-center justify-between">
          <span>Allow automatic approvals for low-risk cases</span>
          <input
            type="checkbox"
            checked={policy.allow_auto_approve}
            onChange={() => toggle("allow_auto_approve")}
          />
        </label>

        <label className="flex items-center justify-between">
          <span>Always generate user-facing explanations</span>
          <input
            type="checkbox"
            checked={policy.enable_explanations}
            onChange={() => toggle("enable_explanations")}
          />
        </label>

        <button
          onClick={saveGovernance}
          className="mt-4 bg-blue-600 px-4 py-2 rounded w-full"
        >
          Save Governance Settings
        </button>
      </div>
    </div>
  );
};

export default Governance;
