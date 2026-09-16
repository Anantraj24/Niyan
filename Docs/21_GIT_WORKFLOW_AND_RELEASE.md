# NIYAM-X — Professional Git Workflow, Push Policy, and Release Discipline

> Purpose: define exactly how NIYAM-X code is committed, reviewed, pushed, merged, tagged, and released so Antigravity and human contributors do not destabilize the project.

---

# 1. CORE RULE

Never push code merely because it compiles.

A change is push-ready only when:

1. the task scope is complete;
2. relevant tests pass;
3. no known correctness regression is hidden;
4. documentation/contracts are updated if affected;
5. generated artifacts, secrets, build outputs, and local databases are excluded;
6. the commit message explains the intent;
7. the branch is rebased or updated against the latest integration branch where appropriate.

For numerical solver work, correctness is more important than green compilation.

---

# 2. REPOSITORY BRANCH MODEL

Use a simple professional branch model.

Primary branches:

```text
main
develop
```

## `main`

Meaning:

Stable, demo-ready, release-quality code.

Rules:

- never commit directly to `main`;
- merge only reviewed and tested work;
- every commit on `main` should be releasable;
- hackathon demo should run from `main` or a release tag.

## `develop`

Meaning:

Integration branch for completed features before release.

Rules:

- feature branches merge into `develop`;
- `develop` may move faster than `main`;
- it should still remain buildable;
- before demo/release, `develop` is stabilized and merged into `main`.

If the team is extremely small and time-limited, `develop` may be omitted.

In that case:

```text
feature/* -> main
```

is acceptable only with the same test/review discipline.

---

# 3. FEATURE BRANCH NAMING

Use:

```text
feature/<short-name>
fix/<short-name>
docs/<short-name>
refactor/<short-name>
test/<short-name>
perf/<short-name>
chore/<short-name>
```

Examples:

```text
feature/model-xray
feature/cuda-spmv
feature/deltasolve
feature/proof-verifier
feature/refinery-dashboard

fix/pdhg-residual-check
fix/sse-reconnect
fix/sqlite-startup-recovery

docs/api-contracts
docs/solver-math

perf/cuda-reduction
test/cpu-gpu-equivalence
```

Do not use meaningless names such as:

```text
new
final
final2
latest
temp
work
test1
```

---

# 4. COMMIT MESSAGE STANDARD

Use Conventional Commits-style messages.

Format:

```text
<type>(<scope>): <short imperative summary>
```

Types:

```text
feat
fix
perf
refactor
test
docs
build
ci
chore
revert
```

Scopes may include:

```text
solver
cuda
cpu
pdhg
mip
xray
autopilot
delta
verifier
api
db
ui
benchmark
docs
build
```

Examples:

```text
feat(xray): add coefficient dynamic-range diagnostics

feat(cuda): implement CSR sparse matrix vector kernel

fix(pdhg): correct primal residual normalization

feat(delta): reuse compatible warm-start vectors

feat(verifier): reject model hash mismatch

feat(api): stream solver iteration events over SSE

fix(ui): show verification failure above objective result

test(cuda): add CPU GPU sparse operation equivalence tests

perf(cuda): reduce temporary allocations in SpMV

docs(api): document solve event contract
```

Bad:

```text
changes
fixed
update code
done
final
working now
```

---

# 5. COMMIT SIZE

Prefer small, logically complete commits.

Good sequence:

```text
feat(model): add CSR validation
test(model): add malformed CSR fixtures
feat(xray): add row statistics
test(xray): verify coefficient range metrics
```

Avoid one massive commit containing:

```text
solver
frontend
database
documentation
CUDA
benchmark
UI redesign
```

unless it is the initial repository bootstrap.

---

# 6. REQUIRED PRE-COMMIT CHECK

Before every commit, Antigravity must determine which checks apply.

## Native C++ changes

Run:

```bash
cmake --build build --config Release
ctest --test-dir build
```

If relevant:

```bash
cmake --build build --target niyam
cmake --build build --target niyam-verify
```

## CUDA changes

Run:

```text
CPU numerical tests
CUDA numerical tests
CPU/CUDA equivalence tests
```

A CUDA kernel is not commit-ready merely because it launches.

## Backend changes

Run:

```bash
pytest
```

and, if configured:

```bash
ruff check .
mypy app
```

## Frontend changes

Run:

```bash
npm run typecheck
npm run lint
npm run test
npm run build
```

Use the actual scripts defined by the project if names differ.

