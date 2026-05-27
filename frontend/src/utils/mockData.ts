import type { WatchItem, NewsItem, ChartPoint } from "../types";

export const genHistory = (base: number, n = 20): number[] =>
  Array.from({ length: n }, () => {
    base = base + (Math.random() - 0.48) * base * 0.01;
    return +base.toFixed(2);
  });

export const genChartData = (base: number, n = 60): ChartPoint[] => {
  let v = base;
  return Array.from({ length: n }, (_, i) => {
    v = v + (Math.random() - 0.47) * v * 0.004 + 0.03;
    const t = new Date(Date.now() - (n - 1 - i) * 5 * 60 * 1000);
    return {
      time: `${t.getHours()}:${String(t.getMinutes()).padStart(2, "0")}`,
      price: +v.toFixed(2),
    };
  });
};

export const INITIAL_WATCHLIST: WatchItem[] = [
  { ticker: "AAPL", name: "Apple Inc.",      price: 189.30, change:  2.14, changePct:  1.14, history: genHistory(189) },
  { ticker: "NVDA", name: "NVIDIA Corp.",    price: 875.40, change: -12.30, changePct: -1.38, history: genHistory(875) },
  { ticker: "TSLA", name: "Tesla Inc.",      price: 242.80, change:  5.60, changePct:  2.36, history: genHistory(242) },
  { ticker: "MSFT", name: "Microsoft Corp.", price: 415.60, change: -1.90, changePct: -0.46, history: genHistory(415) },
];

export const INITIAL_NEWS: NewsItem[] = [
  {
    id: "1", ticker: "NVDA", source: "Reuters", time: "2분 전", signal: "BUY",
    title: "NVIDIA, AI 칩 수요 급증으로 시가총액 2조 달러 돌파",
    summary: "데이터센터 매출이 예상 대비 18% 초과 달성. H100 GPU 백로그는 2025년 3분기까지 연장.",
  },
  {
    id: "2", ticker: "TSLA", source: "Bloomberg", time: "14분 전", signal: "SELL",
    title: "테슬라 1분기 인도량 예상 크게 하회",
    summary: "1분기 인도량 386,810대로 컨센서스 449,080대 대비 크게 미달. 중국 가격 인하가 주요 역풍.",
  },
  {
    id: "3", ticker: "AAPL", source: "WSJ", time: "31분 전", signal: "NEUTRAL",
    title: "애플, 기업향 Vision Pro 로드맵 공개",
    summary: "포춘 500 기업 47곳이 파일럿 진행 중. 서비스 매출 확대가 장기 촉매.",
  },
  {
    id: "4", ticker: "MSFT", source: "CNBC", time: "1시간 전", signal: "BUY",
    title: "MS Azure AI 매출 YoY 31% 성장 가속",
    summary: "Copilot 엔터프라이즈 시트 400만 돌파, 전분기 180만 대비 급증.",
  },
];
