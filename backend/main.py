from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.routes import health, financials, stocks, watchlists, news, ai, feedback

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="openSW 통합 백엔드 API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(financials.router, prefix="/api")
app.include_router(stocks.router, prefix="/api")
app.include_router(watchlists.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running"}
