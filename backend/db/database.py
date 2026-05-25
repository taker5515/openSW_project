from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

Base = declarative_base()
