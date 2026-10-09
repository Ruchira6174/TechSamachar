import { fetchApi } from '../../lib/api-client';
import { Article } from '../../types';

export interface Bookmark {
  id: number;
  article_id: number;
  created_at: string;
  article: Article;
}

export const getBookmarks = async (): Promise<Bookmark[]> => {
  return fetchApi<Bookmark[]>('/bookmarks');
};

export const addBookmark = async (articleId: number): Promise<Bookmark> => {
  return fetchApi<Bookmark>(`/bookmarks/${articleId}`, { method: 'POST' });
};

export const removeBookmark = async (articleId: number): Promise<void> => {
  return fetchApi<void>(`/bookmarks/${articleId}`, { method: 'DELETE' });
};
