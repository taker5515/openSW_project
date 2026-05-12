from fastapi import APIRouter
from app.external.ai_provider import AIProvider
from app.schemas.analysis import AIAnalysisRequest, AIAnalysisResponse

router = APIRouter()

_ai_provider = AIProvider()


@router.post("/news/analyze", response_model=AIAnalysisResponse)
def analyze_news(body: AIAnalysisRequest):
    result = _ai_provider.analyze_news(body.title, body.content)
    return AIAnalysisResponse(
        summary=result.get("summary", ""),
        signal=result.get("signal", "NEUTRAL"),
        confidence=float(result.get("confidence", 0.5)),
        reason=result.get("reason", ""),
    )
