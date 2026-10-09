import { useQuery } from '@tanstack/react-query';
import { getLatestBriefing, getBriefingByDate } from './api';

export const useLatestBriefing = () => {
  return useQuery({
    queryKey: ['briefing', 'latest'],
    queryFn: getLatestBriefing,
    retry: false, // Don't retry much if 404
  });
};

export const useBriefingByDate = (date: string) => {
  return useQuery({
    queryKey: ['briefing', date],
    queryFn: () => getBriefingByDate(date),
    enabled: !!date,
    retry: false,
  });
};
