from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.stock import StockPriceResponse
from services.stock_service import get_stock_prices

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/stocks/{symbol}/prices", response_model=StockPriceResponse)
def read_stock_prices(
    symbol: str,
    period: str = "3mo",
    db: Session = Depends(get_db),
):
    return get_stock_prices(db, symbol.upper(), period)