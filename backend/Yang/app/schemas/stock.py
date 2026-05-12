from pydantic import BaseModel


class ChartPoint(BaseModel):
    time: str
    price: float
    volume: int | None = None


class ChartResponse(BaseModel):
    ticker: str
    period: str
    interval: str
    points: list[ChartPoint]


class StockMetrics(BaseModel):
    open: float | None = None
    high: float | None = None
    low: float | None = None
    volume: int | None = None
    volume_fmt: str | None = None
    market_cap: str | None = None


class StockSummary(BaseModel):
    ticker: str
    name: str
    price: float
    change: float
    changePct: float
    currency: str = "USD"
    market_state: str | None = None
    updated_at: str | None = None
    history: list[float] = []
    metrics: StockMetrics | None = None


class StockSearchItem(BaseModel):
    ticker: str
    name: str
    exchange: str | None = None
    type: str | None = None
