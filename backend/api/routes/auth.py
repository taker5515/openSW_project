from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.auth_deps import get_current_user
from core.security import create_access_token, create_refresh_token
from services.auth_service import AuthService
from services.register_service import RegisterService
from repositories.user_repository import UserRepository
from schemas.auth import (
    LoginRequest, TokenResponse, RegisterRequest, RegisterResponse,
    GoogleAuthRequest, UserMeResponse,
)
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    service = RegisterService(db)
    return service.register(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)


@router.post("/google", response_model=TokenResponse)
def google_auth(data: GoogleAuthRequest, db: Session = Depends(get_db)):
    user = UserRepository(db).find_or_create_google_user(email=data.email, name=data.name)
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.get("/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
