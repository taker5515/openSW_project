from typing import Dict, Any

from repositories.feedback_repository import feedback_repository
from repositories.news_repository import news_repository


def get_feedback(news_id: str) -> Dict[str, Any]:
    if news_repository.get_by_id(news_id) is None:
        return None
    up, down = feedback_repository.get(news_id)
    return {
        "news_id": news_id,
        "up_count": up,
        "down_count": down,
        "user_feedback": None,
    }


def submit_feedback(news_id: str, feedback_type: str) -> Dict[str, Any]:
    if news_repository.get_by_id(news_id) is None:
        return None
    up, down = feedback_repository.add(news_id, feedback_type)
    return {
        "news_id": news_id,
        "up_count": up,
        "down_count": down,
        "user_feedback": feedback_type,
    }
