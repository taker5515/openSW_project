from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.routes import (
    auth,
    stocks,
    market,
    financials,
    news,
    watchlists,
    users,
    health,
    ai,
    feedback,
)
from db.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    description="Stock news, financial analysis, watchlist and auth backend",
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────────────────────
app.include_router(auth.router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(stocks.router,     prefix="/api/stocks",     tags=["Stocks"])
app.include_router(market.router,     prefix="/api/market",     tags=["Market"])
app.include_router(financials.router, prefix="/api/financials", tags=["Financials"])
app.include_router(news.router,       prefix="/api/news",       tags=["News"])
app.include_router(watchlists.router, prefix="/api/watchlists", tags=["Watchlists"])
app.include_router(users.router,      prefix="/api/users",      tags=["Users"])
app.include_router(health.router,     prefix="/api",            tags=["Health"])
app.include_router(ai.router,         prefix="/api",            tags=["AI"])
app.include_router(feedback.router,   prefix="/api",            tags=["Feedback"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
