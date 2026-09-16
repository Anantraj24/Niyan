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
