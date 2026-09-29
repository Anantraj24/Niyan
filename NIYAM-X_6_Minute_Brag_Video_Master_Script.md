# NIYAM-X — 6-Minute Brag Video Master Script

## Purpose

Create a **6-minute hackathon presentation video** for **NIYAM-X**, using Brag's maximum practical scene length of approximately **25 seconds per generated clip**.

- Total target duration: **6:00**
- Number of clips: **15**
- Target clip duration: **24–25 seconds each**
- Each clip must connect visually and narratively to the next.
- The video must feel like **one continuous professional product demonstration**, not 15 unrelated AI clips.
- Use the provided NIYAM-X documentation and PPT as the source of truth.
- Do **not** invent benchmark results, speedups, deployments, customers, or capabilities that are not supported by the documentation.
- Prototype/example values such as objective values, iteration counts, residuals, and re-optimization times should be presented as **prototype/demo values** unless actual measured results are available.
- Keep the narration continuous. **No intentional silent gaps, pauses, filler, or blank frames.**
- Voice: confident, technical, clear, competition-ready.
- Visual style: premium dark industrial technology, black/charcoal interface, restrained blue/green accents, clean typography, realistic refinery/power/logistics imagery, sophisticated data visualization.
- Avoid excessive sci-fi effects. The system should look like a serious industrial optimization platform.

---

# GLOBAL BRAG INSTRUCTIONS

## Visual continuity

Maintain the same:
- NIYAM-X logo
- dashboard design
- typography
- color system
- refinery/model identity
- UI layout language
- mathematical notation
- animation style

The primary product interface should remain recognizable throughout.

Use smooth transitions:
- data flow
- camera push-ins
- panel-to-panel transitions
- graph transformations
- architecture layers assembling
- model state changing from OLD to NEW

Do not randomly redesign the UI between clips.

## Narration

Narration must be:
- one continuous professional voice
- medium-fast but understandable
- technically precise
- no exaggerated marketing claims
- no fake quotations
- no unnecessary introductions
- no "welcome to", "in this video", or generic filler

The narrator should explain **what the viewer is seeing and why it matters**.

## Important terminology

Use these exact names consistently:

- **NIYAM-X**
- **Model X-Ray**
- **Model Fingerprint**
- **Solver Autopilot**
- **NIYAM-X Core**
- **DeltaSolve**
- **Scenario Analysis / Scenario Swarm**
- **Proof Pack**
- **Independent Verifier**
- **Flight Recorder / Telemetry**
- **CPU Backend**
- **CUDA GPU Backend**
- **PDHG**
- **LP**
- **MILP**
- **QP**
- **CSR / CSC sparse matrices**

## Technical architecture to communicate

The documented architecture is:

Input Model
→ Model IR / validation
→ Model X-Ray
→ Model Fingerprint
→ Solver Autopilot
→ NIYAM-X Core
→ CPU/CUDA execution
→ Solution
→ DeltaSolve / scenarios
→ Proof Pack
→ Independent Verifier

Supporting layers:
- FastAPI / Uvicorn
- SQLite / SQLAlchemy
- Artifact filesystem
- SSE / JSONL telemetry and logs
- React / TypeScript / Vite / Tailwind / Recharts / Lucide React

The solver itself should be visually distinguished from the API and frontend:
**C++/CUDA performs numerical computation; FastAPI orchestrates; React visualizes.**

---

# CLIP 01 — 00:00–00:25
## Title: The Industrial Optimization Problem

### Visual direction

Open on a realistic industrial montage:
- refinery
- power infrastructure
- logistics network
- manufacturing floor
- supply-chain routes

Overlay mathematical optimization variables, constraints, graphs, and resource-allocation flows.

Transition into a dark NIYAM-X title card.

On-screen text:

**NIYAM-X**
**Sovereign Adaptive Optimization Engine**

### Voiceover

> Modern industries constantly make complex optimization decisions: how much raw material to buy, how to allocate limited resources, how to schedule production, and how to react when prices, demand, or capacity change. These decisions can involve large mathematical models with thousands of variables and constraints. Reliable optimization is critical to industrial planning. NIYAM-X is our proposed sovereign optimization engine for this challenge.

### Transition

Industrial data streams converge into one optimization model.

---

# CLIP 02 — 00:25–00:50
## Title: The Core Problem and Our Approach

### Visual direction

