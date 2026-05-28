#!/usr/bin/env bash
set -e

BACKEND_PORT=8000
FRONTEND_PORT=5173
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend/choi"

# ── 정리 함수 ──────────────────────────────────────────────
cleanup() {
  echo ""
  echo "서버를 종료합니다..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  echo "종료 완료."
}
trap cleanup INT TERM

# ── .env 없으면 .env.example 복사 ─────────────────────────
if [ ! -f "$BACKEND_DIR/.env" ]; then
  if [ -f "$BACKEND_DIR/.env.example" ]; then
    cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    echo "[setup] backend/.env 를 .env.example 에서 생성했습니다."
    echo "        필요한 API 키는 backend/.env 를 직접 편집하세요."
  else
    echo "[경고] backend/.env.example 을 찾을 수 없습니다."
  fi
fi

# ── Python 명령 결정 ───────────────────────────────────────
if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "[오류] Python 을 찾을 수 없습니다. Python 3.9 이상을 설치하세요."
  exit 1
fi

# ── 가상환경 설정 ──────────────────────────────────────────
VENV_DIR="$BACKEND_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "[setup] 가상환경 생성 중..."
  $PYTHON -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "[setup] 의존성 설치 중 (requirements.txt)..."
pip install -q -r "$BACKEND_DIR/requirements.txt"

# ── 백엔드 실행 ────────────────────────────────────────────
echo ""
echo "[backend] FastAPI 서버 시작 → http://localhost:${BACKEND_PORT}"
cd "$BACKEND_DIR"
uvicorn main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

# ── 프론트엔드 React 앱 실행 ──────────────────────────────
echo "[frontend] React 앱 시작 → http://localhost:${FRONTEND_PORT}"
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
  echo "[setup] npm install 실행 중..."
  npm install
fi
npm run dev &
FRONTEND_PID=$!

# ── 접속 안내 ─────────────────────────────────────────────
sleep 1
echo ""
echo "============================================"
echo "  프론트엔드 : http://localhost:${FRONTEND_PORT}"
echo "  백엔드 API : http://localhost:${BACKEND_PORT}"
echo "  API 문서   : http://localhost:${BACKEND_PORT}/docs"
echo "============================================"
echo "  종료하려면 Ctrl+C 를 누르세요."
echo ""

wait "$BACKEND_PID" "$FRONTEND_PID"
