from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.api.deps import get_db, get_current_user, get_kafka_producer
from app.core.config import settings
from app.database.models import User

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    kafka_producer=Depends(get_kafka_producer),
):
    request_id = request.state.request_id

    task_service = TaskService(db)

    return await task_service.create_task(
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


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    kafka_producer=Depends(get_kafka_producer),
):
    request_id = request.state.request_id

    task_service = TaskService(db)

    return await task_service.update_task(
        task_id=task_id,
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


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    kafka_producer=Depends(get_kafka_producer),
):
    request_id = request.state.request_id

    task_service = TaskService(db)

    await task_service.delete_task(
        task_id=task_id,
        current_user=current_user,
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
