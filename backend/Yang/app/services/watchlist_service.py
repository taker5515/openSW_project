from sqlalchemy.orm import Session
from app.repositories import watchlist_repository
from app.schemas.watchlist import WatchlistItemOut, WatchlistResponse


def get(db: Session, user_id: int) -> WatchlistResponse:
    items = watchlist_repository.get_by_user(db, user_id)
    return WatchlistResponse(
        items=[WatchlistItemOut.model_validate(i) for i in items],
        total=len(items),
    )


def add(db: Session, user_id: int, ticker: str) -> WatchlistItemOut | None:
    item = watchlist_repository.add(db, user_id, ticker)
    return WatchlistItemOut.model_validate(item) if item else None


def remove(db: Session, user_id: int, ticker: str) -> bool:
    return watchlist_repository.remove(db, user_id, ticker)


def get_tickers(db: Session, user_id: int) -> list[str]:
    items = watchlist_repository.get_by_user(db, user_id)
    return [i.ticker for i in items]
