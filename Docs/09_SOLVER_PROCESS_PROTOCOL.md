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
