# NIYAM-X — MASTER ANTIGRAVITY CONTEXT

> This file concatenates the core contract docs for one-shot context loading. Prefer modular docs for task work.

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


---

# NIYAM-X — Product Brain

## 1. Product thesis

Industrial optimization should not be a black box that merely returns an objective value. NIYAM-X is designed to expose the numerical condition of a model, choose a suitable solving configuration, run an owned solver kernel, adapt when operating conditions change, and independently verify the returned result.

### Core narrative

**Diagnose -> Configure -> Solve -> Adapt -> Prove**

## 2. Primary users

### Optimization / OR engineer
Needs:
- model statistics
- residuals
- convergence
- solver configuration
- reproducibility
- detailed failure reason

### Operations planner
Needs:
- business-facing objective
- changed plan after price/demand/capacity shock
- solve status
- confidence that constraints are satisfied
- fast re-solve

### Technical judge / architect
Needs:
- evidence solver is from scratch
- clear CPU/GPU split
- measured performance
- numerical honesty
- verifier independence
- benchmark methodology

### Decision maker
Needs:
- why this matters
- sovereign control
- offline/on-prem path
- measurable impact
- understandable what-if demo

## 3. Key product modules

### 3.1 Model X-Ray
Analyzes:
- variables
- constraints
- nonzeros
- density
- coefficient range
- integer/binary ratio
- fixed variables
- empty/singleton rows
- numerical risk heuristics
- scaling risk
- structure summary

X-Ray is analytical only. It does not solve or mutate the model.

### 3.2 Solver Autopilot
Deterministic P0 rules choose:
- CPU vs CUDA
- scaling mode
- tolerances
- iteration/time budget
- warm-start eligibility

Every decision includes a human-readable reason.

### 3.3 Solver
P0 continuous LP path:
- presolve
- scaling
- CPU or CUDA backend
- PDHG-style continuous solver
- residual monitoring
- honest statuses

P0/P1 integer path:
- branch-and-bound for small MILPs

### 3.4 DeltaSolve
If matrix structure is unchanged and only objective/RHS/bounds change:
- reuse matrix
- reuse compatible scaling
- warm-start x/y
- report cold-vs-warm metrics

### 3.5 Proof Pack + verifier
Independent executable checks:
- bounds
- constraints
- objective reconstruction
- integrality when applicable
- residuals
- dual conditions where available

### 3.6 Flight Recorder
Every solve records:
- model hash
- solver version
- hardware
- X-Ray
- Autopilot
- solve config
- solve status
- runtime
- residuals
- proof status

## 4. The P0 user story

1. User opens workbench.
2. User loads a refinery demo model.
3. X-Ray immediately shows model size and numerical risk.
4. Autopilot explains why CUDA/CPU and scaling mode were selected.
5. User starts solve.
6. UI streams convergence.
7. Final objective and residuals appear.
8. User changes crude price/demand/capacity.
9. DeltaSolve reuses previous state.
10. New plan is shown with changed objective and changed allocations.
11. User runs verification.
12. Proof panel shows VERIFIED with residuals.
13. User opens benchmark view and compares NIYAM CPU vs CUDA.

## 5. What the UI must never imply

Never show:
- `OPTIMAL` unless backend reports a justified optimal status.
- `VERIFIED` unless `niyam-verify` passes.
- fake live solver progress.
- fake GPU utilization.
- hardcoded speedup.
- fake industrial data presented as real.
- "AI" or "autonomous" labels for deterministic heuristics.

## 6. Product success metrics

P0 demo success:
- 100% offline
- 3 pre-tested models load reliably
- solve result is independently verified
- CPU fallback works
- CUDA path is real
- what-if update produces a real re-solve
- benchmark shows actual measured values
- UI does not crash if verification fails

## 7. Differentiation

Do not sell "GPU" alone.

Sell the combination:
- clean-room solver
- numerical diagnosis
- explicit solver strategy
- rapid re-optimization
- independent verification
- local/offline execution
- auditable run history

## 8. Demo domain

Primary demo domain: synthetic refinery planning/blending.

Example adjustable inputs:
- crude A price
- crude B price
- diesel demand
- gasoline demand
- CDU capacity

Example outputs:
- profit/day
- crude mix
- unit utilization
- demand satisfaction
- active constraints
- feasibility/verification status

Synthetic demo data must always be labeled `Synthetic refinery model`.


---

# NIYAM-X — System Architecture

## 1. Architectural style

Local-first modular monolith for the product layer, separate native processes for numerical execution.

No microservices for P0.

```text
Browser
  |
  v
React/Vite SPA
  |
  | JSON REST
  | SSE for job events
  v
FastAPI
  |
  +--> SQLite metadata
  |
  +--> Artifact filesystem
  |
  +--> asyncio subprocess
          |
          +--> niyam
          |
          +--> niyam-verify
```

## 2. Why this architecture

- Solver can evolve independently from web app.
- Native C++/CUDA performance is preserved.
- Web backend cannot accidentally become the numerical solver.
- CLI remains demo/debug fallback.
- SQLite is enough for one-machine prototype.
- Large artifacts do not bloat the database.
- SSE is simpler than WebSockets for one-way solver progress.

## 3. Process boundaries

### Frontend process
Dev: Vite server.
Production/demo: static files served by backend or local static server.

Responsibilities:
- user interactions
- visualization
- forms
- job status display
- no solver math

### FastAPI process
Responsibilities:
- validate requests
- persist metadata
- launch solver/verifier processes
- translate solver JSON/JSONL into API contracts
- stream events
- protect against concurrent duplicate operations
- manage artifact paths

### `niyam`
Responsibilities:
- parse canonical solver input
- X-Ray if requested by CLI mode
- presolve/scaling
- solve
- emit JSONL telemetry to stdout
- write solution/proof files

### `niyam-verify`
Responsibilities:
- independently load model + solution/proof
- verify
- emit verification JSON
- never optimize

## 4. Storage boundaries

### SQLite
Store small, queryable metadata:
- model records
- model versions
- analyses
- solve jobs
- solution summaries
- verification summaries
- benchmark summaries
- user-adjustable scenario metadata

### Filesystem
Store:
- original uploaded model
- normalized model JSON/MPS copy
- solver stdout log
- JSONL events
- solution vectors
- proof packs
- benchmark CSVs
- plots/exports

Canonical artifact root:

