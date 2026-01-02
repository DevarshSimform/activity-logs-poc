from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskUpdate
from app.services.activity_service import ActivityService
from app.database.models import User, ActivityType

class TaskService:

    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)

    async def create_task(
        self,
        *,
        current_user: User,
        payload,
        background_tasks: BackgroundTasks,
        request_id: str,
        kafka_producer,
        kafka_topic: str,
        meta: dict,
    ):
        if payload.parent_task_id:
            parent_task = self.task_repo.get_by_id(payload.parent_task_id)
            if not parent_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent task not found",
                )
            if parent_task.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not allowed to create subtask for this parent task",
                )
        
        task = self.task_repo.create(
            user_id=current_user.id,
            title=payload.title,
            description=payload.description,
            parent_task_id=payload.parent_task_id,
        )

        is_subtask = task.parent_task_id is not None

        activity_type = (
            ActivityType.SUBTASK_CREATED
            if is_subtask
            else ActivityType.TASK_CREATED
        )

        action = "Subtask created" if is_subtask else "Task created"
        event_type = "subtask.created" if is_subtask else "task.created"

        background_tasks.add_task(
            ActivityService.log_task_activity,
            user_id=current_user.id,
            task_id=task.id,
            parent_task_id=task.parent_task_id,
            activity_type=activity_type,
            action=action,
            event_type=event_type,
            request_id=request_id,
            data={
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "parent_task_id": task.parent_task_id,
            },
            kafka_producer=kafka_producer,
            topic=kafka_topic,
            actor={
                "id": current_user.id,
                "email": current_user.email,
                "is_admin": current_user.is_admin,
            },
            meta=meta,
        )

        return task

    async def update_task(
        self,
        *,
        task_id: int,
        current_user: User,
        payload: TaskUpdate,
        background_tasks: BackgroundTasks,
        request_id: str,
        kafka_producer,
        kafka_topic: str,
        meta: dict,
    ):
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise ValueError("Task not found")

        # Optional but recommended: ownership check
        if task.user_id != current_user.id:
            raise ValueError("Not allowed to update this task")

        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            return task  # no-op update

        # Track changes (IMPORTANT for UI)
        changes = {}
        for field, new_value in update_data.items():
            old_value = getattr(task, field)
            if old_value != new_value:
                changes[field] = {
                    "old": old_value,
                    "new": new_value,
                }

        if not changes:
            return task  # nothing changed

        updated_task = self.task_repo.update(task, update_data)

        is_subtask = updated_task.parent_task_id is not None

        activity_type = (
            ActivityType.SUBTASK_UPDATED
            if is_subtask
            else ActivityType.TASK_UPDATED
        )

        action = "Subtask updated" if is_subtask else "Task updated"
        event_type = "subtask.updated" if is_subtask else "task.updated"

        background_tasks.add_task(
            ActivityService.log_task_activity,
            user_id=current_user.id,
            task_id=updated_task.id,
            parent_task_id=updated_task.parent_task_id,
            activity_type=activity_type,
            action=action,
            event_type=event_type,
            request_id=request_id,
            data={
                "id": updated_task.id,
                "changes": changes,
            },
            kafka_producer=kafka_producer,
            topic=kafka_topic,
            actor={
                "id": current_user.id,
                "email": current_user.email,
                "is_admin": current_user.is_admin,
            },
            meta=meta,
        )

        return updated_task


    async def delete_task(
        self,
        *,
        task_id: int,
        current_user: User,
        background_tasks: BackgroundTasks,
        request_id: str,
        kafka_producer,
        kafka_topic: str,
        meta: dict,
    ):
        task = self.task_repo.get_by_id(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this task",
            )
        
        self.task_repo.delete(task)

        is_subtask = task.parent_task_id is not None

        activity_type = (
            ActivityType.SUBTASK_DELETED
            if is_subtask
            else ActivityType.TASK_DELETED
        )

        action = "Subtask deleted" if is_subtask else "Task deleted"
        event_type = "subtask.deleted" if is_subtask else "task.deleted"

        background_tasks.add_task(
            ActivityService.log_task_activity,
            user_id=current_user.id,
            task_id=task.id,
            parent_task_id=task.parent_task_id,
            activity_type=activity_type,
            action=action,
            event_type=event_type,
            request_id=request_id,
            data={
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "parent_task_id": task.parent_task_id,
            },
            kafka_producer=kafka_producer,
            topic=kafka_topic,
            actor={
                "id": current_user.id,
                "email": current_user.email,
                "is_admin": current_user.is_admin,
            },
            meta=meta,
        )

        return
    