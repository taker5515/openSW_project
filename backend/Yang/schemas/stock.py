# 202501552/schemas/stock.py

from pydantic import BaseModel

class StockItem(BaseModel):
    date: str
    close: float

class StockResponse(BaseModel):
    symbol: str
    source: str
    data: list[StockItem]