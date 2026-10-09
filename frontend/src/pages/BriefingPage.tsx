import React from 'react';
import { useLatestBriefing } from '../features/briefing/hooks';
import { ArticleCard } from '../components/news/ArticleCard';
import { LoadingState, ErrorState, EmptyState } from '../components/common/States';

const BriefingPage = () => {
  const { data: briefing, isLoading, isError } = useLatestBriefing();

  if (isLoading) return <LoadingState />;
  if (isError || !briefing) return <EmptyState message="No daily briefing available yet today." />;

  const date = new Date(briefing.briefing_date).toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Your Daily Briefing</h1>
        <p className="mt-2 text-lg text-gray-600">{date}</p>
      </header>

      <section className="bg-blue-50 border border-blue-100 rounded-xl p-8 mb-12 shadow-sm">
        <h2 className="text-sm font-bold text-blue-800 uppercase tracking-widest mb-4 flex items-center">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          Executive Summary
        </h2>
        <p className="text-gray-800 text-lg leading-relaxed">{briefing.summary_text}</p>
      </section>

      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Top Stories</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {briefing.articles.map(ba => (
            <ArticleCard key={ba.id} article={ba.article} />
          ))}
        </div>
      </section>
    </div>
  );
};

export default BriefingPage;
