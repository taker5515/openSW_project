import random
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import settings
from app.external.market_data_provider import MarketDataProvider
from app.repositories import stock_repository
from app.schemas.stock import ChartPoint, ChartResponse, StockMetrics, StockSummary


def _mock_summary(ticker: str) -> StockSummary:
    base = hash(ticker) % 1000 + 50
    price = round(base + random.uniform(-5, 5), 2)
    change = round(random.uniform(-10, 10), 2)
    return StockSummary(
        ticker=ticker,
        name=f"{ticker} Corp. (mock)",
        price=price,
        change=change,
        changePct=round(change / price * 100, 2),
        history=[round(base + random.uniform(-20, 20), 2) for _ in range(20)],
        metrics=StockMetrics(
            open=round(price - 2, 2),
            high=round(price + 5, 2),
            low=round(price - 5, 2),
            volume=random.randint(1_000_000, 50_000_000),
            volume_fmt=f"{random.randint(1, 50)}M",
        ),
    )


def _mock_chart(ticker: str, period: str, interval: str) -> ChartResponse:
    n = 30 if "mo" in period else 24
    base = hash(ticker) % 1000 + 50
    points = []
    for i in range(n):
        price = round(base + random.uniform(-20, 20), 2)
        t = f"{9 + i // 6:02d}:{(i % 6) * 10:02d}" if interval == "1m" else f"2026-{(i % 12) + 1:02d}-01"
        points.append(ChartPoint(time=t, price=price, volume=random.randint(100_000, 5_000_000)))
    return ChartResponse(ticker=ticker, period=period, interval=interval, points=points)


def get_summary(db: Session, ticker: str, provider: MarketDataProvider) -> StockSummary:
    if settings.USE_MOCK_DATA:
        return _mock_summary(ticker)

    raw = provider.get_summary(ticker)
    if raw is None:
        return _mock_summary(ticker)

    db_rows = stock_repository.get_by_symbol(db, ticker, limit=20)
    history = [round(float(r.close), 2) for r in db_rows[-20:]]
    if not history and raw.get("history"):
        history = raw["history"]

    metrics_raw = raw.get("metrics") or {}
    return StockSummary(
        ticker=raw["ticker"],
        name=raw["name"],
        price=raw["price"],
        change=raw["change"],
        changePct=raw["changePct"],
        currency=raw.get("currency", "USD"),
        market_state=raw.get("market_state"),
        updated_at=raw.get("updated_at"),
        history=history or raw.get("history", []),
        metrics=StockMetrics(**metrics_raw) if metrics_raw else None,
    )


def get_chart(db: Session, ticker: str, period: str, interval: str, provider: MarketDataProvider) -> ChartResponse:
    if settings.USE_MOCK_DATA:
        return _mock_chart(ticker, period, interval)

    # For multi-day intervals, use/update DB cache
    if interval in ("1d", "1wk", "1mo") and not stock_repository.is_stale(db, ticker, max_age_hours=1):
        rows = stock_repository.get_by_symbol(db, ticker, limit=365)
        if rows:
            points = [ChartPoint(time=r.date, price=r.close, volume=r.volume) for r in rows]
            return ChartResponse(ticker=ticker, period=period, interval=interval, points=points)

    df = provider.get_chart(ticker, period, interval)
    if df is None:
        return _mock_chart(ticker, period, interval)

    # Persist to DB if daily data
    if interval in ("1d", "1wk"):
        _persist_chart(db, ticker, df)

    points = _df_to_chart_points(df, interval)
    return ChartResponse(ticker=ticker, period=period, interval=interval, points=points)


def _persist_chart(db: Session, ticker: str, df: pd.DataFrame) -> None:
    date_col = "Datetime" if "Datetime" in df.columns else "Date"
    if date_col not in df.columns:
        return
    rows = []
    for _, row in df.iterrows():
        try:
            date_val = str(row[date_col])[:10]
            close = float(row.get("Close", 0))
            if close == 0:
                continue
            rows.append({
                "date": date_val,
                "open": float(row["Open"]) if "Open" in row else None,
                "high": float(row["High"]) if "High" in row else None,
                "low": float(row["Low"]) if "Low" in row else None,
                "close": close,
                "volume": int(row["Volume"]) if "Volume" in row else None,
            })
        except Exception:
            continue
    if rows:
        stock_repository.save_bulk(db, ticker, rows)


def _df_to_chart_points(df: pd.DataFrame, interval: str) -> list[ChartPoint]:
    date_col = "Datetime" if "Datetime" in df.columns else "Date"
    points = []
    for _, row in df.iterrows():
        try:
            dt = row.get(date_col)
            if interval in ("1m", "5m", "15m", "30m", "1h"):
                time_str = str(dt)[11:16] if dt else ""
            else:
                time_str = str(dt)[:10] if dt else ""
            close = float(row.get("Close", 0))
            volume = int(row.get("Volume", 0)) if row.get("Volume") else None
            if close > 0:
                points.append(ChartPoint(time=time_str, price=round(close, 2), volume=volume))
        except Exception:
            continue
    return points


def search(ticker_query: str, provider: MarketDataProvider) -> list[dict]:
    if settings.USE_MOCK_DATA:
        return [{"ticker": "AAPL", "name": "Apple Inc. (mock)", "exchange": "NASDAQ", "type": "EQUITY"}]
    return provider.search(ticker_query)
