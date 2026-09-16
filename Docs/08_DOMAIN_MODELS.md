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
