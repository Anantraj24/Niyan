#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "====================================================================="
echo "                NIYAM-X SOVEREIGN WORKBENCH LAUNCHER"
echo "====================================================================="

# 1. Check Python virtual environment
if [ ! -f "api/.venv/bin/python" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv api/.venv
    api/.venv/bin/pip install -r api/requirements.txt
fi

# 2. Check Node modules
if [ ! -d "frontend/node_modules" ]; then
    echo "[INFO] Installing frontend dependencies..."
    (cd frontend && npm install)
fi

# 3. Seed demo model
echo "[INFO] Initializing demo model..."
api/.venv/bin/python tools/seed_demo.py

# 4. Launch backend and frontend
echo "[INFO] Launching FastAPI Backend on http://127.0.0.1:8000..."
api/.venv/bin/python -m uvicorn api.app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "[INFO] Launching Vite Frontend on http://127.0.0.1:5173..."
(cd frontend && npm run dev -- --host 127.0.0.1 --port 5173) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM EXIT

echo "[INFO] NIYAM-X is live on http://127.0.0.1:5173/"
wait