## Database changes

Required:

```text
Alembic migration exists
upgrade from clean DB works
upgrade from previous schema works
tests pass
```

## API contract changes

Required:

```text
backend schema updated
frontend schema updated
contract docs updated
fixtures updated
tests updated
```

---

# 7. SOLVER-SPECIFIC PUSH GATE

Any change affecting:

```text
LP mathematics
PDHG updates
residual calculation
termination logic
presolve
scaling
branch-and-bound
integrality
objective calculation
CUDA numerical primitives
```

must satisfy all applicable checks:

```text
[ ] unit tests pass
[ ] tiny known-answer model passes
[ ] independent verifier passes
[ ] no regression in CPU reference
[ ] CPU/CUDA equivalence passes if GPU code changed
[ ] solver status remains honest
[ ] no tolerance was weakened without explanation
```

If any box fails:

DO NOT PUSH AS COMPLETE.

A work-in-progress branch may be pushed only if clearly marked and not merged.

---

# 8. WIP PUSHES

If work must be backed up before completion:

Commit:

```text
chore(wip): checkpoint cuda transpose SpMV implementation
```

or use branch prefix:

```text
wip/cuda-transpose-spmv
```

Rules:

- never merge WIP commit into `main`;
- squash/rewrite before merge if needed;
- WIP code must not be presented as working functionality.

---

# 9. PROFESSIONAL `git status` CHECK

Before commit:

```bash
git status
git diff
git diff --staged
```

Antigravity must review:

- unexpected files
- generated binaries
- secrets
- model artifacts
- databases
- logs
- large benchmark outputs

Do not blindly run:

```bash
git add .
```

without reviewing the staged set.

Prefer targeted staging:

```bash
git add core/linalg/csr_matrix.cpp
git add tests/test_csr.cpp
git add docs/antigravity/...
```

---

# 10. `.gitignore` POLICY

Repository should ignore at minimum:

```text
# Native builds
build/
cmake-build-*/
out/

# Python
__pycache__/
*.pyc
.venv/
venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Node
node_modules/
frontend/dist/
.npm/
.pnpm-store/

# IDE / OS
.vscode/
.idea/
.DS_Store
Thumbs.db

# Runtime state
.niyam/
*.db
*.sqlite
*.sqlite3

# Solver artifacts
*.solution.json
*.proof.json
*.events.jsonl
solver.log

# Environment / secrets
.env
.env.*
!.env.example

# CUDA / profiler artifacts
*.nsys-rep
*.ncu-rep

# Temporary
tmp/
temp/
*.tmp
```

Public benchmark files deliberately committed to the repository must live in an approved benchmark directory.

Do not ignore source test fixtures that are required for reproducibility.

---

# 11. SECRET POLICY

Never commit:

```text
API keys
tokens
passwords
private certificates
cloud credentials
SSH private keys
personal access tokens
```

Even though NIYAM-X is local-first, maintain this discipline.

Use:

```text
.env.example
```

for variable names only.

Example:

```text
NIYAM_SOLVER_PATH=
NIYAM_VERIFY_PATH=
NIYAM_HOME=
```

No real secrets.

If a secret is accidentally committed:

1. stop;
2. rotate/revoke the secret;
3. remove it from history if required;
4. do not assume deleting the line in a later commit is sufficient.

---

# 12. LARGE FILE POLICY

Do not commit:

- compiled binaries
- massive MIPLIB/Netlib archives
- huge generated benchmark matrices
- raw profiling dumps
- large screenshots/videos
- local DB

If large datasets become necessary:

- document download/source,
- provide a fetch script,
- or use Git LFS if the team intentionally adopts it.

Hackathon demo models should be compact and reproducible.

---

# 13. PULL / REBASE BEFORE PUSH

Before opening a merge request or merging:

```bash
git fetch origin
git rebase origin/develop
```

or if using `main` only:

```bash
git fetch origin
git rebase origin/main
```

Resolve conflicts carefully.

Do not let an automated agent resolve numerical solver conflicts without reviewing semantics.

Especially inspect conflicts in:

```text
core/lp/
core/presolve/
core/mip/
core/cuda/
verifier/
API contracts
DB migrations
```

---

# 14. SAFE PUSH

Normal:

```bash
git push -u origin feature/model-xray
```

Never use:

```bash
git push --force
```

on shared branches.

If history rewrite is genuinely required on a personal feature branch, prefer:

```bash
git push --force-with-lease
```

