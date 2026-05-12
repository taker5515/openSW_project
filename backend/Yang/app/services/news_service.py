from sqlalchemy.orm import Session
from app.external.news_provider import MockNewsProvider
from app.repositories import news_repository
from app.schemas.news import NewsItemSchema, NewsListResponse

_provider = MockNewsProvider()


def get_latest(db: Session, limit: int = 20) -> NewsListResponse:
    if news_repository.is_stale(db):
        items = _provider.get_latest(limit=50)
        news_repository.save_bulk(db, items)
    rows = news_repository.get_latest(db, limit)
    return NewsListResponse(
        items=[NewsItemSchema.model_validate(r) for r in rows],
        total=len(rows),
    )


def get_by_theme(db: Session, theme_key: str, limit: int = 10) -> NewsListResponse:
    if news_repository.is_stale(db):
        items = _provider.get_latest(limit=50)
        news_repository.save_bulk(db, items)
    rows = news_repository.get_by_theme(db, theme_key, limit)
    if not rows:
        fresh = _provider.get_by_theme(theme_key, limit)
        news_repository.save_bulk(db, fresh)
        rows = news_repository.get_by_theme(db, theme_key, limit)
    return NewsListResponse(
        items=[NewsItemSchema.model_validate(r) for r in rows],
        total=len(rows),
    )


def get_by_ticker(db: Session, ticker: str, limit: int = 10) -> NewsListResponse:
    rows = news_repository.get_by_ticker(db, ticker, limit)
    if not rows:
        fresh = _provider.get_by_ticker(ticker, limit)
        news_repository.save_bulk(db, fresh)
        rows = news_repository.get_by_ticker(db, ticker, limit)
    return NewsListResponse(
        items=[NewsItemSchema.model_validate(r) for r in rows],
        total=len(rows),
    )
