from typing import List, Dict, Any, Optional

from utils.financial_calculations import safe_divide, safe_round, calc_cagr


def calculate_ratios(
    income_data: List[Dict[str, Any]],
    balance_data: List[Dict[str, Any]],
    cashflow_data: List[Dict[str, Any]],
    period: str = "annual",
) -> List[Dict[str, Any]]:
    """
    Takes normalized statement lists and returns a list of ratio dicts,
    one per period aligned with income_data.
    """
    result = []
    n = len(income_data)

    # Calculate 3-year CAGR for revenue if we have 4 periods
    revenue_cagr_3y: Optional[float] = None
    if n >= 4:
        start_rev = income_data[n - 1].get("revenue")
        end_rev = income_data[0].get("revenue")
        revenue_cagr_3y = calc_cagr(start_rev, end_rev, 3)

    for i, inc in enumerate(income_data):
        # Match balance and cashflow by index (same period ordering)
        bal = balance_data[i] if i < len(balance_data) else {}
        cf = cashflow_data[i] if i < len(cashflow_data) else {}

        revenue = inc.get("revenue")
        gross_profit = inc.get("gross_profit")
        operating_income = inc.get("operating_income")
        net_income = inc.get("net_income")

        total_assets = bal.get("total_assets")
        total_equity = bal.get("total_equity")
        total_liabilities = bal.get("total_liabilities")
        current_assets = bal.get("current_assets")
        current_liabilities = bal.get("current_liabilities")
        inventory = bal.get("inventory")
        long_term_debt = bal.get("long_term_debt")

        operating_cf = cf.get("operating_cash_flow")
        free_cf = cf.get("free_cash_flow")

        # Profitability
        gross_margin = safe_round(
            safe_divide(gross_profit, revenue) * 100 if safe_divide(gross_profit, revenue) is not None else None
        )
        operating_margin = safe_round(
            safe_divide(operating_income, revenue) * 100 if safe_divide(operating_income, revenue) is not None else None
        )
        net_margin = safe_round(
            safe_divide(net_income, revenue) * 100 if safe_divide(net_income, revenue) is not None else None
        )
        roe = safe_round(
            safe_divide(net_income, total_equity) * 100 if safe_divide(net_income, total_equity) is not None else None
        )
        roa = safe_round(
            safe_divide(net_income, total_assets) * 100 if safe_divide(net_income, total_assets) is not None else None
        )

        # Stability
        debt_ratio = safe_round(
            safe_divide(total_liabilities, total_assets) * 100 if safe_divide(total_liabilities, total_assets) is not None else None
        )
        debt_to_equity = safe_round(
            safe_divide(long_term_debt, total_equity) * 100 if safe_divide(long_term_debt, total_equity) is not None else None
        )
        current_ratio = safe_round(safe_divide(current_assets, current_liabilities))

        # Quick ratio = (current_assets - inventory) / current_liabilities
        if current_assets is not None and current_liabilities is not None:
            inv = inventory if inventory is not None else 0.0
            quick_ratio = safe_round(safe_divide(current_assets - inv, current_liabilities))
        else:
            quick_ratio = None

        # Cashflow ratios
        free_cash_flow_margin = safe_round(
            safe_divide(free_cf, revenue) * 100 if safe_divide(free_cf, revenue) is not None else None
        )
        ocf_to_ni = safe_round(safe_divide(operating_cf, net_income))

        ratios: Dict[str, Any] = {
            "period": inc.get("period"),
            "fiscal_date": inc.get("fiscal_date"),
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "net_margin": net_margin,
            "roe": roe,
            "roa": roa,
            "revenue_growth": inc.get("revenue_growth"),
            "operating_income_growth": inc.get("operating_income_growth"),
            "net_income_growth": inc.get("net_income_growth"),
            "revenue_cagr_3y": revenue_cagr_3y if i == 0 else None,
            "debt_ratio": debt_ratio,
            "debt_to_equity": debt_to_equity,
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "free_cash_flow": free_cf,
            "free_cash_flow_margin": free_cash_flow_margin,
            "operating_cash_flow_to_net_income": ocf_to_ni,
        }
        result.append(ratios)

    return result
