@echo off
setlocal enabledelayedexpansion

set BACKEND_PORT=8000
set FRONTEND_PORT=5173
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend\choi

:: ── .env 없으면 .env.example 복사 ─────────────────────────
if not exist "%BACKEND_DIR%\.env" (
    if exist "%BACKEND_DIR%\.env.example" (
        copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul
        echo [setup] backend\.env 를 .env.example 에서 생성했습니다.
        echo         필요한 API 키는 backend\.env 를 직접 편집하세요.
    ) else (
        echo [경고] backend\.env.example 을 찾을 수 없습니다.
    )
)

:: ── Python 확인 ───────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [오류] Python 을 찾을 수 없습니다. Python 3.9 이상을 설치하세요.
    pause
    exit /b 1
)

:: ── 가상환경 설정 ──────────────────────────────────────────
if not exist "%BACKEND_DIR%\.venv" (
    echo [setup] 가상환경 생성 중...
    python -m venv "%BACKEND_DIR%\.venv"
)

call "%BACKEND_DIR%\.venv\Scripts\activate.bat"

echo [setup] 의존성 설치 중 (requirements.txt)...
pip install -q -r "%BACKEND_DIR%\requirements.txt"

:: ── 백엔드 실행 ────────────────────────────────────────────
echo.
echo [backend] FastAPI 서버 시작 → http://localhost:%BACKEND_PORT%
start "Backend" cmd /k "cd /d %BACKEND_DIR% && call .venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload"

:: ── 프론트엔드 React 앱 실행 ─────────────────────────────
echo [frontend] React 앱 시작 → http://localhost:%FRONTEND_PORT%
start "Frontend" cmd /k "cd /d %FRONTEND_DIR% && npm install && npm run dev"

:: ── 접속 안내 ─────────────────────────────────────────────
timeout /t 2 /nobreak >nul
echo.
echo ============================================
echo   프론트엔드 : http://localhost:%FRONTEND_PORT%
echo   백엔드 API : http://localhost:%BACKEND_PORT%
echo   API 문서   : http://localhost:%BACKEND_PORT%/docs
echo ============================================
echo   두 개의 창이 열렸습니다. 각 창을 닫으면 서버가 종료됩니다.
echo.
pause
