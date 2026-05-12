from datetime import datetime, timezone
from app.schemas.sse import SSEHeartbeat, SSEStockPrice


def stock_price_event(
    ticker: str,
    name: str,
    price: float,
    change: float,
    change_pct: float,
    volume: int | None = None,
) -> str:
    data = SSEStockPrice(
        ticker=ticker,
        name=name,
        price=price,
        change=change,
        change_pct=change_pct,
        volume=volume,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return f"event: stock.price\ndata: {data.model_dump_json()}\n\n"


def heartbeat_event(tickers: list[str]) -> str:
    data = SSEHeartbeat(
        tickers=tickers,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return f"event: stock.heartbeat\ndata: {data.model_dump_json()}\n\n"
