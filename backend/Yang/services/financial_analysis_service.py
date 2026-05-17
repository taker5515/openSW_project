"""Rule-based financial analysis service. NO AI. NO LLM."""
from typing import List, Dict, Any, Optional


def analyze(ratios_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Takes list of ratio dicts, returns analysis list based on the most recent period."""
    if not ratios_data:
        return []

    latest = ratios_data[0]
    result: List[Dict[str, Any]] = []

    # Profitability: operating_margin
    operating_margin: Optional[float] = latest.get("operating_margin")
    if operating_margin is not None:
        if operating_margin >= 20:
            result.append({
                "category": "profitability",
                "level": "excellent",
                "message": "Operating margin is above 20%, indicating strong profitability.",
                "message_ko": "영업이익률이 20% 이상으로 수익성이 매우 우수합니다.",
            })
        elif operating_margin >= 10:
            result.append({
                "category": "profitability",
                "level": "good",
                "message": "Operating margin is above 10%.",
                "message_ko": "영업이익률이 10% 이상으로 양호합니다.",
            })
        elif operating_margin >= 0:
            result.append({
                "category": "profitability",
                "level": "normal",
                "message": "Operating margin is positive.",
                "message_ko": "영업이익률이 양수입니다.",
            })
        else:
            result.append({
                "category": "profitability",
                "level": "warning",
                "message": "Operating margin is negative, indicating operating losses.",
                "message_ko": "영업이익률이 음수로 영업 손실 상태입니다.",
            })

    # Growth: revenue_growth
    revenue_growth: Optional[float] = latest.get("revenue_growth")
    if revenue_growth is not None:
        if revenue_growth >= 15:
            result.append({
                "category": "growth",
                "level": "excellent",
                "message": "Revenue grew more than 15% YoY, indicating rapid growth.",
                "message_ko": "매출이 전년 대비 15% 이상 성장하여 고성장 중입니다.",
            })
        elif revenue_growth >= 5:
            result.append({
                "category": "growth",
                "level": "good",
                "message": "Revenue grew more than 5% YoY.",
                "message_ko": "매출이 전년 대비 5% 이상 성장했습니다.",
            })
        elif revenue_growth >= 0:
            result.append({
                "category": "growth",
                "level": "normal",
                "message": "Revenue is growing slightly.",
                "message_ko": "매출이 소폭 성장하고 있습니다.",
            })
        else:
            result.append({
                "category": "growth",
                "level": "warning",
                "message": "Revenue declined YoY.",
                "message_ko": "매출이 전년 대비 감소했습니다.",
            })

    # Stability: debt_ratio
    debt_ratio: Optional[float] = latest.get("debt_ratio")
    if debt_ratio is not None:
        if debt_ratio <= 40:
            result.append({
                "category": "stability",
                "level": "good",
                "message": "Debt ratio is relatively low, indicating stable financial structure.",
                "message_ko": "부채 비율이 낮아 재무 구조가 안정적입니다.",
            })
        elif debt_ratio <= 70:
            result.append({
                "category": "stability",
                "level": "normal",
                "message": "Debt ratio is moderate.",
                "message_ko": "부채 비율이 보통 수준입니다.",
            })
        else:
            result.append({
                "category": "stability",
                "level": "warning",
                "message": "Debt ratio is high, which may indicate financial risk.",
                "message_ko": "부채 비율이 높아 재무 리스크가 있을 수 있습니다.",
            })

    # Cashflow: free_cash_flow_margin
    fcf_margin: Optional[float] = latest.get("free_cash_flow_margin")
    if fcf_margin is not None:
        if fcf_margin >= 10:
            result.append({
                "category": "cashflow",
                "level": "good",
                "message": "Free cash flow margin is healthy.",
                "message_ko": "잉여현금흐름 마진이 건전합니다.",
            })
        elif fcf_margin >= 0:
            result.append({
                "category": "cashflow",
                "level": "normal",
                "message": "Free cash flow is positive.",
                "message_ko": "잉여현금흐름이 양수입니다.",
            })
        else:
            result.append({
                "category": "cashflow",
                "level": "warning",
                "message": "Free cash flow is negative.",
                "message_ko": "잉여현금흐름이 음수입니다.",
            })

    return result
