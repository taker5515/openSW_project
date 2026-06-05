import json
import re
from typing import Dict

from core.config import settings
from core.constants import VALID_SIGNALS, DEFAULT_SIGNAL


def _normalize_signal(raw: str) -> str:
    upper = raw.strip().upper()
    return upper if upper in VALID_SIGNALS else DEFAULT_SIGNAL


def _fallback_analysis(ticker: str, title: str) -> Dict[str, str]:
    summary = (
        f"{ticker} 관련 소식으로 시장 반응을 주목할 필요가 있습니다. "
        f"'{title[:40]}...' 뉴스는 추가적인 분석이 필요합니다."
        if len(title) > 40
        else f"{ticker} 관련 소식입니다. '{title}' 뉴스는 투자자 주목이 필요합니다."
    )
    return {"summary": summary, "signal": DEFAULT_SIGNAL}


async def analyze_with_anthropic(ticker: str, title: str, content: str = "") -> Dict[str, str]:
    if not settings.ANTHROPIC_API_KEY:
        return _fallback_analysis(ticker, title)

    try:
        import httpx

        system_prompt = (
            'You are a financial analyst. Respond ONLY with valid JSON: '
            '{"summary":"2-sentence Korean investment analysis","signal":"BUY"|"SELL"|"NEUTRAL"}'
        )
        user_content = f"Ticker: {ticker}\nHeadline: {title}"
        if content:
            user_content += f"\nContent: {content[:500]}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 256,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_content}],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["content"][0]["text"]
            # strip markdown code fences if present
            text = re.sub(r"```json|```", "", text).strip()
            parsed = json.loads(text)
            return {
                "summary": parsed.get("summary", ""),
                "signal": _normalize_signal(parsed.get("signal", DEFAULT_SIGNAL)),
            }
    except Exception:
        return _fallback_analysis(ticker, title)


async def analyze_with_openai(ticker: str, title: str, content: str = "") -> Dict[str, str]:
    if not settings.OPENAI_API_KEY:
        return _fallback_analysis(ticker, title)

    try:
        import httpx

        user_content = f"Ticker: {ticker}\nHeadline: {title}"
        if content:
            user_content += f"\nContent: {content[:500]}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "max_tokens": 256,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                'You are a financial analyst. Respond ONLY with valid JSON: '
                                '{"summary":"2-sentence Korean investment analysis","signal":"BUY"|"SELL"|"NEUTRAL"}'
                            ),
                        },
                        {"role": "user", "content": user_content},
                    ],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            text = re.sub(r"```json|```", "", text).strip()
            parsed = json.loads(text)
            return {
                "summary": parsed.get("summary", ""),
                "signal": _normalize_signal(parsed.get("signal", DEFAULT_SIGNAL)),
            }
    except Exception:
        return _fallback_analysis(ticker, title)


async def analyze_news(ticker: str, title: str, content: str = "") -> Dict[str, str]:
    """Try Anthropic first, then OpenAI, then fallback."""
    if settings.ANTHROPIC_API_KEY:
        return await analyze_with_anthropic(ticker, title, content)
    if settings.OPENAI_API_KEY:
        return await analyze_with_openai(ticker, title, content)
    return _fallback_analysis(ticker, title)
