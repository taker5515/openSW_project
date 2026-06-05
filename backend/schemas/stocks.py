from pydantic import BaseModel
from typing import List, Optional


class ChartPoint(BaseModel):
    time: str
    price: float


class StockQuoteResponse(BaseModel):
    ticker: str
    name: str
    price: float
    change: float
    changePct: float
    history: List[float]


class StockHistoryResponse(BaseModel):
    ticker: str
    history: List[float]


class StockChartResponse(BaseModel):
    ticker: str
    range: str
    interval: str
    data: List[ChartPoint]
