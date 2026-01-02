from pydantic import BaseModel
from typing import Optional



class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    parent_task_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    parent_task_id: Optional[int]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
