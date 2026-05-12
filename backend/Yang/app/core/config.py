from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Stock Newsletter API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./stockdb.sqlite3"

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_USE_OPENSSL_RAND_HEX_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    ANTHROPIC_API_KEY: str = ""
    USE_MOCK_DATA: bool = False

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
