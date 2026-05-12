from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WatchlistAddRequest(BaseModel):
    ticker: str


class WatchlistItemOut(BaseModel):
    id: int
    ticker: str
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WatchlistResponse(BaseModel):
    items: list[WatchlistItemOut]
    total: int
