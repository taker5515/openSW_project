import json
import logging
import random

from sqlalchemy.orm import Session

from app.analytics import financials as fin_mod
from app.analytics import scoring, technical
from app.core.config import settings
from app.external.market_data_provider import MarketDataProvider
from app.repositories import analysis_repository
from app.schemas.analysis import TossStyleResponse

log = logging.getLogger(__name__)


def _mock_toss_style(ticker: str) -> TossStyleResponse:
    return scoring.build_toss_response(
        ticker=ticker,
        name=f"{ticker} Corp. (mock data)",
        price=round(random.uniform(50, 500), 2),
        info={"beta": round(random.uniform(0.5, 2.0), 2)},
        tech={
            "rsi14": round(random.uniform(30, 70), 1),
            "sma20_diff_pct": round(random.uniform(-10, 10), 1),
            "price_vs_52w_high_pct": round(random.uniform(-30, 0), 1),
            "volatility_annual": round(random.uniform(15, 45), 1),
        },
        fundamentals={
            "per": round(random.uniform(10, 50), 1),
            "pbr": round(random.uniform(1, 15), 2),
            "psr": round(random.uniform(2, 20), 1),
            "roe": round(random.uniform(5, 40), 1),
            "operating_margin": round(random.uniform(5, 30), 1),
            "profit_margin": round(random.uniform(3, 25), 1),
            "dividend_yield": round(random.uniform(0, 0.03), 4),
        },
    )


def get_toss_style(db: Session, ticker: str, provider: MarketDataProvider) -> TossStyleResponse:
    cached = analysis_repository.get_cached(db, ticker, "toss_style")
    if cached:
        return TossStyleResponse(**json.loads(cached.payload))

    if settings.USE_MOCK_DATA:
        result = _mock_toss_style(ticker)
        analysis_repository.save(db, ticker, "toss_style", result.model_dump(), ttl_hours=1)
        return result

    info = provider.get_fundamentals(ticker)
    if info is None:
        result = _mock_toss_style(ticker)
        analysis_repository.save(db, ticker, "toss_style", result.model_dump(), ttl_hours=1)
        return result

    hist_df = provider.get_chart(ticker, period="1y", interval="1d")
    fundamentals = fin_mod.extract(info)
    tech_data = technical.analyze(hist_df, info)

    price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
    name = info.get("longName") or info.get("shortName") or ticker

    result = scoring.build_toss_response(
        ticker=ticker,
        name=name,
        price=round(float(price), 2),
        info=info,
        tech=tech_data,
        fundamentals=fundamentals,
    )
    analysis_repository.save(db, ticker, "toss_style", result.model_dump(), ttl_hours=4)
    return result


def get_fundamentals(db: Session, ticker: str, provider: MarketDataProvider) -> dict:
    if settings.USE_MOCK_DATA:
        return {"ticker": ticker, "note": "mock data", "data": {}}
    info = provider.get_fundamentals(ticker)
    if info is None:
        return {"ticker": ticker, "note": "provider unavailable", "data": {}}
    return {"ticker": ticker, "data": fin_mod.extract(info)}


def get_technicals(db: Session, ticker: str, provider: MarketDataProvider) -> dict:
    if settings.USE_MOCK_DATA:
        return {"ticker": ticker, "note": "mock data", "data": {}}
    hist_df = provider.get_chart(ticker, period="1y", interval="1d")
    info = provider.get_fundamentals(ticker)
    data = technical.analyze(hist_df, info)
    return {"ticker": ticker, "data": data}
