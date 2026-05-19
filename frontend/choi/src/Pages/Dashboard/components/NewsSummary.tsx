 import { RefreshCw } from "lucide-react";
import { SignalBadge } from "./SignalBadge";
import type { NewsItem } from "../types";

function NewsCard({ item, onReanalyze }: { item: NewsItem; onReanalyze: (id: string) => void }) {
  return (
    <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#60a5fa", background: "#0d1f3c",
          border: "1px solid #1e3a5f", borderRadius: 4, padding: "2px 7px" }}>
          {item.ticker}
        </span>
        <span style={{ fontSize: 11, color: "#4b5563" }}>{item.source} · {item.time}</span>
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, marginBottom: 10 }}>
        <p style={{ fontSize: 14, fontWeight: 600, color: "#e2e8f0", lineHeight: 1.5, margin: 0 }}>
          {item.title}
        </p>
        <SignalBadge signal={item.signal} />
      </div>
      <div style={{ background: "#080a10", borderRadius: 8, padding: "10px 14px",
        borderLeft: "2px solid #1e3a5f", marginBottom: 10 }}>
        <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6, margin: 0 }}>
          {item.loading
            ? <em style={{ color: "#4b6080" }}>Claude AI 분석 중...</em>
            : item.summary}
        </p>
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        <button onClick={() => onReanalyze(item.id)} disabled={item.loading}
          style={{ display: "flex", alignItems: "center", gap: 5, background: "transparent",
            border: "1px solid #1e2130", borderRadius: 6, color: "#4b6080",
            fontSize: 12, padding: "5px 12px", cursor: "pointer", opacity: item.loading ? 0.5 : 1 }}>
          <RefreshCw size={11} /> AI 재분석
        </button>
      </div>
    </div>
  );
}

export function NewsSummary({ news, onReanalyze }: {
  news: NewsItem[];
  onReanalyze: (id: string) => void;
}) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8" }}>AI 뉴스 분석 피드</span>
        <span style={{ fontSize: 11, color: "#374151" }}>Claude Sonnet 분석</span>
      </div>
      {news.map((item) => (
        <NewsCard key={item.id} item={item} onReanalyze={onReanalyze} />
      ))}
    </div>
  );
}