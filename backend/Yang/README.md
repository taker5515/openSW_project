# Stock Newsletter API — backend/Yang

FastAPI + SQLite 기반 주식 뉴스레터 백엔드.  
`frontend/choi` (서비스 랜딩) 및 `frontend/park` (대시보드 프로토타입) 두 프론트를 모두 지원합니다.

---

## 빠른 시작

```bash
cd backend/Yang

# 1. 가상환경
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env
# .env 파일에서 SECRET_KEY를 반드시 변경하세요

# 4. 서버 실행
python run.py
# → http://localhost:8000
```

API 문서: http://localhost:8000/docs

---

## 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | `sqlite:///./stockdb.sqlite3` | DB 연결 (PostgreSQL 가능) |
| `SECRET_KEY` | 개발용 기본값 | JWT 서명 키 (프로덕션에서 반드시 변경) |
| `USE_MOCK_DATA` | `false` | `true` 설정 시 외부 API 없이 mock 데이터 사용 |
| `ANTHROPIC_API_KEY` | 없음 | AI 뉴스 분석 (없으면 heuristic fallback) |
| `SMTP_HOST` | 없음 | 이메일 발송 (없으면 로그만 출력) |

---

## API Base URL

```
http://localhost:8000/api/v1
```

프론트엔드 `.env`에 다음을 추가하세요:
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 구현된 API 목록

### Health
```
GET /api/v1/health
```

### Auth (JWT)
```
POST /api/v1/auth/register    { email, password }
POST /api/v1/auth/login       { email, password }
GET  /api/v1/auth/me          (Authorization: Bearer <token>)
```

### Themes — choi 프론트
```
GET /api/v1/themes
GET /api/v1/themes/{theme_key}          # ai | semiconductor | ev | bio | finance
GET /api/v1/themes/{theme_key}/news
```

### News
```
GET /api/v1/news/latest
GET /api/v1/news?theme=ai
GET /api/v1/news?ticker=NVDA
```

### Subscriptions — choi 프론트
```
POST   /api/v1/subscriptions            { email, themes, tickers, frequency, send_time }
GET    /api/v1/subscriptions/{email}
PATCH  /api/v1/subscriptions/{id}
DELETE /api/v1/subscriptions/{id}
POST   /api/v1/subscriptions/unsubscribe
```

### Stocks — park 대시보드
```
GET /api/v1/stocks/search?q=apple
GET /api/v1/stocks/{ticker}/summary       # WatchItem 호환
GET /api/v1/stocks/{ticker}/chart?period=3mo&interval=1d
GET /api/v1/stocks/stream?tickers=AAPL,NVDA,TSLA&interval=3   # SSE
```

### Watchlist — park 대시보드
```
GET    /api/v1/watchlist        (demo user if not logged in)
POST   /api/v1/watchlist        { ticker }
DELETE /api/v1/watchlist/{ticker}
GET    /api/v1/watchlist/stream  # SSE (watchlist 종목들)
```

### AI Analysis — park 대시보드
```
POST /api/v1/ai/news/analyze    { ticker, title, content }
→ { summary, signal, confidence, reason }
```

### Analytics — Toss 스타일 정량 분석
```
GET /api/v1/analytics/{ticker}/toss-style      ← 핵심
GET /api/v1/analytics/{ticker}/fundamentals
GET /api/v1/analytics/{ticker}/technicals
GET /api/v1/analytics/{ticker}/overview
GET /api/v1/analytics/{ticker}/score
```

---

## SSE 실시간 주식 정보

> yfinance polling + SSE push 구조 (진짜 WebSocket 스트림 아님).  
> 기본 3초 간격. `interval` 파라미터로 조정 가능 (최소 1초).  
> yfinance 실패 시 mock 가격으로 스트림 유지.

### 연결 예시 (frontend/park에서 붙이기)

```javascript
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

// 특정 티커 스트림
const es = new EventSource(`${API_BASE}/stocks/stream?tickers=AAPL,NVDA,TSLA&interval=3`);

es.addEventListener("stock.price", (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
  // {
  //   type: "stock.price",
  //   ticker: "NVDA",
  //   name: "NVIDIA Corporation",
  //   price: 875.4,
  //   change: -12.3,
  //   change_pct: -1.38,
  //   volume: 53200000,
  //   timestamp: "2026-05-12T09:00:00Z"
  // }
});

es.addEventListener("stock.heartbeat", (event) => {
  const data = JSON.parse(event.data);
  console.log("heartbeat", data.tickers, data.timestamp);
});

es.onerror = () => es.close();

// 관심종목 스트림 (로그인/demo user 기준)
const wlEs = new EventSource(`${API_BASE}/watchlist/stream?interval=5`);
```

### park의 `useWatchlist.ts` 마이그레이션 예시

