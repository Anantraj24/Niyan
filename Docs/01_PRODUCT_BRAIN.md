# NIYAM-X — Product Brain

## 1. Product thesis

Industrial optimization should not be a black box that merely returns an objective value. NIYAM-X is designed to expose the numerical condition of a model, choose a suitable solving configuration, run an owned solver kernel, adapt when operating conditions change, and independently verify the returned result.

### Core narrative

**Diagnose -> Configure -> Solve -> Adapt -> Prove**

## 2. Primary users

### Optimization / OR engineer
Needs:
- model statistics
- residuals
- convergence
- solver configuration
- reproducibility
- detailed failure reason

### Operations planner
Needs:
- business-facing objective
- changed plan after price/demand/capacity shock
- solve status
- confidence that constraints are satisfied
- fast re-solve

### Technical judge / architect
Needs:
- evidence solver is from scratch
- clear CPU/GPU split
- measured performance
- numerical honesty
- verifier independence
- benchmark methodology

### Decision maker
Needs:
- why this matters
- sovereign control
- offline/on-prem path
- measurable impact
- understandable what-if demo

## 3. Key product modules

### 3.1 Model X-Ray
Analyzes:
- variables
- constraints
- nonzeros
- density
- coefficient range
- integer/binary ratio
- fixed variables
- empty/singleton rows
- numerical risk heuristics
- scaling risk
- structure summary

X-Ray is analytical only. It does not solve or mutate the model.

### 3.2 Solver Autopilot
Deterministic P0 rules choose:
- CPU vs CUDA
- scaling mode
- tolerances
- iteration/time budget
- warm-start eligibility

Every decision includes a human-readable reason.

### 3.3 Solver
P0 continuous LP path:
- presolve
- scaling
- CPU or CUDA backend
- PDHG-style continuous solver
- residual monitoring
- honest statuses

P0/P1 integer path:
- branch-and-bound for small MILPs

### 3.4 DeltaSolve
If matrix structure is unchanged and only objective/RHS/bounds change:
- reuse matrix
- reuse compatible scaling
- warm-start x/y
- report cold-vs-warm metrics

### 3.5 Proof Pack + verifier
Independent executable checks:
- bounds
- constraints
- objective reconstruction
- integrality when applicable
- residuals
- dual conditions where available

### 3.6 Flight Recorder
Every solve records:
- model hash
- solver version
- hardware
- X-Ray
- Autopilot
- solve config
- solve status
- runtime
- residuals
- proof status

## 4. The P0 user story

1. User opens workbench.
2. User loads a refinery demo model.
3. X-Ray immediately shows model size and numerical risk.
4. Autopilot explains why CUDA/CPU and scaling mode were selected.
5. User starts solve.
6. UI streams convergence.
7. Final objective and residuals appear.
8. User changes crude price/demand/capacity.
9. DeltaSolve reuses previous state.
10. New plan is shown with changed objective and changed allocations.
11. User runs verification.
12. Proof panel shows VERIFIED with residuals.
13. User opens benchmark view and compares NIYAM CPU vs CUDA.

## 5. What the UI must never imply

Never show:
- `OPTIMAL` unless backend reports a justified optimal status.
- `VERIFIED` unless `niyam-verify` passes.
- fake live solver progress.
- fake GPU utilization.
- hardcoded speedup.
- fake industrial data presented as real.
- "AI" or "autonomous" labels for deterministic heuristics.

## 6. Product success metrics

P0 demo success:
- 100% offline
- 3 pre-tested models load reliably
- solve result is independently verified
- CPU fallback works
- CUDA path is real
- what-if update produces a real re-solve
- benchmark shows actual measured values
- UI does not crash if verification fails

## 7. Differentiation

Do not sell "GPU" alone.

Sell the combination:
- clean-room solver
- numerical diagnosis
- explicit solver strategy
- rapid re-optimization
- independent verification
- local/offline execution
- auditable run history

## 8. Demo domain

Primary demo domain: synthetic refinery planning/blending.

Example adjustable inputs:
- crude A price
- crude B price
- diesel demand
- gasoline demand
- CDU capacity

Example outputs:
- profit/day
- crude mix
- unit utilization
- demand satisfaction
- active constraints
- feasibility/verification status

Synthetic demo data must always be labeled `Synthetic refinery model`.
