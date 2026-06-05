from typing import List, Set
from core.constants import INITIAL_WATCHLIST_TICKERS


class WatchlistRepository:
    def __init__(self) -> None:
        self._tickers: List[str] = list(INITIAL_WATCHLIST_TICKERS)

    def get_all(self) -> List[str]:
        return list(self._tickers)

    def add(self, ticker: str) -> bool:
        """Returns True if added, False if already exists."""
        ticker = ticker.upper()
        if ticker in self._tickers:
            return False
        self._tickers.append(ticker)
        return True

    def remove(self, ticker: str) -> bool:
        """Returns True if removed, False if not found."""
        ticker = ticker.upper()
        if ticker not in self._tickers:
            return False
        self._tickers.remove(ticker)
        return True

    def exists(self, ticker: str) -> bool:
        return ticker.upper() in self._tickers


watchlist_repository = WatchlistRepository()
