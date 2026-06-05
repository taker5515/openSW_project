from fastapi import APIRouter, HTTPException, Query

from services import stock_service

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/{ticker}/quote")
def get_quote(ticker: str):
    ticker = ticker.upper()
    try:
        return stock_service.get_quote(ticker)
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve quote for {ticker}")


@router.get("/{ticker}/history")
def get_history(ticker: str):
    ticker = ticker.upper()
    try:
        return stock_service.get_history(ticker)
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history for {ticker}")


@router.get("/{ticker}/chart")
def get_chart(
    ticker: str,
    range: str = Query("1d", description="e.g. 1d, 5d, 1mo"),
    interval: str = Query("5m", description="e.g. 1m, 5m, 15m, 1h, 1d"),
):
    ticker = ticker.upper()
    try:
        return stock_service.get_chart(ticker, range_=range, interval=interval)
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chart for {ticker}")
