import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../Components/Header";
import "../PageStyles/NewsPage.css";

// 한국어 행 레이블 → API 필드 매핑
// source: "income" | "balance" | "cash" | "cash_calc"
const FINANCE_ROW_MAP = [
  { label: "총매출",              source: "income",     key: "revenue" },
  { label: "총이익",              source: "income",     key: "gross_profit" },
  { label: "영업 이익",           source: "income",     key: "operating_income" },
  { label: "순이익",              source: "income",     key: "net_income" },
  { label: "총 자산",             source: "balance",    key: "total_assets" },
  { label: "총 유동부채",         source: "balance",    key: "current_liabilities" },
  { label: "총 주식",             source: "balance",    key: "total_equity" },
  { label: "부채 상환 후 현금흐름", source: "cash",      key: "free_cash_flow" },
  { label: "영업으로 인한 현금",  source: "cash",       key: "operating_cash_flow" },
  { label: "투자로 인한 현금",    source: "cash",       key: "investing_cash_flow" },
  { label: "재무현금흐름",        source: "cash",       key: "financing_cash_flow" },
  { label: "현금순변동",          source: "cash_calc",  key: null },
];

const fmt = (v) => {
  if (v == null) return "-";
  const abs = Math.abs(v);
  if (abs >= 1_000_000_000) return `${(v / 1_000_000_000).toFixed(1)}B`;
  if (abs >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`;
  return v.toLocaleString();
};

function NewsPage() {
  const { id } = useParams();

  const [news, setNews] = useState(null);
  const [financeData, setFinanceData] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [upCount, setUpCount] = useState(0);
  const [downCount, setDownCount] = useState(0);

  useEffect(() => {
    if (!id) return;
    const fetchData = async () => {
      try {
        const [newsRes, fbRes] = await Promise.all([
          fetch(`/api/news/${id}`),
          fetch(`/api/news/${id}/feedback`),
        ]);
        if (newsRes.ok) {
          const newsJson = await newsRes.json();
          setNews(newsJson);
          // 뉴스 ticker로 재무데이터 조회
          if (newsJson.ticker) {
            const finRes = await fetch(
              `/api/financials/${newsJson.ticker}/summary?period=quarterly`
            );
            if (finRes.ok) setFinanceData(await finRes.json());
          }
        }
        if (fbRes.ok) {
          const fb = await fbRes.json();
          setUpCount(fb.up_count);
          setDownCount(fb.down_count);
        }
      } catch (err) {
        console.error("데이터 로딩 실패:", err);
      }
    };
    fetchData();
  }, [id]);

  const alreadyVoted = feedback !== null;

  const totalCount = upCount + downCount;
  const upPercent = totalCount === 0 ? 0 : ((upCount / totalCount) * 100).toFixed(1);
  const downPercent = totalCount === 0 ? 0 : ((downCount / totalCount) * 100).toFixed(1);

  const handleFeedback = async (type) => {
    if (alreadyVoted) {
      alert("이미 피드백을 남겼습니다.");
      return;
    }

    setFeedback(type);
    try {
      const res = await fetch(`/api/news/${id}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type }),
      });
      if (res.ok) {
        const fb = await res.json();
        setUpCount(fb.up_count);
        setDownCount(fb.down_count);
      } else {
        if (type === "up") setUpCount((prev) => prev + 1);
        else setDownCount((prev) => prev + 1);
      }
    } catch {
      if (type === "up") setUpCount((prev) => prev + 1);
      else setDownCount((prev) => prev + 1);
    }
  };

  return (
    <>
      <Header />

      <main className="news-page">
        <section className="news-title-area">
          <h2>{news?.title || "뉴스 제목"}</h2>
        </section>

        <section className="news-layout">
        <div style={{ display: "flex", flexDirection: "column", gap: "36px" }}>
          <article className="ai-summary-box">
            <h3>AI 뉴스 요약</h3>
            <p>
              {news?.summary || "뉴스 요약 정보를 불러오는 중입니다..."}
            </p>

            <button
                className="news-url-button"
                onClick={() => news?.url && window.open(news.url, "_blank")}
            >
                뉴스 URL
                </button>
          </article>
          <article className="ai-summary-box">
            <h3>AI 차트 분석</h3>
            <p>
              이 영역에는 관련 종목의 주식 차트 분석 내용이 들어갑니다.
            </p>
            <button
              className="news-url-button"
              onClick={() => window.location.href = "/dashboard?tab=overview"}
            >
              종목 차트 보기
            </button>
          </article>
        </div>

          <aside className="finance-section">
            <div className="finance-table-box">
              <table>
                <thead>
                  <tr>
                    <th>마감기준:</th>
                    {financeData
                      ? financeData.income_statement.map((d) => (
                          <th key={d.period}>{d.period}</th>
                        ))
                      : ["", "", "", "", ""].map((_, i) => <th key={i}>-</th>)}
                  </tr>
                </thead>

                <tbody>
                  {FINANCE_ROW_MAP.map(({ label, source, key }) => {
                    const getVal = (src, k, i) => {
                      if (!financeData) return null;
                      if (src === "income") return financeData.income_statement[i]?.[k];
                      if (src === "balance") return financeData.balance_sheet[i]?.[k];
                      if (src === "cash") return financeData.cash_flow[i]?.[k];
                      if (src === "cash_calc") {
                        const cf = financeData.cash_flow[i];
                        if (!cf) return null;
                        const op = cf.operating_cash_flow ?? 0;
                        const inv = cf.investing_cash_flow ?? 0;
                        const fin = cf.financing_cash_flow ?? 0;
                        return op + inv + fin;
                      }
                      return null;
                    };
                    const periods = financeData
                      ? financeData.income_statement
                      : [{}, {}, {}, {}, {}];
                    return (
                      <tr key={label}>
                        <td>{label}</td>
                        {periods.map((_, i) => (
                          <td key={i}>{fmt(getVal(source, key, i))}</td>
                        ))}
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              <button
                className="finance-url-button"
                onClick={() =>
                  news?.ticker &&
                  window.open(
                    `https://finance.yahoo.com/quote/${news.ticker}/financials`,
                    "_blank"
                  )
                }
              >
                재무재표 URL
              </button>
            </div>

            <div className="finance-summary-box">
              <h3>재무재표 요약</h3>
              <p>
                {financeData?.analysis?.summary ||
                  "이 영역에는 재무재표를 기반으로 한 해당 종목의 주요 지표 요약이 들어갑니다."}
              </p>
            </div>
          </aside>
        </section>

        <p className="notice-text">
          본 콘텐츠는 투자 권유 목적이 아닌 정보 제공용입니다.
        </p>

        <section className="feedback-section">
          <div className="feedback-labels">
            <span>{upPercent}%</span>
            <strong>{totalCount === 0 ? "None feedback" : "human feedback"}</strong>
            <span>{downPercent}%</span>
          </div>

          <div
            className="feedback-bar"
            style={{
              gridTemplateColumns:
                totalCount === 0 ? "1fr 1fr" : `${upPercent}fr ${downPercent}fr`,
            }}
          >
            <button
              className={`feedback-up ${feedback === "up" ? "selected" : ""}`}
              onClick={() => handleFeedback("up")}
            >
              ▲ UP
            </button>

            <button
              className={`feedback-down ${feedback === "down" ? "selected" : ""}`}
              onClick={() => handleFeedback("down")}
            >
              ▼ DOWN
            </button>
          </div>
        </section>
      </main>
    </>
  );
}

export default NewsPage;