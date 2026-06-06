import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../Components/Header";
import { useNavigate } from "react-router-dom";
import "../PageStyles/ThemePage.css";


const themeNameMap = {
  "tech&media": "기술/미디어",
  "consumer&life": "소비/생활",
  "industry&energy&realEstate": "산업/에너지/부동산",
  "finance": "금융",
  "HC&pub": "헬스케어/공공",
};

const formatTimeAgo = (dateString) => {
  const now = new Date();
  const past = new Date(dateString);

  const diff = Math.floor((now - past) / 1000);

  if (diff < 60) {
    return `${diff}초 전`;
  }

  if (diff < 3600) {
    return `${Math.floor(diff / 60)}분 전`;
  }

  if (diff < 86400) {
    return `${Math.floor(diff / 3600)}시간 전`;
  }

  return `${Math.floor(diff / 86400)}일 전`;
};

function ThemePage() {
  const { themeName } = useParams();
  const currentTheme = themeName
    ? themeNameMap[themeName] || themeName
    : "전체 뉴스";

  const navigate = useNavigate();

  const [newsList, setNewsList] = useState([]);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const url = themeName
          ? `/api/news?theme=${encodeURIComponent(themeName)}`
          : "/api/news";

        const res = await fetch(url);
        const data = await res.json();

        const items = Array.isArray(data) ? data : data.items || [];
        setNewsList(items.slice(0, 50));
      } catch (err) {
        console.error("뉴스 로딩 실패:", err);
      }
    };
    fetchNews();
  }, [themeName]);

  return (
    <div>
      <Header />

      <main className="theme-page">
        <section className="theme-title-area">
          <h2>{currentTheme}</h2>
        </section>

        {newsList.length === 0 ? (
          <div className="empty-news">관련 뉴스가 없습니다.</div>
        ) : (
          <section className="news-grid">
            {newsList.slice(0, 50).map((news) => (
              <article
                key={news.id}
                className={`news-card ${news.sentiment} level-${news.level}`}
                onClick={() => navigate(`/news/${news.id}`)}
              >
                <div className="news-meta">
                  <span>{formatTimeAgo(news.publishedAt)}</span>
                </div>
                <h3>{news.title}</h3>
                <p>{news.summary}</p>
              </article>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default ThemePage;