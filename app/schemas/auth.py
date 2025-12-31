from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    firstname: str
    lastname: str


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

