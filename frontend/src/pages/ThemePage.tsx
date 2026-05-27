import { useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import "../styles/ThemePage.css";

const themeNameMap: Record<string, string> = {
  "tech&media": "기술/미디어",
  "consumer&life": "소비/생활",
  "industry&energy&realEstate": "산업/에너지/부동산",
  "finance": "금융",
  "HC&pub": "헬스케어/공공",
};

const formatTimeAgo = (dateString: string): string => {
  const now = new Date();
  const past = new Date(dateString);
  const diff = Math.floor((now.getTime() - past.getTime()) / 1000);

  if (diff < 60) return `${diff}초 전`;
  if (diff < 3600) return `${Math.floor(diff / 60)}분 전`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`;
  return `${Math.floor(diff / 86400)}일 전`;
};

interface ThemeNewsItem {
  id: number;
  title: string;
  summary: string;
  sentiment: string;
  level: number;
  publishedAt: string;
}

// 백엔드 연결 전 임시 데이터 — 연결 시 useEffect + fetch로 교체
const DUMMY_NEWS: ThemeNewsItem[] = [
  { id: 1, title: "테스트 bad4", summary: "bad4 news를 테스트하기 위한 임시입니다.", sentiment: "bad", level: 4, publishedAt: "2016-05-21T11:20:00" },
  { id: 2, title: "테스트 bad3", summary: "bad3 news를 테스트하기 위한 임시입니다.", sentiment: "bad", level: 3, publishedAt: "2025-05-21T11:20:00" },
  { id: 3, title: "테스트 bad2", summary: "bad2 news를 테스트하기 위한 임시입니다.", sentiment: "bad", level: 2, publishedAt: "2026-04-21T11:20:00" },
  { id: 4, title: "테스트 bad1", summary: "bad1 news를 테스트하기 위한 임시입니다.", sentiment: "bad", level: 1, publishedAt: "2026-05-20T23:02:00" },
  { id: 5, title: "테스트 good4", summary: "good4 news를 테스트하기 위한 임시입니다.", sentiment: "good", level: 4, publishedAt: "2026-05-20T23:20:00" },
  { id: 6, title: "테스트 good3", summary: "good3 news를 테스트하기 위한 임시입니다.", sentiment: "good", level: 3, publishedAt: "2026-05-21T00:20:00" },
  { id: 7, title: "테스트 good2", summary: "good2 news를 테스트하기 위한 임시입니다.", sentiment: "good", level: 2, publishedAt: "2026-05-21T01:49:00" },
  { id: 8, title: "테스트 good1", summary: "good1 news를 테스트하기 위한 임시입니다.", sentiment: "good", level: 1, publishedAt: "2026-05-21T02:53:00" },
];

function ThemePage() {
  const { themeName } = useParams<{ themeName: string }>();
  const currentTheme = themeNameMap[themeName ?? ""] ?? themeName;

  // 백엔드 연결 시 [] 초기값으로 바꾸고 useEffect + fetch 추가
  const [newsList] = useState<ThemeNewsItem[]>(DUMMY_NEWS);

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
