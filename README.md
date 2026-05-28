# openSW Project — Student Investing

2026 오픈소스SW 팀 프로젝트입니다.  
주식 차트 조회, 경제 뉴스, AI 요약 기능을 제공하는 웹 애플리케이션입니다.

## 구조

```
openSW_project/
├── index.html        # 정적 프론트엔드 (데모 페이지)
├── script.js
├── style.css
├── start-dev.sh      # macOS/Linux 실행 스크립트
├── start-dev.bat     # Windows 실행 스크립트
└── backend/          # FastAPI 백엔드
    ├── main.py
    ├── requirements.txt
    └── .env.example
```

## 요구사항

- **Python 3.9 이상** — `python3 --version` 으로 확인
- **pip** — Python 설치 시 기본 포함
- **최신 웹 브라우저** (Chrome, Firefox, Edge 등)

> Node.js 는 필요 없습니다. 프론트엔드는 Python 내장 HTTP 서버로 실행됩니다.

---

## 빠른 실행 방법

### macOS / Linux

```bash
git clone https://github.com/taker5515/openSW_project.git
cd openSW_project
git checkout dev
chmod +x start-dev.sh
./start-dev.sh
```

### Windows

```bat
git clone https://github.com/taker5515/openSW_project.git
cd openSW_project
git checkout dev
start-dev.bat
```

스크립트가 자동으로 처리하는 것:
1. `backend/.env` 가 없으면 `.env.example` 에서 복사
2. Python 가상환경(`.venv`) 생성
3. `requirements.txt` 의존성 설치
4. 백엔드를 **포트 8000** 에서 실행
5. 프론트엔드를 **포트 3000** 에서 실행

---

## 수동 실행 방법

### 1. 백엔드

```bash
cd backend

# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# .env 준비
cp .env.example .env             # 필요한 값 편집

# 서버 실행 (포트 8000)
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### 2. 프론트엔드

새 터미널에서:

```bash
cd openSW_project   # 루트 디렉터리
python3 -m http.server 3000 --bind 127.0.0.1
```

---

## .env 설정 방법

`backend/.env` 파일을 열어 아래 항목을 편집합니다.

```env
APP_NAME=openSW Backend
APP_ENV=development

# 프론트엔드 CORS 허용 주소 (콤마 구분 JSON 배열)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# DB (기본값: SQLite, 변경 불필요)
DATABASE_URL=sqlite:///./app.db

# AI 요약 기능 (선택) — 없으면 자동 fallback 텍스트 사용
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# 뉴스 API (선택) — 현재 mock 데이터 사용
NEWS_API_KEY=

# JWT 시크릿 (운영 환경에서는 반드시 변경)
SECRET_KEY=changeme-dev-secret-key
```

**API 키 없이도 실행 가능합니다.** AI 요약 및 뉴스는 fallback 더미 데이터로 동작합니다.

---

## 접속 URL

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | http://localhost:3000 |
| 백엔드 API | http://localhost:8000 |
| API 문서 (Swagger) | http://localhost:8000/docs |
| API 문서 (ReDoc) | http://localhost:8000/redoc |

---

## 자주 발생하는 문제

### 포트 8000이 이미 사용 중

macOS에서는 AirPlay 수신 서버가 5000번 포트를 사용할 수 있습니다.

```bash
# 사용 중인 프로세스 확인
lsof -i :5000

# macOS: 시스템 환경설정 → 공유 → AirPlay 수신 해제
```

또는 `start-dev.sh` 상단의 `BACKEND_PORT=5000` 값을 다른 포트로 변경하고, `backend/.env` 의 `CORS_ORIGINS` 도 맞춰 수정하세요.

### CORS 에러 (브라우저 콘솔에 "blocked by CORS policy")

`backend/.env` 의 `CORS_ORIGINS` 에 프론트엔드 주소가 포함되어 있는지 확인합니다.

```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

변경 후 백엔드를 재시작하세요.

### 패키지 설치 실패 (pip install 오류)

```bash
# pip 업그레이드 후 재시도
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### API 키 누락으로 AI 기능 미동작

`backend/.env` 에 `ANTHROPIC_API_KEY` 또는 `OPENAI_API_KEY` 를 설정합니다.  
키가 없으면 AI 요약은 자동으로 fallback 텍스트를 반환하며, 나머지 기능은 정상 작동합니다.

### "ModuleNotFoundError" 발생

가상환경이 활성화되어 있는지 확인하세요.

```bash
# 활성화 확인 — 프롬프트에 (.venv) 가 표시되어야 함
source backend/.venv/bin/activate
```

---

## 기술 스택

- **백엔드**: Python, FastAPI, SQLAlchemy, SQLite
- **프론트엔드**: Vanilla HTML/CSS/JS (데모), React+Vite (frontend/choi)
- **AI**: Anthropic Claude / OpenAI GPT (선택)
- **주식 데이터**: yfinance, TradingView Widget
