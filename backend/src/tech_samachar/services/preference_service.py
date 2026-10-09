from sqlalchemy.orm import Session
from tech_samachar.db.models.preference import Preference, TopicPreference
from tech_samachar.schemas.preference import PreferenceBase
from tech_samachar.db.models.article import Topic

class PreferenceService:
    def __init__(self, db: Session):
        self.db = db

    def get_preferences(self, user_id: int = 1) -> Preference:
        pref = self.db.query(Preference).filter(Preference.user_id == user_id).first()
        if not pref:
            pref = Preference(user_id=user_id)
            self.db.add(pref)
            self.db.commit()
            
            # Init topic preferences
            topics = self.db.query(Topic).all()
            for t in topics:
                tp = TopicPreference(preference_id=pref.id, topic_id=t.id)
                self.db.add(tp)
            self.db.commit()
            
        return pref

    def update_preferences(self, data: PreferenceBase, user_id: int = 1) -> Preference:
        pref = self.get_preferences(user_id)
        pref.preferred_sort = data.preferred_sort
        
        # Clear existing topic prefs
        self.db.query(TopicPreference).filter(TopicPreference.preference_id == pref.id).delete()
        
        # Create new topic prefs
        for tp_data in data.topic_preferences:
            tp = TopicPreference(
                preference_id=pref.id,
                topic_id=tp_data.topic_id,
                weight=tp_data.weight,
                is_enabled=tp_data.is_enabled
            )
            self.db.add(tp)
            
        self.db.commit()
        return pref
