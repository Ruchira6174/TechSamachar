import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTopicNews, useTopics } from '../features/topics/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

const TopicPage = () => {
  const { slug } = useParams<{ slug: string }>();
  const [page, setPage] = useState(1);
  
  const { data: topics } = useTopics();
  const topic = topics?.find(t => t.slug === slug);
  
  const { data, isLoading, isError } = useTopicNews(slug || '', page, 12);

  if (!slug) return <ErrorState message="Invalid topic" />;
  if (isLoading) return <LoadingState />;
  if (isError) return <ErrorState message="Failed to load topic news." />;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{topic?.name || slug}</h1>
        {topic?.description && <p className="mt-2 text-gray-600">{topic.description}</p>}
      </div>
      
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
        <EmptyState message={`No news available for ${topic?.name || slug}.`} />
      )}
    </div>
  );
};

export default TopicPage;
