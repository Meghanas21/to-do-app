from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.task import Task


class AnalyticsService:
    def get_analytics(self, db: Session) -> dict:
        total_tasks = db.query(Task).count()
        completed_tasks = db.query(Task).filter(Task.status == "completed").count()
        pending_tasks = total_tasks - completed_tasks
        most_searched = (
            db.query(ActivityLog.details, func.count(ActivityLog.id).label("count"))
            .filter(ActivityLog.action == "search")
            .group_by(ActivityLog.details)
            .order_by(func.count(ActivityLog.id).desc())
            .first()
        )
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "most_searched_query": most_searched[0] if most_searched else None,
            "most_searched_count": most_searched[1] if most_searched else 0,
        }


analytics_service = AnalyticsService()
