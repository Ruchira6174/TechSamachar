import React from 'react';
import { useBookmarks } from '../features/bookmarks/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

const BookmarksPage = () => {
  const { data: bookmarks, isLoading, isError } = useBookmarks();

  if (isLoading) return <LoadingState />;
  if (isError) return <ErrorState message="Failed to load bookmarks." />;

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Saved Articles</h1>
      
      {bookmarks && bookmarks.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {bookmarks.map(b => (
            <ArticleCard key={b.id} article={b.article} />
          ))}
        </div>
      ) : (
        <EmptyState message="You haven't saved any articles yet." />
      )}
    </div>
  );
};

export default BookmarksPage;
