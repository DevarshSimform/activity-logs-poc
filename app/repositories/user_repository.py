from sqlalchemy.orm import Session
from app.database.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email, User.is_deleted.is_(False))
            .first()
        )
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()

    def create(
        self,
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
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user