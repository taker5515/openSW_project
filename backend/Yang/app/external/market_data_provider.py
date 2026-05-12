from abc import ABC, abstractmethod
import pandas as pd


class MarketDataProvider(ABC):
    @abstractmethod
    def get_summary(self, ticker: str) -> dict | None:
        """Returns WatchItem-compatible dict or None on failure."""

    @abstractmethod
    def get_chart(self, ticker: str, period: str, interval: str) -> pd.DataFrame | None:
        """Returns DataFrame with columns: Date/Datetime, Open, High, Low, Close, Volume."""

    @abstractmethod
    def get_realtime_price(self, ticker: str) -> dict | None:
        """Returns minimal price dict: {ticker, price, change, change_pct, volume, timestamp}."""

    @abstractmethod
    def search(self, query: str) -> list[dict]:
        """Returns list of {ticker, name, exchange, type}."""

    @abstractmethod
    def get_fundamentals(self, ticker: str) -> dict | None:
        """Returns raw fundamental data dict from provider."""
