from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    ticker: Mapped[str] = mapped_column(String, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    signal: Mapped[str] = mapped_column(String, nullable=False, default="NEUTRAL")
    theme_key: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
