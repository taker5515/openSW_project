import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.config import settings
from core.security import create_access_token, create_refresh_token
from repositories.user_repository import UserRepository
from schemas.auth import TokenResponse

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

class GoogleAuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_login_url(self) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{GOOGLE_AUTH_URL}?{query}"

    async def handle_callback(self, code: str) -> TokenResponse:
        async with httpx.AsyncClient() as client:
            token_res = await client.post(GOOGLE_TOKEN_URL, data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            })
            token_data = token_res.json()
            access_token = token_data.get("access_token")

            userinfo_res = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo = userinfo_res.json()
            email = userinfo.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Failed to get email from Google.")

        user = self.user_repo.get_by_email(email)
        if not user:
            import bcrypt
            dummy_pw = bcrypt.hashpw(b"google_oauth", bcrypt.gensalt()).decode()
            user = self.user_repo.create(email=email, hashed_password=dummy_pw)

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
