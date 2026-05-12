from datetime import datetime, timezone
from app.schemas.analysis import AnalysisItem, Section, SummaryCard, TossStyleResponse
from app.analytics import valuation as val_mod

_STATUS_WEIGHT = {"good": 1.0, "neutral": 0.5, "high": 0.6, "low": 0.4, "bad": 0.0, "warning": 0.2}


def _item(key, label, raw_value, unit, norm: dict, description: str) -> AnalysisItem:
    return AnalysisItem(
        key=key,
        label=label,
        value=norm.get("formatted", "N/A") if raw_value is None else norm.get("formatted", "N/A"),
        unit=unit,
        status=norm.get("status", "neutral"),
        description=description,
        interpretation=norm.get("interpretation", ""),
    )


def build_toss_style_sections(
    info: dict,
    tech: dict,
    fundamentals: dict,
) -> list[Section]:
    sections: list[Section] = []

    # --- Valuation ---
    val_items = []
    per = fundamentals.get("per")
    if per is not None:
        val_items.append(_item(
            "per", "PER (주가수익비율)", per, "배",
            val_mod.normalize_per(per),
            "기업이 버는 이익 대비 주가가 몇 배인지 보여주는 지표입니다.",
        ))
    pbr = fundamentals.get("pbr")
    if pbr is not None:
        val_items.append(_item(
            "pbr", "PBR (주가순자산비율)", pbr, "배",
            val_mod.normalize_pbr(pbr),
            "기업의 순자산 대비 주가 수준을 보여주는 지표입니다.",
        ))
    psr = fundamentals.get("psr")
    if psr is not None:
        val_items.append(_item(
            "psr", "PSR (주가매출비율)", psr, "배",
            val_mod.normalize_psr(psr),
            "매출 대비 기업 가치를 보는 지표입니다.",
        ))
    if val_items:
        sections.append(Section(
            key="valuation",
            title="가격이 비싼 편인가요?",
            subtitle="PER, PBR, PSR로 현재 가격 수준을 봅니다.",
            items=val_items,
        ))

    # --- Profitability ---
    profit_items = []
    roe = fundamentals.get("roe")
    if roe is not None:
        profit_items.append(_item(
            "roe", "ROE (자기자본이익률)", roe, "%",
            val_mod.normalize_roe(roe),
            "자기자본으로 얼마나 효율적으로 이익을 내는지 보여줍니다.",
        ))
    op_margin = fundamentals.get("operating_margin")
    if op_margin is not None:
        status = "good" if op_margin >= 15 else ("neutral" if op_margin >= 5 else "low")
        profit_items.append(AnalysisItem(
            key="operating_margin",
            label="영업이익률",
            value=f"{op_margin:.1f}",
            unit="%",
            status=status,
            description="매출에서 영업비용을 뺀 후 남는 이익의 비율입니다.",
            interpretation="높을수록 비용 구조가 효율적임을 나타냅니다.",
        ))
    net_margin = fundamentals.get("profit_margin")
    if net_margin is not None:
        status = "good" if net_margin >= 10 else ("neutral" if net_margin >= 3 else "low")
        profit_items.append(AnalysisItem(
            key="profit_margin",
            label="순이익률",
            value=f"{net_margin:.1f}",
            unit="%",
            status=status,
            description="최종적으로 기업에 남는 이익의 비율입니다.",
            interpretation="높을수록 실질적인 수익 창출 능력이 좋습니다.",
        ))
    if profit_items:
        sections.append(Section(
            key="profitability",
            title="돈을 잘 벌고 있나요?",
            subtitle="ROE, 영업이익률, 순이익률을 봅니다.",
            items=profit_items,
        ))

    # --- Dividend ---
    div_items = []
    div_yield = fundamentals.get("dividend_yield")
    div_norm = val_mod.normalize_dividend_yield(div_yield)
    div_items.append(AnalysisItem(
        key="dividend_yield",
        label="배당수익률",
        value=div_norm.get("formatted", "없음"),
        unit="",
        status=div_norm.get("status", "neutral"),
        description="주가 대비 1년 배당금의 비율입니다.",
        interpretation=div_norm.get("interpretation", ""),
    ))
    sections.append(Section(
        key="dividend",
        title="배당은 어떤가요?",
        subtitle="배당수익률로 주주 환원 수준을 봅니다.",
        items=div_items,
    ))

    # --- Momentum / Technicals ---
    momentum_items = []
    rsi = tech.get("rsi14")
    if rsi is not None:
        rsi_norm = val_mod.normalize_rsi(rsi)
        momentum_items.append(AnalysisItem(
            key="rsi14",
            label="RSI 14",
            value=f"{rsi:.1f}",
            unit="",
            status=rsi_norm.get("status", "neutral"),
            description="최근 상승·하락 강도를 0~100 사이로 나타내는 기술적 지표입니다.",
            interpretation=rsi_norm.get("interpretation", ""),
        ))
    sma20_diff = tech.get("sma20_diff_pct")
    if sma20_diff is not None:
        status = "good" if sma20_diff > 3 else ("bad" if sma20_diff < -3 else "neutral")
        momentum_items.append(AnalysisItem(
            key="sma20_diff",
            label="20일 이평선 대비",
            value=f"{sma20_diff:+.1f}",
            unit="%",
            status=status,
            description="현재 주가가 20일 이동평균선보다 얼마나 위/아래에 있는지 보여줍니다.",
            interpretation="양수면 이평선 위, 음수면 이평선 아래입니다.",
        ))
    price_vs_high = tech.get("price_vs_52w_high_pct")
    if price_vs_high is not None:
        status = "good" if price_vs_high >= -5 else ("neutral" if price_vs_high >= -20 else "low")
        momentum_items.append(AnalysisItem(
            key="price_vs_52w_high",
            label="52주 고가 대비",
            value=f"{price_vs_high:+.1f}",
            unit="%",
            status=status,
            description="52주 최고가 대비 현재 주가 위치입니다.",
            interpretation="0%에 가까울수록 52주 고점 근처, 낮을수록 고점에서 많이 하락한 상태입니다.",
        ))
    if momentum_items:
        sections.append(Section(
            key="momentum",
            title="최근 흐름은 어떤가요?",
            subtitle="RSI, 이동평균, 52주 고가 대비로 봅니다.",
            items=momentum_items,
        ))

    # --- Risk ---
    risk_items = []
    beta = info.get("beta") if info else None
    if beta is not None:
        status = "good" if beta < 1 else ("neutral" if beta < 1.5 else "warning")
        risk_items.append(AnalysisItem(
            key="beta",
            label="베타",
            value=f"{beta:.2f}",
            unit="",
            status=status,
            description="시장 전체 대비 주가 변동성의 상대적 크기입니다.",
            interpretation="1 이상이면 시장보다 변동이 크고, 1 미만이면 상대적으로 안정적입니다.",
        ))
    vol = tech.get("volatility_annual")
    if vol is not None and vol > 0:
        status = "good" if vol < 20 else ("neutral" if vol < 40 else "warning")
        risk_items.append(AnalysisItem(
            key="volatility",
            label="연간 변동성",
            value=f"{vol:.1f}",
            unit="%",
            status=status,
            description="과거 가격 기반으로 계산한 연간 변동성 추정치입니다.",
            interpretation="낮을수록 가격 안정성이 높으며, 높을수록 급등락 가능성이 큽니다.",
        ))
    if risk_items:
        sections.append(Section(
            key="risk",
            title="얼마나 위험한가요?",
            subtitle="베타와 변동성으로 리스크 수준을 봅니다.",
            items=risk_items,
        ))

    return sections


