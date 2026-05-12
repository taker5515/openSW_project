import json
import logging
from app.core.config import settings

log = logging.getLogger(__name__)

_BUY_KEYWORDS = ["급등", "상승", "돌파", "최고", "성장", "호실적", "강세", "확대", "회복", "증가"]
_SELL_KEYWORDS = ["급락", "하락", "부진", "손실", "우려", "악화", "감소", "약세", "하향", "미달"]


class AIProvider:
    def __init__(self):
        self._client = None
        if settings.ANTHROPIC_API_KEY:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            except ImportError:
                log.warning("anthropic package not installed; using heuristic fallback")

    def analyze_news(self, title: str, content: str = "") -> dict:
        if self._client is not None:
            return self._call_anthropic(title, content)
        return self._heuristic_fallback(title)

    def _call_anthropic(self, title: str, content: str) -> dict:
        system = (
            "You are a financial analyst. Respond ONLY with valid JSON (no markdown):\n"
            '{"summary":"2-sentence Korean analysis","signal":"BUY"|"SELL"|"NEUTRAL",'
            '"confidence":0.0-1.0,"reason":"short Korean reason"}'
        )
        user_msg = f"Headline: {title}"
        if content:
            user_msg += f"\nContext: {content[:500]}"

        try:
            msg = self._client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )
            text = msg.content[0].text.strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            result = json.loads(text)
            # Validate signal
            if result.get("signal") not in ("BUY", "SELL", "NEUTRAL"):
                result["signal"] = "NEUTRAL"
            return result
        except Exception as e:
            log.warning("Anthropic API call failed: %s; using heuristic fallback", e)
            return self._heuristic_fallback(title)

    def _heuristic_fallback(self, title: str) -> dict:
        lower = title.lower()
        buy_score = sum(1 for w in _BUY_KEYWORDS if w in title)
        sell_score = sum(1 for w in _SELL_KEYWORDS if w in title)

        if buy_score > sell_score:
            signal, confidence = "BUY", min(0.5 + buy_score * 0.05, 0.75)
            reason = "긍정적 키워드가 다수 포함되어 있어 상승 가능성을 시사합니다. (heuristic)"
        elif sell_score > buy_score:
            signal, confidence = "SELL", min(0.5 + sell_score * 0.05, 0.75)
            reason = "부정적 키워드가 다수 포함되어 있어 하락 가능성을 시사합니다. (heuristic)"
        else:
            signal, confidence = "NEUTRAL", 0.5
            reason = "방향성을 확인하기 어려운 뉴스입니다. 추가 데이터 확인을 권장합니다. (heuristic)"

        summary = (
            f"'{title}' 관련 내용으로 {signal.lower()} 시그널이 감지됩니다. "
            "이 분석은 AI API 없이 키워드 기반으로 생성된 참고용 정보입니다."
        )
        return {"summary": summary, "signal": signal, "confidence": confidence, "reason": reason}
