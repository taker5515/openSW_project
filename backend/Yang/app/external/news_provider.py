import uuid
from datetime import datetime, timedelta, timezone

_NEWS_BANK = [
    # AI/빅테크
    {"ticker": "NVDA", "theme_key": "ai", "title": "NVIDIA, AI 칩 수요 급증으로 분기 매출 역대 최고", "source": "Reuters", "summary": "NVIDIA의 AI 반도체 수요가 폭발적으로 증가하며 분기 매출이 시장 예상치를 크게 상회했습니다. 데이터센터 부문이 전체 매출의 80%를 차지하며 성장을 이끌고 있습니다.", "signal": "BUY"},
    {"ticker": "MSFT", "theme_key": "ai", "title": "Microsoft, Azure AI 서비스 기업 고객 2만 곳 돌파", "source": "Bloomberg", "summary": "마이크로소프트의 Azure AI 플랫폼을 이용하는 기업 고객 수가 2만 곳을 넘어섰습니다. OpenAI와의 파트너십이 기업 시장 점유율 확대에 결정적 역할을 하고 있다는 분석입니다.", "signal": "BUY"},
    {"ticker": "GOOGL", "theme_key": "ai", "title": "Google Gemini 2.0, 기업용 시장 공략 본격화", "source": "TechCrunch", "summary": "구글이 Gemini 2.0 모델을 기반으로 한 기업용 AI 솔루션 출시를 발표했습니다. 광고 수익 의존도를 낮추고 클라우드 AI 부문에서 Microsoft와의 경쟁을 심화할 전망입니다.", "signal": "NEUTRAL"},
    {"ticker": "META", "theme_key": "ai", "title": "Meta, Llama 오픈소스 모델 기업 채택 확산", "source": "WSJ", "summary": "메타의 오픈소스 AI 모델 Llama가 기업들 사이에서 빠르게 채택되고 있습니다. 무료 제공 전략이 장기적으로 AI 생태계 내 영향력 강화로 이어질 수 있다는 평가입니다.", "signal": "NEUTRAL"},
    # 반도체
    {"ticker": "AMD", "theme_key": "semiconductor", "title": "AMD MI300X, AI 훈련 시장서 NVIDIA 추격 가속", "source": "Barron's", "summary": "AMD의 MI300X GPU가 AI 모델 훈련 벤치마크에서 경쟁력을 입증하며 점유율을 높이고 있습니다. 다만 NVIDIA의 소프트웨어 생태계 우위를 단기간에 따라잡기는 어렵다는 분석도 있습니다.", "signal": "BUY"},
    {"ticker": "TSM", "theme_key": "semiconductor", "title": "TSMC, 2나노 공정 양산 일정 순조롭게 진행", "source": "DigiTimes", "summary": "TSMC가 2나노 반도체 공정 양산 일정이 예정대로 진행되고 있다고 밝혔습니다. Apple과 NVIDIA의 차세대 칩 생산 수주를 이미 확보한 것으로 알려졌습니다.", "signal": "BUY"},
    {"ticker": "INTC", "theme_key": "semiconductor", "title": "Intel, 파운드리 사업 분리 검토…구조조정 가속", "source": "FT", "summary": "인텔이 파운드리 사업부 분리를 포함한 구조조정 방안을 검토 중인 것으로 알려졌습니다. 시장 회복 속도가 기대보다 느려 투자자들의 우려가 지속되고 있습니다.", "signal": "SELL"},
    {"ticker": "AVGO", "theme_key": "semiconductor", "title": "Broadcom, 커스텀 AI ASIC 수요로 매출 성장 지속", "source": "Reuters", "summary": "브로드컴의 커스텀 AI 칩(ASIC) 수요가 구글, 메타 등 대형 테크 기업을 중심으로 강세를 보이고 있습니다. 네트워킹 반도체 부문도 AI 인프라 투자 확대로 수혜를 받고 있습니다.", "signal": "BUY"},
    # 전기차
    {"ticker": "TSLA", "theme_key": "ev", "title": "Tesla, 사이버트럭 생산 목표치 하회…주가 약세", "source": "Reuters", "summary": "테슬라의 사이버트럭 분기 생산량이 목표치를 밑돌며 주가가 약세를 보이고 있습니다. 에너지 저장 사업 성장이 이를 일부 상쇄하고 있으나 투자자 우려는 지속됩니다.", "signal": "SELL"},
    {"ticker": "RIVN", "theme_key": "ev", "title": "Rivian, Amazon 배달 밴 납품 순조…현금 소진 우려 지속", "source": "Bloomberg", "summary": "리비안이 아마존 전기 배달 밴 납품을 꾸준히 이어가고 있습니다. 다만 높은 생산 비용으로 인한 현금 소진이 지속돼 자금 조달 이슈가 중장기 과제로 남아 있습니다.", "signal": "NEUTRAL"},
    # 바이오
    {"ticker": "LLY", "theme_key": "bio", "title": "Eli Lilly, 비만 치료제 Zepbound 처방 급증", "source": "FT", "summary": "일라이릴리의 비만 치료제 Zepbound의 처방 건수가 분기 대비 40% 이상 증가했습니다. 공급 확대와 함께 보험 적용 범위가 넓어지면서 성장세가 더욱 가팔라질 전망입니다.", "signal": "BUY"},
    {"ticker": "MRNA", "theme_key": "bio", "title": "Moderna, mRNA 암 백신 임상 3상 진입", "source": "STAT News", "summary": "모더나가 개인 맞춤형 mRNA 암 백신의 임상 3상 진입을 발표했습니다. 머크(MSD)와의 공동 개발로 상업화 가능성이 높아졌다는 평가이나 상용화까지는 수년이 필요합니다.", "signal": "BUY"},
    # 금융
    {"ticker": "JPM", "theme_key": "finance", "title": "JP모건, AI 도입으로 리스크 관리 비용 20% 절감", "source": "Bloomberg", "summary": "JP모건이 AI 기반 리스크 관리 시스템 도입 이후 관련 비용을 20% 절감했다고 밝혔습니다. 금융 대형사들의 AI 투자가 실질적인 비용 효율화로 이어지는 사례가 늘고 있습니다.", "signal": "BUY"},
    {"ticker": "V", "theme_key": "finance", "title": "Visa, 크로스보더 결제 성장세 지속…여행 회복 수혜", "source": "WSJ", "summary": "비자의 국가 간 결제 거래량이 해외 여행 수요 회복에 힘입어 꾸준한 증가세를 보이고 있습니다. 핀테크와의 협력 강화도 신규 수익원 발굴에 긍정적으로 작용하고 있습니다.", "signal": "BUY"},
    {"ticker": "GS", "theme_key": "finance", "title": "골드만삭스, IPO 시장 회복 기대감에 IB 수익 개선", "source": "Reuters", "summary": "골드만삭스의 투자은행 부문이 IPO 시장 회복 기대감 속에 수익이 개선됐습니다. 금리 불확실성이 여전하지만 M&A 및 자본 시장 활동이 점진적으로 살아나고 있는 것으로 보입니다.", "signal": "NEUTRAL"},
]


def _make_id(title: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, title))


def _relative_time(offset_minutes: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(minutes=offset_minutes)
    return dt.strftime("%Y-%m-%d %H:%M")


class MockNewsProvider:
    def get_latest(self, limit: int = 20) -> list[dict]:
        items = []
        for i, n in enumerate(_NEWS_BANK[:limit]):
            items.append({
                **n,
                "id": _make_id(n["title"]),
                "time": _relative_time(i * 7 + 3),
            })
        return items

    def get_by_theme(self, theme_key: str, limit: int = 10) -> list[dict]:
        items = [n for n in _NEWS_BANK if n.get("theme_key") == theme_key]
        result = []
        for i, n in enumerate(items[:limit]):
            result.append({
                **n,
                "id": _make_id(n["title"]),
                "time": _relative_time(i * 10 + 5),
            })
        return result

    def get_by_ticker(self, ticker: str, limit: int = 10) -> list[dict]:
        items = [n for n in _NEWS_BANK if n.get("ticker", "").upper() == ticker.upper()]
        result = []
        for i, n in enumerate(items[:limit]):
            result.append({
                **n,
                "id": _make_id(n["title"]),
                "time": _relative_time(i * 15 + 2),
            })
        return result
