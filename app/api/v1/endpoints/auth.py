from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register_user(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    token = service.login_user(payload)
    return TokenResponse(**token)


@router.post(
    "/login/admin",
    response_model=TokenResponse,
)
def login_admin_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    token = service.login_admin_user(payload)
    return TokenResponse(**token)
