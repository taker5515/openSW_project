from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.stock import Stock


def get_by_symbol(db: Session, symbol: str, limit: int = 90) -> list[Stock]:
    return (
        db.query(Stock)
        .filter(Stock.symbol == symbol)
        .order_by(Stock.date.asc())
        .limit(limit)
        .all()
    )


def get_latest(db: Session, symbol: str) -> Stock | None:
    return (
        db.query(Stock)
        .filter(Stock.symbol == symbol)
        .order_by(Stock.date.desc())
        .first()
    )


def is_stale(db: Session, symbol: str, max_age_hours: int = 1) -> bool:
    latest = get_latest(db, symbol)
    if latest is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    fetched = latest.fetched_at
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=timezone.utc)
    return fetched < cutoff


def save_bulk(db: Session, symbol: str, rows: list[dict]) -> None:
    for row in rows:
        try:
            existing = (
                db.query(Stock)
                .filter(Stock.symbol == symbol, Stock.date == row["date"])
                .first()
            )
            if existing:
                existing.close = row.get("close", existing.close)
                existing.open = row.get("open", existing.open)
                existing.high = row.get("high", existing.high)
                existing.low = row.get("low", existing.low)
                existing.volume = row.get("volume", existing.volume)
            else:
                db.add(Stock(
                    symbol=symbol,
                    date=row["date"],
                    open=row.get("open"),
                    high=row.get("high"),
                    low=row.get("low"),
                    close=row["close"],
                    volume=row.get("volume"),
                ))
        except IntegrityError:
            db.rollback()
    db.commit()
