"""Stock info service - fetches real-time stock data via yfinance."""
import yfinance as yf


def get_stock_info(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1d")
        current_price = float(hist["Close"].iloc[-1]) if not hist.empty else 0.0
        prev_close = info.get("previousClose") or 0
        change_pct = ((current_price - prev_close) / prev_close * 100) if prev_close else 0.0
        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "current_price": round(current_price, 2),
            "change_pct": round(change_pct, 2),
            "market_cap": info.get("marketCap", 0),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}
