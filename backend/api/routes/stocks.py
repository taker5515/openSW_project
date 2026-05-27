from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services import stock_service
from services.stock_info_service import get_stock_info
from services.stock_list_service import get_stock_list, is_valid_ticker, get_company_name, ALL_TICKERS
from services.crawling_service import get_news_from_rss, get_article_content
from services.news_analysis_service import analyze_news
from repositories.news_cache_repository import NewsCacheRepository

router = APIRouter()


@router.get("/list")
def get_stocks_list():
    return get_stock_list()


@router.get("/{ticker}/info")
def get_ticker_info(ticker: str):
    ticker = ticker.upper()
    if not is_valid_ticker(ticker):
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found.")
    return get_stock_info(ticker)


@router.get("/{ticker}/news")
async def get_ticker_news(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.upper()
    if not is_valid_ticker(ticker):
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found.")
    company_name = get_company_name(ticker)
    cache_repo = NewsCacheRepository(db)
    news_list = await get_news_from_rss(ticker)
    if not news_list:
        raise HTTPException(status_code=404, detail="No news found.")
    results = []
    for news in news_list[:3]:
        cached = cache_repo.get(news["url"])
        if cached:
            results.append(cached)
            continue
        content = await get_article_content(news["url"])
        analysis = await analyze_news(ticker, company_name, news["title"], content)
        analysis["news_url"] = news["url"]
        cache_repo.set(ticker, news["url"], analysis)
        results.append(analysis)
    return {"ticker": ticker, "company_name": company_name, "news": results}


# ── Legacy endpoints (kept for frontend compatibility) ──────────────────────

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
