import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getPreferences, updatePreferences, Preference } from './api';

export const usePreferences = () => {
  return useQuery({
    queryKey: ['preferences'],
    queryFn: getPreferences,
  });
};

export const useUpdatePreferences = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Preference) => updatePreferences(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['preferences'] });
      queryClient.invalidateQueries({ queryKey: ['news'] }); // Refresh news based on new prefs
    },
  });
};
