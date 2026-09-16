# NIYAM-X — Local Development and Demo Runbook

## 1. Expected tools

- Git
- CMake
- C++20 compiler
- CUDA Toolkit for CUDA build
- Python 3.11+
- Node.js
- npm/pnpm
- SQLite

## 2. Build native core

Conceptual:

```bash
cmake -S . -B build -DNIYAM_ENABLE_CUDA=ON -DNIYAM_BUILD_TESTS=ON
cmake --build build --config Release
ctest --test-dir build
```

If CUDA unavailable:

```bash
cmake -S . -B build -DNIYAM_ENABLE_CUDA=OFF
```

## 3. Backend

```bash
cd api
python -m venv .venv
# activate venv
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

## 5. Environment example

```text
NIYAM_HOME=.niyam
NIYAM_DB_URL=sqlite:///.niyam/niyam.db
NIYAM_SOLVER_PATH=../build/bin/niyam
NIYAM_VERIFY_PATH=../build/bin/niyam-verify
ENABLE_CUDA=true
MAX_CONCURRENT_SOLVES=1
```

## 6. Seed demo data

Provide a script:

```bash
python tools/seed_demo.py
```

It should:
- import bundled synthetic refinery model
- create scenario schema
- optionally run analysis
- NOT fake solve results

## 7. Demo preflight

Before judging:
1. reboot if machine has been heavily used
2. connect power
3. set performance power mode
4. ensure NVIDIA GPU visible
5. start backend
6. start frontend
7. run one CUDA warmup solve
8. clear only disposable test jobs, not required demo history
9. disconnect internet and verify demo works
10. keep CPU fallback tested

## 8. Troubleshooting

### `niyam` not found
Check `NIYAM_SOLVER_PATH`.

### CUDA unavailable
- check `nvidia-smi`
- check solver CUDA build
- UI should show CPU fallback

### DB locked
P0 concurrency should be low. Ensure long operations are not held inside DB transactions.

### SSE disconnect
Frontend reconnects. Backend must expose current job state via GET endpoint.

### Solver crash
Inspect:
`.niyam/artifacts/solves/<id>/solver.log`
