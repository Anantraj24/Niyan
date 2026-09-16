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
