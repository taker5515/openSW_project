import time
import logging
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

from app.external.market_data_provider import MarketDataProvider

log = logging.getLogger(__name__)


def _fmt_volume(v: int | None) -> str | None:
    if v is None:
        return None
    if v >= 1_000_000_000:
        return f"{v / 1_000_000_000:.1f}B"
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return str(v)


class YFinanceProvider(MarketDataProvider):
    _MIN_INTERVAL = 0.5  # seconds between calls

    def __init__(self):
        self._last_call: float = 0.0

    def _throttle(self):
        elapsed = time.monotonic() - self._last_call
        if elapsed < self._MIN_INTERVAL:
            time.sleep(self._MIN_INTERVAL - elapsed)
        self._last_call = time.monotonic()

    def get_summary(self, ticker: str) -> dict | None:
        try:
            self._throttle()
            t = yf.Ticker(ticker)
            info = t.info or {}
            hist = t.history(period="1mo")

            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
            prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose") or price
            change = round(price - prev_close, 4)
            change_pct = round((change / prev_close * 100) if prev_close else 0.0, 2)

            history: list[float] = []
            if not hist.empty and "Close" in hist.columns:
                history = [round(float(v), 2) for v in hist["Close"].dropna().tolist()[-20:]]

            volume = info.get("regularMarketVolume") or info.get("volume")
            market_cap = info.get("marketCap")

            return {
                "ticker": ticker.upper(),
                "name": info.get("longName") or info.get("shortName") or ticker,
                "price": round(float(price), 2),
                "change": change,
                "changePct": change_pct,
                "currency": info.get("currency", "USD"),
                "market_state": info.get("marketState"),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "history": history,
                "metrics": {
                    "open": info.get("open") or info.get("regularMarketOpen"),
                    "high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
                    "low": info.get("dayLow") or info.get("regularMarketDayLow"),
                    "volume": volume,
                    "volume_fmt": _fmt_volume(volume),
                    "market_cap": _fmt_volume(market_cap),
                },
            }
        except Exception as e:
            log.warning("yfinance get_summary(%s) failed: %s", ticker, e)
            return None

    def get_chart(self, ticker: str, period: str = "3mo", interval: str = "1d") -> pd.DataFrame | None:
        try:
            self._throttle()
            df = yf.Ticker(ticker).history(period=period, interval=interval)
            if df.empty:
                return None
            df = df.reset_index()
            return df
        except Exception as e:
            log.warning("yfinance get_chart(%s) failed: %s", ticker, e)
            return None

    def get_realtime_price(self, ticker: str) -> dict | None:
        try:
            self._throttle()
            t = yf.Ticker(ticker)
            info = t.info or {}
            price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
            prev_close = info.get("previousClose") or price
            change = round(float(price) - float(prev_close), 4)
            change_pct = round((change / float(prev_close) * 100) if prev_close else 0.0, 2)
            return {
                "ticker": ticker.upper(),
                "name": info.get("longName") or ticker,
                "price": round(float(price), 2),
                "change": change,
                "change_pct": change_pct,
                "volume": info.get("regularMarketVolume"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            log.warning("yfinance get_realtime_price(%s) failed: %s", ticker, e)
            return None

    def search(self, query: str) -> list[dict]:
        try:
            self._throttle()
            results = yf.Search(query, max_results=10)
            quotes = results.quotes if hasattr(results, "quotes") else []
            return [
                {
                    "ticker": q.get("symbol", ""),
                    "name": q.get("longname") or q.get("shortname") or q.get("symbol", ""),
                    "exchange": q.get("exchange"),
                    "type": q.get("quoteType"),
                }
                for q in quotes
                if q.get("symbol")
            ]
        except Exception as e:
            log.warning("yfinance search(%s) failed: %s", query, e)
            return []

    def get_fundamentals(self, ticker: str) -> dict | None:
        try:
            self._throttle()
            t = yf.Ticker(ticker)
            info = t.info or {}
            return info if info else None
        except Exception as e:
            log.warning("yfinance get_fundamentals(%s) failed: %s", ticker, e)
            return None
