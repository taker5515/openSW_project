def extract(info: dict | None) -> dict:
    """Normalize yfinance info dict into a flat fundamentals dict."""
    if not info:
        return {}

    def _safe(key):
        v = info.get(key)
        return None if v in (None, "N/A", float("inf"), float("-inf")) else v

    def _pct(key):
        v = _safe(key)
        return round(float(v) * 100, 2) if v is not None else None

    return {
        "per": _safe("trailingPE") or _safe("forwardPE"),
        "forward_per": _safe("forwardPE"),
        "pbr": _safe("priceToBook"),
        "psr": _safe("priceToSalesTrailing12Months"),
        "roe": _pct("returnOnEquity"),
        "roa": _pct("returnOnAssets"),
        "operating_margin": _pct("operatingMargins"),
        "profit_margin": _pct("profitMargins"),
        "gross_margin": _pct("grossMargins"),
        "revenue_growth": _pct("revenueGrowth"),
        "earnings_growth": _pct("earningsGrowth"),
        "eps": _safe("trailingEps"),
        "forward_eps": _safe("forwardEps"),
        "bps": _safe("bookValue"),
        "dividend_yield": _safe("dividendYield"),
        "payout_ratio": _pct("payoutRatio"),
        "market_cap": _safe("marketCap"),
        "fifty_two_week_high": _safe("fiftyTwoWeekHigh"),
        "fifty_two_week_low": _safe("fiftyTwoWeekLow"),
        "beta": _safe("beta"),
        "current_ratio": _safe("currentRatio"),
        "debt_to_equity": _safe("debtToEquity"),
        "free_cashflow": _safe("freeCashflow"),
        "total_revenue": _safe("totalRevenue"),
        "target_mean_price": _safe("targetMeanPrice"),
        "recommendation": info.get("recommendationKey"),
    }