Only after confirming nobody else depends on the branch.

Antigravity must never force-push `main` or `develop`.

---

# 15. PULL REQUEST / MERGE REQUEST TEMPLATE

Every PR should include:

```markdown
## What changed

Short explanation.

## Why

Problem being solved.

## Areas affected

- [ ] Solver core
- [ ] CUDA
- [ ] Verifier
- [ ] API
- [ ] Database
- [ ] Frontend
- [ ] Benchmarks
- [ ] Docs

## Correctness evidence

Tests and known-answer checks.

## Performance impact

Measured only if relevant.

## API / schema changes

Describe contract changes.

## Screenshots

Only for UI work.

## Risks

Numerical / migration / compatibility concerns.

## Checklist

- [ ] build passes
- [ ] tests pass
- [ ] no prohibited solver dependency
- [ ] no secrets
- [ ] docs updated
- [ ] verifier checked if solver output changed
```

---

# 16. MERGE POLICY

Preferred:

```text
feature branch
     |
     v
PR review
     |
     v
develop
     |
     v
stabilization
     |
     v
main
```

Recommended merge strategy:

`Squash and merge` for small feature branches.

Use normal merge when preserving meaningful multi-commit development history is useful.

Do not squash away evidence needed for a numerical bug investigation unless the final commit message remains clear.

---

# 17. PROTECTED BRANCH RULES

If GitHub/GitLab supports it, protect `main`.

Require:

- PR before merge
- branch up to date
- required CI checks
- no force push
- no deletion
- at least one review where team size permits

Optional protection for `develop`.

---

# 18. CI PIPELINE

Professional target CI:

```text
1. formatting/lint
2. CPU native build
3. native unit tests
4. verifier tests
5. backend tests
6. frontend typecheck
7. frontend tests
8. frontend production build
9. documentation consistency
```

GPU CI may be unavailable.

Therefore:

- CPU path MUST be CI-tested.
- CUDA path MUST be locally tested on the RTX development machine.
- CUDA evidence should be recorded before release/demo.

Do not pretend cloud CI validated CUDA if it did not.

---

# 19. RECOMMENDED GITHUB ACTIONS JOBS

Conceptually:

```text
native-cpu
backend
frontend
contracts
```

`native-cpu`:
- configure CMake with CUDA OFF
- build
- run CTest

`backend`:
- install Python deps
- run migrations on temp SQLite
- pytest

`frontend`:
- npm ci
- typecheck
- test
- build

`contracts`:
- ensure required Antigravity docs exist
- optional schema checks

CUDA remains separate until GPU runner exists.

---

# 20. RELEASE VERSIONING

Use Semantic Versioning.

During prototype:

```text
0.1.0
0.2.0
0.3.0
```

Meaning:

```text
0.x.y
```

is still pre-production.

Examples:

```text
v0.1.0
CPU LP solver + verifier

v0.2.0
CUDA LP path + X-Ray

v0.3.0
DeltaSolve + dashboard

v0.4.0
basic MILP
```

Patch:

```text
v0.3.1
```

for bug fixes.

---

# 21. RELEASE TAGGING

After stable merge to main:

```bash
git checkout main
git pull --ff-only
git tag -a v0.3.0 -m "NIYAM-X v0.3.0"
git push origin v0.3.0
```

Never tag an untested local branch as a release.

---

# 22. CHANGELOG

Maintain:

```text
CHANGELOG.md
```

Format:

```markdown
# Changelog

## [0.3.0]

### Added
- DeltaSolve warm re-optimization
- refinery what-if controls

### Fixed
- primal residual scaling issue

### Changed
- solver event protocol v2
```

Do not write marketing language in changelog.

---

# 23. RELEASE CHECKLIST

Before hackathon demo release:

```text
[ ] clean clone builds
[ ] CPU build passes
[ ] CUDA build passes locally
[ ] native tests pass
[ ] backend tests pass
[ ] frontend checks pass
[ ] DB migrations pass
[ ] three demo models tested repeatedly
[ ] verifier passes trusted demo results
[ ] benchmark numbers regenerated
[ ] all benchmark results labeled honestly
[ ] synthetic data clearly labeled
[ ] no external solver in runtime
[ ] offline demo tested
[ ] no secrets
[ ] no local DB/artifacts committed
[ ] version bumped
[ ] changelog updated
[ ] release tag created
```

---

# 24. HOTFIX POLICY

If a demo-critical bug is found on `main`:

