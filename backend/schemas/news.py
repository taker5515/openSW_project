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
    theme: Optional[str] = None
    title: str
    source: str
    time: str
    publishedAt: Optional[str] = None
    url: Optional[str] = None
    summary: str
    signal: Signal
    sentiment: Optional[str] = None   # "good" | "bad"
    level: Optional[int] = None       # 1(강) ~ 4(약)


class NewsListResponse(BaseModel):
    items: List[NewsItemResponse]
    total: int
