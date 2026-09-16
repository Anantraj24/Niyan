# NIYAM-X — Antigravity START HERE

> Purpose: let an Antigravity agent understand the project and begin work without scanning the entire repository.

## 0.1 One-sentence product definition

**NIYAM-X is a local-first, clean-room optimization platform that diagnoses an optimization model, chooses a numerical strategy, runs the sovereign C++/CUDA solver, supports warm re-optimization, and independently verifies the returned decision.**

Tagline: **Solve. Adapt. Prove.**

## 0.2 What is sovereign and what is not

The **solver mathematics and solver control path** are implemented by NIYAM-X.

The web application is only an orchestration and visualization layer.

Forbidden inside the solver runtime:
- Gurobi
- CPLEX
- Xpress
- HiGHS
- SCIP
- CBC
- GLPK
- OR-Tools solver engines
- NVIDIA cuOpt
- any external optimizer called as a hidden fallback

External solvers may exist only in `benchmarks/reference/` and may be used for comparison/differential testing.

## 0.3 Architecture at a glance

```text
React + TypeScript
        |
        | REST + SSE
        v
FastAPI orchestration
        |
        | subprocess + JSON/JSONL
        v
NIYAM C++/CUDA CLI
        |
        +--> CPU backend
        +--> CUDA backend
        |
        v
solution + proof metadata
        |
        v
independent niyam-verify executable

Metadata/history -> SQLite
Large artifacts   -> local filesystem
```

## 0.4 Mandatory read order

Every agent MUST read:
1. `00_START_HERE.md`
2. `01_PRODUCT_BRAIN.md`
3. `02_SYSTEM_ARCHITECTURE.md`
4. `14_ANTIGRAVITY_WORK_PROTOCOL.md`

Then read only task-specific docs:

| Task | Additional docs |
|---|---|
| Frontend component/page | `03_FRONTEND_SPEC.md`, `04_UI_UX_DESIGN_SYSTEM.md`, `06_API_CONTRACTS.md`, `10_STATE_MACHINES.md` |
| Backend/API | `05_BACKEND_SPEC.md`, `06_API_CONTRACTS.md`, `07_DATABASE_SPEC.md`, `09_SOLVER_PROCESS_PROTOCOL.md` |
| Database/migrations | `07_DATABASE_SPEC.md`, `08_DOMAIN_MODELS.md` |
| Solver bridge | `08_DOMAIN_MODELS.md`, `09_SOLVER_PROCESS_PROTOCOL.md`, `10_STATE_MACHINES.md` |
| Testing | `11_TESTING_QA.md`, `16_ACCEPTANCE_CRITERIA.md` |
| Local setup/deploy | `12_LOCAL_DEV_RUNBOOK.md` |
| Demo work | `17_DEMO_GOLDEN_PATH.md`, `18_UI_COPY_AND_STATES.md` |
| File placement/refactor | `15_FILE_OWNERSHIP_MAP.md` |
| Git / commit / push / release | `21_GIT_WORKFLOW_AND_RELEASE.md` |
| API payload examples | `19_JSON_EXAMPLES.md` |

## 0.5 DO NOT scan the whole repository by default

The docs are the source of architectural truth.

Do not recursively read the entire repository before every task.

Allowed discovery sequence:
1. Read mandatory docs.
2. Read task-specific docs.
3. Open only files listed in `15_FILE_OWNERSHIP_MAP.md` for the feature being changed.
4. Use targeted search for a symbol/path only if the docs point to stale or missing code.
5. If architecture and code disagree, STOP and report the mismatch. Do not silently invent a new architecture.

## 0.6 Product boundaries

P0 product:
- import/load optimization model
- Model X-Ray
- deterministic Solver Autopilot
- run CPU or CUDA solve
- live convergence telemetry
- solution summary
- independent verification
- what-if parameter change
- warm DeltaSolve
- CPU vs GPU benchmark
- local audit history

P1:
- basic MILP UI
- Scenario Swarm
- decision stability
- richer benchmark views
- MPS import improvements

Not P0:
- authentication
- cloud accounts
- multi-tenant SaaS
- chatbot
- RAG
- Kubernetes
- distributed branch-and-bound
- full CPLEX/Gurobi feature parity

## 0.7 Development principles

1. Correctness before performance.
2. Performance before polish.
3. Measured results before marketing claims.
4. Solver core remains independent of frontend/backend.
5. UI never decides numerical truth.
6. Verifier never calls the solver.
7. All demo numbers come from actual runs.
8. CPU backend is the numerical reference for CUDA equivalence.
9. Offline demo must work.
10. A failed verification must be visible, never hidden.

## 0.8 Canonical names

Use these names consistently:

- Product: `NIYAM-X`
- Core solver executable: `niyam`
- Independent verifier: `niyam-verify`
- Benchmark helper: `niyam-bench`
- Main web app: `NIYAM-X Workbench`
- Model analysis feature: `Model X-Ray`
- Strategy selector: `Solver Autopilot`
- warm re-optimization: `DeltaSolve`
- verification artifact: `Proof Pack`
- immutable run metadata: `Flight Recorder`

Do not rename these casually.

## 0.9 Agent kickoff prompt

```text
Read docs/antigravity/00_START_HERE.md first.
Then read the mandatory docs it names and only the task-specific docs for this task.
Do not scan the entire repository.

Task: <task>

Before coding:
- identify the exact files you expect to modify,
- restate the relevant API/data contracts,
- call out any mismatch between docs and code.

Then implement only the task, run relevant tests, and report:
- changed files,
- test/build results,
- unresolved issues.
```
