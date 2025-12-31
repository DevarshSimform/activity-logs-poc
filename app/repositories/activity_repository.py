from sqlalchemy.orm import Session
from app.database.models import ActivityLog
from app.database.models.activity import ActivityType


class ActivityRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        user_id: int,
        activity_type: ActivityType,
        action: str,
        request_id: str,
        data: str | None = None,
        task_id: int | None = None,
    ) -> ActivityLog:
        activity = ActivityLog(
            user_id=user_id,
            task_id=task_id,
            activity_type=activity_type,
            action=action,
            request_id=request_id,
            data=data,
        )
        db.add(activity)
        db.commit()
        return activity
