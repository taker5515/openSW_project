import yfinance as yf
from typing import Optional, List, Dict, Any


COMPANY_NAMES: Dict[str, str] = {
    "NVDA": "NVIDIA Corp.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.",
    "META": "Meta Platforms", "AMZN": "Amazon.com Inc.", "AAPL": "Apple Inc.",
    "AVGO": "Broadcom Inc.", "AMD": "AMD Inc.", "MU": "Micron Technology",
    "QCOM": "Qualcomm Inc.", "TSM": "TSMC", "ASML": "ASML Holding",
    "AMAT": "Applied Materials", "LRCX": "Lam Research", "ORCL": "Oracle Corp.",
    "CRM": "Salesforce Inc.", "NOW": "ServiceNow", "ADBE": "Adobe Inc.",
    "NFLX": "Netflix Inc.", "DIS": "The Walt Disney Co.",
    "WMT": "Walmart Inc.", "COST": "Costco Wholesale", "HD": "Home Depot",
    "LOW": "Lowe's Companies", "MCD": "McDonald's Corp.", "SBUX": "Starbucks Corp.",
    "KO": "Coca-Cola Co.", "PEP": "PepsiCo Inc.", "V": "Visa Inc.",
    "MA": "Mastercard Inc.", "JPM": "JPMorgan Chase", "BAC": "Bank of America",
    "GS": "Goldman Sachs", "MS": "Morgan Stanley", "LLY": "Eli Lilly",
    "JNJ": "Johnson & Johnson", "PFE": "Pfizer Inc.", "TSLA": "Tesla Inc.",
    "XOM": "Exxon Mobil", "RTX": "RTX Corporation",
}

_FALLBACK_PRICES: Dict[str, float] = {
    "AAPL": 189.30, "NVDA": 875.40, "TSLA": 242.80, "MSFT": 415.60,
    "GOOGL": 175.50, "AMZN": 195.20, "META": 520.10, "AMD": 165.30,
}


def _fallback_quote(ticker: str) -> Dict[str, Any]:
    price = _FALLBACK_PRICES.get(ticker, 100.0)
    name = COMPANY_NAMES.get(ticker, ticker)
    history = [round(price * (1 + (i - 10) * 0.001), 2) for i in range(20)]
    return {
        "ticker": ticker,
        "name": name,
        "price": price,
        "change": 0.0,
        "changePct": 0.0,
        "history": history,
    }


def get_quote(ticker: str) -> Dict[str, Any]:
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}

        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose") or price
        change = round(price - prev_close, 2) if price and prev_close else 0.0
        change_pct = round((change / prev_close) * 100, 2) if prev_close else 0.0

        name = (
            info.get("longName")
            or info.get("shortName")
            or COMPANY_NAMES.get(ticker, ticker)
        )

        hist = t.history(period="5d", interval="1d")
        history: List[float] = []
        if hist is not None and not hist.empty:
            history = [round(float(p), 2) for p in hist["Close"].tolist()][-20:]

        if not price:
            return _fallback_quote(ticker)

        return {
            "ticker": ticker,
            "name": name,
            "price": round(float(price), 2),
            "change": change,
            "changePct": change_pct,
            "history": history if history else _fallback_quote(ticker)["history"],
        }
    except Exception:
        return _fallback_quote(ticker)


def get_history(ticker: str, period: str = "1mo") -> List[float]:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period, interval="1d")
        if hist is None or hist.empty:
            return _fallback_quote(ticker)["history"]
        return [round(float(p), 2) for p in hist["Close"].tolist()]
    except Exception:
        return _fallback_quote(ticker)["history"]


def get_chart(ticker: str, range_: str = "1d", interval: str = "5m") -> List[Dict[str, Any]]:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=range_, interval=interval)
        if hist is None or hist.empty:
            return _fallback_chart(ticker)

        result = []
        for ts, row in hist.iterrows():
            time_str = ts.strftime("%H:%M") if hasattr(ts, "strftime") else str(ts)
            result.append({"time": time_str, "price": round(float(row["Close"]), 2)})
        return result
    except Exception:
        return _fallback_chart(ticker)


def _fallback_chart(ticker: str) -> List[Dict[str, Any]]:
    base = _FALLBACK_PRICES.get(ticker, 100.0)
    result = []
    for i in range(60):
        h = 9 + i // 12
        m = (i % 12) * 5
        result.append({
            "time": f"{h:02d}:{m:02d}",
            "price": round(base * (1 + (i - 30) * 0.0005), 2),
        })
    return result
