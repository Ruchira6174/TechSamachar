import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ArticleCard } from '../components/news/ArticleCard';
import { Article } from '../types';

const mockArticle: Article = {
  id: 1,
  title: 'Test Title',
  canonical_url: 'http://test.com',
  source_id: 1,
  source: { id: 1, name: 'Test Source', url: '', feed_url: '', source_type: 'rss', is_enabled: true, quality_score: 100 },
  topics: [{ id: 1, name: 'AI', slug: 'ai', default_priority: 50 }],
  description: 'Test description',
  created_at: new Date().toISOString(),
  published_time: new Date().toISOString()
};

describe('ArticleCard', () => {
  it('renders correctly', () => {
    render(
      <BrowserRouter>
        <ArticleCard article={mockArticle} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Test Title')).toBeDefined();
    expect(screen.getByText('Test Source')).toBeDefined();
    expect(screen.getByText('Test description')).toBeDefined();
    expect(screen.getByText('AI')).toBeDefined();
  });
});
