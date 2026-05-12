# 202501552/api/routes/stock.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from services.stock_service import get_stock_data

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stock/{symbol}")
def read_stock(symbol: str, db: Session = Depends(get_db)):
    return get_stock_data(db, symbol)