"""Market news crawler - fetches Yahoo Finance RSS for major market indices."""
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

MARKET_RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^DJI&region=US&lang=en-US",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^IXIC&region=US&lang=en-US",
]


async def fetch_market_headlines(max_per_feed: int = 2) -> List[Dict]:
    """Fetch headlines from market RSS feeds."""
    all_news = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        for url in MARKET_RSS_URLS:
            try:
                res = await client.get(url)
                soup = BeautifulSoup(res.text, "xml")
                for item in soup.find_all("item")[:max_per_feed]:
                    title = item.find("title")
                    link = item.find("link")
                    if title and link:
                        all_news.append({"title": title.text.strip(), "url": link.text.strip()})
            except Exception:
                continue
    return all_news


async def fetch_article_content(url: str) -> str:
    """Fetch and extract text content from an article URL."""
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10, follow_redirects=True) as client:
            res = await client.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception:
        return ""
