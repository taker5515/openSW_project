from typing import List, Optional, Dict

# theme 기준: 프론트엔드 Header.jsx의 테마 URL 슬러그와 일치
# signal -> sentiment/level 매핑:
#   BUY (강)   -> good, level 1
#   BUY (보통) -> good, level 2
#   NEUTRAL    -> good/bad, level 3-4
#   SELL (보통)-> bad, level 2
#   SELL (강)  -> bad, level 1

_MOCK_NEWS: List[Dict] = [
    # ── 기술/미디어 (tech&media) ──────────────────────────────────
    {
        "id": "1",
        "ticker": "NVDA",
        "theme": "tech&media",
        "title": "NVIDIA, AI 칩 수요 급증으로 시가총액 2조 달러 돌파",
        "source": "Reuters",
        "time": "2분 전",
        "publishedAt": "2026-05-29T01:48:00",
        "url": "https://www.reuters.com/technology/nvidia",
        "summary": "데이터센터 매출이 예상 대비 18% 초과 달성. H100 GPU 백로그는 2025년 3분기까지 연장.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "4",
        "ticker": "MSFT",
        "theme": "tech&media",
        "title": "MS Azure AI 매출 YoY 31% 성장 가속",
        "source": "CNBC",
        "time": "1시간 전",
        "publishedAt": "2026-05-29T00:50:00",
        "url": "https://www.cnbc.com/microsoft-azure",
        "summary": "Copilot 엔터프라이즈 시트 400만 돌파, 전분기 180만 대비 급증.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "5",
        "ticker": "NVDA",
        "theme": "tech&media",
        "title": "NVIDIA Blackwell GPU 양산 가속, 공급망 안정화 신호",
        "source": "Reuters",
        "time": "2시간 전",
        "publishedAt": "2026-05-28T23:50:00",
        "url": "https://www.reuters.com/technology/nvidia-blackwell",
        "summary": "TSMC와의 CoWoS 패키징 계약 확대로 Blackwell 공급 병목 해소 전망. 2025년 매출 가이던스 상향 기대.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 2,
    },
    {
        "id": "3",
        "ticker": "AAPL",
        "theme": "tech&media",
        "title": "애플, 기업향 Vision Pro 로드맵 공개",
        "source": "WSJ",
        "time": "31분 전",
        "publishedAt": "2026-05-29T01:19:00",
        "url": "https://www.wsj.com/apple-vision-pro",
        "summary": "포춘 500 기업 47곳이 파일럿 진행 중. 서비스 매출 확대가 장기 촉매.",
        "signal": "NEUTRAL",
        "sentiment": "good",
        "level": 3,
    },
    {
        "id": "6",
        "ticker": "AAPL",
        "theme": "tech&media",
        "title": "애플 인도 생산 비중 2025년 25%로 확대 예정",
        "source": "FT",
        "time": "3시간 전",
        "publishedAt": "2026-05-28T22:50:00",
        "url": "https://www.ft.com/apple-india",
        "summary": "중국 리스크 헤지 전략의 일환으로 인도 공장 투자 확대. 관세 불확실성 대응 구조 강화.",
        "signal": "NEUTRAL",
        "sentiment": "good",
        "level": 3,
    },
    {
        "id": "7",
        "ticker": "MSFT",
        "theme": "tech&media",
        "title": "마이크로소프트, OpenAI 외 Mistral·Cohere 투자 다각화",
        "source": "Bloomberg",
        "time": "4시간 전",
        "publishedAt": "2026-05-28T21:50:00",
        "url": "https://www.bloomberg.com/microsoft-ai",
        "summary": "AI 공급망 단일 의존 리스크 분산 전략. Azure 플랫폼 중립성 강화로 기업 고객 유치 기대.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 2,
    },

    # ── 소비/생활 (consumer&life) ──────────────────────────────────
    {
        "id": "2",
        "ticker": "TSLA",
        "theme": "consumer&life",
        "title": "테슬라 1분기 인도량 예상 크게 하회",
        "source": "Bloomberg",
        "time": "14분 전",
        "publishedAt": "2026-05-29T01:36:00",
        "url": "https://www.bloomberg.com/tesla-deliveries",
        "summary": "1분기 인도량 386,810대로 컨센서스 449,080대 대비 크게 미달. 중국 가격 인하가 주요 역풍.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 1,
    },
    {
        "id": "8",
        "ticker": "TSLA",
        "theme": "consumer&life",
        "title": "테슬라 FSD v13, 완전 자율주행 규제 승인 재도전",
        "source": "WSJ",
        "time": "5시간 전",
        "publishedAt": "2026-05-28T20:50:00",
        "url": "https://www.wsj.com/tesla-fsd",
        "summary": "NHTSA 재검토 요청 제출. 긍정적 결과 시 로보택시 서비스 2025년 하반기 출시 가능.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 2,
    },
    {
        "id": "9",
        "ticker": "AMZN",
        "theme": "consumer&life",
        "title": "아마존, 프라임 구독자 3억 명 돌파 기록",
        "source": "Reuters",
        "time": "6시간 전",
        "publishedAt": "2026-05-28T19:50:00",
        "url": "https://www.reuters.com/amazon-prime",
        "summary": "글로벌 프라임 구독자 3억 명 달성. 광고·물류 수익 다각화 전략이 성과 견인.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "10",
        "ticker": "NKE",
        "theme": "consumer&life",
        "title": "나이키, 중국 소비 둔화로 연간 가이던스 하향",
        "source": "Bloomberg",
        "time": "7시간 전",
        "publishedAt": "2026-05-28T18:50:00",
        "url": "https://www.bloomberg.com/nike-china",
        "summary": "중국 리테일 매출 전년比 12% 감소. 재고 적체 해소에 최소 2분기 소요 전망.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 2,
    },

    # ── 산업/에너지/부동산 (industry&energy&realEstate) ───────────
    {
        "id": "11",
        "ticker": "XOM",
        "theme": "industry&energy&realEstate",
        "title": "엑슨모빌, 퍼미안 분지 생산량 신기록 경신",
        "source": "Reuters",
        "time": "1시간 전",
        "publishedAt": "2026-05-29T00:50:00",
        "url": "https://www.reuters.com/exxon-permian",
        "summary": "2분기 퍼미안 일산 130만 배럴 돌파. 저비용 구조 유지로 유가 하락 방어력 높음.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "12",
        "ticker": "BA",
        "theme": "industry&energy&realEstate",
        "title": "보잉 787 생산 결함 재발, 납품 지연 불가피",
        "source": "WSJ",
        "time": "2시간 전",
        "publishedAt": "2026-05-28T23:50:00",
        "url": "https://www.wsj.com/boeing-787",
        "summary": "FAA 품질 감사에서 복합재 접합 공정 이상 적발. 연간 납품 목표 달성에 빨간불.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 1,
    },
    {
        "id": "13",
        "ticker": "CAT",
        "theme": "industry&energy&realEstate",
        "title": "캐터필러, 인프라 투자 수혜로 북미 수주 급증",
        "source": "CNBC",
        "time": "3시간 전",
        "publishedAt": "2026-05-28T22:50:00",
        "url": "https://www.cnbc.com/caterpillar",
        "summary": "미국 인프라법 집행 본격화로 굴착기·건설장비 수주 40% 증가. 공급망 정상화 효과도 반영.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 2,
    },
    {
        "id": "14",
        "ticker": "PLD",
        "theme": "industry&energy&realEstate",
        "title": "프롤로지스, 이커머스 물류창고 공실률 급등 경고",
        "source": "FT",
        "time": "4시간 전",
        "publishedAt": "2026-05-28T21:50:00",
        "url": "https://www.ft.com/prologis",
        "summary": "미국 e-커머스 성장 둔화로 물류 리츠 공실률 5년 만에 최고치. 임대료 하락 압력 증가.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 2,
    },

    # ── 금융 (finance) ────────────────────────────────────────────
    {
        "id": "15",
        "ticker": "JPM",
        "theme": "finance",
        "title": "JP모건, 1분기 순이익 사상 최대…IB 부문 부활",
        "source": "Bloomberg",
        "time": "30분 전",
        "publishedAt": "2026-05-29T01:20:00",
        "url": "https://www.bloomberg.com/jpmorgan-q1",
        "summary": "순이익 138억 달러로 전년比 6% 증가. IPO·M&A 시장 회복으로 투자은행 수수료 급등.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "16",
        "ticker": "GS",
        "theme": "finance",
        "title": "골드만삭스, 소비자 금융 사업 완전 철수 결정",
        "source": "Reuters",
        "time": "2시간 전",
        "publishedAt": "2026-05-28T23:50:00",
        "url": "https://www.reuters.com/goldman-sachs",
        "summary": "Marcus 플랫폼 종료 및 GM카드 매각 확정. 핵심 기관 사업 집중 전략으로 회귀.",
        "signal": "NEUTRAL",
        "sentiment": "good",
        "level": 3,
    },
    {
        "id": "17",
        "ticker": "BAC",
        "theme": "finance",
        "title": "뱅크오브아메리카, 고금리 지속에 NIM 하락 우려",
        "source": "CNBC",
        "time": "3시간 전",
        "publishedAt": "2026-05-28T22:50:00",
        "url": "https://www.cnbc.com/bank-of-america",
        "summary": "연준 금리 인하 지연으로 예금 비용 상승. 순이자마진(NIM) 2분기 추가 압박 예상.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 2,
    },

    # ── 헬스케어/공공 (HC&pub) ────────────────────────────────────
    {
        "id": "18",
        "ticker": "JNJ",
        "theme": "HC&pub",
        "title": "존슨앤드존슨, 암 치료제 임상 3상 성공 발표",
        "source": "Reuters",
        "time": "45분 전",
        "publishedAt": "2026-05-29T01:05:00",
        "url": "https://www.reuters.com/jnj-cancer",
        "summary": "폐암 표적치료제 임상 3상에서 무진행 생존 기간 8개월 연장 확인. FDA 패스트트랙 지정 기대.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 1,
    },
    {
        "id": "19",
        "ticker": "PFE",
        "theme": "HC&pub",
        "title": "화이자, 코로나 백신 매출 급감으로 연간 가이던스 대폭 하향",
        "source": "Bloomberg",
        "time": "2시간 전",
        "publishedAt": "2026-05-28T23:50:00",
        "url": "https://www.bloomberg.com/pfizer",
        "summary": "mRNA 백신 수요 정상화로 관련 매출 70% 급감 예상. 파이프라인 다각화 속도가 관건.",
        "signal": "SELL",
        "sentiment": "bad",
        "level": 1,
    },
    {
        "id": "20",
        "ticker": "UNH",
        "theme": "HC&pub",
        "title": "유나이티드헬스, 메디케어 부문 보험료 인상 승인",
        "source": "WSJ",
        "time": "4시간 전",
        "publishedAt": "2026-05-28T21:50:00",
        "url": "https://www.wsj.com/unitedhealth",
        "summary": "CMS의 메디케어 어드밴티지 보험료 4.7% 인상 최종 승인. 수익성 회복 청신호.",
        "signal": "BUY",
        "sentiment": "good",
        "level": 2,
    },
]

# ticker -> theme 역매핑 (ticker 필터 편의용)
_TICKER_THEME: Dict[str, str] = {n["ticker"]: n["theme"] for n in _MOCK_NEWS}


class NewsRepository:
    def __init__(self) -> None:
        self._news: List[Dict] = list(_MOCK_NEWS)

    def get_all(
        self,
        ticker: Optional[str] = None,
        theme: Optional[str] = None,
    ) -> List[Dict]:
        result = self._news
        if ticker:
            result = [n for n in result if n["ticker"] == ticker.upper()]
        if theme:
            result = [n for n in result if n.get("theme") == theme]
        return list(result)

    def get_by_id(self, news_id: str) -> Optional[Dict]:
        for n in self._news:
            if n["id"] == news_id:
                return n
        return None


news_repository = NewsRepository()
