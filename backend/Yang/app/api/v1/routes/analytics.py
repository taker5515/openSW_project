from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_market_provider
from app.external.yfinance_provider import YFinanceProvider
from app.schemas.analysis import TossStyleResponse
from app.services import analytics_service

router = APIRouter()


@router.get("/{ticker}/toss-style", response_model=TossStyleResponse)
def toss_style(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    return analytics_service.get_toss_style(db, ticker.upper(), provider)


@router.get("/{ticker}/fundamentals")
def fundamentals(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    return analytics_service.get_fundamentals(db, ticker.upper(), provider)


@router.get("/{ticker}/technicals")
def technicals(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    return analytics_service.get_technicals(db, ticker.upper(), provider)


@router.get("/{ticker}/overview")
def overview(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    summary = analytics_service.get_fundamentals(db, ticker.upper(), provider)
    tech = analytics_service.get_technicals(db, ticker.upper(), provider)
    return {"ticker": ticker.upper(), "fundamentals": summary.get("data", {}), "technicals": tech.get("data", {})}


@router.get("/{ticker}/score")
def score(
    ticker: str,
    db: Session = Depends(get_db),
    provider: YFinanceProvider = Depends(get_market_provider),
):
    result = analytics_service.get_toss_style(db, ticker.upper(), provider)
    return {"ticker": ticker.upper(), "score": result.score, "disclaimer": result.disclaimer}
