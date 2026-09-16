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
