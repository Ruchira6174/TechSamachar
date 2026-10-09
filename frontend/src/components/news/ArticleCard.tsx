import React from 'react';
import { Article } from '../../../types';
import { Link } from 'react-router-dom';

export const ArticleCard = ({ article }: { article: Article }) => {
  const date = article.published_time ? new Date(article.published_time).toLocaleDateString() : 'Unknown Date';
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow p-5 flex flex-col h-full">
      <div className="flex-1">
        <div className="flex items-center text-xs text-gray-500 mb-2 space-x-2">
          {article.source && <span className="font-semibold text-gray-700">{article.source.name}</span>}
          <span>&bull;</span>
          <span>{date}</span>
        </div>
        <Link to={`/article/${article.id}`} className="block mt-2">
          <h3 className="text-lg font-bold text-gray-900 leading-tight hover:text-blue-600 transition-colors">{article.title}</h3>
        </Link>
        {article.summary ? (
          <p className="mt-3 text-sm text-gray-600 line-clamp-3">{article.summary.summary_text}</p>
        ) : article.description ? (
          <p className="mt-3 text-sm text-gray-600 line-clamp-3">{article.description}</p>
        ) : null}
      </div>
      <div className="mt-4 pt-4 border-t border-gray-100 flex flex-wrap gap-2 items-center justify-between">
        <div className="flex gap-2">
          {article.topics.slice(0, 2).map(t => (
            <Link key={t.id} to={`/topics/${t.slug}`} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {t.name}
            </Link>
          ))}
        </div>
        <div className="flex gap-2">
          {/* We'd hook these up to useAddBookmark and useSubmitFeedback */}
          <button className="text-gray-400 hover:text-blue-600 transition-colors" title="Bookmark">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>
          </button>
          <button className="text-gray-400 hover:text-green-600 transition-colors" title="More like this">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
          </button>
        </div>
      </div>
    </div>
  );
};
