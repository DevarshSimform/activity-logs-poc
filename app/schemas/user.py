from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class UserProfileUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    bio: str | None
    profile_picture: str | None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True
