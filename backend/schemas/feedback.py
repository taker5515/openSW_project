from pydantic import BaseModel, field_validator
from typing import Optional


class FeedbackRequest(BaseModel):
    type: str

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("up", "down"):
            raise ValueError("type must be 'up' or 'down'")
        return v


class FeedbackResponse(BaseModel):
    news_id: str
    up_count: int
    down_count: int
    user_feedback: Optional[str] = None
