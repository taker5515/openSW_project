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


# GET /api/summary — 정적 프론트엔드(index.html)의 간단 데모용 엔드포인트
@router.get("/summary", response_model=NewsAnalysisResponse, tags=["demo"])
async def get_summary():
    """최신 시장 동향 요약 (데모용 — API 키 없이도 fallback 텍스트 반환)"""
    try:
        result = await ai_analysis_service.analyze(
            ticker="MARKET",
            title="오늘의 글로벌 증시 동향 요약",
            content="",
        )
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Summary generation failed")
