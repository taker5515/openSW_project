# Investment Analysis API — backend/Yang

미국 주식 재무제표 기반 투자분석 API입니다.  
FastAPI + yfinance를 이용해 손익계산서, 재무상태표, 현금흐름표, 재무비율, 룰기반 분석 결과를 JSON으로 제공합니다.

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| 웹 프레임워크 | FastAPI |
| 서버 | Uvicorn |
| 데이터 소스 | yfinance |
| 데이터 처리 | pandas, numpy |
| 스키마 검증 | Pydantic v2 |
| DB (예정) | SQLAlchemy + SQLite / PostgreSQL |
| 언어 | Python 3.11+ |

---

## 폴더 구조

```
backend/Yang/
  main.py               ← FastAPI 앱 진입점
  requirements.txt      ← 의존성
  README.md             ← 이 파일

  api/routes/
    financials.py       ← 재무제표 API (구현 완료)
    valuation.py        ← 예정
    kpi.py              ← 예정
    ir.py               ← 예정
    earnings.py         ← 예정
    community.py        ← 예정
    news.py             ← 예정
    macro.py            ← 예정
    newsletters.py      ← 예정
    auth.py             ← 예정
    users.py            ← 예정
    watchlists.py       ← 예정

  core/
    config.py           ← 앱 설정 (pydantic-settings)
    constants.py        ← 상수 정의

  db/
    database.py         ← SQLAlchemy 엔진 및 Base
    session.py          ← get_db 의존성

  external/
    financial_data_client.py  ← yfinance 클라이언트 (구현 완료)
    [기타 클라이언트]          ← 예정

  services/
    financial_statement_service.py  ← DataFrame 정규화
    financial_ratio_service.py      ← 재무비율 계산
    financial_analysis_service.py   ← 룰기반 분석
    financial_segment_service.py    ← 세그먼트 (미지원)
    [기타 서비스]                    ← 예정

  repositories/         ← DB 캐시용 레포지토리 (예정)
  models/               ← SQLAlchemy ORM 모델 (예정)
  schemas/
    financials.py       ← Pydantic 응답 스키마 (구현 완료)
    [기타 스키마]         ← 예정

  utils/
    financial_calculations.py  ← 안전 계산 헬퍼
    financial_mappings.py      ← yfinance 컬럼명 매핑
    response.py                ← 응답 포맷 헬퍼
    date.py                    ← 날짜 포맷 헬퍼
```

---

## 설치 방법

```bash
cd backend/Yang

# 1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정 (선택)
cp .env.example .env

# 4. 서버 실행
uvicorn main:app --reload
```

서버 실행 후 Swagger 문서: **http://localhost:8000/docs**

---

## API 목록

### 기본

```
GET /           → {"message": "Investment Analysis API is running"}
GET /health     → {"status": "ok"}
```

### 재무제표 (구현 완료)

모든 엔드포인트에서 `?period=annual` (기본) 또는 `?period=quarterly` 사용 가능.

```
GET /api/financials/{symbol}/income-statement
GET /api/financials/{symbol}/balance-sheet
GET /api/financials/{symbol}/cash-flow
GET /api/financials/{symbol}/ratios
GET /api/financials/{symbol}/segments
GET /api/financials/{symbol}/summary
```

**요청 예시:**

```bash
# 손익계산서 (연간)
curl http://localhost:8000/api/financials/NVDA/income-statement

# 재무비율 (분기)
curl "http://localhost:8000/api/financials/AAPL/ratios?period=quarterly"

# 전체 요약
curl http://localhost:8000/api/financials/MSFT/summary
```

---

## 응답 JSON 예시

### 손익계산서 (`/income-statement`)

```json
{
  "symbol": "NVDA",
  "period": "annual",
  "currency": "USD",
  "data": [
    {
      "period": "2025",
      "fiscal_date": "2025-01-26",
      "revenue": 130497000000,
      "gross_profit": 97856000000,
      "operating_income": 81453000000,
      "net_income": 72880000000,
      "basic_eps": 2.99,
      "diluted_eps": 2.94,
      "ebitda": 83310000000,
      "revenue_growth": 114.2,
      "operating_income_growth": 173.5,
      "net_income_growth": 145.3
    }
  ],
  "chart_data": {
    "revenue": [{"period": "2025", "value": 130497000000}],
    "net_income": [{"period": "2025", "value": 72880000000}],
    "operating_income": [{"period": "2025", "value": 81453000000}],
    "gross_profit": [{"period": "2025", "value": 97856000000}]
  },
  "message": null
}
```

### 재무비율 (`/ratios`)

```json
{
  "symbol": "NVDA",
  "period": "annual",
  "currency": "USD",
  "data": [
    {
      "period": "2025",
      "fiscal_date": "2025-01-26",
      "gross_margin": 74.99,
      "operating_margin": 62.42,
      "net_margin": 55.85,
      "roe": 123.45,
      "roa": 67.12,
      "revenue_growth": 114.2,
      "revenue_cagr_3y": 89.5,
      "debt_ratio": 38.2,
      "current_ratio": 4.17,
      "free_cash_flow": 60050000000,
      "free_cash_flow_margin": 46.02
    }
  ],
  "chart_data": {...},
  "message": null
}
```

### 룰기반 분석 (`/summary` 내 `analysis` 필드)

