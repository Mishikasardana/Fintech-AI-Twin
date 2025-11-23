import React, { useEffect, useState } from "react";

interface SummaryData {
  total_spend: number;
  last_receipt: string;
  risk_score: number;
}

const formatUSD = (value: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);

const HomeDashboard: React.FC = () => {
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // simulate backend call
    setTimeout(() => {
      setSummary({
        total_spend: 2895.75,
        last_receipt: "The Corner Cafe – $15.80",
        risk_score: 0.41,
      });
      setLoading(false);
    }, 900);
  }, []);

  return (
    <div className="p-6 text-white space-y-6">
      <h1 className="text-3xl font-bold">Welcome back, Jane 👋</h1>
      <p className="text-brand-text-secondary">
        Here's a quick snapshot of your financial activity.
      </p>

      <div className="grid gap-6 md:grid-cols-3">

        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">Total Spend (30 days)</h2>
          <p className="text-2xl">
            {loading ? "Loading..." : formatUSD(summary!.total_spend)}
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">Latest Purchase</h2>
          <p className="text-xl">
            {loading ? "Loading..." : summary?.last_receipt}
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-5">
          <h2 className="text-lg font-semibold mb-2">AI Risk Score</h2>
          <p className="text-2xl">
            {loading ? "Loading..." : summary?.risk_score}
          </p>
          <p className="text-sm text-gray-400 mt-1">
            Lower is better ✅
          </p>
        </div>

      </div>
    </div>
  );
};

export default HomeDashboard;
