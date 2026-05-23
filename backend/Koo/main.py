from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.stocks import router as stocks_router
from db.base import Base
from db.session import engine
import models.user
import models.news_cache

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Investment Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(stocks_router)

@app.get("/")
def root():
    return {"message": "ok"}