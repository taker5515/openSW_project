from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from schemas.news import NewsItemResponse, NewsListResponse
from services import news_service

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=NewsListResponse)
def get_news(
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
    theme: Optional[str] = Query(None, description="Filter by theme slug (e.g. tech&media)"),
):
    ticker_upper = ticker.upper() if ticker else None
    items = news_service.get_news(ticker=ticker_upper, theme=theme)
    return {"items": items, "total": len(items)}


@router.get("/{news_id}", response_model=NewsItemResponse)
def get_news_by_id(news_id: str):
    item = news_service.get_news_by_id(news_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"News {news_id} not found")
    return item