```text
.niyam/
  niyam.db
  artifacts/
    models/<model_id>/<version_id>/
    solves/<solve_id>/
    benchmarks/<benchmark_id>/
```

## 5. Main runtime flow

```text
POST /models/import
    |
    v
persist model record + file
    |
    v
POST /models/{id}/analyze
    |
    v
create analysis
    |
    v
POST /solves
    |
    v
create solve_job QUEUED
    |
    v
spawn niyam
    |
    +--> stdout JSONL -> event buffer/SSE
    +--> solution.json
    +--> proof.json
    +--> solver.log
    |
    v
update solve_job terminal state
    |
    v
POST /solves/{id}/verify
    |
    v
spawn niyam-verify
    |
    v
persist verification
```

## 6. Concurrency

P0 target: one active heavy solve by default.

Config:
- `MAX_CONCURRENT_SOLVES=1` default
- queue extra jobs
- verifier may run separately if resources permit

Reason: laptop has limited RAM/VRAM. Predictable demo stability matters more than throughput.

## 7. Error containment

Backend must distinguish:
- request validation error
- model parsing error
- solver process launch error
- solver numerical failure
- solver crash
- time limit
- verifier failure
- backend internal error

Never collapse these into "500 Solver failed".

## 8. Versioning

Every solve stores:
- API schema version
- NIYAM solver version
- proof format version
- frontend build version if available
- model content hash

This lets the Flight Recorder reproduce what happened.

## 9. Configuration

Environment variables:

```text
NIYAM_HOME=.niyam
NIYAM_DB_URL=sqlite:///.niyam/niyam.db
NIYAM_SOLVER_PATH=./bin/niyam
NIYAM_VERIFY_PATH=./bin/niyam-verify
MAX_CONCURRENT_SOLVES=1
DEFAULT_TIME_LIMIT_SEC=15
DEFAULT_ITERATION_LIMIT=100000
ENABLE_CUDA=true
```

## 10. Non-goals

P0 architecture does not include:
- Redis
- Celery
- Kafka
- Kubernetes
- cloud object storage
- OAuth
- multi-tenant isolation
- serverless execution


---

# NIYAM-X — Frontend Engineering Specification

## 1. Stack

- React
- TypeScript
- Vite
- React Router
- TanStack Query for server state
- Zod for runtime payload validation
- Recharts for convergence/benchmark charts
- Tailwind CSS or equivalent utility CSS if already configured

Do not add a global state library unless a real need appears.

Use local component state + URL state + TanStack Query first.

## 2. Routes

```text
/                         Home / model library
/workbench/:modelId       Main NIYAM-X workflow
/runs/:solveId            Deep link to one run
/benchmarks               CPU/GPU/reference comparisons
/settings                 Local runtime/hardware info only
```

P0 can redirect `/` directly to a seeded demo model if needed for hackathon reliability.

## 3. Main Workbench layout

Desktop-first industrial dashboard.

```text
+------------------------------------------------------------------+
| NIYAM-X | model name | solver hardware badge | run controls      |
+--------------+---------------------------------------------------+
| Left rail    | Main content                                      |
|              |                                                   |
| Model        | [X-Ray] [Autopilot] [Solve] [What-if] [Proof]    |
| Overview     |                                                   |
|              | Context-dependent main panel                      |
| Run History  |                                                   |
|              |                                                   |
+--------------+---------------------------------------------------+
| bottom status strip: API | solver | GPU | current job | version |
+------------------------------------------------------------------+
```

## 4. Workbench panels

### 4.1 Model Overview
Show:
- model name
- source format
- synthetic/public badge
- variables
- constraints
- nonzeros
- last analysis time

Actions:
- Analyze
- Solve
- duplicate scenario
- show raw metadata

### 4.2 X-Ray
Required cards:
- Numerical Risk
- Coefficient Range
- Sparsity
- Integer Ratio
- Fixed Variables
- Singleton Rows

Issue list:
```text
HIGH Poor scaling
MEDIUM Many fixed variables
LOW Empty rows
```

Recommendation area:
- backend
- scaling
- monitoring
- explanation

No fake AI language.

### 4.3 Autopilot
Show selected configuration as a readable plan:

```text
Backend       CUDA
Reason        1.3M nonzeros + compatible GPU

Scaling       Robust
Reason        coefficient range > heuristic threshold

Warm start    Eligible
Reason        previous compatible solve found
```

Allow advanced user override only behind `Advanced` disclosure.

P0 overrides:
- CPU/CUDA
- time limit
- scaling mode

### 4.4 Solve
Show:
- status
- elapsed time
- objective
- iteration
- primal residual
- dual residual
- backend
- warm/cold start badge

Charts:
1. residual vs iteration (log scale)
2. objective vs elapsed time

Do not create multiple decorative charts.

### 4.5 What-if / DeltaSolve
For refinery demo:
- crude A price
- crude B price
- diesel demand
- gasoline demand
- unit capacity

Each control shows:
- baseline
- new value
- % delta

Primary action:
`Re-optimize with DeltaSolve`

After run show comparison:

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| objective | | | |
| solve time | | | |
| iterations | | | |
| crude A allocation | | | |

### 4.6 Proof
States:
- not generated
- verifying
- verified
- failed
- unavailable

Verified card:
- max primal violation
- max bound violation
- objective reconstruction error
- integrality violation
- dual residual if present
- proof/model hash match

Failed card must be prominent and explain exactly what failed.

### 4.7 Benchmarks
Compare:
- NIYAM CPU
- NIYAM CUDA
- optional external reference

Always show status and residual next to runtime.

Never display speedup if either compared run is invalid.

## 5. Frontend folder map

```text
frontend/src/
  app/
    router.tsx
    queryClient.ts
    AppShell.tsx

  api/
    client.ts
    schemas.ts
    models.ts
    solves.ts
    verification.ts
    benchmarks.ts

  features/
    models/
      ModelSummary.tsx
      ModelImport.tsx
    xray/
      XRayPanel.tsx
      RiskBadge.tsx
    autopilot/
      AutopilotPanel.tsx
    solve/
      SolvePanel.tsx
      SolveStatus.tsx
      ConvergenceChart.tsx
      useSolveEvents.ts
    delta/
      DeltaSolvePanel.tsx
      ScenarioControls.tsx
      BeforeAfterTable.tsx
    proof/
      ProofPanel.tsx
    benchmarks/
      BenchmarkTable.tsx
      BenchmarkChart.tsx

  pages/
    HomePage.tsx
    WorkbenchPage.tsx
    RunPage.tsx
    BenchmarksPage.tsx
    SettingsPage.tsx

  components/
    ui/
    layout/
    feedback/

  styles/
    tokens.css
    globals.css

  types/
    domain.ts
```

