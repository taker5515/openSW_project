def normalize_per(value: float | None) -> dict:
    if value is None or value != value:
        return {"formatted": "N/A", "status": "neutral",
                "interpretation": "데이터를 가져올 수 없습니다."}
    if value < 0:
        return {"formatted": f"{value:.1f}배", "status": "bad",
                "interpretation": "현재 적자 기업입니다. PER 해석에 주의가 필요합니다."}
    if value < 15:
        return {"formatted": f"{value:.1f}배", "status": "good",
                "interpretation": "상대적으로 저평가 구간에 위치할 수 있습니다."}
    if value < 30:
        return {"formatted": f"{value:.1f}배", "status": "neutral",
                "interpretation": "적정 수준의 밸류에이션으로 볼 수 있습니다."}
    if value < 60:
        return {"formatted": f"{value:.1f}배", "status": "high",
                "interpretation": "성장 기대가 반영된 높은 밸류에이션입니다. 성장 지속성이 중요합니다."}
    return {"formatted": f"{value:.1f}배", "status": "warning",
            "interpretation": "매우 높은 PER로 고평가 부담이 있을 수 있습니다."}


def normalize_pbr(value: float | None) -> dict:
    if value is None or value != value:
        return {"formatted": "N/A", "status": "neutral",
                "interpretation": "데이터를 가져올 수 없습니다."}
    if value < 1:
        return {"formatted": f"{value:.2f}배", "status": "good",
                "interpretation": "자산 가치 대비 낮게 평가돼 있을 수 있습니다."}
    if value < 3:
        return {"formatted": f"{value:.2f}배", "status": "neutral",
                "interpretation": "자산 대비 적정 수준의 프리미엄으로 볼 수 있습니다."}
    if value < 8:
        return {"formatted": f"{value:.2f}배", "status": "high",
                "interpretation": "시장이 기업 자산에 높은 프리미엄을 부여하고 있습니다."}
    return {"formatted": f"{value:.2f}배", "status": "warning",
            "interpretation": "매우 높은 PBR로 순자산 대비 주가 부담이 있습니다."}


def normalize_psr(value: float | None) -> dict:
    if value is None or value != value:
        return {"formatted": "N/A", "status": "neutral",
                "interpretation": "데이터를 가져올 수 없습니다."}
    if value < 3:
        return {"formatted": f"{value:.1f}배", "status": "good",
                "interpretation": "매출 대비 낮은 밸류에이션입니다."}
    if value < 10:
        return {"formatted": f"{value:.1f}배", "status": "neutral",
                "interpretation": "성장주에서 일반적으로 나타나는 PSR 수준입니다."}
    if value < 20:
        return {"formatted": f"{value:.1f}배", "status": "high",
                "interpretation": "매출 성장 지속성이 핵심 관건입니다."}
    return {"formatted": f"{value:.1f}배", "status": "warning",
            "interpretation": "매우 높은 PSR로 매출 성장에 대한 시장 기대가 이미 선반영된 상태입니다."}


def normalize_roe(value: float | None) -> dict:
    if value is None or value != value:
        return {"formatted": "N/A", "status": "neutral",
                "interpretation": "데이터를 가져올 수 없습니다."}
    if value < 0:
        return {"formatted": f"{value:.1f}%", "status": "bad",
                "interpretation": "자기자본으로 손실이 발생하고 있습니다."}
    if value < 10:
        return {"formatted": f"{value:.1f}%", "status": "low",
                "interpretation": "자본 효율성이 다소 낮은 편입니다."}
    if value < 20:
        return {"formatted": f"{value:.1f}%", "status": "neutral",
                "interpretation": "양호한 수준의 자본 효율성입니다."}
    return {"formatted": f"{value:.1f}%", "status": "good",
            "interpretation": "높은 ROE로 자기자본 대비 이익 창출 능력이 우수합니다."}


def normalize_dividend_yield(value: float | None) -> dict:
    if value is None or value != value or value == 0:
        return {"formatted": "없음", "status": "neutral",
                "interpretation": "배당을 지급하지 않거나 데이터가 없습니다."}
    pct = value * 100 if value < 1 else value
    if pct < 1:
        return {"formatted": f"{pct:.2f}%", "status": "low",
                "interpretation": "배당수익률이 낮은 편입니다. 성장주의 특성일 수 있습니다."}
    if pct < 3:
        return {"formatted": f"{pct:.2f}%", "status": "neutral",
                "interpretation": "적정 수준의 배당수익률입니다."}
    if pct < 6:
        return {"formatted": f"{pct:.2f}%", "status": "good",
                "interpretation": "높은 배당수익률로 인컴 투자자에게 매력적입니다."}
    return {"formatted": f"{pct:.2f}%", "status": "warning",
            "interpretation": "매우 높은 배당수익률은 배당 지속 가능성을 확인해야 합니다."}


def normalize_rsi(value: float) -> dict:
    if value >= 70:
        return {"formatted": f"{value:.1f}", "status": "warning",
                "interpretation": "RSI 70 이상은 단기 과열 신호로 해석되는 경우가 많습니다."}
    if value >= 50:
        return {"formatted": f"{value:.1f}", "status": "neutral",
                "interpretation": "중립~강세 구간입니다."}
    if value >= 30:
        return {"formatted": f"{value:.1f}", "status": "neutral",
                "interpretation": "중립~약세 구간입니다."}
    return {"formatted": f"{value:.1f}", "status": "good",
            "interpretation": "RSI 30 이하는 단기 침체로 반등 가능성을 보는 시각도 있습니다."}
