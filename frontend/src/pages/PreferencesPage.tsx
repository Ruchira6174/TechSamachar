import React from 'react';
import { usePreferences, useUpdatePreferences } from '../features/preferences/hooks';
import { useTopics } from '../features/topics/hooks';
import { LoadingState, ErrorState } from '../components/common/States';

const PreferencesPage = () => {
  const { data: prefs, isLoading: prefsLoading, isError: prefsError } = usePreferences();
  const { data: topics, isLoading: topicsLoading } = useTopics();
  const updatePrefs = useUpdatePreferences();

  if (prefsLoading || topicsLoading) return <LoadingState />;
  if (prefsError || !prefs) return <ErrorState message="Failed to load preferences." />;

  const handleToggle = (topicId: number) => {
    const existing = prefs.topic_preferences.find(tp => tp.topic_id === topicId);
    let newTopicPrefs = [...prefs.topic_preferences];
    
    if (existing) {
      newTopicPrefs = newTopicPrefs.map(tp => 
        tp.topic_id === topicId ? { ...tp, is_enabled: !tp.is_enabled } : tp
      );
    } else {
      newTopicPrefs.push({ topic_id: topicId, weight: 1.0, is_enabled: true });
    }
    
    updatePrefs.mutate({
      ...prefs,
      topic_preferences: newTopicPrefs
    });
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-sm border border-gray-200">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Personalize Your Feed</h1>
      
      <div className="mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Topics</h2>
        <div className="space-y-4">
          {topics?.map(topic => {
            const pref = prefs.topic_preferences.find(tp => tp.topic_id === topic.id);
            const isEnabled = pref ? pref.is_enabled : false;
            
            return (
              <div key={topic.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-md">
                <div>
                  <h3 className="font-semibold text-gray-900">{topic.name}</h3>
                  {topic.description && <p className="text-sm text-gray-500">{topic.description}</p>}
                </div>
                <button 
                  onClick={() => handleToggle(topic.id)}
                  className={`px-4 py-2 rounded-md font-medium text-sm ${isEnabled ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}
                >
                  {isEnabled ? 'Following' : 'Follow'}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default PreferencesPage;
