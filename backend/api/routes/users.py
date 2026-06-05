from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from db.session import get_db
from core.auth_deps import get_current_user
from repositories.user_repository import UserRepository
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class ThemesRequest(BaseModel):
    themes: List[str]


@router.put("/me/themes")
def update_themes(
    data: ThemesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    UserRepository(db).update_themes(current_user.id, ",".join(data.themes))
    return {"themes": data.themes}


@router.get("/me/themes")
def get_themes(current_user: User = Depends(get_current_user)):
    themes = current_user.themes.split(",") if current_user.themes else []
    return {"themes": themes}