Show a conventional optimization pipeline becoming a NIYAM-X pipeline.

First show:

**MODEL → SOLVER → ANSWER**

Then transform it into:

**DIAGNOSE → SOLVE → ADAPT → VERIFY**

Show the four stages as large animated blocks.

### Voiceover

> NIYAM-X is designed around a complete optimization workflow, not a simple black-box solver. Instead of only receiving a model and returning an answer, the system first diagnoses its mathematical structure, builds a Model Fingerprint, selects an appropriate solving configuration, and solves using its own optimization core. When conditions change, it can adapt the solution, compare scenarios, and independently verify the result.

### On-screen

**Diagnose. Solve. Adapt. Verify.**

---

# CLIP 03 — 00:50–01:15
## Title: Model Input

### Visual direction

Show the dashboard and an industrial refinery model being uploaded.

Display:

```text
LOAD MODEL

refinery_demo.mps

Variables       25,000
Constraints     18,000
Non-zeros       210,000

JSON | LP | MPS
```

Show the model becoming an internal structured representation.

### Voiceover

> The process begins with the optimization model. NIYAM-X is designed to accept standard representations including JSON, LP, and MPS. For our industrial demonstration, we use a refinery-style model containing variables, constraints, and a large sparse coefficient structure. Before optimization begins, the model is validated and converted into an internal representation, giving the rest of the system a consistent foundation for analysis, solving, and verification.

### Transition

The uploaded model zooms into its coefficient matrix.

---

# CLIP 04 — 01:15–01:40
## Title: Model X-Ray

### Visual direction

Show Model X-Ray dashboard.

Display:

```text
MODEL X-RAY

Numerical Risk        HIGH
Coefficient Range    1e-8 → 1e7
Sparsity              99.95%
Fixed Variables       421
Poorly Scaled Rows    817
```

Show radar chart for:
Scaling, Sparsity, Structure, Numerical Risk, Redundancy, Bounds.

### Voiceover

> NIYAM-X does not immediately start solving. Model X-Ray first examines the mathematical model. It measures properties such as sparsity, coefficient range, fixed variables, poorly scaled rows, bounds, structure, and numerical risk. This analysis exposes characteristics that can affect numerical behavior before an algorithm is selected. The result is a detailed diagnostic view that helps the system understand what it is about to solve.

### Transition

X-Ray metrics collapse into a fingerprint.

---

# CLIP 05 — 01:40–02:05
## Title: Model Fingerprint and Autopilot

### Visual direction

Show fingerprint metrics:

```text
MODEL FINGERPRINT

Density
Integer Ratio
Coefficient Spread
Equality Ratio
Bound Density
Block Structure
Degeneracy Risk
```

Then show Autopilot selecting:

```text
Backend      GPU / CUDA
Algorithm    PDHG
Scaling      Robust
Precision    Mixed
Warm Start   Enabled
```

### Voiceover

> These diagnostics become the Model Fingerprint: a compact description of the model's structure, density, integer ratio, coefficient spread, equality ratio, bounds, block structure, and potential degeneracy. Solver Autopilot uses this fingerprint to select an appropriate configuration, including algorithm, scaling, execution backend, precision, and warm-start behavior. In the prototype, this selection is deterministic and rule-based, making the decision explainable and reproducible.

### Transition

Configuration flows directly into the solver core.

---

# CLIP 06 — 02:05–02:30
## Title: NIYAM-X Solver Core

### Visual direction

Build the architecture visually:

```text
MODEL IR
   ↓
SPARSE MATRIX
   ↓
NIYAM-X CORE
   ↓
CPU Backend ─── CUDA Backend
   ↓
PDHG
```

Animate sparse matrix-vector multiplication and transpose multiplication.

### Voiceover

> At the center is the NIYAM-X solver core. The prototype begins with Linear Programming and sparse CSR and CSC matrix operations. The initial LP method uses Primal-Dual Hybrid Gradient, or PDHG. Its main operations, including matrix-vector multiplication, transpose multiplication, vector updates, projections, and reductions, map naturally to accelerated computation. The architecture supports a CUDA GPU backend while keeping CPU execution available as a fallback.

### Transition

Matrix operations accelerate toward the GPU.

---

# CLIP 07 — 02:30–02:55
## Title: GPU Execution and Live Solving

### Visual direction

Show CUDA GPU visualization and the live solver dashboard.

Display:

