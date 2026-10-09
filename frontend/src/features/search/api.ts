import { fetchApi } from '../../lib/api-client';
import { Article, PaginatedResponse } from '../../types';

export const searchNews = async (
  query: string,
  page = 1,
  pageSize = 20
): Promise<PaginatedResponse<Article>> => {
  const params = new URLSearchParams({
    q: query,
    page: page.toString(),
    page_size: pageSize.toString(),
  });
  
  return fetchApi<PaginatedResponse<Article>>(`/search?${params.toString()}`);
};
