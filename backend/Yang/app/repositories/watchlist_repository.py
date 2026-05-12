from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.watchlist import WatchlistItem

DEMO_USER_ID = 1


def get_by_user(db: Session, user_id: int) -> list[WatchlistItem]:
    return db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id).all()


def add(db: Session, user_id: int, ticker: str) -> WatchlistItem | None:
    item = WatchlistItem(user_id=user_id, ticker=ticker.upper())
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        return db.query(WatchlistItem).filter(
            WatchlistItem.user_id == user_id,
            WatchlistItem.ticker == ticker.upper(),
        ).first()


def remove(db: Session, user_id: int, ticker: str) -> bool:
    item = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == user_id,
        WatchlistItem.ticker == ticker.upper(),
    ).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def exists(db: Session, user_id: int, ticker: str) -> bool:
    return db.query(WatchlistItem).filter(
        WatchlistItem.user_id == user_id,
        WatchlistItem.ticker == ticker.upper(),
    ).count() > 0
