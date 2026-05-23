import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

async def get_news_from_investing(ticker: str) -> list[dict]:
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            res = await client.get(url)
            soup = BeautifulSoup(res.text, "xml")
            items = soup.find_all("item")[:5]
            news_list = []
            for item in items:
                title = item.find("title")
                link = item.find("link")
                if title and link:
                    news_list.append({
                        "title": title.text.strip(),
                        "url": link.text.strip()
                    })
            return news_list
    except Exception as e:
        return []

async def get_news_content(url: str) -> str:
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10, follow_redirects=True) as client:
            res = await client.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            content = soup.get_text(separator=" ", strip=True)
            return content[:3000]
    except:
        return ""