import { useState } from "react";
import { ThumbsUp, ThumbsDown, ExternalLink } from "lucide-react";
import { NewsSummary } from "./Dashboard/components/NewsSummary";
import { useNewsFeed } from "./Dashboard/hooks/useNewsFeed";

export default function NewsPage() {
  const { news, reanalyze } = useNewsFeed();
  const [feedback, setFeedback] = useState(null); // 'like' | 'dislike' | null

  return (
    <div style={{ minHeight: "100vh", background: "#060810", color: "#e2e8f0",
      fontFamily: "'Inter', 'Segoe UI', sans-serif", padding: 24 }}>

      {/* 상단 제목 */}
      <h1 style={{ fontSize: 20, fontWeight: 700, marginBottom: 24, color: "#e2e8f0" }}>
        뉴스 분석
      </h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>

        {/* 왼쪽: AI 뉴스 요약 */}
        <div>
          <NewsSummary news={news} onReanalyze={reanalyze} />
        </div>

        {/* 오른쪽: 재무재표 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ background: "#0f1117", border: "1px solid #1e2130",
            borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>
              재무재표 요약
            </h2>
            <p style={{ fontSize: 13, color: "#4b5563" }}>준비 중입니다.</p>
          </div>

          <div style={{ background: "#0f1117", border: "1px solid #1e2130",
            borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>
              재무재표 원문
            </h2>
            <a href="#" style={{ display: "flex", alignItems: "center", gap: 6,
              color: "#60a5fa", fontSize: 13, textDecoration: "none" }}>
              <ExternalLink size={13} /> 원문 보기
            </a>
          </div>

          {/* Human Feedback */}
          <div style={{ background: "#0f1117", border: "1px solid #1e2130",
            borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>
              이 분석이 도움이 됐나요?
            </h2>
            <div style={{ display: "flex", gap: 12 }}>
              <button onClick={() => setFeedback("like")}
                style={{ display: "flex", alignItems: "center", gap: 6,
                  background: feedback === "like" ? "#0d2a1f" : "transparent",
                  border: `1px solid ${feedback === "like" ? "#22c55e" : "#1e2130"}`,
                  borderRadius: 8, padding: "8px 16px", cursor: "pointer",
                  color: feedback === "like" ? "#22c55e" : "#4b5563", fontSize: 13 }}>
                <ThumbsUp size={14} /> 도움됐어요
              </button>
              <button onClick={() => setFeedback("dislike")}
                style={{ display: "flex", alignItems: "center", gap: 6,
                  background: feedback === "dislike" ? "#2a0d0d" : "transparent",
                  border: `1px solid ${feedback === "dislike" ? "#ef4444" : "#1e2130"}`,
                  borderRadius: 8, padding: "8px 16px", cursor: "pointer",
                  color: feedback === "dislike" ? "#ef4444" : "#4b5563", fontSize: 13 }}>
                <ThumbsDown size={14} /> 별로예요
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}