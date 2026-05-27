from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import get_password_hash
from repositories.user_repository import UserRepository
from schemas.auth import RegisterRequest, RegisterResponse


class RegisterService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> RegisterResponse:
        existing = self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use.",
            )
        hashed_pw = get_password_hash(data.password)
        user = self.user_repo.create(email=data.email, hashed_password=hashed_pw)
        return RegisterResponse(id=user.id, email=user.email)
