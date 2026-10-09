import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useArticle } from '../features/news/hooks';
import { LoadingState, ErrorState } from '../components/common/States';

const ArticlePage = () => {
  const { id } = useParams<{ id: string }>();
  const { data: article, isLoading, isError } = useArticle(Number(id));

  if (isLoading) return <LoadingState />;
  if (isError || !article) return <ErrorState message="Article not found or failed to load." />;

  const date = article.published_time ? new Date(article.published_time).toLocaleDateString() : 'Unknown Date';

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center text-sm text-gray-500 mb-4 space-x-2">
        {article.source && <span className="font-semibold text-blue-600">{article.source.name}</span>}
        <span>&bull;</span>
        <span>{date}</span>
        {article.author && (
          <>
            <span>&bull;</span>
            <span>By {article.author}</span>
          </>
        )}
      </div>
      
      <h1 className="text-4xl font-bold text-gray-900 mb-6">{article.title}</h1>
      
      <div className="flex flex-wrap gap-2 mb-8">
        {article.topics.map(t => (
          <Link key={t.id} to={`/topics/${t.slug}`} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800 hover:bg-gray-200">
            {t.name}
          </Link>
        ))}
      </div>

      {article.summary ? (
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-6 mb-8">
          <h2 className="text-sm font-semibold text-blue-800 uppercase tracking-wide mb-2 flex items-center">
            AI Summary
            {article.summary.model_name && <span className="ml-2 text-xs font-normal text-blue-600 opacity-75">via {article.summary.model_name}</span>}
          </h2>
          <p className="text-gray-800 text-lg leading-relaxed">{article.summary.summary_text}</p>
        </div>
      ) : article.description ? (
        <div className="prose max-w-none text-gray-700 mb-8">
          <p className="text-lg leading-relaxed">{article.description}</p>
        </div>
      ) : null}

      <div className="mt-8 pt-8 border-t border-gray-200">
        <a 
          href={article.canonical_url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
        >
          Read full article at source
        </a>
      </div>
    </div>
  );
};

export default ArticlePage;
