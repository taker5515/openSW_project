from google import genai
from google.genai import types
import json
from core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

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

async def analyze_news(ticker: str, company_name: str, news_title: str, news_content: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        ticker=ticker,
        company_name=company_name,
        news_title=news_title,
        news_content=news_content
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "ticker": ticker,
            "summary": "Analysis failed",
            "sentiment_score": "불호재",
            "related_tickers": [],
            "market_outlook": str(e)
        }