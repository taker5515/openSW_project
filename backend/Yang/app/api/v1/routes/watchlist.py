from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_market_provider, get_optional_user
from app.external.yfinance_provider import YFinanceProvider
from app.models.user import User
from app.repositories.watchlist_repository import DEMO_USER_ID
from app.schemas.watchlist import WatchlistAddRequest, WatchlistItemOut, WatchlistResponse
from app.services import realtime_service, watchlist_service

router = APIRouter()


def _resolve_user_id(current_user: User | None) -> int:
    return current_user.id if current_user else DEMO_USER_ID


# /stream before /{ticker} to avoid path conflict
@router.get("/stream")
async def stream_watchlist(
    interval: int = 3,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    user_id = _resolve_user_id(current_user)
    tickers = watchlist_service.get_tickers(db, user_id)
    if not tickers:
        tickers = ["AAPL", "NVDA", "TSLA"]  # demo fallback

    async def event_generator():
        try:
            async for event in realtime_service.stream_prices(tickers, interval, provider):
                yield event
        except Exception:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("", response_model=WatchlistResponse)
def get_watchlist(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    return watchlist_service.get(db, _resolve_user_id(current_user))


@router.post("", response_model=WatchlistItemOut, status_code=201)
def add_to_watchlist(
    body: WatchlistAddRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    item = watchlist_service.add(db, _resolve_user_id(current_user), body.ticker)
    if not item:
        raise HTTPException(status_code=400, detail="이미 관심종목에 추가된 종목입니다.")
    return item


@router.delete("/{ticker}", status_code=204)
def remove_from_watchlist(
    ticker: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    if not watchlist_service.remove(db, _resolve_user_id(current_user), ticker):
        raise HTTPException(status_code=404, detail="관심종목에 없는 종목입니다.")
