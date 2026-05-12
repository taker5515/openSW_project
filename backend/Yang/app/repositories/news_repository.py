from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.news import NewsItem


def get_latest(db: Session, limit: int = 20) -> list[NewsItem]:
    return db.query(NewsItem).order_by(NewsItem.fetched_at.desc()).limit(limit).all()


def get_by_theme(db: Session, theme_key: str, limit: int = 10) -> list[NewsItem]:
    return (
        db.query(NewsItem)
        .filter(NewsItem.theme_key == theme_key)
        .order_by(NewsItem.fetched_at.desc())
        .limit(limit)
        .all()
    )


def get_by_ticker(db: Session, ticker: str, limit: int = 10) -> list[NewsItem]:
    return (
        db.query(NewsItem)
        .filter(NewsItem.ticker == ticker.upper())
        .order_by(NewsItem.fetched_at.desc())
        .limit(limit)
        .all()
    )


def save_bulk(db: Session, items: list[dict]) -> None:
    for item in items:
        existing = db.query(NewsItem).filter(NewsItem.id == item["id"]).first()
        if existing:
            continue
        db.add(NewsItem(
            id=item["id"],
            ticker=item.get("ticker", ""),
            title=item.get("title", ""),
            source=item.get("source", ""),
            time=item.get("time", ""),
            summary=item.get("summary", ""),
            signal=item.get("signal", "NEUTRAL"),
            theme_key=item.get("theme_key"),
        ))
    db.commit()


def is_stale(db: Session, max_age_hours: int = 1) -> bool:
    latest = db.query(NewsItem).order_by(NewsItem.fetched_at.desc()).first()
    if latest is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    fetched = latest.fetched_at
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    return fetched < cutoff