```text
main
 |
 +--> fix/<bug>
        |
        v
      test
        |
        v
      main
```

Then merge the same fix back into `develop` if `develop` exists.

Example:

```text
fix/verifier-objective-tolerance
```

---

# 25. ROLLBACK POLICY

Never "fix forward" blindly minutes before a demo.

If a new merge breaks the golden path:

1. identify last known-good release/tag;
2. revert the problematic merge;
3. rerun demo regression;
4. only reintroduce after confidence is restored.

Useful command:

```bash
git revert <commit>
```

Prefer revert over destructive history rewrite on shared branches.

---

# 26. ANTIGRAVITY GIT BEHAVIOR

Antigravity MUST NOT automatically:

- commit unrelated files;
- push to `main`;
- force-push;
- create tags;
- merge PRs;
- rewrite shared history;
- delete branches;
- change `.gitignore` broadly;
- commit secrets;
- commit generated solver artifacts.

Unless the user explicitly asks Antigravity to execute Git operations, it should prepare changes and provide the exact recommended commands.

If Git execution is requested, Antigravity should still show:

```text
branch
files staged
commit message
tests passed
target remote
```

before push.

---

# 27. ANTIGRAVITY PRE-PUSH REPORT FORMAT

Before recommending or performing push, output:

```text
NIYAM-X PRE-PUSH REPORT

Branch:
feature/model-xray

Changed areas:
- Model X-Ray
- tests
- docs

Files staged:
...

Checks:
C++ build       PASS
CTest           PASS
Backend tests   N/A
Frontend build  N/A
Verifier        PASS

Known issues:
None / list

Recommended commit:
feat(xray): add model numerical diagnostics

Push target:
origin/feature/model-xray

Safe to push:
YES
```

If any required check fails:

```text
Safe to push:
NO
```

---

# 28. PROFESSIONAL FEATURE DELIVERY FLOW

For every feature:

```text
Issue / task
   |
   v
feature branch
   |
   v
implementation
   |
   v
tests
   |
   v
docs/contracts
   |
   v
pre-push report
   |
   v
push
   |
   v
PR
   |
   v
review
   |
   v
merge
   |
   v
integration tests
```

---

# 29. FEATURE ISSUE TEMPLATE

Before implementation, define:

```markdown
## Feature

Model X-Ray

## Goal

Analyze structural/numerical properties before solve.

## User value

Shows why the model is difficult and explains solver configuration.

## Scope

Included:
- coefficient range
- density
- fixed variables
- numerical risk

Excluded:
- automatic decomposition
- ML configuration

## Acceptance criteria

- metrics match fixtures
- JSON contract implemented
- UI renders LOW/MEDIUM/HIGH
- tests pass

## Files expected

core/...
api/...
frontend/...
docs/...
```

This prevents scope creep.

---

# 30. BUG ISSUE TEMPLATE

```markdown
## Bug

Short description.

## Observed

What happened.

## Expected

What should happen.

## Reproduction

Exact model/config/steps.

## Evidence

Residuals/log/stack trace.

## Severity

Critical / High / Medium / Low.

## Suspected area

solver / cuda / verifier / api / db / ui.

## Regression?

Yes/No/Unknown.
```

Numerical bugs must include the model or a minimal reproducible model when possible.

---

# 31. CODE REVIEW PRIORITIES

Review order:

## Solver changes

1. mathematical correctness
2. stopping/status correctness
3. memory safety
4. tests
5. numerical stability
6. performance
7. style

## Backend

1. API contract
2. process safety
3. state correctness
4. persistence
5. error semantics
6. tests
7. style

## Frontend

1. correct state/status display
2. verification precedence
3. API schema consistency
4. failure/loading states
5. accessibility
6. visual quality

---

# 32. DEMO FREEZE

Before final presentation create:

```text
demo-freeze
```

or release candidate tag:

```text
v0.4.0-rc.1
```

After freeze:

Allowed:
- critical bug fixes
- typo fixes
- demo reliability improvements

Avoid:
- new algorithms
- architecture changes
- dependency upgrades
- UI redesign
- CUDA toolkit upgrades

---

# 33. FINAL RULE

The Git history should tell the story of a serious engineering project.

A judge, mentor, investor, or future maintainer should be able to see:

- what feature was added;
- why it was added;
- how it was tested;
- when numerical behavior changed;
- which release produced the demo.

Professional Git discipline is part of NIYAM-X's credibility.
