from fastapi import APIRouter, HTTPException
from typing import List

from schemas.watchlists import WatchItemResponse, AddWatchlistRequest, DeleteWatchlistResponse
from services import watchlist_service

router = APIRouter()


@router.get("", response_model=List[WatchItemResponse])
def get_watchlist():
    return watchlist_service.get_watchlist()


@router.post("", response_model=WatchItemResponse)
def add_to_watchlist(body: AddWatchlistRequest):
    ticker = body.ticker.upper()
    result = watchlist_service.add_to_watchlist(ticker)
    if result is None:
        raise HTTPException(status_code=400, detail=f"Failed to add {ticker}")
    return result


@router.delete("/{ticker}", response_model=DeleteWatchlistResponse)
def remove_from_watchlist(ticker: str):
    ticker = ticker.upper()
    deleted = watchlist_service.remove_from_watchlist(ticker)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")
    return {"ticker": ticker, "deleted": True}
