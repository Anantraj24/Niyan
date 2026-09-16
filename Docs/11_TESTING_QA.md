# NIYAM-X — Testing and QA Strategy

## 1. Test pyramid

### Native core
Highest priority:
- unit tests
- numerical invariants
- CPU/CUDA equivalence
- golden optimization tests

### Backend
- service tests
- repository tests
- solver protocol fixture tests
- API integration tests

### Frontend
- component tests for critical state
- API schema validation
- small number of E2E flows

## 2. Backend contract fixtures

Keep solver event fixtures under:

```text
api/tests/fixtures/solver_protocol/
```

Examples:
- successful LP
- time limit with feasible result
- numerical failure
- malformed JSONL
- CUDA unavailable fallback
- verifier failure

Backend parser tests should not need real GPU.

## 3. API tests

Required:
- health
- hardware
- import model
- analyze
- create solve
- get solve
- SSE parser/stream behavior
- verify
- resolve
- invalid IDs
- solver unavailable

## 4. Frontend critical tests

Test at least:
- X-Ray HIGH risk rendering
- running solve
- OPTIMAL verified
- FEASIBLE time-limit
- NUMERICAL_FAILURE
- verification failed
- DeltaSolve before/after comparison
- benchmark speedup hidden when invalid

## 5. E2E golden test

Using a tiny model:
1. import
2. analyze
3. solve CPU
4. wait terminal
5. verify
6. assert VERIFIED
7. change supported parameter
8. re-solve
9. assert child solve parent reference

## 6. Performance tests

Do not run heavy benchmarks in every unit test suite.

Separate command:
`make benchmark-smoke`

## 7. Demo regression

Before presentation run:
- refinery model 5 times
- ill-conditioned LP 5 times
- small MILP 5 times if included

Record failures and timing spread.

## 8. Definition of red flags

Release blocker:
- verifier says FAILED on claimed demo result
- CPU/CUDA objective mismatch beyond tolerance
- solver status says OPTIMAL with residual above configured threshold
- API loses job terminal status
- UI hardcodes benchmark values
- demo requires internet
