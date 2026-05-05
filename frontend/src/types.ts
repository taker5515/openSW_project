 export type Signal = "BUY" | "SELL" | "NEUTRAL";

export interface NewsItem {
  id: string;
  ticker: string;
  title: string;
  source: string;
  time: string;
  summary: string;
  signal: Signal;
  loading?: boolean;
}

export interface WatchItem {
  ticker: string;
  name: string;
  price: number;
  change: number;
  changePct: number;
  history: number[];
}

export interface ChartPoint {
  time: string;
  price: number;
}
