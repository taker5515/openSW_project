import pandas as pd
from typing import Optional

INCOME_STATEMENT_MAPPINGS = {
    "revenue": ["Total Revenue", "Revenue"],
    "cost_of_revenue": ["Cost Of Revenue", "Cost of Goods Sold"],
    "gross_profit": ["Gross Profit"],
    "selling_general_admin_expense": [
        "Selling General Administrative",
        "Selling General And Administration",
        "General And Administrative Expense",
    ],
    "research_and_development": ["Research And Development", "Research Development"],
    "operating_expense": ["Total Operating Expenses", "Operating Expense"],
    "operating_income": ["Operating Income", "Ebit"],
    "interest_expense": ["Interest Expense", "Net Interest Income"],
    "pretax_income": ["Pretax Income"],
    "tax_provision": ["Tax Provision"],
    "net_income": ["Net Income", "Net Income Common Stockholders"],
    "basic_eps": ["Basic EPS"],
    "diluted_eps": ["Diluted EPS"],
    "ebitda": ["EBITDA", "Normalized EBITDA"],
}

BALANCE_SHEET_MAPPINGS = {
    "total_assets": ["Total Assets"],
    "current_assets": ["Current Assets"],
    "cash_and_cash_equivalents": [
        "Cash And Cash Equivalents",
        "Cash Cash Equivalents And Short Term Investments",
    ],
    "accounts_receivable": ["Accounts Receivable", "Receivables"],
    "inventory": ["Inventory"],
    "non_current_assets": ["Total Non Current Assets", "Other Non Current Assets"],
    "total_liabilities": [
        "Total Liabilities Net Minority Interest",
        "Total Liabilities",
    ],
    "current_liabilities": ["Current Liabilities", "Total Current Liabilities"],
    "long_term_debt": [
        "Long Term Debt",
        "Long Term Debt And Capital Lease Obligation",
    ],
    "total_equity": [
        "Stockholders Equity",
        "Common Stock Equity",
        "Total Stockholders Equity",
    ],
    "retained_earnings": ["Retained Earnings"],
}

CASH_FLOW_MAPPINGS = {
    "operating_cash_flow": ["Operating Cash Flow", "Cash From Operations"],
    "investing_cash_flow": [
        "Investing Cash Flow",
        "Cash From Investing Activities",
    ],
    "financing_cash_flow": [
        "Financing Cash Flow",
        "Cash From Financing Activities",
    ],
    "depreciation_and_amortization": [
        "Depreciation And Amortization",
        "Depreciation Amortization Depletion",
    ],
    "change_in_working_capital": [
        "Change In Working Capital",
        "Changes In Working Capital",
    ],
    "capital_expenditure": ["Capital Expenditure", "Capital Expenditures"],
    "free_cash_flow": ["Free Cash Flow"],
}


def safe_get_value(
    df: pd.DataFrame, field: str, mappings: dict, col_index: int = 0
) -> Optional[float]:
    """Try each alias for a field and return the first found value."""
    if df is None or df.empty:
        return None
    aliases = mappings.get(field, [])
    for alias in aliases:
        if alias in df.index:
            try:
                cols = df.columns
                if col_index < len(cols):
                    val = df.loc[alias, cols[col_index]]
                    if pd.notna(val) and val is not None:
                        return float(val)
            except Exception:
                continue
    return None
