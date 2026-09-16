# NIYAM-X — JSON Examples

## 1. Solve request

```json
{
  "model_id": "mod_refinery_demo",
  "version_id": "mv_01",
  "config": {
    "backend": "AUTO",
    "scaling": "AUTO",
    "time_limit_sec": 15,
    "iteration_limit": 100000,
    "tolerance": 1e-6
  }
}
```

## 2. Solve summary

```json
{
  "solve_id": "sol_01",
  "state": "COMPLETED",
  "solver_status": "OPTIMAL",
  "backend": "CUDA",
  "warm_start": false,
  "objective": 318200000.0,
  "iterations": 8241,
  "solve_time_ms": 2140,
  "primal_residual": 4.1e-7,
  "dual_residual": 8.7e-7
}
```

## 3. Iteration event

```json
{
  "protocol_version": 1,
  "seq": 102,
  "type": "solver.iteration",
  "timestamp_ms": 1234567890,
  "data": {
    "iteration": 500,
    "elapsed_ms": 412,
    "objective": 318510000.0,
    "primal_residual": 0.00012,
    "dual_residual": 0.00021
  }
}
```

## 4. X-Ray

```json
{
  "profile": {
    "variables": 128410,
    "constraints": 201844,
    "nonzeros": 2812991,
    "density": 0.000108,
    "coefficient_dynamic_range": 820000000000.0,
    "integer_ratio": 0.142,
    "fixed_variables": 4820
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
  }
}
```

## 5. Verification

```json
{
  "verification_id": "ver_01",
  "state": "COMPLETED",
  "verdict": "VERIFIED",
  "max_primal_violation": 3.8e-7,
  "max_bound_violation": 0.0,
  "max_integrality_violation": 0.0,
  "objective_error": 2.0e-8,
  "model_hash_match": true
}
```

## 6. Delta patch

```json
{
  "changes": {
    "parameters": {
      "crude_a_price": 78.4,
      "diesel_demand": 1200,
      "cdu_capacity": 0.88
    }
  },
  "config": {
    "time_limit_sec": 10
  }
}
```

## 7. API error

```json
{
  "error": {
    "code": "SOLVER_PROTOCOL_ERROR",
    "message": "The solver emitted an invalid telemetry event.",
    "details": {
      "line": 42
    },
    "request_id": "req_01"
  }
}
```
