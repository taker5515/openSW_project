import { useState } from "react";
import Header from "../components/Header";
import "../styles/NewsPage.css";

const financeRows = [
  "총매출",
  "총이익",
  "영업 이익",
  "순이익",
  "총 자산",
  "총 유동부채",
  "총 주식",
  "부채 상환 후 현금흐름",
  "영업으로 인한 현금",
  "투자로 인한 현금",
  "재무현금흐름",
  "현금순변동",
];

type FeedbackType = "up" | "down";

function NewsPage() {
  const [feedback, setFeedback] = useState<FeedbackType | null>(null);
  const [upCount, setUpCount] = useState(0);
  const [downCount, setDownCount] = useState(0);

  const isLogin = false;
  const alreadyVoted = feedback !== null;

  const totalCount = upCount + downCount;
  const upPercent = totalCount === 0 ? 0 : +((upCount / totalCount) * 100).toFixed(1);
  const downPercent = totalCount === 0 ? 0 : +((downCount / totalCount) * 100).toFixed(1);

  const handleFeedback = (type: FeedbackType) => {
    if (!isLogin) {
      alert("로그인 후 이용할 수 있습니다.");
      return;
    }

    if (alreadyVoted) {
      alert("이미 피드백을 남겼습니다.");
      return;
    }

    setFeedback(type);

    if (type === "up") {
      setUpCount((prev) => prev + 1);
    } else {
      setDownCount((prev) => prev + 1);
    }
  };

  return (
    <>
      <Header />

      <main className="news-page">
        <section className="news-title-area">
          <h2>뉴스 제목</h2>
        </section>

        <section className="news-layout">
          <article className="ai-summary-box">
            <h3>AI 뉴스 요약</h3>
            <p>
              이 영역에는 뉴스 내용을 투자 관점에서 AI가 요약한 내용이 들어갑니다.
              향후 백엔드에서 받아온 요약 데이터를 표시하면 됩니다.
            </p>

            <button className="news-url-button">뉴스 URL</button>
          </article>

          <aside className="finance-section">
            <div className="finance-table-box">
              <table>
                <thead>
                  <tr>
                    <th>마감기준:</th>
                    <th>2025<br />27/04</th>
                    <th>2025<br />27/07</th>
                    <th>2025<br />26/10</th>
                    <th>2026<br />25/01</th>
                    <th>2026<br />26/04</th>
                  </tr>
                </thead>

                <tbody>
                  {financeRows.map((item) => (
                    <tr key={item}>
                      <td>{item}</td>
                      <td>000,000,000</td>
                      <td>000,000,000</td>
                      <td>000,000,000</td>
                      <td>000,000,000</td>
                      <td>000,000,000</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <button className="finance-url-button">재무재표 URL</button>
            </div>

            <div className="finance-summary-box">
              <h3>재무재표 요약</h3>
              <p>
                이 영역에는 재무재표를 기반으로 한 해당 종목의 주요 지표 요약이 들어갑니다.
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