## 6. Server state policy

TanStack Query keys:

```text
['models']
['model', modelId]
['analysis', modelId]
['solve', solveId]
['solve-events', solveId]
['verification', solveId]
['benchmarks']
```

After mutation:
- import -> invalidate models
- analysis -> update analysis/model summary
- solve creation -> navigate to run or set active solve
- verification -> update proof panel
- resolve -> keep parent solve reference

## 7. SSE behavior

Endpoint:
`GET /api/v1/solves/{solveId}/events`

Event types:
- `job.state`
- `solver.iteration`
- `solver.restart`
- `solver.warning`
- `solver.completed`
- `solver.failed`

Frontend hook:
`useSolveEvents(solveId)`

Rules:
- reconnect on transient disconnect
- stop reconnecting after terminal state
- deduplicate by `seq`
- never synthesize missing iteration points

## 8. Loading and error UX

Never block the full screen for small operations.

Use:
- skeleton for initial model data
- inline spinner for analysis
- progress state for solve
- error panel with retry for API errors

Solver numerical failure is not a generic red error toast. It is a domain result and should be displayed in Solve panel.

## 9. Accessibility

- keyboard reachable controls
- labels for all inputs
- do not communicate status by color alone
- charts need numeric summary
- respect reduced motion
- minimum target size 40px
- no tiny gray text for solver diagnostics

## 10. Frontend acceptance

A frontend task is complete only if:
- TypeScript passes
- lint passes
- no mocked data remains in production path
- error state exists
- loading state exists
- empty state exists
- terminal solver statuses are handled
- invalid verification is visible


---

# NIYAM-X — UI/UX and Visual Design System

## 1. Design personality

NIYAM-X should feel like:
- industrial
- precise
- calm
- technical
- trustworthy
- high-information-density without clutter

It should NOT feel like:
- generic AI chatbot
- neon cyberpunk dashboard
- crypto product
- consumer finance app
- flashy landing page

## 2. Visual hierarchy

Priority:
1. current solve status
2. numerical correctness
3. business outcome
4. solver diagnostics
5. historical detail

Use space and typography before adding borders.

## 3. Color semantics

Use design tokens, not hardcoded component colors.

Suggested semantic tokens:

```text
--bg
--surface
--surface-raised
--text-primary
--text-secondary
--border
--accent
--success
--warning
--danger
--info
--chart-1
--chart-2
```

Status meaning:
- success: verified / optimal
- warning: feasible / time limit / elevated numerical risk
- danger: failed verification / crash / infeasible request
- info: running / queued / CPU-CUDA selection

Do not use red for ordinary high numerical risk if no actual failure occurred; use warning.

## 4. Typography

Use one highly readable UI family already available in the project/system.

Hierarchy:
- Page title: 24–28px
- Panel title: 16–18px
- Metric value: 24–36px
- Body: 14–16px
- Dense table: 13–14px
- Monospace: solver logs, hashes, scientific notation

Scientific notation should use tabular/monospace numbers where possible.

## 5. Spacing

Base unit: 4px.

Common:
- 8px compact
- 12px internal controls
- 16px cards
- 24px sections
- 32px major layout break

## 6. Component patterns

### Metric card
Contains:
- short label
- value
- unit
- optional small explanation
- no more than one status badge

### Status badge
Canonical labels:
- QUEUED
- RUNNING
- OPTIMAL
- FEASIBLE
- TIME LIMIT
- ITERATION LIMIT
- INFEASIBLE
- NUMERICAL FAILURE
- VERIFIED
- VERIFICATION FAILED

### Risk indicator
Use:
- LOW
- MEDIUM
- HIGH

Always pair with text.

### Technical table
- right-align numbers
- keep units in header
- preserve significant digits
- allow copy of hashes/IDs

### Disclosure
Advanced diagnostics belong in collapsible sections, not hidden permanently.

## 7. Workbench information architecture

Top-level user mental model:

```text
MODEL
  -> DIAGNOSE
  -> SOLVE
  -> CHANGE CONDITIONS
  -> PROVE
```

Use these as the visual flow.

## 8. Empty states

Examples:

X-Ray:
`Run Model X-Ray to inspect sparsity, coefficient scale, and formulation risk.`

Solve:
`No solve has been started for this model.`

Proof:
`Verification becomes available after a solution is produced.`

Benchmark:
`Run the benchmark suite to compare NIYAM CPU and CUDA backends.`

## 9. Running state

A solve screen must remain useful while running.

Show:
- elapsed time
- current iteration
- current residual
- latest objective
- backend
- stop button if supported

Do not show fake percentage complete because iterative optimization often has no reliable percent completion.

## 10. Failure UX

### Numerical failure
Headline:
`Solver stopped because numerical progress became unreliable.`

Show:
- last residual
- iteration
- scaling mode
- backend
- suggested next action from backend if available

### Verification failure
Headline:
`Solution failed independent verification.`

This must visually outrank the objective value.

### Solver process crash
Headline:
`Solver process exited unexpectedly.`

Show:
- exit code
- run ID
- link/button to local log

## 11. Responsive behavior

Primary target: laptop 1440px-ish width.

At narrower widths:
- left rail collapses
- tables scroll horizontally
- metric cards wrap
- charts remain at least 280px high

Mobile is not a P0 target.

## 12. Motion

Use minimal motion:
- panel transitions < 200ms
- running pulse only where useful
- no animated backgrounds
- convergence chart updates should not constantly rescale aggressively

## 13. Demo mode

Support a `?demo=1` optional mode that:
- opens seeded refinery model
- hides destructive/debug controls
- highlights primary flow
- does NOT change numerical data or fake results

Demo mode may simplify navigation only.

## 14. Key screen wireframe

