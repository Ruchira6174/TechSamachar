import { useQuery } from '@tanstack/react-query';
import { searchNews } from './api';

export const useSearchNews = (query: string, page = 1, pageSize = 20) => {
  return useQuery({
    queryKey: ['search', query, { page, pageSize }],
    queryFn: () => searchNews(query, page, pageSize),
    enabled: query.length > 0,
  });
};
