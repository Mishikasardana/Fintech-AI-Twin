
import React, { useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import type { NavItem } from "../../types";
import {
  ChartBarIcon,
  AdjustmentsIcon,
  ShieldCheckIcon,
  ReceiptIcon,
} from "../../components/icons/Icons";

import BankHome from "./BankHome.tsx";
import ModelRegistry from "./ModelRegistry";
import AuditIncidents from "./AuditIncidents";
import Governance from "./Governance.tsx";


const bankNavItems: NavItem[] = [
  { label: "Dashboard", screen: "dashboard", icon: ChartBarIcon },
  { label: "Model Registry", screen: "models", icon: AdjustmentsIcon },
  { label: "Audit Incidents", screen: "incidents", icon: ShieldCheckIcon },
  { label: "Governance", screen: "governance", icon: ReceiptIcon },
];

const userProfile = {
  name: "Admin User",
  role: "Bank Administrator",
  avatarUrl: "https://picsum.photos/seed/admin/200",
};

interface BankDashboardProps {
  onLogout: () => void;
}

const BankDashboard: React.FC<BankDashboardProps> = ({ onLogout }) => {
  const [activeScreen, setActiveScreen] = useState("dashboard");

  const renderContent = () => {
    switch (activeScreen) {
      case "dashboard":
        return <BankHome />;
      case "models":
        return <ModelRegistry />;
      case "incidents":
        return <AuditIncidents />;
      case "governance":
        return <Governance />;
      default:
        return <BankHome />;
    }
  };

  return (
    <DashboardLayout
      navItems={bankNavItems}
      activeScreen={activeScreen}
      setActiveScreen={setActiveScreen}
      onLogout={onLogout}
      userProfile={userProfile}
    >
      {renderContent()}
    </DashboardLayout>
  );
};

export default BankDashboard;
