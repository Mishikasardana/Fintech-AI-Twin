
import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import type { NavItem } from '../../types';

interface DashboardLayoutProps {
  navItems: NavItem[];
  activeScreen: string;
  setActiveScreen: (screen: string) => void;
  onLogout: () => void;
  children: React.ReactNode;
  userProfile: { name: string; role: string; avatarUrl: string };
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ navItems, activeScreen, setActiveScreen, onLogout, children, userProfile }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-brand-primary overflow-hidden">
      <Sidebar 
        navItems={navItems} 
        activeScreen={activeScreen} 
        setActiveScreen={setActiveScreen} 
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      <div className="flex flex-col flex-1 w-0 overflow-hidden">
        <Header 
            userProfile={userProfile} 
            onLogout={onLogout} 
            onMenuClick={() => setSidebarOpen(true)}
        />
        <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none p-6 md:p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
