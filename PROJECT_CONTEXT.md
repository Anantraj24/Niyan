# PROJECT_CONTEXT.md — NIYAM-X

## Project Overview
**NIYAM-X** is a local-first, clean-room sovereign optimization platform. It diagnoses an optimization model, selects an optimal numerical strategy via deterministic heuristics, runs a clean-room sovereign C++/CUDA solver CLI (`niyam`), supports warm re-optimization (`DeltaSolve`), and independently verifies returned mathematical decisions (`niyam-verify`).

- **Tagline**: Solve. Adapt. Prove.
- **Core Loop**: Diagnose -> Configure -> Solve -> Adapt -> Prove

## Tech Stack & Architecture
- **Frontend**: React 18+ / Vite SPA, TypeScript, Tailwind CSS, Framer Motion (purposeful micro-interactions), Lucide Icons, TanStack Query.
- **Backend API**: FastAPI (Python 3.11+), Asyncio subprocess manager, SSE (Server-Sent Events) for real-time solve telemetry, Pydantic v2 data validation.
- **Persistence**: SQLite (via SQLAlchemy + Alembic) for metadata/history; local filesystem for models, solve streams, vectors, and proof packs.
- **Numerical Core**: Sovereign C++20 / CUDA CLI (`niyam` solver kernel, `niyam-verify` independent verifier, `niyam-bench` benchmark runner). No external commercial/third-party solver engines permitted inside runtime.

## Important Files & Specifications
- `Docs/00_START_HERE.md`: Agent orientation and canonical definitions.
- `Docs/01_PRODUCT_BRAIN.md`: Core product thesis, modules (Model X-Ray, Solver Autopilot, DeltaSolve, Proof Pack, Flight Recorder).
- `Docs/02_SYSTEM_ARCHITECTURE.md`: Local-first modular monolith architecture and process boundaries.
- `Docs/03_FRONTEND_SPEC.md` & `Docs/04_UI_UX_DESIGN_SYSTEM.md`: Frontend layout, design tokens, and components.
- `Docs/05_BACKEND_SPEC.md` & `Docs/06_API_CONTRACTS.md`: FastAPI architecture and REST/SSE endpoints.
- `Docs/07_DATABASE_SPEC.md` & `Docs/08_DOMAIN_MODELS.md`: SQLite schema and data contracts.
- `Docs/09_SOLVER_PROCESS_PROTOCOL.md`: JSON/JSONL protocol between FastAPI and CLI.
- `Docs/14_ANTIGRAVITY_WORK_PROTOCOL.md` & `Docs/15_FILE_OWNERSHIP_MAP.md`: Development boundaries and file ownership.
- `Docs/21_GIT_WORKFLOW_AND_RELEASE.md`: Branching, commit conventions, and release gates.

## Current Objective
Initialize the project memory (`PROJECT_CONTEXT.md`) and establish the foundational monorepo structure and initial scaffolding according to `Docs/15_FILE_OWNERSHIP_MAP.md`.

## Completed Work
- [x] Cloned empty repository `https://github.com/Anantraj24/Niyan.git`.
- [x] Committed and pushed 25 core architecture and specification documents in `Docs/` to remote `main`.
- [x] Analyzed project requirements, architectural principles, clean-room rules, and conventions.
- [x] Created `PROJECT_CONTEXT.md` as persistent project memory.

## In-Progress Work
- [ ] Setting up workspace structure and project scaffolding (core native skeleton, backend FastAPI app, frontend React/Vite app).

## Pending Work
- [ ] Native Core: C++ clean-room solver CLI skeleton (`niyam`) and verifier CLI (`niyam-verify`).
- [ ] Backend API: FastAPI skeleton with SQLite database setup, Alembic migrations, and model endpoints.
- [ ] Frontend: Vite + React + TypeScript + Tailwind CSS UI shell with Model X-Ray and Solver Workbench.
- [ ] Protocol & Bridge: Async subprocess execution and SSE telemetry stream parser.
- [ ] Verification & Demo Golden Path: Refinery problem demo dataset and end-to-end verification tests.

## Known Bugs / Blockers
- None at present.

## Important Decisions
- **ADR-001**: Local-first modular monolith over microservices to eliminate cloud network latency and preserve native solver performance.
- **ADR-002**: Clean-room sovereign solver rule — zero third-party solver dependencies (Gurobi, CPLEX, HiGHS, cuOpt, etc.) in runtime path.
- **ADR-003**: SSE over WebSockets for unidirectional live solver telemetry.
- **ADR-004**: Verifier independence — `niyam-verify` must be a separate binary and never call solver logic.

## Git / Branch Status
- Branch: `main`
- Status: Clean working tree, in sync with `origin/main` (commit `11b3184`).

## Exact Next Step
Establish workspace directory scaffolding (`core/`, `verifier/`, `api/`, `frontend/`, `benchmarks/`, `demo/`, `tools/`) and setup `.gitignore` and basic project configurations.
