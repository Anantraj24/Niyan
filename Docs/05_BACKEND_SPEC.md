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
