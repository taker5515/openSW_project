# Student Investing API — Backend

FastAPI 기반의 주식 투자 학습 플랫폼 백엔드입니다.

## 주요 기능

- JWT + Google OAuth 인증
- 뉴스 크롤링 및 Gemini AI 기반 감성 분석
- yfinance 기반 재무제표 / 비율 / 분석
- 관심 종목(Watchlist) 관리
- 시장 개요 뉴스

---

## 폴더 구조

```
backend/
├─ main.py              # FastAPI 앱 진입점
├─ requirements.txt
├─ .env.example
├─ api/routes/          # HTTP 요청/응답 계층
├─ core/                # config, security, exceptions
├─ db/                  # DB 엔진, 세션, Base
├─ models/              # SQLAlchemy ORM 모델
├─ schemas/             # Pydantic request/response
├─ repositories/        # DB CRUD
├─ services/            # 비즈니스 로직
├─ external/            # 외부 API 클라이언트
└─ utils/               # 공통 유틸
```

---

## 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 실제 값 입력
```

필수 환경변수:

| 변수 | 설명 |
|------|------|
| `DATABASE_URL` | SQLite 또는 PostgreSQL URL |
| `JWT_SECRET_KEY` | JWT 서명 비밀키 |
| `GEMINI_API_KEY` | Google Gemini API 키 (뉴스 분석) |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret |

---

## 설치 및 실행

### macOS / Linux

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### Windows

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

서버 실행 후 Swagger UI: http://localhost:8000/docs

---

## 주요 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/auth/register` | 회원가입 |
| POST | `/api/auth/login` | 로그인 |
| GET | `/api/auth/google` | Google 로그인 리다이렉트 |
| GET | `/api/auth/google/callback` | Google OAuth 콜백 |
| GET | `/api/stocks/list` | 지원 종목 목록 |
| GET | `/api/stocks/{ticker}/info` | 종목 정보 |
| GET | `/api/stocks/{ticker}/news` | 종목 뉴스 + AI 분석 |
| GET | `/api/market/overview` | 시장 개요 뉴스 |
| GET | `/api/financials/{symbol}/summary` | 재무 종합 |
| GET | `/api/financials/{symbol}/income-statement` | 손익계산서 |
| GET | `/api/financials/{symbol}/balance-sheet` | 재무상태표 |
| GET | `/api/financials/{symbol}/cash-flow` | 현금흐름표 |
| GET | `/api/financials/{symbol}/ratios` | 재무비율 |
| GET | `/api/financials/{symbol}/segments` | 세그먼트 |
| GET | `/api/watchlists` | 관심 종목 목록 |
| POST | `/api/watchlists` | 관심 종목 추가 |
| DELETE | `/api/watchlists/{ticker}` | 관심 종목 삭제 |

---

## 개발 시 주의사항

- `.env` 파일은 절대 커밋하지 마세요 (`.gitignore` 포함됨)
- Gemini API 키 없이도 서버는 실행되지만 뉴스 분석은 fallback 응답을 반환합니다
- Google OAuth 없이도 이메일/비밀번호 인증은 동작합니다
- DB는 기본 SQLite (`app.db`)로 설정되어 있습니다
