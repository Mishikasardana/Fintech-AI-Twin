
import React from 'react';
import { MenuIcon, LogoutIcon } from '../icons/Icons';

interface HeaderProps {
  userProfile: {
    name: string;
    role: string;
    avatarUrl: string;
  };
  onLogout: () => void;
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ userProfile, onLogout, onMenuClick }) => {
  return (
    <div className="relative z-10 flex-shrink-0 flex h-16 bg-brand-secondary shadow-md">
      <button
        onClick={onMenuClick}
        className="px-4 border-r border-gray-700 text-gray-400 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-brand-accent md:hidden"
      >
        <span className="sr-only">Open sidebar</span>
        <MenuIcon className="h-6 w-6" />
      </button>
      <div className="flex-1 px-4 flex justify-between items-center">
        <div className="flex-1 flex">
          {/* Search bar could go here */}
        </div>
        <div className="ml-4 flex items-center md:ml-6">
          <div className="ml-3 relative">
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-brand-text-primary">{userProfile.name}</p>
                <p className="text-xs text-brand-text-secondary">{userProfile.role}</p>
              </div>
              <img className="h-10 w-10 rounded-full" src={userProfile.avatarUrl} alt="User avatar" />
              <button
                onClick={onLogout}
                className="p-2 rounded-full text-brand-text-secondary hover:text-brand-text-primary hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
                title="Logout"
              >
                <LogoutIcon className="h-6 w-6"/>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
