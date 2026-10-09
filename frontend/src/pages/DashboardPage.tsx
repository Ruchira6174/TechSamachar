import React from 'react';
import { useLatestNews } from '../features/news/hooks';
import { useTopics } from '../features/topics/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

const DashboardPage = () => {
  const { data: latestNews, isLoading, isError } = useLatestNews(6);
  const { data: topics } = useTopics();
  
  if (isLoading) return <LoadingState />;
  if (isError) return <ErrorState message="Failed to load dashboard data." />;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <header>
        <h1 className="text-3xl font-bold text-gray-900">Your Briefing</h1>
        <p className="mt-2 text-gray-600">Top stories based on your interests.</p>
      </header>

      <section>
        <h2 className="text-xl font-bold text-gray-900 mb-4">Latest Technology News</h2>
        {latestNews && latestNews.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {latestNews.map(article => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        ) : (
          <EmptyState message="No news available right now." />
        )}
      </section>

      {/* Featured topics section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {topics?.slice(0, 2).map(topic => (
          <section key={topic.id}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">{topic.name}</h2>
              <a href={`/topics/${topic.slug}`} className="text-sm font-medium text-blue-600 hover:text-blue-800">View all</a>
            </div>
            {/* We could use useTopicNews here, but for simplicity in Phase 3 dashboard we might just show an empty placeholder or fetch 2 per topic */}
            <div className="bg-white p-6 rounded-lg border border-gray-200 text-center text-gray-500 text-sm">
              Explore the latest in {topic.name}. Click 'View all' to see articles.
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default DashboardPage;
