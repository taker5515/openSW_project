from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    return {"ok": True, "service": settings.APP_NAME, "version": settings.VERSION}
