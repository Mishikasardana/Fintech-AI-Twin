
import React, { useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import type { NavItem } from '../../types';
import { HomeIcon, ReceiptIcon, AdjustmentsIcon, ShieldCheckIcon, ChartBarIcon } from '../../components/icons/Icons';
import ReceiptList from './ReceiptList';
import PlaceholderScreen from './PlaceholderScreen';
import AITwinEditor from "./AITwinEditor";
import WhatIfSimulator from "./WhatIfSimulator";
import DataWallet from "./DataWallet";
import HomeDashboard from "./HomeDashboard";
import APITester from "./APITester";





const customerNavItems: NavItem[] = [
  { label: 'Home', screen: 'home', icon: HomeIcon },
  { label: 'AI Receipts', screen: 'receipts', icon: ReceiptIcon },
  { label: 'AI Twin Editor', screen: 'editor', icon: AdjustmentsIcon },
  { label: 'What-If Simulator', screen: 'simulator', icon: ChartBarIcon },
  { label: 'Data Wallet', screen: 'wallet', icon: ShieldCheckIcon },
];

const userProfile = {
  name: 'Jane Doe',
  role: 'Customer',
  avatarUrl: 'https://picsum.photos/seed/customer/200',
};

interface CustomerDashboardProps {
  onLogout: () => void;
}

const CustomerDashboard: React.FC<CustomerDashboardProps> = ({ onLogout }) => {
  const [activeScreen, setActiveScreen] = useState('receipts');

  const renderContent = () => {
  switch (activeScreen) {
    case 'receipts':
      return <ReceiptList />;

    case 'home':
  return <HomeDashboard />;

  case 'tester':
  return <APITester />;


    case 'editor':
      return <AITwinEditor />;  // ✅ NEW

    case 'simulator':
  return <WhatIfSimulator />;


    case 'wallet':
  return <DataWallet />;


    default:
      return <ReceiptList />;
  }
};

  return (
    <DashboardLayout
      navItems={customerNavItems}
      activeScreen={activeScreen}
      setActiveScreen={setActiveScreen}
      onLogout={onLogout}
      userProfile={userProfile}
    >
      {renderContent()}
    </DashboardLayout>
  );
};

export default CustomerDashboard;
