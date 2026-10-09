import { fetchApi } from '../../lib/api-client';
import { Topic, PaginatedResponse, Article } from '../../types';

export const getTopics = async (): Promise<Topic[]> => {
  return fetchApi<Topic[]>('/topics');
};

export const getTopicNews = async (
  slug: string,
  page = 1,
  pageSize = 20
): Promise<PaginatedResponse<Article>> => {
  return fetchApi<PaginatedResponse<Article>>(`/topics/${slug}/news?page=${page}&page_size=${pageSize}`);
};
