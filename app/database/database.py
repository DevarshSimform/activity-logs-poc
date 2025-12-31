from typing import Generator
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from app.core.config import settings


DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    echo=settings.database_echo,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create metadata and base class
metadata = MetaData()
Base = declarative_base(metadata=metadata)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


