import pandas as pd
from typing import Optional


def format_fiscal_date(date) -> Optional[str]:
    try:
        if date is None:
            return None
        if isinstance(date, str):
            return date
        return pd.Timestamp(date).strftime("%Y-%m-%d")
    except Exception:
        return None


def get_period_label(date, period: str = "annual") -> str:
    try:
        ts = pd.Timestamp(date)
        if period == "quarterly":
            return f"Q{(ts.month - 1) // 3 + 1} {ts.year}"
        return str(ts.year)
    except Exception:
        return str(date)
