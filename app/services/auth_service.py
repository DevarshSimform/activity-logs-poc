from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.core.security import JWTService
from app.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.database.models import User


class AuthService:

    def __init__(self):
        self.jwt_service = JWTService()

    def register_user(
        self,
        db: Session,
        payload: UserRegisterRequest,
    ) -> User:
        existing_user = UserRepository.get_by_email(db, payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_password = self.jwt_service.hash_password(payload.password)

        user = UserRepository.create(
            db,
            email=payload.email,
            firstname=payload.firstname,
            lastname=payload.lastname,
            hashed_password=hashed_password,
        )

        return user

    def login_user(
        self,
        db: Session,
        payload: UserLoginRequest,
    ) -> str:
        user = UserRepository.get_by_email(db, payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not self.jwt_service.verify_password(
            payload.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = self.jwt_service.create_access_token(
            subject=str(user.id),
            extra_claims={
                "is_admin": user.is_admin,
            },
        )

        expires_in = self.jwt_service.access_token_expire_minutes

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": expires_in,
        }

    def login_admin_user(
        self,
        db: Session,
        payload: UserLoginRequest,
    ) -> str:
        user = UserRepository.get_by_email(db, payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        if not self.jwt_service.verify_password(
            payload.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = self.jwt_service.create_access_token(
            subject=str(user.id),
            extra_claims={
                "is_admin": user.is_admin,
            },
        )

        expires_in = self.jwt_service.access_token_expire_minutes

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": expires_in,
        }
