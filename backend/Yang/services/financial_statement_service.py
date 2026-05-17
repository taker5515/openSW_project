import pandas as pd
from typing import Optional, List, Dict, Any

from utils.financial_mappings import (
    INCOME_STATEMENT_MAPPINGS,
    BALANCE_SHEET_MAPPINGS,
    CASH_FLOW_MAPPINGS,
    safe_get_value,
)
from utils.financial_calculations import calc_growth, safe_round
from utils.date import format_fiscal_date, get_period_label

MAX_PERIODS = 4


def normalize_income_statement(
    df: Optional[pd.DataFrame], symbol: str, period: str = "annual"
) -> List[Dict[str, Any]]:
    """Normalize income statement DataFrame into a list of period dicts."""
    if df is None or df.empty:
        return []

    cols = df.columns[:MAX_PERIODS]
    result = []

    for i, col in enumerate(cols):
        row: Dict[str, Any] = {
            "period": get_period_label(col, period),
            "fiscal_date": format_fiscal_date(col),
            "revenue": safe_round(safe_get_value(df, "revenue", INCOME_STATEMENT_MAPPINGS, i)),
            "cost_of_revenue": safe_round(safe_get_value(df, "cost_of_revenue", INCOME_STATEMENT_MAPPINGS, i)),
            "gross_profit": safe_round(safe_get_value(df, "gross_profit", INCOME_STATEMENT_MAPPINGS, i)),
            "selling_general_admin_expense": safe_round(safe_get_value(df, "selling_general_admin_expense", INCOME_STATEMENT_MAPPINGS, i)),
            "research_and_development": safe_round(safe_get_value(df, "research_and_development", INCOME_STATEMENT_MAPPINGS, i)),
            "operating_expense": safe_round(safe_get_value(df, "operating_expense", INCOME_STATEMENT_MAPPINGS, i)),
            "operating_income": safe_round(safe_get_value(df, "operating_income", INCOME_STATEMENT_MAPPINGS, i)),
            "interest_expense": safe_round(safe_get_value(df, "interest_expense", INCOME_STATEMENT_MAPPINGS, i)),
            "pretax_income": safe_round(safe_get_value(df, "pretax_income", INCOME_STATEMENT_MAPPINGS, i)),
            "tax_provision": safe_round(safe_get_value(df, "tax_provision", INCOME_STATEMENT_MAPPINGS, i)),
            "net_income": safe_round(safe_get_value(df, "net_income", INCOME_STATEMENT_MAPPINGS, i)),
            "basic_eps": safe_round(safe_get_value(df, "basic_eps", INCOME_STATEMENT_MAPPINGS, i)),
            "diluted_eps": safe_round(safe_get_value(df, "diluted_eps", INCOME_STATEMENT_MAPPINGS, i)),
            "ebitda": safe_round(safe_get_value(df, "ebitda", INCOME_STATEMENT_MAPPINGS, i)),
            "revenue_growth": None,
            "operating_income_growth": None,
            "net_income_growth": None,
        }
        result.append(row)

    # Calculate YoY growth (current vs next index which is previous year in yfinance ordering)
    for i in range(len(result) - 1):
        current = result[i]
        previous = result[i + 1]
        current["revenue_growth"] = calc_growth(current["revenue"], previous["revenue"])
        current["operating_income_growth"] = calc_growth(
            current["operating_income"], previous["operating_income"]
        )
        current["net_income_growth"] = calc_growth(
            current["net_income"], previous["net_income"]
        )

    return result


def normalize_balance_sheet(
    df: Optional[pd.DataFrame], symbol: str, period: str = "annual"
) -> List[Dict[str, Any]]:
    """Normalize balance sheet DataFrame into a list of period dicts."""
    if df is None or df.empty:
        return []

    cols = df.columns[:MAX_PERIODS]
    result = []

    for i, col in enumerate(cols):
        row: Dict[str, Any] = {
            "period": get_period_label(col, period),
            "fiscal_date": format_fiscal_date(col),
            "total_assets": safe_round(safe_get_value(df, "total_assets", BALANCE_SHEET_MAPPINGS, i)),
            "current_assets": safe_round(safe_get_value(df, "current_assets", BALANCE_SHEET_MAPPINGS, i)),
            "cash_and_cash_equivalents": safe_round(safe_get_value(df, "cash_and_cash_equivalents", BALANCE_SHEET_MAPPINGS, i)),
            "accounts_receivable": safe_round(safe_get_value(df, "accounts_receivable", BALANCE_SHEET_MAPPINGS, i)),
            "inventory": safe_round(safe_get_value(df, "inventory", BALANCE_SHEET_MAPPINGS, i)),
            "non_current_assets": safe_round(safe_get_value(df, "non_current_assets", BALANCE_SHEET_MAPPINGS, i)),
            "total_liabilities": safe_round(safe_get_value(df, "total_liabilities", BALANCE_SHEET_MAPPINGS, i)),
            "current_liabilities": safe_round(safe_get_value(df, "current_liabilities", BALANCE_SHEET_MAPPINGS, i)),
            "long_term_debt": safe_round(safe_get_value(df, "long_term_debt", BALANCE_SHEET_MAPPINGS, i)),
            "total_equity": safe_round(safe_get_value(df, "total_equity", BALANCE_SHEET_MAPPINGS, i)),
            "retained_earnings": safe_round(safe_get_value(df, "retained_earnings", BALANCE_SHEET_MAPPINGS, i)),
        }
        result.append(row)

    return result


def normalize_cash_flow(
    df: Optional[pd.DataFrame], symbol: str, period: str = "annual"
) -> List[Dict[str, Any]]:
    """Normalize cash flow DataFrame into a list of period dicts."""
    if df is None or df.empty:
        return []

    cols = df.columns[:MAX_PERIODS]
    result = []

    for i, col in enumerate(cols):
        operating_cf = safe_round(safe_get_value(df, "operating_cash_flow", CASH_FLOW_MAPPINGS, i))
        capex = safe_round(safe_get_value(df, "capital_expenditure", CASH_FLOW_MAPPINGS, i))

        # Free cash flow = operating CF + capex (capex is usually negative in yfinance)
        free_cf = safe_get_value(df, "free_cash_flow", CASH_FLOW_MAPPINGS, i)
        if free_cf is None and operating_cf is not None and capex is not None:
            free_cf = safe_round(operating_cf + capex)
        else:
            free_cf = safe_round(free_cf)

        row: Dict[str, Any] = {
            "period": get_period_label(col, period),
            "fiscal_date": format_fiscal_date(col),
            "operating_cash_flow": operating_cf,
            "investing_cash_flow": safe_round(safe_get_value(df, "investing_cash_flow", CASH_FLOW_MAPPINGS, i)),
            "financing_cash_flow": safe_round(safe_get_value(df, "financing_cash_flow", CASH_FLOW_MAPPINGS, i)),
            "depreciation_and_amortization": safe_round(safe_get_value(df, "depreciation_and_amortization", CASH_FLOW_MAPPINGS, i)),
            "change_in_working_capital": safe_round(safe_get_value(df, "change_in_working_capital", CASH_FLOW_MAPPINGS, i)),
            "capital_expenditure": capex,
            "free_cash_flow": free_cf,
        }
        result.append(row)

    return result
