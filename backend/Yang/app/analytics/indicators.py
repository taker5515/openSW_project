import logging
import pandas as pd
import numpy as np

log = logging.getLogger(__name__)


def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def calculate_rsi(series: pd.Series, length: int = 14) -> float:
    try:
        import pandas_ta as ta
        result = ta.rsi(series, length=length)
        if result is not None and not result.empty:
            val = result.dropna()
            if not val.empty:
                return round(float(val.iloc[-1]), 2)
    except Exception:
        pass

    # Manual RSI fallback
    try:
        delta = series.diff().dropna()
        if len(delta) < length:
            return 50.0
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=length, min_periods=length).mean().iloc[-1]
        avg_loss = loss.rolling(window=length, min_periods=length).mean().iloc[-1]
        if avg_gain == 0 and avg_loss == 0:
            return 50.0
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100.0 - (100.0 / (1.0 + rs)), 2)
    except Exception as e:
        log.warning("RSI calculation failed: %s", e)
        return 50.0


def calculate_volatility(series: pd.Series, window: int = 20) -> float:
    try:
        returns = series.pct_change().dropna()
        if len(returns) < 2:
            return 0.0
        vol = returns.rolling(window=min(window, len(returns))).std().iloc[-1]
        return round(float(vol * (252 ** 0.5) * 100), 2)
    except Exception:
        return 0.0


def calculate_drawdown(series: pd.Series) -> float:
    """Returns maximum drawdown as a positive percentage."""
    try:
        if len(series) < 2:
            return 0.0
        rolling_max = series.cummax()
        drawdown = (series - rolling_max) / rolling_max
        return round(float(drawdown.min() * -100), 2)
    except Exception:
        return 0.0


def price_vs_sma(series: pd.Series, window: int = 20) -> dict:
    """Returns current price position vs SMA as percent diff."""
    try:
        sma = calculate_sma(series, window)
        current = series.iloc[-1]
        sma_val = sma.iloc[-1]
        diff_pct = round((current - sma_val) / sma_val * 100, 2) if sma_val else 0.0
        return {"sma": round(float(sma_val), 2), "diff_pct": diff_pct}
    except Exception:
        return {"sma": None, "diff_pct": 0.0}
