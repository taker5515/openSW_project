from typing import Dict, Any, List

from external import stock_price_client as client


def get_quote(ticker: str) -> Dict[str, Any]:
    ticker = ticker.upper()
    return client.get_quote(ticker)


def get_history(ticker: str) -> Dict[str, Any]:
    ticker = ticker.upper()
    history = client.get_history(ticker)
    return {"ticker": ticker, "history": history}


def get_chart(ticker: str, range_: str = "1d", interval: str = "5m") -> Dict[str, Any]:
    ticker = ticker.upper()
    data = client.get_chart(ticker, range_=range_, interval=interval)
    return {"ticker": ticker, "range": range_, "interval": interval, "data": data}
