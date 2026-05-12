import pandas as pd
import pandas_ta as ta
import yfinance as yf
from fastapi import FastAPI

app = FastAPI()

@app.get("/stock")
def get_stock():
    return {
        "price": 150,
        "rsi": 45
    }

# 데이터 가져오기
# pandas 계산
data = {
    "name": ["A", "B", "C"],
    "price": [100, 200, 300]
}
df = pd.DataFrame(data)
df["double_price"] = df["price"] * 2

stock = yf.Ticker("AAPL")
data = stock.history(period="1y")

print(data)

print(data.head()) # 최근 데이터 일부
print(data["Close"]) # 종가만 보기

data["MA5"] = data["Close"].rolling(5).mean()
data["MA20"] = data["Close"].rolling(20).mean()
data["MA60"] = data["Close"].rolling(60).mean()

data["RSI"] = ta.rsi(data["Close"], length=14)

def interpret_rsi(rsi):
    if rsi > 70:
        return "overbought"
    elif rsi < 30:
        return "oversold"
    else:
        return "neutral"
print(data.tail())

# JSON 반환
result = data.to_dict(orient="records")
print(result)

print(df)
print(df["price"]) # 칼럼 선택
print(df.head()) # 위 5개
print(df.tail()) # 아래 5개
print(df.describe()) # 통계 요약