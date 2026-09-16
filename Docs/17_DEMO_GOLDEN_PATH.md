# NIYAM-X — Demo Golden Path

## 1. Goal

Three-minute deterministic story.

## 2. Preloaded model

`Synthetic Refinery Planning — Medium`

Visible label:
`Synthetic Demo Dataset`

## 3. Sequence

### 0:00 — Open Workbench
Say:
`This is not a modeling UI wrapped around an external optimizer. The solver core is NIYAM-X.`

### 0:15 — X-Ray
Show:
- variables
- constraints
- nonzeros
- coefficient range
- numerical risk

Say:
`Before solving, NIYAM-X inspects the mathematical structure and numerical risk.`

### 0:35 — Autopilot
Show CUDA + robust scaling.

Say:
`It chooses a numerical strategy based on the model and hardware; P0 uses deterministic rules, not an LLM.`

### 0:50 — Solve
Start real solve.

Show:
- convergence
- objective
- residuals
- elapsed time

### 1:20 — Result
Show:
- business objective
- allocation summary
- solver status

### 1:35 — Shock
Change crude price +8% and demand +4%.

Click:
`DeltaSolve`

Say:
`The structure is mostly unchanged, so NIYAM-X reuses compatible solver state instead of treating this as a brand-new problem.`

### 2:00 — Compare
Show before/after:
- objective
- iterations
- solve time
- key allocation

### 2:20 — Verify
Run independent verification.

Show:
`VERIFIED`

Say:
`The verifier does not rerun the optimizer. It independently reconstructs feasibility and the objective.`

### 2:40 — CPU vs CUDA
Open measured benchmark.

Say:
`GPU acceleration is used where the numerical workload benefits. CPU remains the correctness reference and fallback.`

### 2:55 — Close
`NIYAM-X diagnoses the model, chooses how to solve it, adapts when reality changes, and proves the returned decision can be trusted.`

## 4. Never do live

- install packages
- download benchmark
- change CUDA driver
- run unknown giant MIP
- rely on internet
- type long model input manually

## 5. Backup

If CUDA path fails:
- show hardware warning
- run CPU fallback
- be transparent

Never show prerecorded numbers as live.
