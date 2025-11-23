import React, { useState } from "react";

export default function DataWallet() {
  const [consents, setConsents] = useState({
    share_with_bank: true,
    share_with_insurance: false,
    share_with_fintech_apps: false,
  });

  const updateConsent = async () => {
    await fetch("http://127.0.0.1:8000/consent/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": import.meta.env.VITE_API_KEY,
      },
      body: JSON.stringify(consents),
    });

    alert("✅ Consent settings updated successfully!");
  };

  const toggle = (key: keyof typeof consents) => {
    setConsents((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl font-bold mb-6">Data Wallet</h1>

      <div className="bg-gray-800 p-6 rounded-xl space-y-6 w-96">
        {Object.keys(consents).map((key) => (
          <label key={key} className="flex items-center justify-between">
            <span className="capitalize">
              {key.replace(/_/g, " ")}
            </span>
            <input
              type="checkbox"
              checked={consents[key as keyof typeof consents]}
              onChange={() => toggle(key as keyof typeof consents)}
            />
          </label>
        ))}

        <button
          onClick={updateConsent}
          className="bg-blue-600 w-full py-2 rounded mt-4"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
}
