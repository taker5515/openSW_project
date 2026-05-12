from pydantic import BaseModel


class SSEStockPrice(BaseModel):
    type: str = "stock.price"
    ticker: str
    name: str = ""
    price: float
    change: float
    change_pct: float
    volume: int | None = None
    timestamp: str


class SSEHeartbeat(BaseModel):
    type: str = "stock.heartbeat"
    ok: bool = True
    tickers: list[str]
    timestamp: str