```text
LIVE SOLVER

Iteration
Objective
Primal Residual
Dual Residual

CONVERGENCE
```

Animate convergence graph downward.

### Voiceover

> During optimization, NIYAM-X continuously tracks the solver state instead of hiding the computation behind a single progress bar. The live dashboard exposes iterations, objective value, primal residual, dual residual, and convergence behavior. These signals help show whether the numerical process is progressing toward a feasible solution. GPU execution accelerates sparse computation, while the same solver architecture can fall back to the CPU when required.

### Transition

Convergence reaches the solution state.

---

# CLIP 08 — 02:55–03:20
## Title: Industrial Solution

### Visual direction

Show the refinery solution as a clear operational dashboard.

Display:
- optimized crude allocation
- production quantities
- resource utilization
- objective value
- feasibility status

Then show:

**SOLUTION READY**

### Voiceover

> Once the solver reaches its stopping conditions, NIYAM-X produces optimized decision variables, the objective value, solver statistics, and exportable artifacts. In the refinery scenario, those decisions can represent an optimized production or blending plan while respecting the model's constraints. The result is not the end of the workflow, because industrial planning is dynamic. The next question is what happens when market conditions change.

### Transition

A market alert appears.

---

# CLIP 09 — 03:20–03:45
## Title: Reality Changes

### Visual direction

Show:

```text
MARKET UPDATE

Crude A Price      +8%
Demand             +4%
Capacity           No Change
```

Show the old solution fading into a new scenario.

### Voiceover

> Now we introduce a realistic scenario change. Crude A price increases by eight percent and demand increases by four percent, while capacity remains unchanged. A conventional static workflow could require the modified problem to be solved again from scratch. NIYAM-X is designed for this situation through DeltaSolve, which carries useful information from the previous optimization state into the updated problem instead of discarding the work already performed.

### Transition

Old primal and dual states flow into DeltaSolve.

---

# CLIP 10 — 03:45–04:10
## Title: DeltaSolve

### Visual direction

Show:

```text
PREVIOUS STATE
Primal State
Dual State
Scaling
Structure
       ↓
DELTASOLVE
       ↓
UPDATED SOLUTION
```

Then show the plan changing.

### Voiceover

> DeltaSolve is NIYAM-X's warm re-optimization layer. It can reuse the previous primal and dual states, scaling information, model structure, and other relevant solver state. The changed parameters are incorporated into the updated scenario, and the solver starts from an informed state. This design is intended for changing prices, demand, capacity, availability, and other operational parameters that can alter an existing optimization plan.

### Transition

One updated scenario branches into many.

---

# CLIP 11 — 04:10–04:35
## Title: Scenario Analysis

### Visual direction

Show a scenario grid:

```text
PRICE × DEMAND × CAPACITY

Scenario A
Scenario B
Scenario C
Scenario D
...
```

Animate multiple scenario branches and compare objective/convergence.

### Voiceover

> The same warm-state approach can be extended into scenario analysis and Scenario Swarm. Instead of evaluating only one future condition, NIYAM-X can explore multiple combinations of price, demand, capacity, outages, and operational assumptions. Shared model structure and solver state can support these comparisons. Planners can examine different objectives, convergence behavior, and decision stability to understand how sensitive a proposed operating plan is to future changes.

### Transition

Scenario results merge into a decision-stability visualization.

---

# CLIP 12 — 04:35–05:00
## Title: Decision Stability, Anytime Mode and Telemetry

### Visual direction

Show:
- solution stability chart
- scenario comparison
- solver telemetry
- iteration history
- Flight Recorder / JSONL logs

Then show an Anytime-style progress indicator.

### Voiceover

> Around the solver, NIYAM-X provides telemetry and decision-analysis capabilities. Scenario results can be compared for objective stability and operational sensitivity. The Flight Recorder captures solver history and structured telemetry for replay, debugging, and analysis. An Anytime-style workflow can expose the best validated solution available so far if computation is interrupted. Precision escalation and numerical monitoring provide additional safeguards when difficult models require greater numerical care.

### Transition

Telemetry records become a formal proof package.

---

# CLIP 13 — 05:00–05:25
## Title: Proof Pack and Independent Verification

### Visual direction

Show verification screen:

```text
NIYAM-X VERIFICATION REPORT

✓ Constraints satisfied
✓ Variable bounds satisfied
✓ Objective reconstructed
✓ Primal residual within tolerance
✓ Dual residual within tolerance

VERIFIED
```

