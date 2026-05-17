from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from app.auth_service import AuthService
from app.register_service import RegisterService
from schemas.auth import LoginRequest, TokenResponse, RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    service = RegisterService(db)
    return service.register(data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)
