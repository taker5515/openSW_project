import json
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class SubscriptionCreate(BaseModel):
    email: EmailStr
    themes: list[str] = []
    tickers: list[str] = []
    frequency: Literal["daily", "weekly"] = "daily"
    send_time: str = "08:00"


class SubscriptionUpdate(BaseModel):
    themes: list[str] | None = None
    tickers: list[str] | None = None
    frequency: Literal["daily", "weekly"] | None = None
    send_time: str | None = None
    is_active: bool | None = None


class SubscriptionOut(BaseModel):
    id: int
    email: str
    themes: list[str]
    tickers: list[str]
    frequency: str
    send_time: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @field_validator("themes", "tickers", mode="before")
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class UnsubscribeRequest(BaseModel):
    email: EmailStr
