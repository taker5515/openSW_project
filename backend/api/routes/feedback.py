from fastapi import APIRouter, HTTPException

from schemas.feedback import FeedbackRequest, FeedbackResponse
from services import feedback_service

router = APIRouter(tags=["feedback"])


@router.get("/news/{news_id}/feedback", response_model=FeedbackResponse)
def get_feedback(news_id: str):
    result = feedback_service.get_feedback(news_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"News {news_id} not found")
    return result


@router.post("/news/{news_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(news_id: str, body: FeedbackRequest):
    result = feedback_service.submit_feedback(news_id, body.type)
    if result is None:
        raise HTTPException(status_code=404, detail=f"News {news_id} not found")
    return result
