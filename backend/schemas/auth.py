from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    id: int
    email: str


class GoogleAuthRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserMeResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    themes: Optional[str] = None
