from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

class JWTService:
    """
    Handles JWT creation and validation.
    """

    def __init__(
        self,
        secret_key: str = settings.jwt_secret_key,
        algorithm: str = settings.jwt_algorithm,
        access_token_expire_minutes: int = settings.access_token_expire_minutes,
    ):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes


    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.pwd_context.verify(password, hashed)

    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
        extra_claims: dict | None = None,
    ) -> str:
        """
        Create JWT access token.
        """
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self.access_token_expire_minutes)
        )

        payload = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }

        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        """
        Decode and validate JWT token.
        """
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except JWTError:
            raise
