import React from 'react';
import { Link } from 'react-router-dom';
import { Home, Rss, Search, Bookmark, Settings } from 'lucide-react';
import { useTopics } from '../../features/topics/hooks';

const AppSidebar = () => {
  const { data: topics } = useTopics();
  
  return (
    <aside className="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-gray-200">
        <Link to="/" className="text-xl font-bold text-blue-600">Tech Samachar</Link>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="px-4 space-y-1">
          <Link to="/" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <Home className="mr-3 h-5 w-5 text-gray-500" /> Dashboard
          </Link>
          <Link to="/briefing" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <svg className="mr-3 h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2.5 2.5 0 00-2.5-2.5H15"></path></svg>
            Daily Briefing
          </Link>
          <Link to="/latest" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <Rss className="mr-3 h-5 w-5 text-gray-500" /> Latest News
          </Link>
          <Link to="/search" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <Search className="mr-3 h-5 w-5 text-gray-500" /> Search
          </Link>
          <Link to="/bookmarks" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <Bookmark className="mr-3 h-5 w-5 text-gray-500" /> Bookmarks
          </Link>
          <Link to="/preferences" className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
            <Settings className="mr-3 h-5 w-5 text-gray-500" /> Preferences
          </Link>
        </nav>
        
        <div className="mt-8">
          <h3 className="px-6 text-xs font-semibold text-gray-500 uppercase tracking-wider">Topics</h3>
          <nav className="mt-2 px-4 space-y-1">
            {topics?.map(topic => (
              <Link key={topic.id} to={`/topics/${topic.slug}`} className="flex items-center px-2 py-2 text-sm font-medium rounded-md hover:bg-gray-100">
                {topic.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </aside>
  );
};

export default AppSidebar;