def calculate_overall_score(sections: list[Section]) -> float:
    all_items = [item for s in sections for item in s.items]
    if not all_items:
        return 50.0
    total = sum(_STATUS_WEIGHT.get(item.status, 0.5) for item in all_items)
    return round(total / len(all_items) * 100, 1)


def build_summary_cards(
    sections: list[Section],
    score: float,
    fundamentals: dict,
    tech: dict,
) -> list[SummaryCard]:
    cards: list[SummaryCard] = []

    # Valuation card
    val_section = next((s for s in sections if s.key == "valuation"), None)
    if val_section and val_section.items:
        statuses = [i.status for i in val_section.items]
        if "warning" in statuses:
            cards.append(SummaryCard(title="밸류에이션", value="높음", tone="warning",
                                     description="이익 또는 매출 대비 가격 부담이 있는 편입니다."))
        elif "good" in statuses:
            cards.append(SummaryCard(title="밸류에이션", value="낮음", tone="positive",
                                     description="상대적으로 저렴한 구간으로 볼 수 있습니다."))
        else:
            cards.append(SummaryCard(title="밸류에이션", value="보통", tone="neutral",
                                     description="적정 수준의 밸류에이션으로 보입니다."))

    # Profitability card
    profit_section = next((s for s in sections if s.key == "profitability"), None)
    if profit_section and profit_section.items:
        good_count = sum(1 for i in profit_section.items if i.status == "good")
        if good_count >= 2:
            cards.append(SummaryCard(title="수익성", value="좋음", tone="positive",
                                     description="ROE와 이익률이 양호합니다."))
        elif good_count == 0:
            cards.append(SummaryCard(title="수익성", value="낮음", tone="negative",
                                     description="수익성 지표가 다소 부진한 편입니다."))
        else:
            cards.append(SummaryCard(title="수익성", value="보통", tone="neutral",
                                     description="수익성이 평균 수준입니다."))

    # Momentum card
    rsi = tech.get("rsi14")
    if rsi is not None:
        if rsi >= 70:
            cards.append(SummaryCard(title="단기 흐름", value="과열", tone="warning",
                                     description="RSI 기준 단기 과열 구간에 진입했습니다."))
        elif rsi <= 30:
            cards.append(SummaryCard(title="단기 흐름", value="침체", tone="negative",
                                     description="RSI 기준 단기 침체 구간입니다."))
        else:
            cards.append(SummaryCard(title="단기 흐름", value="중립", tone="neutral",
                                     description="RSI 기준 과열이나 침체 구간이 아닙니다."))

    # Overall score card
    if score >= 70:
        tone = "positive"
        label = "양호"
    elif score >= 40:
        tone = "neutral"
        label = "보통"
    else:
        tone = "negative"
        label = "주의"
    cards.append(SummaryCard(
        title="종합 점수",
        value=f"{score:.0f}점",
        tone=tone,
        description=f"지표 기반 종합 평가 {label}. 투자 판단의 참고 자료로만 활용하세요.",
    ))

    return cards


def build_toss_response(
    ticker: str,
    name: str,
    price: float,
    info: dict,
    tech: dict,
    fundamentals: dict,
) -> TossStyleResponse:
    sections = build_toss_style_sections(info, tech, fundamentals)
    score = calculate_overall_score(sections)
    cards = build_summary_cards(sections, score, fundamentals, tech)
    return TossStyleResponse(
        ticker=ticker,
        name=name,
        price=price,
        score=score,
        sections=sections,
        summary_cards=cards,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
