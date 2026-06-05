import math
from typing import Optional


def safe_divide(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    if numerator is None or denominator is None:
        return None
    if denominator == 0:
        return None
    if math.isnan(numerator) or math.isnan(denominator):
        return None
    return numerator / denominator


def to_percent(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return round(value * 100, 2)


def calc_growth(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None:
        return None
    if previous == 0:
        return None
    return round(((current - previous) / abs(previous)) * 100, 2)


def calc_cagr(start: Optional[float], end: Optional[float], years: int) -> Optional[float]:
    if start is None or end is None or years <= 0:
        return None
    if start <= 0:
        return None
    try:
        return round(((end / start) ** (1 / years) - 1) * 100, 2)
    except Exception:
        return None


def safe_round(value: Optional[float], decimals: int = 2) -> Optional[float]:
    if value is None:
        return None
    if math.isnan(value) or math.isinf(value):
        return None
    return round(value, decimals)
