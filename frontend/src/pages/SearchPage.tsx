import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useSearchNews } from '../features/search/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';
import { Search } from 'lucide-react';

const SearchPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  
  const [inputValue, setInputValue] = useState(initialQuery);
  const [debouncedQuery, setDebouncedQuery] = useState(initialQuery);
  const [page, setPage] = useState(1);
  
  // Debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(inputValue);
      setSearchParams(inputValue ? { q: inputValue } : {});
      setPage(1);
    }, 500);
    return () => clearTimeout(timer);
  }, [inputValue, setSearchParams]);

  const { data, isLoading, isError } = useSearchNews(debouncedQuery, page, 12);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Search News</h1>
        <div className="relative max-w-xl">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm shadow-sm"
            placeholder="Search articles, topics, summaries..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </div>
      </div>

      {!debouncedQuery ? (
        <div className="text-gray-500 mt-8">Enter a search term to find articles.</div>
      ) : isLoading ? (
        <LoadingState />
      ) : isError ? (
        <ErrorState message="Failed to perform search." />
      ) : data?.items && data.items.length > 0 ? (
        <>
          <p className="text-gray-600 mb-6">Found {data.pagination.total} results for "{debouncedQuery}"</p>
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
        <EmptyState message={`No results found for "${debouncedQuery}".`} />
      )}
    </div>
  );
};

export default SearchPage;