Show an independent verifier process visually separated from the solver.

### Voiceover

> Trust is a separate layer in NIYAM-X. After solving, the system generates a Proof Pack containing solution evidence and numerical checks. An Independent Verifier then checks feasibility, variable bounds, objective reconstruction, primal residuals, dual residuals, and other consistency information without simply trusting the optimizer's status flag. This separation is designed to make optimization results more auditable, reproducible, and easier to validate before they influence an industrial decision.

### Transition

Verification result becomes a benchmark report.

---

# CLIP 14 — 05:25–05:50
## Title: Validation, Feasibility, Technology and Scale

### Visual direction

Rapid but readable montage:

```text
BENCHMARKS
Netlib | MIPLIB | Industrial Models

TECH
C++20 | CUDA
FastAPI | SQLite
React | TypeScript

DOMAINS
Refinery
Energy
Logistics
Manufacturing
```

Then show roadmap:

```text
LP → GPU → X-Ray/Autopilot
→ DeltaSolve/Scenarios → MILP/Benchmarking
```

### Voiceover

> NIYAM-X is designed for incremental validation and scale. The roadmap starts with a verified LP core, sparse computation, and basic verification, then adds CUDA acceleration, Model X-Ray and Autopilot, DeltaSolve and scenarios, and broader MILP support with benchmarking. Validation can include Netlib, MIPLIB, Mittelmann, and industrial-style models. The stack combines C++20 and CUDA for computation, FastAPI for orchestration, and React with TypeScript for visualization.

### Transition

All layers assemble into one complete architecture.

---

# CLIP 15 — 05:50–06:00
## Title: Final Message

### Visual direction

Show the complete NIYAM-X pipeline:

```text
INPUT
 ↓
MODEL X-RAY
 ↓
AUTOPILOT
 ↓
NIYAM-X CORE
 ↓
DELTASOLVE
 ↓
SCENARIOS
 ↓
PROOF PACK
 ↓
INDEPENDENT VERIFIER
```

End on NIYAM-X logo.

On-screen:

**NIYAM-X**
**DIAGNOSE. SOLVE. ADAPT. VERIFY.**

### Voiceover

> NIYAM-X diagnoses the model, solves it intelligently, adapts as reality changes, and independently verifies the decision — a sovereign optimization engine for modern industry.

### END SCREEN

**NIYAM-X**  
*Sovereign Adaptive Optimization Engine*

**Smart India Hackathon 2026**  
**Problem Statement 26119**  
**Team TRINETRA 05**

---

# BRAG GENERATION RULES

## 1. Generate exactly 15 clips

Each clip should be approximately 24–25 seconds.

Do not compress multiple clips into one generated scene.

## 2. Preserve continuity

Clip N+1 must visually begin from the state established at the end of Clip N.

Examples:

- Clip 3 ends with the matrix → Clip 4 begins by analyzing that matrix.
- Clip 4 ends with X-Ray metrics → Clip 5 turns those metrics into the fingerprint.
- Clip 5 ends with Autopilot configuration → Clip 6 feeds that configuration into the core.
- Clip 8 ends with an optimized plan → Clip 9 changes the real-world parameters.
- Clip 10 ends with a new solution → Clip 11 branches it into scenarios.
- Clip 12 ends with telemetry → Clip 13 converts evidence into Proof Pack.
- Clip 13 ends verified → Clip 14 benchmarks and contextualizes the system.
- Clip 14 ends with the complete architecture → Clip 15 delivers the final message.

## 3. UI consistency

Every NIYAM-X dashboard should use the same:
- sidebar
- top navigation
- cards
- typography
- spacing
- graph style
- status indicators
- numerical formatting

Do not create a completely different product UI for every clip.

## 4. Industrial realism

When showing refinery operations:
- use realistic refinery equipment
- pipelines
- tanks
- process units
- control-room dashboards
- industrial data
- production planning

Do not make the refinery look like a fictional spaceship.

## 5. Mathematical realism

Show authentic-looking:
- sparse matrices
- optimization graphs
- residual curves
- vectors
- constraint structures
- solver iterations
- CPU/GPU execution
- model fingerprints

Avoid random decorative equations that have no connection to the narration.

## 6. No unsupported claims

