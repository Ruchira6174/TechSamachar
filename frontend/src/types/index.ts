export interface Source {
  id: number;
  name: string;
  url: string;
  feed_url: string;
  source_type: string;
  is_enabled: boolean;
  quality_score: number;
}

export interface Topic {
  id: number;
  name: string;
  slug: string;
  description?: string;
  default_priority: number;
}

export interface ArticleSummary {
  id: number;
  summary_text: string;
  provider?: string;
  model_name?: string;
}

export interface Article {
  id: number;
  title: string;
  canonical_url: string;
  author?: string;
  published_time?: string;
  description?: string;
  source_id: number;
  source?: Source;
  topics: Topic[];
  summary?: ArticleSummary;
  created_at: string;
}

export interface Pagination {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: Pagination;
}
