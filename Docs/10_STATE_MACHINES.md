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
