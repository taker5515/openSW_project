from typing import Literal
from pydantic import BaseModel, ConfigDict


class NewsItemSchema(BaseModel):
    id: str
    ticker: str
    title: str
    source: str
    time: str
    summary: str
    signal: Literal["BUY", "SELL", "NEUTRAL"] = "NEUTRAL"
    loading: bool = False

    model_config = ConfigDict(from_attributes=True)


class NewsListResponse(BaseModel):
    items: list[NewsItemSchema]
    total: int
