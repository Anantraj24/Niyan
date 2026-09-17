@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo                 NIYAM-X SOVEREIGN WORKBENCH LAUNCHER
echo =====================================================================
echo.

set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

rem 1. Check Python virtual environment
if not exist "api\.venv\Scripts\python.exe" (
    echo [ERROR] Python virtual environment not found in api\.venv.
    echo Please run: python -m venv api\.venv ^&^& api\.venv\Scripts\pip install -r api\requirements.txt
    pause
    exit /b 1
)

rem 2. Check Node modules
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd frontend && npm install && cd ..
)

rem 3. Ensure demo model is seeded
echo [INFO] Ensuring database and demo model are initialized...
api\.venv\Scripts\python.exe tools\seed_demo.py

rem 4. Launch FastAPI Backend in a new window
echo [INFO] Launching FastAPI Backend on http://127.0.0.1:8000...
start "NIYAM-X Backend (Port 8000)" cmd /k "api\.venv\Scripts\python.exe -m uvicorn api.app.main:app --host 127.0.0.1 --port 8000"

rem 5. Launch Vite Frontend in a new window
echo [INFO] Launching Vite Frontend on http://127.0.0.1:5173...
start "NIYAM-X Frontend (Port 5173)" cmd /k "cd frontend && npm run dev -- --host 127.0.0.1 --port 5173"

rem 6. Wait a moment and launch default browser
timeout /t 3 /nobreak >nul
echo [INFO] Opening NIYAM-X Industrial Operations Workbench...
start http://127.0.0.1:5173/

echo.
echo =====================================================================
echo  NIYAM-X is running! Press any key in the server windows to stop.
echo =====================================================================
