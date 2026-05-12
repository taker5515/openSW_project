from sqlalchemy.orm import Session
from app.repositories import theme_repository
from app.schemas.theme import ThemeItem, ThemeListResponse


def get_all(db: Session) -> ThemeListResponse:
    themes = theme_repository.get_all(db)
    items = [ThemeItem.model_validate(t) for t in themes]
    return ThemeListResponse(items=items, total=len(items))


def get_by_key(db: Session, key: str) -> ThemeItem | None:
    theme = theme_repository.get_by_key(db, key)
    if not theme:
        return None
    return ThemeItem.model_validate(theme)
