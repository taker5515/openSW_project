from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(String, index=True, nullable=False)
    feedback_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
