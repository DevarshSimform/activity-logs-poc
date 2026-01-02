from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.deps import get_db, get_current_user, get_kafka_producer
from app.schemas.user import UserProfileUpdate, UserResponse
from app.services.user_service import UserService
from app.database.models import User

router = APIRouter()


@router.patch("/me/profile", response_model=UserResponse)
async def update_profile(
    payload: UserProfileUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    kafka_producer = Depends(get_kafka_producer),
):
    request_id = request.state.request_id

    user_service = UserService(db)

    return await user_service.update_profile(
        current_user=current_user,
        payload=payload,
        background_tasks=background_tasks,
        request_id=request_id,
        kafka_producer=kafka_producer,
        kafka_topic=settings.kafka_activity_topic,
        meta={
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "source": "fastapi",
        },
    )
