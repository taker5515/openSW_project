from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from core.security import verify_password, create_access_token, create_refresh_token
from schemas.auth import LoginRequest, TokenResponse

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="��Ȱ��ȭ�� �����Դϴ�.")
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
