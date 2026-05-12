from fastapi import APIRouter
from app.api.v1.routes import (
    health, auth, themes, stocks, news,
    subscriptions, watchlist, ai, analytics,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(themes.router, prefix="/themes", tags=["themes"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
