# 202501552/repositories/stock_repository.py

from models.stocks import Stock

def get_by_symbol(db, symbol: str):
    return db.query(Stock).filter(Stock.symbol == symbol).all()

def save_bulk(db, symbol: str, data: list):
    for row in data:
        db.add(Stock(
            symbol=symbol,
            date=row["Date"],
            close=row["Close"]
        ))
    db.commit()