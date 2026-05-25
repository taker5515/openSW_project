from pydantic import BaseModel
from typing import List


class WatchItemResponse(BaseModel):
    ticker: str
    name: str
    price: float
    change: float
    changePct: float
    history: List[float]


class AddWatchlistRequest(BaseModel):
    ticker: str


class DeleteWatchlistResponse(BaseModel):
    ticker: str
    deleted: bool
