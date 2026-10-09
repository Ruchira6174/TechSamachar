import { fetchApi } from '../../lib/api-client';

export interface TopicPreference {
  id?: number;
  topic_id: number;
  weight: number;
  is_enabled: boolean;
}

export interface Preference {
  id?: number;
  user_id?: number;
  preferred_sort: string;
  topic_preferences: TopicPreference[];
}

export const getPreferences = async (): Promise<Preference> => {
  return fetchApi<Preference>('/preferences');
};

export const updatePreferences = async (data: Preference): Promise<Preference> => {
  return fetchApi<Preference>('/preferences', {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};
