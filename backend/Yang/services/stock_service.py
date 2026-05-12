# 202501552/services/stock_service.py (RSI, SMA, ... 추가예정)

from repositories import stock_repository
from external.yfinance_client import fetch_stock
import pandas_ta as ta
import pandas as pd
import numpy as np

def get_stock_data(db, symbol: str):

    db_data = stock_repository.get_by_symbol(db, symbol)

    if db_data:
        return {
            "symbol": symbol,
            "source": "db",
            "data": [
                {"date": row.date, "close": row.close}
                for row in db_data
            ]
        }

    external_data = fetch_stock(symbol)

    stock_repository.save_bulk(db, symbol, external_data)

    return {
        "symbol": symbol,
        "source": "api",
        "data": [
            {"date": row["Date"], "close": row["Close"]}
            for row in external_data
        ]
    }
# rsi, sma, 