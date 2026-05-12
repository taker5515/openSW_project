from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.news import NewsListResponse
from app.services import news_service

router = APIRouter()


@router.get("/latest", response_model=NewsListResponse)
def latest_news(limit: int = 20, db: Session = Depends(get_db)):
    return news_service.get_latest(db, limit)


@router.get("", response_model=NewsListResponse)
def get_news(
    theme: str | None = Query(None),
    ticker: str | None = Query(None),
    limit: int = 10,
    db: Session = Depends(get_db),
):
    if ticker:
        return news_service.get_by_ticker(db, ticker.upper(), limit)
    if theme:
        return news_service.get_by_theme(db, theme, limit)
    return news_service.get_latest(db, limit)
