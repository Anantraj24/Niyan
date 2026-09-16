# NIYAM-X — Acceptance Criteria

## 1. Frontend P0

PASS if:
- model loads
- X-Ray renders actual backend data
- Autopilot renders reasoned configuration
- solve starts
- live events update without page reload
- terminal statuses render correctly
- DeltaSolve can start child solve
- proof result renders
- benchmark renders actual data
- error/loading/empty states exist

## 2. Backend P0

PASS if:
- API starts with SQLite
- model import persists
- analysis persists
- solve launches native process safely
- SSE emits parsed events
- terminal result persists
- verifier launches separately
- artifact directories are deterministic
- process crash is represented clearly
- startup reconciles orphaned running jobs

## 3. Database P0

PASS if:
- Alembic creates schema from empty DB
- core CRUD works
- large vectors are not stored in DB
- parent solve relationship works
- verification history is preserved
- model content hash is stored

## 4. Solver integration P0

PASS if:
- stdout JSONL parses
- malformed event is handled
- CPU and CUDA labels reflect actual backend
- warm start reports actual use
- solution/proof paths exist after completion
- solver exit code is recorded

## 5. Demo P0

PASS if:
- works offline
- synthetic refinery model is clearly labeled
- X-Ray shows at least one meaningful finding
- real CUDA solve runs
- what-if change produces a different result when expected
- verification passes for trusted demo result
- CPU/GPU benchmark is measured, not hardcoded

## 6. Quality gate

Do not call P0 done if:
- TypeScript/build fails
- backend tests fail
- verifier test fails
- UI masks failed verification
- performance number lacks validity/correctness context
