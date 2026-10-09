import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import { AppLayout } from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import LatestNewsPage from './pages/LatestNewsPage';
import TopicPage from './pages/TopicPage';
import ArticlePage from './pages/ArticlePage';
import SearchPage from './pages/SearchPage';
import BookmarksPage from './pages/BookmarksPage';
import PreferencesPage from './pages/PreferencesPage';
import BriefingPage from './pages/BriefingPage';
import NotFoundPage from './pages/NotFoundPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    errorElement: <NotFoundPage />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'latest', element: <LatestNewsPage /> },
      { path: 'briefing', element: <BriefingPage /> },
      { path: 'topics/:slug', element: <TopicPage /> },
      { path: 'article/:id', element: <ArticlePage /> },
      { path: 'search', element: <SearchPage /> },
      { path: 'bookmarks', element: <BookmarksPage /> },
      { path: 'preferences', element: <PreferencesPage /> },
    ],
  },
]);
