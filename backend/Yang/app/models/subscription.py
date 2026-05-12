from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    themes: Mapped[str] = mapped_column(String, nullable=False, default="[]")
    tickers: Mapped[str] = mapped_column(String, nullable=False, default="[]")
    frequency: Mapped[str] = mapped_column(String, nullable=False, default="daily")
    send_time: Mapped[str] = mapped_column(String, nullable=False, default="08:00")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
