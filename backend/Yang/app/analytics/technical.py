import pandas as pd
from app.analytics.indicators import calculate_rsi, price_vs_sma, calculate_volatility, calculate_drawdown


def analyze(hist_df: pd.DataFrame | None, info: dict | None) -> dict:
    """Returns technical analysis dict from OHLCV DataFrame + info."""
    result = {
        "rsi14": None,
        "sma20": None,
        "sma20_diff_pct": None,
        "sma50": None,
        "volatility_annual": None,
        "max_drawdown": None,
        "fifty_two_week_high": None,
        "fifty_two_week_low": None,
        "price_vs_52w_high_pct": None,
    }

    if info:
        result["fifty_two_week_high"] = info.get("fiftyTwoWeekHigh")
        result["fifty_two_week_low"] = info.get("fiftyTwoWeekLow")

    if hist_df is None or hist_df.empty:
        return result

    close_col = "Close" if "Close" in hist_df.columns else None
    if close_col is None:
        return result

    closes = hist_df[close_col].dropna()
    if len(closes) < 2:
        return result

    result["rsi14"] = calculate_rsi(closes, 14)
    result["volatility_annual"] = calculate_volatility(closes)
    result["max_drawdown"] = calculate_drawdown(closes)

    sma20 = price_vs_sma(closes, 20)
    result["sma20"] = sma20["sma"]
    result["sma20_diff_pct"] = sma20["diff_pct"]

    sma50 = price_vs_sma(closes, 50)
    result["sma50"] = sma50["sma"]

    if result["fifty_two_week_high"] and result["fifty_two_week_high"] > 0:
        current = float(closes.iloc[-1])
        high_52w = float(result["fifty_two_week_high"])
        result["price_vs_52w_high_pct"] = round((current - high_52w) / high_52w * 100, 2)

    return result
