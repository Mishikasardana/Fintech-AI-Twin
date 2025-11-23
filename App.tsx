
import React, { useState } from 'react';
import { UserRole } from './types';
import CustomerDashboard from './screens/customer/CustomerDashboard';
import BankDashboard from './screens/bank/BankDashboard';
import { BriefcaseIcon, UserIcon, SparklesIcon } from './components/icons/Icons';
import FloatingChat from './components/FloatingChat';

export default function App() {
  const [userRole, setUserRole] = useState<UserRole | null>(null);

  const handleLogin = (role: UserRole) => {
    setUserRole(role);
  };

  const handleLogout = () => {
    setUserRole(null);
  };

  if (!userRole) {
    return (
      <div className="min-h-screen bg-brand-primary flex flex-col items-center justify-center p-4">
        <div className="text-center">
          <SparklesIcon className="w-16 h-16 text-brand-accent mx-auto mb-4" />
          <h1 className="text-4xl md:text-5xl font-bold text-brand-text-primary mb-2">Welcome to FinTech AI Twin</h1>
          <p className="text-lg text-brand-text-secondary mb-12">Your Personal Financial Intelligence Engine</p>
        </div>
        <div className="flex flex-col md:flex-row gap-6">
          <button
            onClick={() => handleLogin(UserRole.Customer)}
            className="group flex flex-col items-center justify-center p-8 bg-brand-secondary rounded-lg border border-transparent hover:border-brand-accent transition-all duration-300 w-64 h-64"
          >
            <UserIcon className="w-12 h-12 text-brand-text-secondary group-hover:text-brand-accent transition-colors mb-4" />
            <h2 className="text-2xl font-semibold text-brand-text-primary">Customer Portal</h2>
            <p className="text-brand-text-secondary mt-1">Access your AI financial twin.</p>
          </button>
          <button
            onClick={() => handleLogin(UserRole.Bank)}
            className="group flex flex-col items-center justify-center p-8 bg-brand-secondary rounded-lg border border-transparent hover:border-brand-accent transition-all duration-300 w-64 h-64"
          >
            <BriefcaseIcon className="w-12 h-12 text-brand-text-secondary group-hover:text-brand-accent transition-colors mb-4" />
            <h2 className="text-2xl font-semibold text-brand-text-primary">Bank Console</h2>
            <p className="text-brand-text-secondary mt-1">Administer models and audits.</p>
          </button>
        </div>
      </div>
    );
  }

 return (
  <>
    {userRole === UserRole.Customer && <CustomerDashboard onLogout={handleLogout} />}
    {userRole === UserRole.Bank && <BankDashboard onLogout={handleLogout} />}

    {/* ✅ Add chat here */}
    <FloatingChat />
  </>
);
}
