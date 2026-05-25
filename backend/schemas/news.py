from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


class NewsItemResponse(BaseModel):
    id: str
    ticker: str
    title: str
    source: str
    time: str
    summary: str
    signal: Signal


class NewsListResponse(BaseModel):
    items: List[NewsItemResponse]
    total: int
