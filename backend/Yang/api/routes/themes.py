from fastapi import APIRouter, HTTPException

from schemas.theme import ThemeListResponse, ThemeNewsResponse
from services.theme_service import get_all_themes, get_news_by_theme

router = APIRouter()

@router.get("/themes", response_model=ThemeListResponse)
def read_themes():
    return get_all_themes()

@router.get("/themes/{theme_name}/news", response_model=ThemeNewsResponse)
def read_theme_news(theme_name: str, limit: int = 10):
    result = get_news_by_theme(theme_name, limit)

    if result is None:
        raise HTTPException(status_code=404, detail="Unknown theme")

    return result