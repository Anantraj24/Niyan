# NIYAM-X — UI/UX and Visual Design System

## 1. Design personality

NIYAM-X should feel like:
- industrial
- precise
- calm
- technical
- trustworthy
- high-information-density without clutter

It should NOT feel like:
- generic AI chatbot
- neon cyberpunk dashboard
- crypto product
- consumer finance app
- flashy landing page

## 2. Visual hierarchy

Priority:
1. current solve status
2. numerical correctness
3. business outcome
4. solver diagnostics
5. historical detail

Use space and typography before adding borders.

## 3. Color semantics

Use design tokens, not hardcoded component colors.

Suggested semantic tokens:

```text
--bg
--surface
--surface-raised
--text-primary
--text-secondary
--border
--accent
--success
--warning
--danger
--info
--chart-1
--chart-2
```

Status meaning:
- success: verified / optimal
- warning: feasible / time limit / elevated numerical risk
- danger: failed verification / crash / infeasible request
- info: running / queued / CPU-CUDA selection

Do not use red for ordinary high numerical risk if no actual failure occurred; use warning.

## 4. Typography

Use one highly readable UI family already available in the project/system.

Hierarchy:
- Page title: 24–28px
- Panel title: 16–18px
- Metric value: 24–36px
- Body: 14–16px
- Dense table: 13–14px
- Monospace: solver logs, hashes, scientific notation

Scientific notation should use tabular/monospace numbers where possible.

## 5. Spacing

Base unit: 4px.

Common:
- 8px compact
- 12px internal controls
- 16px cards
- 24px sections
- 32px major layout break

## 6. Component patterns

### Metric card
Contains:
- short label
- value
- unit
- optional small explanation
- no more than one status badge

### Status badge
Canonical labels:
- QUEUED
- RUNNING
- OPTIMAL
- FEASIBLE
- TIME LIMIT
- ITERATION LIMIT
- INFEASIBLE
- NUMERICAL FAILURE
- VERIFIED
- VERIFICATION FAILED

### Risk indicator
Use:
- LOW
- MEDIUM
- HIGH

Always pair with text.

### Technical table
- right-align numbers
- keep units in header
- preserve significant digits
- allow copy of hashes/IDs

### Disclosure
Advanced diagnostics belong in collapsible sections, not hidden permanently.

## 7. Workbench information architecture

Top-level user mental model:

```text
MODEL
  -> DIAGNOSE
  -> SOLVE
  -> CHANGE CONDITIONS
  -> PROVE
```

Use these as the visual flow.

## 8. Empty states

Examples:

X-Ray:
`Run Model X-Ray to inspect sparsity, coefficient scale, and formulation risk.`

Solve:
`No solve has been started for this model.`

Proof:
`Verification becomes available after a solution is produced.`

Benchmark:
`Run the benchmark suite to compare NIYAM CPU and CUDA backends.`

## 9. Running state

A solve screen must remain useful while running.

Show:
- elapsed time
- current iteration
- current residual
- latest objective
- backend
- stop button if supported

Do not show fake percentage complete because iterative optimization often has no reliable percent completion.

## 10. Failure UX

### Numerical failure
Headline:
`Solver stopped because numerical progress became unreliable.`

Show:
- last residual
- iteration
- scaling mode
- backend
- suggested next action from backend if available

### Verification failure
Headline:
`Solution failed independent verification.`

This must visually outrank the objective value.

### Solver process crash
Headline:
`Solver process exited unexpectedly.`

Show:
- exit code
- run ID
- link/button to local log

## 11. Responsive behavior

Primary target: laptop 1440px-ish width.

At narrower widths:
- left rail collapses
- tables scroll horizontally
- metric cards wrap
- charts remain at least 280px high

Mobile is not a P0 target.

## 12. Motion

Use minimal motion:
- panel transitions < 200ms
- running pulse only where useful
- no animated backgrounds
- convergence chart updates should not constantly rescale aggressively

## 13. Demo mode

Support a `?demo=1` optional mode that:
- opens seeded refinery model
- hides destructive/debug controls
- highlights primary flow
- does NOT change numerical data or fake results

Demo mode may simplify navigation only.

## 14. Key screen wireframe

```text
+------------------------------------------------------------------+
| NIYAM-X | Refinery LP / Synthetic | CUDA Ready | Run #A72        |
+----------+-------------------------------------------------------+
| Model    | MODEL X-RAY                                           |
| X-Ray    | [HIGH Numerical Risk] [99.95% sparse] [1e13 range]    |
| Autopilot|                                                       |
| Solve    | Issues                                                |
| What-if  | - poor scaling in 812 rows                            |
| Proof    | - 421 fixed variables                                |
| Runs     |                                                       |
|          | AUTOPILOT                                             |
|          | CUDA | Robust Scaling | Warm-start eligible           |
|          |                                                       |
|          | [Start Solve]                                         |
+----------+-------------------------------------------------------+
| API Connected | Solver v0.1.0 | RTX 5060 | No active warnings    |
+------------------------------------------------------------------+
```
