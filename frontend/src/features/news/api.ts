import { fetchApi } from '../../lib/api-client';
import { Article, PaginatedResponse } from '../../types';

export const getNews = async (
  page = 1,
  pageSize = 20,
  topic?: number,
  source?: number,
  sort = 'published_time'
): Promise<PaginatedResponse<Article>> => {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
    sort,
  });
  if (topic) params.append('topic', topic.toString());
  if (source) params.append('source', source.toString());
  
  return fetchApi<PaginatedResponse<Article>>(`/news?${params.toString()}`);
};

export const getLatestNews = async (limit = 10): Promise<Article[]> => {
  return fetchApi<Article[]>(`/news/latest?limit=${limit}`);
};

export const getFeaturedNews = async (limit = 5): Promise<Article[]> => {
  return fetchApi<Article[]>(`/news/featured?limit=${limit}`);
};

export const getArticle = async (id: number): Promise<Article> => {
  return fetchApi<Article>(`/news/${id}`);
};
