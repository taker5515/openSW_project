from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import financials

app = FastAPI(
    title="Investment Analysis API",
    description="미국주식 재무제표 기반 투자분석 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(financials.router, prefix="/api/financials", tags=["financials"])


@app.get("/")
def root():
    return {"message": "Investment Analysis API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
