from typing import Dict

from external.ai_client import analyze_news


async def analyze(ticker: str, title: str, content: str = "") -> Dict[str, str]:
    return await analyze_news(ticker=ticker, title=title, content=content)
