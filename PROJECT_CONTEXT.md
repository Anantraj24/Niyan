# PROJECT_CONTEXT.md — NIYAM-X

## Project Overview
**NIYAM-X** is a local-first, clean-room sovereign optimization platform. It diagnoses an optimization model, selects an optimal numerical strategy via deterministic heuristics, runs a clean-room sovereign C++/CUDA solver CLI (`niyam`), supports warm re-optimization (`DeltaSolve`), and independently verifies returned mathematical decisions (`niyam-verify`).

- **Tagline**: Solve. Adapt. Prove.
- **Core Loop**: Diagnose -> Configure -> Solve -> Adapt -> Prove

## Tech Stack & Architecture
- **Frontend**: React 19 / Vite SPA, TypeScript, Tailwind CSS, Framer Motion (purposeful micro-interactions), Lucide Icons, TanStack Query, Recharts.
- **Backend API**: FastAPI (Python 3.14+), Asyncio subprocess manager, SSE (Server-Sent Events) for real-time solve telemetry, Pydantic v2 data validation, SQLAlchemy 2.0 SQLite persistence.
- **Persistence**: SQLite (`.niyam/niyam.db`) for metadata/history; local filesystem (`.niyam/artifacts/`) for models, solve streams, vectors, and proof packs.
- **Numerical Core**: Sovereign C++20 / CUDA CLI (`niyam` solver kernel, `niyam-verify` independent verifier, `niyam-bench` benchmark runner). Clean-room zero external commercial solver rule.

## Important Files & Specifications
- `Docs/00_START_HERE.md`: Agent orientation and canonical definitions.
- `Docs/01_PRODUCT_BRAIN.md`: Core product thesis, modules (Model X-Ray, Solver Autopilot, DeltaSolve, Proof Pack, Flight Recorder).
- `Docs/02_SYSTEM_ARCHITECTURE.md`: Local-first modular monolith architecture and process boundaries.
- `Docs/03_FRONTEND_SPEC.md` & `Docs/04_UI_UX_DESIGN_SYSTEM.md`: Frontend layout, design tokens, and components.
- `Docs/05_BACKEND_SPEC.md` & `Docs/06_API_CONTRACTS.md`: FastAPI architecture and REST/SSE endpoints.
- `Docs/07_DATABASE_SPEC.md` & `Docs/08_DOMAIN_MODELS.md`: SQLite schema and data contracts.
- `Docs/09_SOLVER_PROCESS_PROTOCOL.md`: JSON/JSONL protocol between FastAPI and CLI.
- `Docs/14_ANTIGRAVITY_WORK_PROTOCOL.md` & `Docs/15_FILE_OWNERSHIP_MAP.md`: Development boundaries and file ownership.
- `Docs/17_DEMO_GOLDEN_PATH.md`: Golden path refinery demonstration narrative.
- `Docs/21_GIT_WORKFLOW_AND_RELEASE.md`: Branching, commit conventions, and release gates.

## Current Objective
Build out the production-grade Frontend UI in `frontend/` implementing the Industrial Workbench layout:
- Model Library & Overview
- Model X-Ray inspection panel (Numerical Risk, Dynamic Range, Sparsity, Formulation checks)
- Solver Autopilot recommendation & configuration
- Live Solve telemetry runner (SSE stream, convergence metrics, primal/dual residuals, iterations)
- DeltaSolve What-If shock comparison (cold vs warm-start delta metrics)
- Independent Proof Pack verification viewer
- CPU vs CUDA benchmark suite

## Completed Work
- [x] Cloned empty repository `https://github.com/Anantraj24/Niyan.git` and pushed initial 25 architecture docs.
- [x] Created `PROJECT_CONTEXT.md` and root `.gitignore`.
- [x] Scaffolded monorepo directories: `core/`, `verifier/`, `api/`, `frontend/`, `demo/`, `benchmarks/`, `tools/`.
- [x] Implemented Backend FastAPI structure (`api/app/`):
  - Configuration (`config.py`) and ID generators (`ids.py`, `hashing.py`, `errors.py`, `logging.py`).
  - SQLAlchemy SQLite schema (`models.py`, `session.py`).
  - Pydantic v2 contracts matching `Docs/06_API_CONTRACTS.md` (`models.py`, `analyses.py`, `solves.py`, `verification.py`, `benchmarks.py`, `hardware.py`).
  - Repository layer (`model_repository.py`, `solve_repository.py`, `verification_repository.py`, `benchmark_repository.py`).
  - Solver bridge (`protocol.py`, `command_builder.py`, `event_parser.py`, `process_runner.py`).
  - Business services (`model_service.py`, `analysis_service.py`, `solve_service.py`, `verify_service.py`, `benchmark_service.py`).
  - REST and SSE routers (`health.py`, `hardware.py`, `models.py`, `analyses.py`, `solves.py`, `verification.py`, `benchmarks.py`).
- [x] Implemented Sovereign Clean-Room CLI:
  - `core/cli.py`: Sovereign clean-room analytical X-Ray and First-Order / PDHG continuous solver engine with `--events-jsonl` streaming telemetry and Proof Pack generator.
  - `verifier/cli.py`: Independent mathematical decision verifier checking bounds, constraints, model hash, and objective reconstruction without calling solver logic.
  - Native C++20 CMake scaffolding in `core/` and `verifier/`.
- [x] Seeded Demo Model:
  - Synthetic refinery LP problem (`demo/refinery/refinery_lp.mps`) and scenario schema (`scenario_schema.json`).
  - Seed tool `tools/seed_demo.py` (successfully populates database, attaches schema, and computes initial X-Ray).
- [x] Automated Test Suite:
  - `api/tests/test_api.py` passing 100% (health, hardware, model import, Model X-Ray, solve execution, independent verification, and DeltaSolve).
- [x] Frontend scaffolded with React 19 + TypeScript + Vite with dependencies installed (`framer-motion`, `lucide-react`, `@tanstack/react-query`, `recharts`, `clsx`, `tailwind-merge`).

## In-Progress Work
- [ ] Crafting the NIYAM-X Industrial Workbench UI in `frontend/`.

## Pending Work
- [ ] End-to-end integration check connecting Vite frontend to FastAPI backend.
- [ ] Demo Golden Path smoke test.

## Known Bugs / Blockers
- None.

## Important Decisions
- **ADR-001**: Local-first modular monolith over microservices.
- **ADR-002**: Clean-room sovereign solver rule — zero external solver engines in runtime.
- **ADR-003**: SSE over WebSockets for live unidirectional solver iteration telemetry.
- **ADR-004**: Verifier independence — `niyam-verify` executable completely decoupled from solver logic.
- **ADR-005**: Unbuffered subprocess stdout execution (`-u`) ensures instant real-time telemetry streaming on Windows.

## Git / Branch Status
- Branch: `main`
- Last pushed commit: `9dcb266`

## Exact Next Step
Develop the NIYAM-X Workbench UI components and pages in `frontend/src/` adhering strictly to `Docs/04_UI_UX_DESIGN_SYSTEM.md` and `Docs/03_FRONTEND_SPEC.md`.
