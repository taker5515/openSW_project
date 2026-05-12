# 202501552/external/yfinance_client.py

import yfinance as yf

def fetch_stock(symbol: str):
    df = yf.Ticker(symbol).history(period="3mo")
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)

    return df[["Date", "Close"]].to_dict(orient="records")