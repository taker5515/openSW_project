from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from app.auth_service import AuthService
from schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)
