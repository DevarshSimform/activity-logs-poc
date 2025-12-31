from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.database.models.base import BaseModelMixin

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    bio = Column(String(500), nullable=True)
    profile_picture = Column(String(255), nullable=True)

    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, is_admin={self.is_admin})>"