```text
+------------------------------------------------------------------+
| NIYAM-X | Refinery LP / Synthetic | CUDA Ready | Run #A72        |
+----------+-------------------------------------------------------+
| Model    | MODEL X-RAY                                           |
| X-Ray    | [HIGH Numerical Risk] [99.95% sparse] [1e13 range]    |
| Autopilot|                                                       |
| Solve    | Issues                                                |
| What-if  | - poor scaling in 812 rows                            |
| Proof    | - 421 fixed variables                                |
| Runs     |                                                       |
|          | AUTOPILOT                                             |
|          | CUDA | Robust Scaling | Warm-start eligible           |
|          |                                                       |
|          | [Start Solve]                                         |
+----------+-------------------------------------------------------+
| API Connected | Solver v0.1.0 | RTX 5060 | No active warnings    |
+------------------------------------------------------------------+
```


---

# NIYAM-X — Backend Engineering Specification

## 1. Purpose

FastAPI is the orchestration boundary between UI and native solver processes.

It must not implement optimization mathematics.

## 2. Stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- SQLite for P0
- asyncio subprocess APIs
- standard logging

Optional:
- `psutil` only if needed for local process metrics

## 3. Backend modules

```text
api/app/
  main.py
  config.py
  dependencies.py

  routers/
    health.py
    hardware.py
    models.py
    analyses.py
    solves.py
    verification.py
    benchmarks.py

  schemas/
    common.py
    models.py
    analyses.py
    solves.py
    verification.py
    benchmarks.py

  services/
    model_service.py
    analysis_service.py
    solve_service.py
    verify_service.py
    benchmark_service.py
    artifact_service.py

  solver_bridge/
    process_runner.py
    protocol.py
    event_parser.py
    command_builder.py

  db/
    base.py
    session.py
    models.py

  repositories/
    model_repository.py
    solve_repository.py
    verification_repository.py
    benchmark_repository.py

  core/
    errors.py
    logging.py
    ids.py
    hashing.py
```

## 4. Dependency rule

Routers -> Services -> Repositories / Solver Bridge.

Forbidden:
- Router directly running subprocess.
- SQLAlchemy code inside React-facing schemas.
- Service importing frontend concepts.
- Database model used as API response without mapping.

## 5. Job execution model

### Create solve
1. Validate model/version exists.
2. Validate no incompatible active operation.
3. Insert solve row with `QUEUED`.
4. Create artifact directory.
5. Background coroutine acquires solve semaphore.
6. Update to `STARTING`.
7. Build CLI command.
8. Launch `niyam`.
9. Read stdout line-by-line.
10. Parse JSONL event.
11. Store current summary in memory + selected DB fields.
12. Publish to SSE subscribers.
13. On terminal event, persist final result.
14. Release semaphore.

## 6. In-process job manager

P0 may keep live subscriber queues in memory.

Example conceptual structure:

```python
class JobHub:
    subscribers: dict[str, set[asyncio.Queue]]
    latest_event: dict[str, SolveEvent]
```

Database remains source for durable terminal status.

If backend restarts during a solve, mark orphaned jobs `INTERRUPTED` during startup reconciliation.

## 7. Process launch safety

Use argument arrays, never shell-concatenated strings.

Good:
```python
await asyncio.create_subprocess_exec(
    solver_path,
    "solve",
    "--model", model_path,
    "--output", solution_path,
)
```

Avoid:
```python
subprocess(..., shell=True)
```

Never pass arbitrary user text as CLI option names.

## 8. Artifact directories

For solve ID `abc`:

```text
.niyam/artifacts/solves/abc/
  request.json
  solver-events.jsonl
  solver.log
  solution.json
  proof.json
  verification.json
```

Backend owns directory creation.

Solver owns files explicitly passed to it.

## 9. Model import

P0 accepted:
- canonical NIYAM JSON
- MPS when parser is available

Import pipeline:
1. save original
2. calculate SHA-256
3. create model + version
4. optional normalization
5. no automatic solve

## 10. Analysis

Preferred P0:
backend calls:
`niyam analyze --model ... --json`

Alternative if X-Ray library is exposed as a native library later.

Persist analysis JSON + key searchable fields.

## 11. Verification

`POST /solves/{solve_id}/verify`

Backend:
1. confirms solution exists
2. creates verification record `RUNNING`
3. launches `niyam-verify`
4. parses JSON
5. persists result
6. exposes artifact path

A verification failure is a valid domain response, not a backend exception.

## 12. Timeouts

Distinguish:
- API request timeout
- solver time limit
- process kill timeout

Solver should receive explicit time limit and terminate gracefully.

Backend may force-kill only after grace period.

## 13. Cancellation

P0 optional but recommended:
`POST /solves/{id}/cancel`

Flow:
- set cancellation requested
- send terminate signal
- wait grace period
- kill if necessary
- mark `CANCELLED`

## 14. Hardware endpoint

`GET /api/v1/hardware`

Return:
- CPU label
- logical cores
- system RAM
- CUDA available
- GPU name
- VRAM if discoverable
- solver binary found
- verifier binary found

Do not infer CUDA readiness solely from GPU name; backend should use solver/hardware probe.

## 15. Logging

Backend logs must include:
- request ID
- solve ID where applicable
- model ID
- process exit code
- duration

Never log huge solution vectors.

## 16. Error taxonomy

API error envelope:

```json
{
  "error": {
    "code": "MODEL_PARSE_FAILED",
    "message": "Model could not be parsed.",
    "details": {},
    "request_id": "..."
  }
}
```

Canonical codes:
- VALIDATION_ERROR
- MODEL_NOT_FOUND
- MODEL_PARSE_FAILED
- SOLVE_NOT_FOUND
- SOLVER_UNAVAILABLE
- SOLVER_PROCESS_FAILED
- SOLVER_PROTOCOL_ERROR
- ARTIFACT_MISSING
- VERIFIER_UNAVAILABLE
- DATABASE_ERROR
- CONFLICT


---

# NIYAM-X — API Contracts

Base path: `/api/v1`

Content type: `application/json` except file import and SSE.

IDs are opaque strings, preferably UUIDv7/UUID4.

## 1. Health

### GET `/health`

```json
{
  "status": "ok",
  "api_version": "1",
  "solver_available": true,
  "verifier_available": true
}
```

## 2. Hardware

### GET `/hardware`

```json
{
  "cpu": {
    "name": "Intel Core Ultra ...",
    "logical_cores": 20,
    "system_ram_bytes": 17179869184
  },
  "gpu": {
    "cuda_available": true,
    "name": "NVIDIA GeForce RTX ...",
    "vram_bytes": 8589934592
  }
}
```

## 3. Models

