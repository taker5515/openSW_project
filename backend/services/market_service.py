"""Market overview service - fetches and analyzes market-level news."""
from typing import List, Dict

from external.market_news_client import fetch_market_headlines, fetch_article_content
from services.news_analysis_service import analyze_news


async def get_market_overview(max_articles: int = 3) -> List[Dict]:
    """Fetch market headlines, analyze them, return results list."""
    headlines = await fetch_market_headlines()
    results = []
    for news in headlines[:max_articles]:
        try:
            content = await fetch_article_content(news["url"])
            analysis = await analyze_news("MARKET", "US Stock Market", news["title"], content)
            analysis["news_url"] = news["url"]
            results.append(analysis)
        except Exception:
            continue
    return results
