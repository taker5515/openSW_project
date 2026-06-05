from typing import List, Dict, Any, Optional

from repositories.watchlist_repository import watchlist_repository
from services.stock_service import get_quote


def get_watchlist() -> List[Dict[str, Any]]:
    tickers = watchlist_repository.get_all()
    return [get_quote(t) for t in tickers]


def add_to_watchlist(ticker: str) -> Optional[Dict[str, Any]]:
    ticker = ticker.upper()
    watchlist_repository.add(ticker)
    return get_quote(ticker)


def remove_from_watchlist(ticker: str) -> bool:
    return watchlist_repository.remove(ticker.upper())


def exists_in_watchlist(ticker: str) -> bool:
    return watchlist_repository.exists(ticker.upper())
