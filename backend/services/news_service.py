from typing import List, Optional, Dict

from repositories.news_repository import news_repository


def get_news(ticker: Optional[str] = None) -> List[Dict]:
    return news_repository.get_all(ticker=ticker)


def get_news_by_id(news_id: str) -> Optional[Dict]:
    return news_repository.get_by_id(news_id)
