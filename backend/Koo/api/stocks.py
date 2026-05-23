from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from app.crawling_service import get_news_from_investing, get_news_content
from app.gemini_service import analyze_news
from app.stock_info_service import get_stock_info
from app.stock_list import ALL_TICKERS, STOCK_LIST
from repositories.news_cache_repository import NewsCacheRepository

router = APIRouter(prefix="/stocks", tags=["stocks"])

COMPANY_NAMES = {
    "NVDA": "NVIDIA", "MSFT": "Microsoft", "GOOGL": "Alphabet",
    "META": "Meta Platforms", "AMZN": "Amazon", "AAPL": "Apple",
    "AVGO": "Broadcom", "AMD": "AMD", "MU": "Micron", "QCOM": "Qualcomm",
    "TSM": "TSMC", "ASML": "ASML", "AMAT": "Applied Materials",
    "LRCX": "Lam Research", "ORCL": "Oracle", "CRM": "Salesforce",
    "NOW": "ServiceNow", "ADBE": "Adobe", "NFLX": "Netflix", "DIS": "Disney",
    "WMT": "Walmart", "COST": "Costco", "HD": "Home Depot", "LOW": "Lowes",
    "MCD": "McDonalds", "CMG": "Chipotle", "SBUX": "Starbucks",
    "KO": "Coca-Cola", "PEP": "PepsiCo", "PG": "Procter Gamble",
    "CL": "Colgate", "NKE": "Nike", "LULU": "Lululemon", "ABNB": "Airbnb",
    "BKNG": "Booking Holdings", "UBER": "Uber", "DASH": "DoorDash",
    "V": "Visa", "MA": "Mastercard", "ETN": "Eaton", "VRT": "Vertiv",
    "GEV": "GE Vernova", "PWR": "Quanta Services", "CAT": "Caterpillar",
    "NEE": "NextEra Energy", "EQIX": "Equinix", "PLD": "Prologis",
    "XOM": "Exxon Mobil", "RTX": "RTX", "JPM": "JPMorgan Chase",
    "BAC": "Bank of America", "WFC": "Wells Fargo", "C": "Citigroup",
    "GS": "Goldman Sachs", "MS": "Morgan Stanley", "BLK": "BlackRock",
    "BX": "Blackstone", "KKR": "KKR", "APO": "Apollo Global",
    "BRK-B": "Berkshire Hathaway", "AXP": "American Express",
    "COF": "Capital One", "PYPL": "PayPal", "COIN": "Coinbase",
    "CME": "CME Group", "ICE": "Intercontinental Exchange", "SPGI": "S&P Global",
    "LLY": "Eli Lilly", "NVO": "Novo Nordisk", "JNJ": "Johnson & Johnson",
    "MRK": "Merck", "PFE": "Pfizer", "ABBV": "AbbVie", "AMGN": "Amgen",
    "ISRG": "Intuitive Surgical", "BSX": "Boston Scientific"
}

@router.get("/{ticker}/news")
async def get_stock_news(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.upper()
    if ticker not in ALL_TICKERS:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    company_name = COMPANY_NAMES.get(ticker, ticker)
    cache_repo = NewsCacheRepository(db)
    news_list = await get_news_from_investing(ticker)
    if not news_list:
        raise HTTPException(status_code=404, detail="No news found.")
    results = []
    for news in news_list[:3]:
        cached = cache_repo.get(news["url"])
        if cached:
            results.append(cached)
            continue
        content = await get_news_content(news["url"])
        analysis = await analyze_news(ticker, company_name, news["title"], content)
        analysis["news_url"] = news["url"]
        cache_repo.set(ticker, news["url"], analysis)
        results.append(analysis)
    return {"ticker": ticker, "company_name": company_name, "news": results}

@router.get("/{ticker}/info")
def get_stock_info_api(ticker: str):
    ticker = ticker.upper()
    if ticker not in ALL_TICKERS:
        raise HTTPException(status_code=404, detail="Ticker not found.")
    return get_stock_info(ticker)

@router.get("/list")
def get_stock_list():
    return STOCK_LIST