from sqlalchemy.orm import Session
from app.database.models import User


class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return (
            db.query(User)
            .filter(User.email == email, User.is_deleted.is_(False))
            .first()
        )
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()

    @staticmethod
    def create(
        db: Session,
        *,
        email: str,
        firstname: str,
        lastname: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            hashed_password=hashed_password,
            is_admin=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user