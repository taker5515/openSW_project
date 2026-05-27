from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.auth import LoginRequest, TokenResponse, RegisterRequest, RegisterResponse
from services.auth_service import AuthService
from services.register_service import RegisterService
from services.google_auth_service import GoogleAuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    service = RegisterService(db)
    return service.register(data)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)


@router.get("/google")
def google_login(db: Session = Depends(get_db)):
    service = GoogleAuthService(db)
    url = service.get_login_url()
    return RedirectResponse(url)


@router.get("/google/callback", response_model=TokenResponse)
async def google_callback(code: str, db: Session = Depends(get_db)):
    service = GoogleAuthService(db)
    return await service.handle_callback(code)
