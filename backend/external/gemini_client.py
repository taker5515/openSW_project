"""Gemini API client - handles SDK init and raw API calls."""
import json
from typing import Optional

from core.config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            return None
        try:
            from google import genai
            _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception:
            return None
    return _client


async def generate_json(prompt: str) -> Optional[dict]:
    """Call Gemini and parse JSON response. Returns None if API key missing or call fails."""
    client = _get_client()
    if client is None:
        return None
    try:
        from google.genai import types
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)
    except Exception:
        return None
