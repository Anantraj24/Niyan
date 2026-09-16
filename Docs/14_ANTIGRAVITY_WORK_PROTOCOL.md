# NIYAM-X — Antigravity Work Protocol

## 1. Purpose

Prevent agents from wasting time rescanning the repository or rewriting architecture.

## 2. Context loading protocol

At the start of every task:

Mandatory:
- `00_START_HERE.md`
- `01_PRODUCT_BRAIN.md`
- `02_SYSTEM_ARCHITECTURE.md`
- `14_ANTIGRAVITY_WORK_PROTOCOL.md`

Then task-specific docs only.

Do not recursively index/read the full repository unless:
- required file cannot be found
- docs conflict with implementation
- user explicitly requests an architectural audit

## 3. File discovery rule

Use `15_FILE_OWNERSHIP_MAP.md`.

Open only files in the relevant ownership zone.

Example frontend X-Ray task:
- frontend feature/xray files
- frontend API analysis client
- shared API schema
Do not inspect native branch-and-bound code.

## 4. Before coding response

Agent must briefly state:
- goal
- docs read
- files expected to change
- contract being followed
- notable risk

## 5. During coding

Do not:
- add unrelated dependencies
- refactor unrelated modules
- rename canonical domain terms
- change API schema without updating contract docs
- change DB schema without migration
- change native protocol without fixture tests

## 6. If contract change is necessary

Create/update an Architecture Decision Record entry in `20_ADR_LOG.md`.

Describe:
- current behavior
- proposed change
- reason
- affected docs/files
- migration/compatibility impact

Then update all source-of-truth docs in same task.

## 7. Task completion report

Always report:
- changed files
- tests run
- build status
- known limitations
- docs updated
- whether acceptance criteria passed

## 8. No hidden mocks

Mocking is allowed in unit tests.

Production UI must not silently fall back to canned solve data.

If backend unavailable, show unavailable state.

## 9. Agent stop conditions

Stop and ask/report rather than improvising if:
- solver math is unclear
- API contract conflicts with code
- DB migration would destroy existing data
- verifier semantics are ambiguous
- requested feature violates clean-room rule

## 10. Recommended Antigravity prompt

```text
Read docs/antigravity/00_START_HERE.md.
Follow its required read order for this task.
Do not scan the full repo.

Implement: <task>.

Before editing, state:
1. relevant contracts,
2. files you will touch,
3. acceptance checks.

After editing:
- run targeted tests,
- run type/build checks,
- report changed files and remaining limitations.
```
