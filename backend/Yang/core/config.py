from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Investment Analysis API"
    VERSION: str = "1.0.0"
    CORS_ORIGINS: List[str] = ["*"]
    DATABASE_URL: str = "sqlite:///./investdb.sqlite3"

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
