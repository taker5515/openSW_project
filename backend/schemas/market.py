from pydantic import BaseModel
from typing import List, Optional


class MarketNewsItem(BaseModel):
    ticker: str
    summary: str
    sentiment_score: str
    related_tickers: List[str]
    market_outlook: str
    news_url: Optional[str] = None


class MarketOverviewResponse(BaseModel):
    market_overview: List[MarketNewsItem]
