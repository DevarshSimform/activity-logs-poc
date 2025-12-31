from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.database.models.base import BaseModelMixin


class Task(Base, BaseModelMixin):
    __tablename__ = "tasks"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True
    )

    owner = relationship("User", back_populates="tasks")
    parent_task = relationship(
        "Task",
        remote_side="Task.id",
        back_populates="sub_tasks"
    )

    sub_tasks = relationship(
        "Task",
        back_populates="parent_task",
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, user_id={self.user_id})>"