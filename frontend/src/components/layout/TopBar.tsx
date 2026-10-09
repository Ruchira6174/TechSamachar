import React from 'react';
import { Menu } from 'lucide-react';

const TopBar = () => {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 md:px-6">
      <div className="flex items-center md:hidden">
        <button className="text-gray-500 hover:text-gray-700">
          <Menu className="h-6 w-6" />
        </button>
        <span className="ml-3 text-lg font-bold text-blue-600">Tech Samachar</span>
      </div>
      <div className="hidden md:block">
        {/* Placeholder for future topbar items like user profile */}
      </div>
    </header>
  );
};

export default TopBar;