### POST `/models/import`

Multipart:
- `file`
- optional `display_name`
- optional `dataset_kind`: `synthetic | public | user`

Response `201`:

```json
{
  "model_id": "mod_...",
  "version_id": "mv_...",
  "display_name": "Synthetic Refinery LP",
  "format": "mps",
  "sha256": "...",
  "dataset_kind": "synthetic",
  "created_at": "..."
}
```

### GET `/models`

Returns summaries.

### GET `/models/{model_id}`

Returns model metadata + current version summary.

## 4. Analysis / X-Ray

### POST `/models/{model_id}/analyze`

```json
{
  "version_id": "mv_..."
}
```

Response:

```json
{
  "analysis_id": "ana_...",
  "model_id": "mod_...",
  "profile": {
    "variables": 128410,
    "constraints": 201844,
    "nonzeros": 2812991,
    "density": 0.000108,
    "coefficient_min_abs": 1e-8,
    "coefficient_max_abs": 8200.0,
    "coefficient_dynamic_range": 8.2e11,
    "integer_ratio": 0.142,
    "binary_ratio": 0.08,
    "fixed_variables": 4820,
    "singleton_rows": 812
  },
  "risk": {
    "level": "HIGH",
    "issues": [
      {
        "code": "COEFFICIENT_RANGE_HIGH",
        "severity": "HIGH",
        "message": "Coefficient dynamic range is large."
      }
    ]
  },
  "autopilot": {
    "backend": "CUDA",
    "scaling": "ROBUST",
    "warm_start_eligible": false,
    "reasons": [
      "Large sparse model and CUDA backend available.",
      "Coefficient range exceeds robust-scaling heuristic threshold."
    ]
  }
}
```

## 5. Create solve

### POST `/solves`

```json
{
  "model_id": "mod_...",
  "version_id": "mv_...",
  "config": {
    "backend": "AUTO",
    "scaling": "AUTO",
    "time_limit_sec": 15,
    "iteration_limit": 100000,
    "tolerance": 1e-6
  }
}
```

Response `202`:

```json
{
  "solve_id": "sol_...",
  "state": "QUEUED",
  "events_url": "/api/v1/solves/sol_.../events"
}
```

## 6. Solve status

### GET `/solves/{solve_id}`

```json
{
  "solve_id": "sol_...",
  "model_id": "mod_...",
  "state": "COMPLETED",
  "solver_status": "OPTIMAL",
  "backend": "CUDA",
  "warm_start": false,
  "objective": 318200000.0,
  "iterations": 8241,
  "solve_time_ms": 2140,
  "primal_residual": 4.1e-7,
  "dual_residual": 8.7e-7,
  "verification_state": "NOT_RUN",
  "created_at": "...",
  "completed_at": "..."
}
```

## 7. SSE solve events

### GET `/solves/{solve_id}/events`

`text/event-stream`

Event:
```text
id: 102
event: solver.iteration
data: {"seq":102,"iteration":500,"elapsed_ms":412,"objective":318510000.0,"primal_residual":0.00012,"dual_residual":0.00021}
```

Terminal:
```text
event: solver.completed
data: {"seq":504,"solver_status":"OPTIMAL","objective":318200000.0}
```

## 8. DeltaSolve

### POST `/solves/{solve_id}/resolve`

Request:

```json
{
  "changes": {
    "objective": {
      "crude_a_price": 78.4
    },
    "parameters": {
      "diesel_demand": 1200,
      "cdu_capacity": 0.88
    }
  },
  "config": {
    "time_limit_sec": 10
  }
}
```

Important: business-friendly parameter keys are valid only for models that have an associated scenario schema. Generic models may accept normalized objective/RHS/bound patches instead.

Response:
```json
{
  "solve_id": "sol_child_...",
  "parent_solve_id": "sol_...",
  "state": "QUEUED",
  "warm_start_requested": true
}
```

## 9. Verification

### POST `/solves/{solve_id}/verify`

Response `202` or synchronous short response.

Final GET solve/verification data:

```json
{
  "verification_id": "ver_...",
  "state": "COMPLETED",
  "verdict": "VERIFIED",
  "max_primal_violation": 3.8e-7,
  "max_bound_violation": 0.0,
  "max_integrality_violation": 0.0,
  "objective_error": 2.0e-8,
  "model_hash_match": true
}
```

## 10. Benchmarks

### POST `/benchmarks`

```json
{
  "model_ids": ["mod_..."],
  "backends": ["CPU", "CUDA"],
  "include_reference": false
}
```

### GET `/benchmarks/{id}`

```json
{
  "benchmark_id": "ben_...",
  "state": "COMPLETED",
  "results": [
    {
      "solver": "NIYAM",
      "backend": "CPU",
      "valid": true,
      "runtime_ms": 8400,
      "objective": 318200000.0,
      "primal_residual": 4.3e-7
    },
    {
      "solver": "NIYAM",
      "backend": "CUDA",
      "valid": true,
      "runtime_ms": 2100,
      "objective": 318200000.0,
      "primal_residual": 4.1e-7
    }
  ]
}
```

## 11. Error contract

All non-domain errors:

```json
{
  "error": {
    "code": "SOLVER_UNAVAILABLE",
    "message": "NIYAM solver executable was not found.",
    "details": {
      "configured_path": "..."
    },
    "request_id": "req_..."
  }
}
```

Numerical statuses such as `NUMERICAL_FAILURE` should normally return a successful HTTP response containing a failed solver status, not HTTP 500.


---

# NIYAM-X — Database and Persistence Specification

## 1. P0 database decision

Use **SQLite**.

Reason:
- single-machine local prototype
- offline
- zero service dependency
- easy backup
- enough metadata volume
- deterministic demo

Use SQLAlchemy + Alembic.

Do not store large solution vectors or raw event streams in SQLite.

## 2. Database location

Default:

```text
.niyam/niyam.db
```

Large artifacts:

```text
.niyam/artifacts/
```

## 3. Tables

### `models`

```text
id                  TEXT PK
display_name        TEXT NOT NULL
dataset_kind        TEXT NOT NULL
current_version_id  TEXT NULL
created_at          DATETIME NOT NULL
updated_at          DATETIME NOT NULL
```

`dataset_kind`:
- synthetic
- public
- user

### `model_versions`

