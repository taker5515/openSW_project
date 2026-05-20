import { Link } from "react-router-dom";
import Header from "../Components/Header";

const themeNews = {
  AI: [
    { id: 1, title: "NVIDIA, AI 칩 수요 급증으로 시가총액 2조 달러 돌파", source: "Reuters", time: "2분 전", ticker: "NVDA" },
    { id: 2, title: "OpenAI, GPT-5 출시 임박...AI 시장 판도 변화 예고", source: "Bloomberg", time: "15분 전", ticker: "MSFT" },
    { id: 3, title: "구글 딥마인드, 신약 개발 AI 모델 공개", source: "TechCrunch", time: "1시간 전", ticker: "GOOGL" },
  ],
  반도체: [
    { id: 4, title: "삼성전자, HBM4 양산 성공...SK하이닉스와 격차 줄여", source: "한국경제", time: "5분 전", ticker: "005930" },
    { id: 5, title: "TSMC, 2nm 공정 수율 개선...애플 독점 공급 유력", source: "DigiTimes", time: "30분 전", ticker: "TSM" },
    { id: 6, title: "인텔, 파운드리 사업 분사 공식화", source: "WSJ", time: "2시간 전", ticker: "INTC" },
  ],
  전기차: [
    { id: 7, title: "테슬라, 중국 시장 점유율 회복...BYD와 치열한 경쟁", source: "Reuters", time: "10분 전", ticker: "TSLA" },
    { id: 8, title: "현대차, 美 전기차 보조금 혜택 확대 수혜", source: "연합뉴스", time: "45분 전", ticker: "005380" },
    { id: 9, title: "BYD, 유럽 시장 공략 가속...관세 장벽 우회 전략", source: "FT", time: "3시간 전", ticker: "BYDDY" },
  ],
  바이오: [
    { id: 10, title: "삼성바이오로직스, 글로벌 CMO 수주 역대 최대", source: "바이오스펙테이터", time: "20분 전", ticker: "207940" },
    { id: 11, title: "셀트리온, 자가면역 치료제 FDA 승인 획득", source: "메디파나", time: "2시간 전", ticker: "068270" },
    { id: 12, title: "한미약품, 비만치료제 임상 3상 진입", source: "팜뉴스", time: "4시간 전", ticker: "128940" },
  ],
  금융: [
    { id: 13, title: "Fed, 금리 동결 유지...연내 인하 가능성 시사", source: "WSJ", time: "1시간 전", ticker: "JPM" },
    { id: 14, title: "카카오뱅크, 기업대출 확대로 순이익 급증", source: "이데일리", time: "3시간 전", ticker: "323410" },
    { id: 15, title: "토스, 기업공개 본격화...기업가치 20조 목표", source: "한국경제", time: "5시간 전", ticker: "TOSS" },
  ],
};

const themes = ["AI", "반도체", "전기차", "바이오", "금융"];

export default function ThemePage() {
  return (
    <div style={{ minHeight: "100vh", background: "#f8fafc", fontFamily: "'Inter', 'Segoe UI', sans-serif" }}>
      <Header />
      <main style={{ maxWidth: 1200, margin: "0 auto", padding: "40px 24px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 16 }}>
          {themes.map((theme) => (
            <div key={theme}>
              {/* 테마 제목 */}
              <h2 style={{ fontSize: 15, fontWeight: 700, color: "#0f172a",
                marginBottom: 12, paddingBottom: 8, borderBottom: "2px solid #3b82f6" }}>
                {theme}
              </h2>
              {/* 뉴스 카드 목록 */}
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {themeNews[theme].map((item) => (
                  <Link to={`/news/${item.id}`} key={item.id}
                    style={{ background: "#fff", border: "1px solid #e2e8f0",
                      borderRadius: 10, padding: "12px 14px", textDecoration: "none",
                      color: "inherit", display: "block" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
                      <span style={{ fontSize: 10, fontWeight: 700, color: "#3b82f6",
                        background: "#eff6ff", borderRadius: 4, padding: "2px 6px" }}>
                        {item.ticker}
                      </span>
                      <span style={{ fontSize: 10, color: "#94a3b8" }}>{item.source} · {item.time}</span>
                    </div>
                    <p style={{ fontSize: 13, fontWeight: 600, color: "#0f172a", margin: 0, lineHeight: 1.5 }}>
                      {item.title}
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}