from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from db.base import Base

class NewsCache(Base):
    __tablename__ = "news_cache"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    news_url = Column(String, unique=True)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())