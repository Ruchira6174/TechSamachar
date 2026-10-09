import React, { useState } from 'react';
import { useNews } from '../features/news/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

const LatestNewsPage = () => {
  const [page, setPage] = useState(1);
  const { data, isLoading, isError } = useNews(page, 12);

  if (isLoading) return <LoadingState />;
  if (isError) return <ErrorState message="Failed to load latest news." />;

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Latest News</h1>
      
      {data?.items && data.items.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.items.map(article => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
          
          <div className="mt-8 flex justify-center space-x-4">
            <button 
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <span className="inline-flex items-center text-sm text-gray-500">
              Page {page} of {data.pagination.total_pages}
            </span>
            <button 
              onClick={() => setPage(p => p + 1)}
              disabled={page >= data.pagination.total_pages}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      ) : (
        <EmptyState message="No news available right now." />
      )}
    </div>
  );
};

export default LatestNewsPage;
