from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from db.base import Base


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    title = Column(String, nullable=False)
    source = Column(String)
    summary = Column(Text)
    signal = Column(String, default="NEUTRAL")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
