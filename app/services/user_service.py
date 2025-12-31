import json
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.services.activity_service import ActivityService
from app.schemas.user import UserProfileUpdate
from app.database.models import User


class UserService:
    @staticmethod
    async def update_profile(
        *,
        db: Session,
        current_user: User,
        payload: UserProfileUpdate,
        background_tasks: BackgroundTasks,
        request_id: str,
        kafka_producer,
        kafka_topic: str,
        meta: dict,
    ) -> User:

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(current_user, field, value)

        updated_user = UserRepository.update(db, current_user)

        # Add activity log in background
        background_tasks.add_task(
            ActivityService.log_profile_updated,
            user_id=current_user.id,
            request_id=request_id,
            data=update_data,
            kafka_producer=kafka_producer,
            topic=kafka_topic,
            actor={
                "id": current_user.id,
                "email": current_user.email,
                "is_admin": current_user.is_admin,
            },
            meta=meta,
        )

        return updated_user
