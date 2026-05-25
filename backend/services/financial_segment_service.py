def get_segments(symbol: str, period: str) -> dict:
    return {
        "symbol": symbol,
        "period": period,
        "available": False,
        "message": "Segment revenue data is not available from the current data provider.",
        "segments": [],
        "chart_data": [],
    }
