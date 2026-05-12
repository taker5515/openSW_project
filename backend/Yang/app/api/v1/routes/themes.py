from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.news import NewsListResponse
from app.schemas.theme import ThemeItem, ThemeListResponse
from app.services import news_service, theme_service

router = APIRouter()


@router.get("", response_model=ThemeListResponse)
def list_themes(db: Session = Depends(get_db)):
    return theme_service.get_all(db)


@router.get("/{theme_key}", response_model=ThemeItem)
def get_theme(theme_key: str, db: Session = Depends(get_db)):
    theme = theme_service.get_by_key(db, theme_key)
    if not theme:
        raise HTTPException(status_code=404, detail="테마를 찾을 수 없습니다.")
    return theme


@router.get("/{theme_key}/news", response_model=NewsListResponse)
def get_theme_news(theme_key: str, limit: int = 10, db: Session = Depends(get_db)):
    return news_service.get_by_theme(db, theme_key, limit)
