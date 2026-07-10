from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


class ActivityService:
    def log_action(self, db: Session, user_id: int | None, action: str, details: str | None = None) -> ActivityLog:
        entry = ActivityLog(action=action, details=details, user_id=user_id)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry


activity_service = ActivityService()
