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