```typescript
// 기존: mock 데이터 직접 생성
// 변경 후: 백엔드 API 호출

const [watchlist, setWatchlist] = useState<WatchItem[]>([]);

useEffect(() => {
  // 초기 데이터 로드
  fetch(`${API_BASE}/stocks/NVDA/summary`)
    .then(r => r.json())
    .then(data => {
      // data는 WatchItem 호환 (ticker, name, price, change, changePct, history)
      setWatchlist(prev => [...prev, data]);
    });

  // 실시간 업데이트
  const es = new EventSource(`${API_BASE}/stocks/stream?tickers=AAPL,NVDA,TSLA`);
  es.addEventListener("stock.price", (e) => {
    const update = JSON.parse(e.data);
    setWatchlist(prev =>
      prev.map(item =>
        item.ticker === update.ticker
          ? { ...item, price: update.price, change: update.change, changePct: update.change_pct }
          : item
      )
    );
  });
  return () => es.close();
}, []);
```

### park의 `useNewsFeed.ts` 마이그레이션 예시

```typescript
// 기존: 프론트에서 Anthropic API 직접 호출
// 변경 후: 백엔드 /ai/news/analyze 프록시

const analyzeNews = async (item: NewsItem) => {
  const res = await fetch(`${API_BASE}/ai/news/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker: item.ticker, title: item.title }),
  });
  const result = await res.json();
  // { summary, signal, confidence, reason }
  return result;
};
```

---

## Toss 스타일 정량 지표 UI 붙이기

`GET /api/v1/analytics/NVDA/toss-style` 응답 구조:

```json
{
  "ticker": "NVDA",
  "name": "NVIDIA Corporation",
  "price": 875.4,
  "score": 72.5,
  "disclaimer": "이 정보는 투자 판단을 위한 참고용이며 투자 추천이 아닙니다.",
  "sections": [...],
  "summary_cards": [...]
}
```

### summaryCards → MetricCard 컴포넌트

```typescript
// summary_cards 배열을 park의 MetricCard 스타일로 직접 렌더링
{data.summary_cards.map(card => (
  <MetricCard
    key={card.title}
    title={card.title}
    value={card.value}
    tone={card.tone}   // "positive" | "negative" | "neutral" | "warning"
    description={card.description}
  />
))}
```

### sections → 카드 리스트

```typescript
{data.sections.map(section => (
  <div key={section.key}>
    <h3>{section.title}</h3>
    <p>{section.subtitle}</p>
    {section.items.map(item => (
      <div key={item.key} className={`metric-item status-${item.status}`}>
        <span className="label">{item.label}</span>
        <span className="value">{item.value}{item.unit}</span>
        <p className="description">{item.description}</p>
        <p className="interpretation">{item.interpretation}</p>
      </div>
    ))}
  </div>
))}
```

`item.status`: `"good" | "bad" | "neutral" | "high" | "low" | "warning"`

---

## choi 프론트 연동

```typescript
// 테마 목록
fetch(`${API_BASE}/themes`)
  .then(r => r.json())
  .then(data => data.items); // [{ key, name, description, tickers }]

// 테마별 뉴스
fetch(`${API_BASE}/themes/ai/news?limit=10`)
  .then(r => r.json())
  .then(data => data.items); // NewsItem[]

// 이메일 구독
fetch(`${API_BASE}/subscriptions`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "user@example.com",
    themes: ["ai", "semiconductor"],
    frequency: "daily",
    send_time: "08:00"
  })
});

// 로그인
fetch(`${API_BASE}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "...", password: "..." })
}).then(r => r.json()); // { access_token, token_type }
```

---

## Mock 모드

외부 API 없이 프론트 개발 가능:

```bash
USE_MOCK_DATA=true python run.py
```

Mock 모드에서도 응답 스키마는 실제와 동일합니다.

---

## 아직 Mock/Stub인 부분

| 기능 | 현재 상태 | 실제 연동 방법 |
|------|-----------|----------------|
| 뉴스 데이터 | MockNewsProvider (하드코딩) | `app/external/news_provider.py` 교체 (NewsAPI, RSS) |
| AI 분석 | `ANTHROPIC_API_KEY` 없으면 heuristic | `.env`에 `ANTHROPIC_API_KEY` 추가 |
| 이메일 발송 | `SMTP_HOST` 없으면 로그만 | `.env`에 SMTP 설정 또는 SendGrid/Resend 연동 |
| 실시간 가격 | yfinance polling (지연 있음) | `app/external/market_data_provider.py` 교체 |

---

## 주의 사항

- 이 서비스의 모든 분석 정보는 **투자 추천이 아닌 참고용**입니다.
- yfinance 데이터는 지연될 수 있으며 외부 API 정책에 따라 달라집니다.
- 실시간 가격 업데이트는 3~60초 간격으로 제공되며 실시간 거래 시스템이 아닙니다.

---

## 테스트

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## 확장 포인트

- `MarketDataProvider` 교체 → Alpaca, Polygon.io, KIS API
- `NewsProvider` 교체 → NewsAPI, Naver 금융, RSS
- `EmailProvider` 교체 → SendGrid, Resend, AWS SES
- `AIProvider` 교체 → OpenAI, Gemini
- `DATABASE_URL` 변경 → PostgreSQL 즉시 전환
- `analytics/scoring.py` → 섹터 평균 비교, AI 기반 scoring 추가

---

> **현재 watchlist는 demo user 기반입니다.**  
> 로그인 없이도 watchlist가 동작하며, demo user (id=1)를 공유합니다.  
> JWT 로그인 후에는 본인 계정의 watchlist가 분리됩니다.
