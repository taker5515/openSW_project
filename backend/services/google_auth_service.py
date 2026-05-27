import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token, create_refresh_token
from external.google_oauth_client import build_login_url, exchange_code_for_email
from repositories.user_repository import UserRepository
from schemas.auth import TokenResponse


class GoogleAuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_login_url(self) -> str:
        return build_login_url(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_REDIRECT_URI)

    async def handle_callback(self, code: str) -> TokenResponse:
        email = await exchange_code_for_email(
            code=code,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
        if not email:
            raise HTTPException(status_code=400, detail="Failed to get email from Google.")

        user = self.user_repo.get_by_email(email)
        if not user:
            dummy_pw = bcrypt.hashpw(b"google_oauth", bcrypt.gensalt()).decode()
            user = self.user_repo.create(email=email, hashed_password=dummy_pw)

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
