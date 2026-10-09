import { useMutation } from '@tanstack/react-query';
import { submitFeedback, FeedbackData } from './api';

export const useSubmitFeedback = () => {
  return useMutation({
    mutationFn: (data: FeedbackData) => submitFeedback(data),
  });
};
