import { useQuery } from '@tanstack/react-query';
import { getTopics, getTopicNews } from './api';

export const useTopics = () => {
  return useQuery({
    queryKey: ['topics'],
    queryFn: getTopics,
  });
};

export const useTopicNews = (slug: string, page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: ['topics', slug, 'news', { page, pageSize }],
    queryFn: () => getTopicNews(slug, page, pageSize),
    enabled: !!slug,
  });
};
