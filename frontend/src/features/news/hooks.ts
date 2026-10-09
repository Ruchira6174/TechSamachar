import { useQuery } from '@tanstack/react-query';
import { getNews, getLatestNews, getFeaturedNews, getArticle } from './api';

export const useNews = (page = 1, pageSize = 20, topic?: number, source?: number, sort = 'published_time') => {
  return useQuery({
    queryKey: ['news', { page, pageSize, topic, source, sort }],
    queryFn: () => getNews(page, pageSize, topic, source, sort),
  });
};

export const useLatestNews = (limit = 10) => {
  return useQuery({
    queryKey: ['news', 'latest', limit],
    queryFn: () => getLatestNews(limit),
  });
};

export const useFeaturedNews = (limit = 5) => {
  return useQuery({
    queryKey: ['news', 'featured', limit],
    queryFn: () => getFeaturedNews(limit),
  });
};

export const useArticle = (id: number) => {
  return useQuery({
    queryKey: ['article', id],
    queryFn: () => getArticle(id),
    enabled: !!id,
  });
};
