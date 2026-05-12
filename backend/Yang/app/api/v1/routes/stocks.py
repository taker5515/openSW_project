from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_market_provider
from app.external.yfinance_provider import YFinanceProvider
from app.schemas.stock import ChartResponse, StockSearchItem, StockSummary
from app.services import realtime_service, stock_service

router = APIRouter()


# /stream must be registered BEFORE /{ticker}/... to avoid path conflict
@router.get("/stream")
async def stream_stocks(
    tickers: str = Query(..., description="쉼표로 구분된 티커 (예: AAPL,NVDA,TSLA)"),
    interval: int = Query(default=3, ge=1, le=60, description="업데이트 간격 (초)"),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]

    async def event_generator():
        try:
            async for event in realtime_service.stream_prices(ticker_list, interval, provider):
                yield event
        except Exception:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/search", response_model=list[StockSearchItem])
def search_stocks(
    q: str = Query(..., min_length=1),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    results = stock_service.search(q, provider)
    return [StockSearchItem(**r) for r in results]


@router.get("/{ticker}/summary", response_model=StockSummary)
def get_summary(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    return stock_service.get_summary(db, ticker.upper(), provider)


@router.get("/{ticker}/chart", response_model=ChartResponse)
def get_chart(
    ticker: str,
    period: str = Query(default="3mo"),
    interval: str = Query(default="1d"),
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    return stock_service.get_chart(db, ticker.upper(), period, interval, provider)
