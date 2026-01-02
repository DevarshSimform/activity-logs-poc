from sqlalchemy.orm import Session
from app.database.models import Task

class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        title: str,
        description: str | None,
        parent_task_id: int | None,
    ) -> Task:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            parent_task_id=parent_task_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    
    def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task: Task) -> None:
        task.is_deleted = True
        self.db.commit()
        self.db.refresh(task)
        return

