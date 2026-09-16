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
