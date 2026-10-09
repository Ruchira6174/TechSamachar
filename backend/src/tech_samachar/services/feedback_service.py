from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tech_samachar.db.models.preference import Feedback

class FeedbackService:
    def __init__(self, db: Session):
        self.db = db

    def add_feedback(self, article_id: int, feedback_type: str, user_id: int = 1) -> Feedback:
        valid_types = ['relevant', 'not_relevant', 'more_like_this', 'less_like_this']
        if feedback_type not in valid_types:
            raise ValueError(f"Invalid feedback type: {feedback_type}")
            
        try:
            f = Feedback(user_id=user_id, article_id=article_id, feedback_type=feedback_type)
            self.db.add(f)
            self.db.commit()
            return f
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Invalid article ID")
