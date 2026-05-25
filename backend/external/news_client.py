"""
Placeholder for future external news API integration.
Currently the news data is served from in-memory mock via news_repository.
Replace this with a real news API (e.g. NewsAPI, Finnhub) when ready.
"""
from typing import List, Dict, Optional


class NewsClient:
    async def fetch_news(self, ticker: Optional[str] = None) -> List[Dict]:
        return []


news_client = NewsClient()
