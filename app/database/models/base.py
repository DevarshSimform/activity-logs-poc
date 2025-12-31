from sqlalchemy import Column, Integer, Boolean, DateTime, func
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class BaseModelMixin:
    """Common production-grade fields for all tables."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # override manually if needed

    id = Column(Integer, primary_key=True, index=True)

    is_deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
