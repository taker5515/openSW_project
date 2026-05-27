"""News crawling service - fetches article lists and content from Yahoo Finance RSS."""
from typing import List, Dict

import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def get_news_from_rss(ticker: str) -> List[Dict]:
    """Fetch news headlines for a ticker from Yahoo Finance RSS."""
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            res = await client.get(url)
            soup = BeautifulSoup(res.text, "xml")
            news_list = []
            for item in soup.find_all("item")[:5]:
                title = item.find("title")
                link = item.find("link")
                if title and link:
                    news_list.append({"title": title.text.strip(), "url": link.text.strip()})
            return news_list
    except Exception:
        return []


async def get_article_content(url: str) -> str:
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