```text
id                  TEXT PK
model_id            TEXT FK models.id
format              TEXT NOT NULL
source_path         TEXT NOT NULL
normalized_path     TEXT NULL
sha256              TEXT NOT NULL
size_bytes          INTEGER NOT NULL
created_at          DATETIME NOT NULL
```

Index:
- model_id
- sha256

### `analyses`

```text
id                  TEXT PK
model_version_id    TEXT FK
profile_json        JSON/TEXT NOT NULL
risk_level          TEXT NOT NULL
autopilot_json      JSON/TEXT NOT NULL
created_at          DATETIME NOT NULL
```

### `solve_jobs`

```text
id                    TEXT PK
model_version_id      TEXT FK
parent_solve_id       TEXT NULL FK solve_jobs.id
state                 TEXT NOT NULL
solver_status         TEXT NULL
backend_requested     TEXT NOT NULL
backend_used          TEXT NULL
scaling_requested     TEXT NOT NULL
scaling_used          TEXT NULL
warm_start_requested  BOOLEAN NOT NULL DEFAULT 0
warm_start_used       BOOLEAN NOT NULL DEFAULT 0
time_limit_sec        REAL NULL
iteration_limit       INTEGER NULL
tolerance             REAL NULL
objective             REAL NULL
iterations            INTEGER NULL
solve_time_ms         INTEGER NULL
primal_residual       REAL NULL
dual_residual         REAL NULL
artifact_dir          TEXT NOT NULL
error_code            TEXT NULL
error_message         TEXT NULL
created_at            DATETIME NOT NULL
started_at            DATETIME NULL
completed_at          DATETIME NULL
```

Indexes:
- model_version_id
- parent_solve_id
- state
- created_at

### `verifications`

```text
id                         TEXT PK
solve_id                   TEXT FK solve_jobs.id
state                      TEXT NOT NULL
verdict                    TEXT NULL
max_primal_violation       REAL NULL
max_bound_violation        REAL NULL
max_integrality_violation  REAL NULL
objective_error            REAL NULL
model_hash_match           BOOLEAN NULL
artifact_path              TEXT NULL
error_message              TEXT NULL
created_at                 DATETIME NOT NULL
completed_at               DATETIME NULL
```

### `benchmark_runs`

```text
id                  TEXT PK
state               TEXT NOT NULL
config_json         JSON/TEXT NOT NULL
artifact_dir        TEXT NOT NULL
created_at          DATETIME NOT NULL
completed_at        DATETIME NULL
```

### `benchmark_results`

```text
id                  TEXT PK
benchmark_run_id    TEXT FK
model_version_id    TEXT FK
solver_name         TEXT NOT NULL
backend             TEXT NULL
valid               BOOLEAN NOT NULL
runtime_ms          INTEGER NULL
objective           REAL NULL
primal_residual     REAL NULL
dual_residual       REAL NULL
solver_status       TEXT NULL
details_json        JSON/TEXT NULL
```

### `scenario_schemas` (optional P0, useful for refinery demo)

Maps business controls to normalized model patches.

```text
id                  TEXT PK
model_id            TEXT FK
schema_json         JSON/TEXT NOT NULL
created_at          DATETIME NOT NULL
```

## 4. Do not store in DB

Do NOT store:
- million-element solution vectors
- raw MPS text
- full solver stdout
- every iteration event
- binary artifacts

Store paths to filesystem artifacts.

## 5. Artifact retention

P0: retain all local runs.

Future cleanup command:
`niyam-workbench clean --older-than 30d`

Not required for demo.

## 6. Transaction rules

Model import:
- DB row and source file creation must be consistent.
- if file write fails, rollback DB.

Solve creation:
- insert job before process launch.
- terminal state update in one transaction.

Verification:
- never overwrite previous verification result silently; create new row if re-run.

## 7. Startup reconciliation

On API startup:
- find solve_jobs in `STARTING` or `RUNNING`
- if no owned process exists, mark `INTERRUPTED`
- never assume solve completed while API was down

## 8. Migration policy

Alembic migration for each schema change.

Do not edit an existing applied migration during team development.

## 9. Future PostgreSQL migration

Repository/service layers should avoid SQLite-specific SQL.

Future hosted edition can switch DB URL to PostgreSQL with minimal changes.

P0 remains SQLite.


---

# NIYAM-X — Domain Models and Shared Vocabulary

This document is the canonical vocabulary shared by frontend, backend, database, and solver bridge.

## 1. Enumerations

### JobState

```text
QUEUED
STARTING
RUNNING
COMPLETED
FAILED
CANCELLED
INTERRUPTED
```

### SolverStatus

```text
OPTIMAL
FEASIBLE
INFEASIBLE
TIME_LIMIT
ITERATION_LIMIT
NUMERICAL_FAILURE
UNKNOWN
```

### VerificationVerdict

```text
VERIFIED
FAILED
UNAVAILABLE
```

### BackendKind

```text
AUTO
CPU
CUDA
```

### ScalingMode

```text
AUTO
NONE
BASIC
ROBUST
```

### NumericalRisk

```text
LOW
MEDIUM
HIGH
```

## 2. Model identity

`Model` = logical named optimization model.

`ModelVersion` = immutable file/content version.

Solve always references a ModelVersion, never a mutable Model alone.

## 3. Solve identity

`SolveJob` is one execution attempt.

DeltaSolve creates a NEW SolveJob with:
`parent_solve_id`.

Never mutate a previous completed solve into a re-solve.

## 4. Analysis

`ModelAnalysis` belongs to ModelVersion.

It contains:
- profile
- risk
- autopilot recommendation

If file content hash changes, previous analysis is not automatically valid.

## 5. Solver configuration

Canonical conceptual model:

```text
backend
scaling
time_limit_sec
iteration_limit
tolerance
warm_start
```

Autopilot may fill `AUTO` values.

Final effective config must be recorded.

## 6. Result semantics

`objective` is meaningful only if a primal solution exists.

For infeasible/unknown runs, it may be null.

`primal_residual`:
maximum normalized/defined primal feasibility metric from solver.

`dual_residual`:
only present when solver can compute meaningful dual metric.

Frontend must tolerate null.

## 7. Refinery ScenarioPatch

Business-level patch:

```json
{
  "crude_a_price": 78.4,
  "diesel_demand": 1200,
  "cdu_capacity": 0.88
}
```

The backend scenario adapter converts it into normalized model modifications.

Business keys must be defined by a scenario schema associated with a demo model.

