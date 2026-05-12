from sqlalchemy.orm import Session
from app.core import security
from app.repositories import user_repository
from app.schemas.auth import TokenResponse


def register(db: Session, email: str, password: str) -> TokenResponse:
    if user_repository.email_exists(db, email):
        raise ValueError("이미 등록된 이메일입니다.")
    hashed = security.hash_password(password)
    user = user_repository.create(db, email, hashed)
    token = security.create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


def login(db: Session, email: str, password: str) -> TokenResponse:
    user = user_repository.get_by_email(db, email)
    if not user or not security.verify_password(password, user.hashed_password):
        raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")
    token = security.create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
