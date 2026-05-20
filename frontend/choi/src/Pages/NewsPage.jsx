import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { ThumbsUp, ThumbsDown, ExternalLink, RefreshCw } from "lucide-react";

const allNews = {
  1: { id: 1, title: "NVIDIA, AI 칩 수요 급증으로 시가총액 2조 달러 돌파", source: "Reuters", time: "2분 전", ticker: "NVDA", signal: "매수", url: "https://reuters.com" },
  2: { id: 2, title: "OpenAI, GPT-5 출시 임박...AI 시장 판도 변화 예고", source: "Bloomberg", time: "15분 전", ticker: "MSFT", signal: "매수", url: "https://bloomberg.com" },
  3: { id: 3, title: "구글 딥마인드, 신약 개발 AI 모델 공개", source: "TechCrunch", time: "1시간 전", ticker: "GOOGL", signal: "중립", url: "https://techcrunch.com" },
  4: { id: 4, title: "삼성전자, HBM4 양산 성공...SK하이닉스와 격차 줄여", source: "한국경제", time: "5분 전", ticker: "005930", signal: "매수", url: "https://hankyung.com" },
  5: { id: 5, title: "TSMC, 2nm 공정 수율 개선...애플 독점 공급 유력", source: "DigiTimes", time: "30분 전", ticker: "TSM", signal: "매수", url: "https://digitimes.com" },
  6: { id: 6, title: "인텔, 파운드리 사업 분사 공식화", source: "WSJ", time: "2시간 전", ticker: "INTC", signal: "중립", url: "https://wsj.com" },
  7: { id: 7, title: "테슬라, 중국 시장 점유율 회복...BYD와 치열한 경쟁", source: "Reuters", time: "10분 전", ticker: "TSLA", signal: "중립", url: "https://reuters.com" },
  8: { id: 8, title: "현대차, 美 전기차 보조금 혜택 확대 수혜", source: "연합뉴스", time: "45분 전", ticker: "005380", signal: "매수", url: "https://yna.co.kr" },
  9: { id: 9, title: "BYD, 유럽 시장 공략 가속...관세 장벽 우회 전략", source: "FT", time: "3시간 전", ticker: "BYDDY", signal: "중립", url: "https://ft.com" },
  10: { id: 10, title: "삼성바이오로직스, 글로벌 CMO 수주 역대 최대", source: "바이오스펙테이터", time: "20분 전", ticker: "207940", signal: "매수", url: "https://biospectator.com" },
  11: { id: 11, title: "셀트리온, 자가면역 치료제 FDA 승인 획득", source: "메디파나", time: "2시간 전", ticker: "068270", signal: "매수", url: "https://medipana.com" },
  12: { id: 12, title: "한미약품, 비만치료제 임상 3상 진입", source: "팜뉴스", time: "4시간 전", ticker: "128940", signal: "중립", url: "https://pharmnews.com" },
  13: { id: 13, title: "Fed, 금리 동결 유지...연내 인하 가능성 시사", source: "WSJ", time: "1시간 전", ticker: "JPM", signal: "중립", url: "https://wsj.com" },
  14: { id: 14, title: "카카오뱅크, 기업대출 확대로 순이익 급증", source: "이데일리", time: "3시간 전", ticker: "323410", signal: "매수", url: "https://edaily.co.kr" },
  15: { id: 15, title: "토스, 기업공개 본격화...기업가치 20조 목표", source: "한국경제", time: "5시간 전", ticker: "TOSS", signal: "매수", url: "https://hankyung.com" },
};

const signalColor = { 매수: "#22c55e", 매도: "#ef4444", 중립: "#f59e0b" };

export default function NewsPage() {
  const { newsId } = useParams();
  const item = allNews[newsId];
  const [feedback, setFeedback] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchAnalysis = async () => {
    if (!item) return;
    setLoading(true);
    setAnalysis("");
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{
            role: "user",
            content: `다음 주식 뉴스를 투자자 관점에서 상세히 분석해줘. 
뉴스 제목: "${item.title}"
티커: ${item.ticker}
출처: ${item.source}

다음 항목으로 분석해줘:
1. 핵심 요약 (2-3문장)
2. 주가 영향 분석 (긍정/부정 요인)
3. 단기/중기 전망
4. 투자자 주의사항

한국어로 간결하게 작성해줘.`
          }]
        })
      });
      const data = await response.json();
      const text = data.content?.map(c => c.text).join("") ?? "분석 실패";
      setAnalysis(text);
    } catch (e) {
      setAnalysis("분석 중 오류가 발생했습니다.");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAnalysis();
  }, [newsId]);

  if (!item) return <div style={{ padding: 40, color: "#e2e8f0" }}>뉴스를 찾을 수 없습니다.</div>;

  return (
    <div style={{ minHeight: "100vh", background: "#060810", color: "#e2e8f0",
      fontFamily: "'Inter', 'Segoe UI', sans-serif", padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 700, marginBottom: 24 }}>뉴스 분석</h1>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>

        {/* 왼쪽: AI 뉴스 분석 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

          {/* 뉴스 헤더 */}
          <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
              <span style={{ fontSize: 11, fontWeight: 700, color: "#60a5fa", background: "#0d1f3c",
                border: "1px solid #1e3a5f", borderRadius: 4, padding: "2px 7px" }}>{item.ticker}</span>
              <span style={{ fontSize: 11, color: "#4b5563" }}>{item.source} · {item.time}</span>
              <span style={{ marginLeft: "auto", fontSize: 12, fontWeight: 700,
                color: signalColor[item.signal], border: `1px solid ${signalColor[item.signal]}`,
                borderRadius: 6, padding: "2px 10px" }}>{item.signal}</span>
            </div>
            <p style={{ fontSize: 15, fontWeight: 600, color: "#e2e8f0", marginBottom: 12 }}>{item.title}</p>
            <a href={item.url} target="_blank" rel="noopener noreferrer"
              style={{ display: "inline-flex", alignItems: "center", gap: 6,
                color: "#60a5fa", fontSize: 12, textDecoration: "none" }}>
              <ExternalLink size={12} /> 뉴스 원문 보기
            </a>
          </div>

          {/* AI 상세 분석 */}
          <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <span style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8" }}>AI 상세 분석</span>
              <button onClick={fetchAnalysis} disabled={loading}
                style={{ display: "flex", alignItems: "center", gap: 5, background: "transparent",
                  border: "1px solid #1e2130", borderRadius: 6, color: "#4b6080",
                  fontSize: 12, padding: "5px 12px", cursor: "pointer", opacity: loading ? 0.5 : 1 }}>
                <RefreshCw size={11} /> 재분석
              </button>
            </div>
            {loading ? (
              <p style={{ fontSize: 13, color: "#4b6080", fontStyle: "italic" }}>Claude AI 분석 중...</p>
            ) : (
              <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.8, margin: 0, whiteSpace: "pre-wrap" }}>
                {analysis}
              </p>
            )}
          </div>
        </div>

        {/* 오른쪽: 재무재표 + feedback */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>재무재표 요약</h2>
            <p style={{ fontSize: 13, color: "#4b5563" }}>준비 중입니다.</p>
          </div>

          <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>재무재표 원문</h2>
            <a href="#" style={{ display: "flex", alignItems: "center", gap: 6,
              color: "#60a5fa", fontSize: 13, textDecoration: "none" }}>
              <ExternalLink size={13} /> 원문 보기
            </a>
          </div>

          <div style={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 12, padding: "16px 18px" }}>
            <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", marginBottom: 12 }}>이 분석이 도움이 됐나요?</h2>
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