## 8. Verification semantics

`VERIFIED` means verifier checks implemented by current proof format passed within configured tolerances.

It does NOT automatically mean formal proof of arbitrary MILP optimality.

UI should phrase:
`Independent checks passed`
rather than
`Mathematically proven for all cases`.

## 9. Benchmark validity

A benchmark result has `valid = true` only if:
- process completed in accepted status
- returned solution meets verification/check criteria required for comparison

Speedup comparisons require both source and target result valid.


---

# NIYAM-X — Native Solver Process Protocol

## 1. Goal

Define a stable protocol so FastAPI and frontend do not need to know internal solver code.

## 2. CLI commands

### Analyze

```bash
niyam analyze \
  --model <path> \
  --output <analysis.json>
```

### Solve

```bash
niyam solve \
  --model <path> \
  --output <solution.json> \
  --proof <proof.json> \
  --backend auto|cpu|cuda \
  --scaling auto|none|basic|robust \
  --time-limit 15 \
  --iteration-limit 100000 \
  --tolerance 1e-6 \
  --events-jsonl
```

### Re-solve

```bash
niyam solve \
  --model <updated-model-or-patch> \
  --warm-state <previous-state-path> \
  ...
```

Exact warm state format is internal to solver but path is explicit.

### Verify

```bash
niyam-verify \
  --model <path> \
  --solution <solution.json> \
  --proof <proof.json> \
  --output <verification.json>
```

## 3. Stdout contract

When `--events-jsonl` is set, stdout contains one JSON object per line.

Do not print human banners to stdout in JSONL mode.

Human-readable logs go to stderr or log file.

## 4. Event envelope

```json
{
  "protocol_version": 1,
  "seq": 42,
  "type": "solver.iteration",
  "timestamp_ms": 1234567890,
  "data": {}
}
```

`seq` strictly increases per process.

## 5. Event types

### `process.started`

```json
{
  "pid": 1234,
  "solver_version": "0.1.0"
}
```

### `model.loaded`

```json
{
  "variables": 100000,
  "constraints": 80000,
  "nonzeros": 1300000
}
```

### `autopilot.selected`

```json
{
  "backend": "CUDA",
  "scaling": "ROBUST",
  "reasons": ["..."]
}
```

### `presolve.completed`

```json
{
  "variables_before": 100000,
  "variables_after": 83000,
  "constraints_before": 80000,
  "constraints_after": 71000
}
```

### `solver.iteration`

```json
{
  "iteration": 500,
  "elapsed_ms": 420,
  "objective": 318500000.0,
  "primal_residual": 0.00013,
  "dual_residual": 0.00021
}
```

Do not emit every iteration if excessive.
Suggested telemetry interval:
- first few iterations
- every N iterations
- every 100–250ms max

### `solver.warning`

```json
{
  "code": "STAGNATION",
  "message": "Residual improvement has slowed."
}
```

### `solver.completed`

```json
{
  "solver_status": "OPTIMAL",
  "objective": 318200000.0,
  "iterations": 8241,
  "elapsed_ms": 2140,
  "primal_residual": 4.1e-7,
  "dual_residual": 8.7e-7,
  "backend": "CUDA",
  "warm_start_used": false
}
```

### `solver.failed`

For process-level/domain terminal error before a valid solver status.

```json
{
  "code": "MODEL_PARSE_FAILED",
  "message": "..."
}
```

## 6. Exit codes

Suggested:

```text
0  command completed; inspect solver_status for domain result
2  CLI usage error
3  model parse/validation error
4  artifact write error
5  CUDA initialization failure with no fallback
6  unexpected internal solver crash path
```

`NUMERICAL_FAILURE` may still exit 0 if it is a handled solver status.

## 7. Solution JSON

Must include:
- format_version
- model_sha256
- solver_version
- status
- objective
- primal vector artifact/reference
- dual vector if available
- iterations
- residuals
- backend
- solve time

Large vector may be separate binary/JSON artifact referenced from solution file.

## 8. Warm state

Warm state must carry compatibility metadata:
- model structural hash
- dimension
- solver algorithm version
- scaling signature

If incompatible, solver must reject warm state and emit:
`warm_start_used=false`
with reason.

## 9. Protocol stability

Frontend never parses native stdout directly.
Only backend parses this protocol.

Changing protocol requires:
- protocol version bump if breaking
- backend parser tests
- JSON fixture update


---

# NIYAM-X — State Machines

## 1. Solve job

```text
QUEUED
  |
  v
STARTING
  |
  v
RUNNING
  | \
  |  \--> CANCELLED
  |  \--> FAILED
  |  \--> INTERRUPTED
  v
COMPLETED
```

`COMPLETED` means native process ended normally and produced a handled solver status.

A completed job can have:
- OPTIMAL
- FEASIBLE
- INFEASIBLE
- TIME_LIMIT
- ITERATION_LIMIT
- NUMERICAL_FAILURE
- UNKNOWN

Do not map every non-optimal solver status to job FAILED.

## 2. Verification

```text
NOT_RUN
  |
  v
RUNNING
  | \
  |  \--> ERROR
  v
COMPLETED
   |
   +--> VERIFIED
   +--> FAILED
```

## 3. Model analysis

```text
NOT_ANALYZED
  |
  v
ANALYZING
  |
  +--> READY
  +--> ERROR
```

## 4. Frontend solve button rules

Disable start if:
- model missing
- model import incomplete
- another solve for same model is STARTING/RUNNING unless parallel allowed
- backend reports solver unavailable

Allow new solve if previous solve has terminal state.

## 5. DeltaSolve eligibility

Eligible if:
- parent solve has usable primal/dual warm state
- model structural hash matches required compatibility rule
- requested patch only touches supported fields
- solver version can load warm state

If not eligible:
- UI may offer normal cold re-solve
- must explain why warm start is unavailable

## 6. Verification display precedence

If verification FAILED:
- objective remains visible
- but failure banner must appear above success-looking result styling

If solver OPTIMAL but verifier FAILED:
- UI must NOT present overall result as trusted.

Recommended overall label:
`OPTIMAL — VERIFICATION FAILED`

## 7. Benchmark state

```text
QUEUED -> RUNNING -> COMPLETED
                   \-> FAILED
                   \-> CANCELLED
```

Individual rows can fail without entire benchmark run failing if configured to continue.


---

# NIYAM-X — Antigravity Work Protocol

