
import React from 'react';
import type { NavItem } from '../../types';
import { SparklesIcon, XIcon } from '../icons/Icons';

interface SidebarProps {
  navItems: NavItem[];
  activeScreen: string;
  setActiveScreen: (screen: string) => void;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ navItems, activeScreen, setActiveScreen, sidebarOpen, setSidebarOpen }) => {
    
  const navLinkClasses = (screen: string) => 
    `flex items-center px-4 py-3 text-lg font-medium rounded-lg transition-colors duration-200 ${
      activeScreen === screen 
        ? 'bg-brand-accent text-white' 
        : 'text-brand-text-secondary hover:bg-gray-700 hover:text-brand-text-primary'
    }`;

  const sidebarContent = (
    <div className="h-full flex flex-col bg-brand-secondary">
        <div className="flex items-center justify-between h-16 px-4 flex-shrink-0 border-b border-gray-700">
          <div className="flex items-center">
            <SparklesIcon className="h-8 w-8 text-brand-accent" />
            <span className="ml-3 text-2xl font-semibold text-brand-text-primary">AI Twin</span>
          </div>
          <button
              onClick={() => setSidebarOpen(false)}
              className="md:hidden text-gray-400 hover:text-white"
          >
              <XIcon className="h-6 w-6" />
          </button>
        </div>
        <nav className="flex-1 mt-5 px-4 space-y-2">
            {navItems.map((item) => (
            <a
                key={item.label}
                href="#"
                onClick={(e) => {
                e.preventDefault();
                setActiveScreen(item.screen);
                setSidebarOpen(false);
                }}
                className={navLinkClasses(item.screen)}
            >
                <item.icon className="h-6 w-6 mr-4" />
                {item.label}
            </a>
            ))}
        </nav>
    </div>
  );

  return (
    <>
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out`}>
        <div className="fixed inset-0 bg-gray-900 bg-opacity-75" onClick={() => setSidebarOpen(false)}></div>
        <div className="relative flex-1 flex flex-col max-w-xs w-full">
          {sidebarContent}
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          {sidebarContent}
        </div>
      </div>
    </>
  );
};

export default Sidebar;