Do NOT show:
- "10× faster"
- "100× faster"
- "beats Gurobi"
- "beats every commercial solver"
- "production deployed"
- "guaranteed optimal"
- fabricated customers
- fabricated benchmark scores
- fabricated cost savings

unless the team has actual evidence for those claims.

## 7. Prototype values

The documentation contains example prototype values such as:
- 25,000 variables
- 18,000 constraints
- 210,000 nonzeros
- 99.95% sparsity
- coefficient range 1e-8 to 1e7
- 421 fixed variables
- 817 poorly scaled rows
- ₹31.82 Cr and ₹29.91 Cr example objectives
- residual values
- example DeltaSolve timings

Use these only as **prototype/demo visualization values** unless the actual implementation produces the same measurements.

## 8. Narration timing

Target approximately **140–150 spoken words per minute** for the expanded narration. The 25-second clips should generally carry about 58–65 words; the final 10-second clip should stay around 24–26 words.

Keep the voice natural and clear. If Brag's voice engine runs slightly long, reduce animation density or trim a few visual beats before removing important technical narration.

If Brag's generated voice runs long, reduce visual animation density before removing important technical narration.

## 9. Camera language

Use:
- slow push-in for important concepts
- controlled zoom into UI
- smooth lateral movement across architecture
- macro view of sparse matrices
- GPU computational visualization
- clean graph animations

Avoid:
- constant camera shaking
- random rotations
- excessive lens flares
- gaming-style explosions
- cartoon effects

## 10. Music

Use subtle cinematic technology/industrial background music.

Music must remain below narration.

Increase intensity slightly during:
- solver start
- DeltaSolve
- verification
- final architecture reveal

Never let music overpower technical narration.

---

# COMPLETE STORY ARC

The six-minute video must answer these questions in order:

1. **What problem exists?**
2. **Why does optimization matter?**
3. **What is NIYAM-X?**
4. **How does the user provide a model?**
5. **How does Model X-Ray analyze it?**
6. **What is the Model Fingerprint?**
7. **How does Solver Autopilot decide what to use?**
8. **What is the NIYAM-X solver core?**
9. **Why sparse computation and GPU execution?**
10. **How is convergence monitored?**
11. **What does the industrial solution look like?**
12. **What happens when reality changes?**
13. **How does DeltaSolve work?**
14. **How does scenario analysis work?**
15. **How are decisions analyzed for stability?**
16. **How are telemetry and solver history captured?**
17. **What is the Proof Pack?**
18. **How does independent verification work?**
19. **How is the system benchmarked?**
20. **What technologies implement it?**
21. **Where can it be applied?**
22. **How is it deployed and scaled?**
23. **What is the development roadmap?**
24. **What is the broader industrial/strategic impact?**
25. **What is the final NIYAM-X message?**

Nothing above should be omitted from the six-minute story.

---

# FINAL QUALITY CHECK BEFORE EXPORT

Verify that the final video:

- [ ] Is approximately 6 minutes.
- [ ] Contains 15 connected clips.
- [ ] Has continuous narration.
- [ ] Clearly introduces the SIH problem.
- [ ] Shows the refinery industrial example.
- [ ] Demonstrates Model X-Ray.
- [ ] Demonstrates Model Fingerprint.
- [ ] Demonstrates Solver Autopilot.
- [ ] Explains the NIYAM-X Core.
- [ ] Shows CPU and CUDA execution.
- [ ] Explains sparse computation.
- [ ] Shows live convergence.
- [ ] Shows the optimization result.
- [ ] Demonstrates the price/demand change.
- [ ] Demonstrates DeltaSolve.
- [ ] Explains warm-start/state reuse.
- [ ] Shows scenario analysis.
- [ ] Mentions decision stability/analysis.
- [ ] Shows telemetry/Flight Recorder concept.
- [ ] Shows Proof Pack.
- [ ] Shows independent verification.
- [ ] Covers benchmarking.
- [ ] Covers the technology stack.
- [ ] Covers industrial application domains.
- [ ] Covers feasibility and CPU fallback.
- [ ] Covers the development roadmap.
- [ ] Covers the broader impact.
- [ ] Ends with NIYAM-X branding.
- [ ] Contains no unsupported performance claims.
- [ ] Does not accidentally present example numbers as measured benchmark results.
- [ ] Maintains identical UI/product identity across all clips.

# FINAL TAGLINE

**NIYAM-X — Diagnose the model. Solve intelligently. Adapt to reality. Verify the decision.**
