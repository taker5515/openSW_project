from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import Base, engine
from models import stocks as stock_model

from api.routes import stocks, themes, subscriptions

app = FastAPI(title="Stock Newsletter API")

# 프론트 개발 서버 허용
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/api/health")
def health_check():
    return {"ok": True, "message": "backend is running"}

app.include_router(themes.router, prefix="/api", tags=["themes"])
app.include_router(subscriptions.router, prefix="/api", tags=["subscriptions"])
app.include_router(stocks.router, prefix="/api", tags=["stocks"])