## 1. Purpose

Prevent agents from wasting time rescanning the repository or rewriting architecture.

## 2. Context loading protocol

At the start of every task:

Mandatory:
- `00_START_HERE.md`
- `01_PRODUCT_BRAIN.md`
- `02_SYSTEM_ARCHITECTURE.md`
- `14_ANTIGRAVITY_WORK_PROTOCOL.md`

Then task-specific docs only.

Do not recursively index/read the full repository unless:
- required file cannot be found
- docs conflict with implementation
- user explicitly requests an architectural audit

## 3. File discovery rule

Use `15_FILE_OWNERSHIP_MAP.md`.

Open only files in the relevant ownership zone.

Example frontend X-Ray task:
- frontend feature/xray files
- frontend API analysis client
- shared API schema
Do not inspect native branch-and-bound code.

## 4. Before coding response

Agent must briefly state:
- goal
- docs read
- files expected to change
- contract being followed
- notable risk

## 5. During coding

Do not:
- add unrelated dependencies
- refactor unrelated modules
- rename canonical domain terms
- change API schema without updating contract docs
- change DB schema without migration
- change native protocol without fixture tests

## 6. If contract change is necessary

Create/update an Architecture Decision Record entry in `20_ADR_LOG.md`.

Describe:
- current behavior
- proposed change
- reason
- affected docs/files
- migration/compatibility impact

Then update all source-of-truth docs in same task.

## 7. Task completion report

Always report:
- changed files
- tests run
- build status
- known limitations
- docs updated
- whether acceptance criteria passed

## 8. No hidden mocks

Mocking is allowed in unit tests.

Production UI must not silently fall back to canned solve data.

If backend unavailable, show unavailable state.

## 9. Agent stop conditions

Stop and ask/report rather than improvising if:
- solver math is unclear
- API contract conflicts with code
- DB migration would destroy existing data
- verifier semantics are ambiguous
- requested feature violates clean-room rule

## 10. Recommended Antigravity prompt

```text
Read docs/antigravity/00_START_HERE.md.
Follow its required read order for this task.
Do not scan the full repo.

Implement: <task>.

Before editing, state:
1. relevant contracts,
2. files you will touch,
3. acceptance checks.

After editing:
- run targeted tests,
- run type/build checks,
- report changed files and remaining limitations.
```


---

# NIYAM-X — File Ownership Map

This is the map agents should use instead of scanning the whole project.

## 1. Native core

```text
core/model/       canonical model representation
core/linalg/      sparse math interfaces/primitives
core/presolve/    presolve + scaling
core/lp/          continuous solver
core/mip/         integer solver
core/cpu/         CPU backend
core/cuda/        CUDA backend
```

Change rule:
- frontend/backend agents should not touch these unless task explicitly concerns native integration.

## 2. Verifier

```text
verifier/
```

Independent of solver control logic.

## 3. Backend

```text
api/app/routers/         HTTP endpoints
api/app/schemas/         Pydantic API contracts
api/app/services/        use cases/business orchestration
api/app/solver_bridge/   native process protocol
api/app/db/              SQLAlchemy setup/entities
api/app/repositories/    persistence abstraction
api/app/core/            errors/logging/IDs/hashes
api/tests/               backend tests
```

## 4. Frontend

```text
frontend/src/app/             router/app shell/query client
frontend/src/api/             HTTP client + schemas
frontend/src/features/models/
frontend/src/features/xray/
frontend/src/features/autopilot/
frontend/src/features/solve/
frontend/src/features/delta/
frontend/src/features/proof/
frontend/src/features/benchmarks/
frontend/src/pages/
frontend/src/components/
frontend/src/styles/
```

## 5. Database migration

```text
api/alembic/
```

Any table change requires migration here.

## 6. Demo data

```text
benchmarks/refinery/
demo/
tools/seed_demo.py
```

Keep synthetic inputs clearly labeled.

## 7. Docs

```text
docs/antigravity/
```

Contract docs live here.

## 8. Common feature touch sets

### Add X-Ray UI field
Touch:
- `frontend/src/api/schemas.ts`
- `frontend/src/features/xray/*`
Maybe backend schema if field new.

Do not touch solver if backend already returns the field.

### Add backend X-Ray field
Touch:
- `api/app/schemas/analyses.py`
- `api/app/services/analysis_service.py`
- solver bridge parser if native field
- tests
- API contract doc

### Add solve telemetry field
Touch:
- native protocol emitter
- backend `solver_bridge/event_parser.py`
- frontend event schema/hook
- protocol doc
- fixtures/tests

### Add database solve summary field
Touch:
- SQLAlchemy model
- Alembic migration
- repository
- response mapper
- DB spec doc

### Change verifier result
Touch:
- verifier
- backend verification schema/service
- frontend Proof panel
- API contract
- fixtures/tests


---

# NIYAM-X — Acceptance Criteria

## 1. Frontend P0

PASS if:
- model loads
- X-Ray renders actual backend data
- Autopilot renders reasoned configuration
- solve starts
- live events update without page reload
- terminal statuses render correctly
- DeltaSolve can start child solve
- proof result renders
- benchmark renders actual data
- error/loading/empty states exist

## 2. Backend P0

PASS if:
- API starts with SQLite
- model import persists
- analysis persists
- solve launches native process safely
- SSE emits parsed events
- terminal result persists
- verifier launches separately
- artifact directories are deterministic
- process crash is represented clearly
- startup reconciles orphaned running jobs

## 3. Database P0

PASS if:
- Alembic creates schema from empty DB
- core CRUD works
- large vectors are not stored in DB
- parent solve relationship works
- verification history is preserved
- model content hash is stored

## 4. Solver integration P0

PASS if:
- stdout JSONL parses
- malformed event is handled
- CPU and CUDA labels reflect actual backend
- warm start reports actual use
- solution/proof paths exist after completion
- solver exit code is recorded

## 5. Demo P0

PASS if:
- works offline
- synthetic refinery model is clearly labeled
- X-Ray shows at least one meaningful finding
- real CUDA solve runs
- what-if change produces a different result when expected
- verification passes for trusted demo result
- CPU/GPU benchmark is measured, not hardcoded

## 6. Quality gate

Do not call P0 done if:
- TypeScript/build fails
- backend tests fail
- verifier test fails
- UI masks failed verification
- performance number lacks validity/correctness context
