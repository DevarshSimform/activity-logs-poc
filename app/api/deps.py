from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.websockets import WebSocketDisconnect
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.core.security import JWTService
from app.kafka.registry import get_kafka_producer_instance



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract current authenticated user from JWT.
    """
    jwt_service = JWTService()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
    
        payload = jwt_service.decode_token(token)
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id),
        User.is_deleted.is_(False)
    ).first()

    if not user:
        raise credentials_exception

    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def get_kafka_producer():
    """
    FastAPI dependency.
    Returns the singleton Kafka producer.
    """
    return get_kafka_producer_instance()



async def get_current_admin_from_ws(
    websocket: WebSocket,
    db: Session,
) -> User:
    """
    Authenticate admin user from WebSocket connection.
    """

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        raise WebSocketDisconnect()

    jwt_service = JWTService()

    try:
        payload = jwt_service.decode_token(token)
        user_id: str | None = payload.get("sub")

        if not user_id:
            raise JWTError()

    except JWTError:
        await websocket.close(code=1008)
        raise WebSocketDisconnect()

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id),
            User.is_deleted.is_(False),
            User.is_admin.is_(True),
        )
        .first()
    )

    if not user:
        await websocket.close(code=1008)
        raise WebSocketDisconnect()

    return user

