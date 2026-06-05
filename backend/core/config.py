from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "openSW Backend"
    APP_ENV: str = "development"
    VERSION: str = "1.0.0"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    DATABASE_URL: str = "sqlite:///./app.db"

    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    NEWS_API_KEY: str = ""

    SECRET_KEY: str = "changeme-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
