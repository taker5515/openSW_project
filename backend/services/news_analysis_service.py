"""News analysis service - builds prompts, calls Gemini, parses results."""
from typing import Dict

from external.gemini_client import generate_json

PROMPT_TEMPLATE = """
You are a professional financial analyst specializing in US stock markets and global macroeconomics.

Input Data:
- Target Stock: {ticker} ({company_name})
- News Title: {news_title}
- News Content: {news_content}

Instructions:
Analyze the news and respond ONLY in the following JSON format:

{{
  "ticker": "{ticker}",
  "summary": "News summary in Korean (2-3 sentences)...",
  "sentiment_score": "호재",
  "related_tickers": ["TSM", "AMD"],
  "market_outlook": "Macro analysis in Korean (1-2 sentences)..."
}}

sentiment_score must be one of: 강한 호재, 호재, 불호재, 강한 불호재
"""


def _fallback_result(ticker: str, reason: str = "") -> Dict:
    return {
        "ticker": ticker,
        "summary": "뉴스 분석을 일시적으로 수행할 수 없습니다.",
        "sentiment_score": "불호재",
        "related_tickers": [],
        "market_outlook": reason or "Gemini API key not configured or call failed.",
    }


async def analyze_news(ticker: str, company_name: str, news_title: str, news_content: str) -> Dict:
    """Analyze news via Gemini. Returns fallback dict if API unavailable."""
    from core.config import settings
    if not settings.GEMINI_API_KEY:
        return _fallback_result(ticker, "Gemini API key not configured.")

    prompt = PROMPT_TEMPLATE.format(
        ticker=ticker,
        company_name=company_name,
        news_title=news_title,
        news_content=news_content,
    )
    result = await generate_json(prompt)
    if result is None:
        return _fallback_result(ticker, "Gemini API call failed.")
    return result
