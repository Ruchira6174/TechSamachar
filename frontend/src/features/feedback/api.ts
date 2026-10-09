import { fetchApi } from '../../lib/api-client';

export interface FeedbackData {
  article_id: number;
  feedback_type: 'relevant' | 'not_relevant' | 'more_like_this' | 'less_like_this';
}

export const submitFeedback = async (data: FeedbackData): Promise<void> => {
  return fetchApi<void>('/feedback', {
    method: 'POST',
    body: JSON.stringify(data)
  });
};
