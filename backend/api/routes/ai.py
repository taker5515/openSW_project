from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services import ai_analysis_service

router = APIRouter(prefix="/ai", tags=["ai"])


class NewsAnalysisRequest(BaseModel):
    ticker: str
    title: str
    content: Optional[str] = ""


class NewsAnalysisResponse(BaseModel):
    summary: str
    signal: str


@router.post("/news-analysis", response_model=NewsAnalysisResponse)
async def analyze_news(body: NewsAnalysisRequest):
    try:
        result = await ai_analysis_service.analyze(
            ticker=body.ticker.upper(),
            title=body.title,
            content=body.content or "",
        )
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="AI analysis failed")
