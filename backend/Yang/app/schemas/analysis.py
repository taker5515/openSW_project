from typing import Literal
from pydantic import BaseModel

StatusType = Literal["good", "bad", "neutral", "high", "low", "warning"]
ToneType = Literal["positive", "negative", "neutral", "warning"]


class AnalysisItem(BaseModel):
    key: str
    label: str
    value: str
    unit: str = ""
    status: StatusType = "neutral"
    description: str = ""
    interpretation: str = ""


class Section(BaseModel):
    key: str
    title: str
    subtitle: str
    items: list[AnalysisItem]


class SummaryCard(BaseModel):
    title: str
    value: str
    tone: ToneType = "neutral"
    description: str = ""


class TossStyleResponse(BaseModel):
    ticker: str
    name: str
    price: float
    score: float
    disclaimer: str = "이 정보는 투자 판단을 위한 참고용이며 투자 추천이 아닙니다."
    sections: list[Section]
    summary_cards: list[SummaryCard]
    generated_at: str


class AIAnalysisRequest(BaseModel):
    ticker: str = ""
    title: str
    content: str = ""


class AIAnalysisResponse(BaseModel):
    summary: str
    signal: Literal["BUY", "SELL", "NEUTRAL"]
    confidence: float
    reason: str
