from fastapi import APIRouter
from app.crawling_service import get_news_from_investing, get_news_content
from app.gemini_service import analyze_news

router = APIRouter(prefix="/market", tags=["market"])

MARKET_NEWS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^DJI&region=US&lang=en-US",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^IXIC&region=US&lang=en-US",
]

@router.get("/overview")
async def get_market_overview():
    import httpx
    from bs4 import BeautifulSoup

    HEADERS = {"User-Agent": "Mozilla/5.0"}
    all_news = []

    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        for url in MARKET_NEWS_URLS:
            try:
                res = await client.get(url)
                soup = BeautifulSoup(res.text, "xml")
                items = soup.find_all("item")[:2]
                for item in items:
                    title = item.find("title")
                    link = item.find("link")
                    if title and link:
                        all_news.append({
                            "title": title.text.strip(),
                            "url": link.text.strip()
                        })
            except:
                continue

    results = []
    for news in all_news[:3]:
        try:
            async with httpx.AsyncClient(headers=HEADERS, timeout=10, follow_redirects=True) as client:
                res = await client.get(news["url"])
                soup = BeautifulSoup(res.text, "html.parser")
                for tag in soup(["script", "style", "nav", "header", "footer"]):
                    tag.decompose()
                content = soup.get_text(separator=" ", strip=True)[:3000]
            analysis = await analyze_news("MARKET", "US Stock Market", news["title"], content)
            analysis["news_url"] = news["url"]
            results.append(analysis)
        except:
            continue

    return {"market_overview": results}