from typing import List, Optional, Dict


_MOCK_NEWS: List[Dict] = [
    {
        "id": "1",
        "ticker": "NVDA",
        "title": "NVIDIA, AI 칩 수요 급증으로 시가총액 2조 달러 돌파",
        "source": "Reuters",
        "time": "2분 전",
        "summary": "데이터센터 매출이 예상 대비 18% 초과 달성. H100 GPU 백로그는 2025년 3분기까지 연장.",
        "signal": "BUY",
    },
    {
        "id": "2",
        "ticker": "TSLA",
        "title": "테슬라 1분기 인도량 예상 크게 하회",
        "source": "Bloomberg",
        "time": "14분 전",
        "summary": "1분기 인도량 386,810대로 컨센서스 449,080대 대비 크게 미달. 중국 가격 인하가 주요 역풍.",
        "signal": "SELL",
    },
    {
        "id": "3",
        "ticker": "AAPL",
        "title": "애플, 기업향 Vision Pro 로드맵 공개",
        "source": "WSJ",
        "time": "31분 전",
        "summary": "포춘 500 기업 47곳이 파일럿 진행 중. 서비스 매출 확대가 장기 촉매.",
        "signal": "NEUTRAL",
    },
    {
        "id": "4",
        "ticker": "MSFT",
        "title": "MS Azure AI 매출 YoY 31% 성장 가속",
        "source": "CNBC",
        "time": "1시간 전",
        "summary": "Copilot 엔터프라이즈 시트 400만 돌파, 전분기 180만 대비 급증.",
        "signal": "BUY",
    },
    {
        "id": "5",
        "ticker": "NVDA",
        "title": "NVIDIA Blackwell GPU 양산 가속, 공급망 안정화 신호",
        "source": "Reuters",
        "time": "2시간 전",
        "summary": "TSMC와의 CoWoS 패키징 계약 확대로 Blackwell 공급 병목 해소 전망. 2025년 매출 가이던스 상향 기대.",
        "signal": "BUY",
    },
    {
        "id": "6",
        "ticker": "AAPL",
        "title": "애플 인도 생산 비중 2025년 25%로 확대 예정",
        "source": "FT",
        "time": "3시간 전",
        "summary": "중국 리스크 헤지 전략의 일환으로 인도 공장 투자 확대. 관세 불확실성 대응 구조 강화.",
        "signal": "NEUTRAL",
    },
    {
        "id": "7",
        "ticker": "MSFT",
        "title": "마이크로소프트, OpenAI 외 Mistral·Cohere 투자 다각화",
        "source": "Bloomberg",
        "time": "4시간 전",
        "summary": "AI 공급망 단일 의존 리스크 분산 전략. Azure 플랫폼 중립성 강화로 기업 고객 유치 기대.",
        "signal": "BUY",
    },
    {
        "id": "8",
        "ticker": "TSLA",
        "title": "테슬라 FSD v13, 완전 자율주행 규제 승인 재도전",
        "source": "WSJ",
        "time": "5시간 전",
        "summary": "NHTSA 재검토 요청 제출. 긍정적 결과 시 로보택시 서비스 2025년 하반기 출시 가능.",
        "signal": "BUY",
    },
]


class NewsRepository:
    def __init__(self) -> None:
        self._news: List[Dict] = list(_MOCK_NEWS)

    def get_all(self, ticker: Optional[str] = None) -> List[Dict]:
        if ticker:
            return [n for n in self._news if n["ticker"] == ticker.upper()]
        return list(self._news)

    def get_by_id(self, news_id: str) -> Optional[Dict]:
        for n in self._news:
            if n["id"] == news_id:
                return n
        return None


news_repository = NewsRepository()