```json
[
  {
    "category": "profitability",
    "level": "excellent",
    "message": "Operating margin is above 20%, indicating strong profitability.",
    "message_ko": "영업이익률이 20% 이상으로 수익성이 매우 우수합니다."
  },
  {
    "category": "growth",
    "level": "excellent",
    "message": "Revenue grew more than 15% YoY, indicating rapid growth.",
    "message_ko": "매출이 전년 대비 15% 이상 성장하여 고성장 중입니다."
  }
]
```

---

## 프론트엔드 연동 가이드

### JavaScript / TypeScript fetch 예시

```typescript
const API_BASE = "http://localhost:8000";

// 손익계산서 가져오기
async function getIncomeStatement(symbol: string, period = "annual") {
  const res = await fetch(`${API_BASE}/api/financials/${symbol}/income-statement?period=${period}`);
  if (!res.ok) throw new Error(`No data for ${symbol}`);
  return res.json();
}

// 재무 요약 (모든 데이터 한 번에)
async function getSummary(symbol: string) {
  const res = await fetch(`${API_BASE}/api/financials/${symbol}/summary`);
  if (!res.ok) throw new Error(`No data for ${symbol}`);
  return res.json();
}
```

### React 예시

```typescript
import { useEffect, useState } from "react";

export function useFinancialSummary(symbol: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!symbol) return;
    setLoading(true);
    fetch(`http://localhost:8000/api/financials/${symbol}/summary`)
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, [symbol]);

  return { data, loading, error };
}
```

---

## chart_data 사용법

각 응답의 `chart_data` 필드는 차트 라이브러리에 바로 연결할 수 있는 배열 구조입니다.

```typescript
// Recharts 예시
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

function RevenueChart({ chartData }) {
  // chartData.revenue = [{ period: "2024", value: 60922000000 }, ...]
  const formatted = chartData.revenue.map((d) => ({
    period: d.period,
    revenue: d.value ? d.value / 1e9 : null, // 단위: 십억 달러
  }));

  return (
    <BarChart data={formatted} width={400} height={250}>
      <XAxis dataKey="period" />
      <YAxis unit="B" />
      <Tooltip />
      <Bar dataKey="revenue" fill="#6366f1" />
    </BarChart>
  );
}

// margins 차트 (gross/operating/net 동시 표시)
function MarginsChart({ chartData }) {
  // chartData.margins = [{ period, gross_margin, operating_margin, net_margin }]
  return (
    <LineChart data={chartData.margins} width={400} height={250}>
      <XAxis dataKey="period" />
      <YAxis unit="%" />
      <Tooltip />
      <Line dataKey="gross_margin" name="매출총이익률" stroke="#10b981" />
      <Line dataKey="operating_margin" name="영업이익률" stroke="#6366f1" />
      <Line dataKey="net_margin" name="순이익률" stroke="#f59e0b" />
    </LineChart>
  );
}
```

---

## null 처리 안내

모든 수치 필드는 데이터가 없을 경우 `null`로 반환됩니다.  
프론트엔드에서 반드시 null 체크 후 표시하세요:

```typescript
// 안전한 표시
const displayValue = (v: number | null, unit = "") =>
  v != null ? `${(v / 1e9).toFixed(2)}B${unit}` : "N/A";

const displayPercent = (v: number | null) =>
  v != null ? `${v.toFixed(1)}%` : "N/A";
```

---

## 세그먼트 데이터 한계

`/segments` 엔드포인트는 현재 항상 아래 응답을 반환합니다:

```json
{
  "available": false,
  "message": "Segment revenue data is not available from the current data provider.",
  "segments": [],
  "chart_data": []
}
```

yfinance는 세그먼트별 매출 데이터를 신뢰성 있게 제공하지 않습니다.  
향후 SEC EDGAR API 연동으로 구현 예정입니다.

---

## 현재 구현 vs 예정 기능

| 기능 | 상태 |
|------|------|
| 손익계산서 API | 구현 완료 |
| 재무상태표 API | 구현 완료 |
| 현금흐름표 API | 구현 완료 |
| 재무비율 계산 | 구현 완료 |
| 룰기반 투자 분석 | 구현 완료 |
| 기업 요약 (summary) | 구현 완료 |
| 세그먼트 데이터 | 예정 (SEC EDGAR) |
| 밸류에이션 (DCF, 멀티플) | 예정 |
| 어닝스 (EPS 추정/실적) | 예정 |
| 거시경제 지표 | 예정 |
| 뉴스 피드 | 예정 |
| 뉴스레터 | 예정 |
| 사용자 인증 (JWT) | 예정 |
| 관심종목 (Watchlist) | 예정 |
| 커뮤니티 | 예정 |

---

## 추천 테스트 심볼

| 심볼 | 기업 | 특징 |
|------|------|------|
| NVDA | NVIDIA | 초고성장, 높은 마진 |
| AAPL | Apple | 안정적, 높은 현금흐름 |
| MSFT | Microsoft | 클라우드 성장, 안정성 |
| TSLA | Tesla | 변동성 높음 |
| AMZN | Amazon | 낮은 마진, 높은 성장 |
| GOOGL | Alphabet | 다각화, 광고 의존 |

---

## 데이터 출처 및 주의 사항

- 모든 재무 데이터는 **yfinance** 라이브러리를 통해 Yahoo Finance에서 수집합니다.
- 데이터는 투자 판단의 참고 자료이며, **투자 추천이 아닙니다**.
- 데이터의 정확성은 Yahoo Finance 제공 데이터에 따라 달라질 수 있습니다.
- yfinance를 이용한 대량 무단 크롤링은 Yahoo Finance 이용 약관에 위배될 수 있습니다.
- 본 API는 개인/교육 목적으로 사용하세요.
