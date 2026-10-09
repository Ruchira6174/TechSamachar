import { fetchApi } from '../../lib/api-client';
import { Article } from '../../types';

export interface BriefingArticle {
  id: number;
  rank_position: int;
  article: Article;
}

export interface Briefing {
  id: number;
  briefing_date: string;
  summary_text: string;
  created_at: string;
  articles: BriefingArticle[];
}

export const getLatestBriefing = async (): Promise<Briefing> => {
  return fetchApi<Briefing>('/briefing');
};

export const getBriefingByDate = async (date: string): Promise<Briefing> => {
  return fetchApi<Briefing>(`/briefing/${date}`);
};
