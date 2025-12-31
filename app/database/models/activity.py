from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.database.models.base import BaseModelMixin


class ActivityType(str, PyEnum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"

    SUBTASK_CREATED = "subtask_created"
    SUBTASK_UPDATED = "subtask_updated"
    SUBTASK_DELETED = "subtask_deleted"

    PROFILE_UPDATED = "profile_updated"



class ActivityLog(Base, BaseModelMixin):
    __tablename__ = "activity_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    activity_type = Column(SqlEnum(ActivityType), nullable=False)

    action = Column(String(255), nullable=False)
    request_id = Column(String(100), nullable=False)
    data = Column(Text, nullable=True)

    user = relationship("User")
    task = relationship("Task")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, activity_type={self.activity_type}, user_id={self.user_id})>"