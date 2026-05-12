import asyncio
import logging
import random
from datetime import datetime, timezone

from app.core.config import settings
from app.external.market_data_provider import MarketDataProvider
from app.schemas.sse import SSEHeartbeat, SSEStockPrice

log = logging.getLogger(__name__)


def _mock_price(ticker: str) -> dict:
    base = hash(ticker) % 1000 + 50
    price = round(base + random.uniform(-5, 5), 2)
    change = round(random.uniform(-10, 10), 2)
    return {
        "ticker": ticker,
        "name": f"{ticker}",
        "price": price,
        "change": change,
        "change_pct": round(change / price * 100, 2),
        "volume": random.randint(100_000, 5_000_000),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


async def stream_prices(
    tickers: list[str],
    interval: int,
    provider: MarketDataProvider,
):
    """Async generator yielding SSE-formatted strings."""
    while True:
        for ticker in tickers:
            try:
                data = None if settings.USE_MOCK_DATA else await asyncio.to_thread(provider.get_realtime_price, ticker)
                if data is None:
                    data = _mock_price(ticker)
                event = SSEStockPrice(
                    ticker=data["ticker"],
                    name=data.get("name", ticker),
                    price=data["price"],
                    change=data["change"],
                    change_pct=data["change_pct"],
                    volume=data.get("volume"),
                    timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
                )
                yield f"event: stock.price\ndata: {event.model_dump_json()}\n\n"
            except asyncio.CancelledError:
                return
            except Exception as e:
                log.warning("SSE price fetch error for %s: %s", ticker, e)
                mock = _mock_price(ticker)
                event = SSEStockPrice(**mock)
                yield f"event: stock.price\ndata: {event.model_dump_json()}\n\n"

        heartbeat = SSEHeartbeat(
            tickers=tickers,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        yield f"event: stock.heartbeat\ndata: {heartbeat.model_dump_json()}\n\n"
        await asyncio.sleep(interval)
