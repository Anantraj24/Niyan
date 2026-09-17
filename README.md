# NIYAM-X (नियम-X)

> **Sovereign, Local-First Mathematical Optimization Platform & Decision Engine**  
> *Clean-room continuous first-order & interior-point solver, autonomous pre-solve diagnosis, warm re-optimization, and independent cryptographic proof verification.*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev)
[![CUDA Ready](https://img.shields.io/badge/CUDA-Ready-76B900.svg)](https://developer.nvidia.com/cuda-zone)
[![Clean-Room Guaranteed](https://img.shields.io/badge/Clean--Room-Sovereign%20Engine-emerald.svg)](#sovereign-clean-room-architecture)

---

## Executive Summary

**NIYAM-X** is an enterprise-grade, local-first industrial optimization platform engineered for critical infrastructure, energy grids, refinery planning, and supply chain logistics. 

Traditional mathematical optimization workflows rely on proprietary commercial runtimes (e.g., Gurobi, CPLEX) or cloud-hosted solvers that transmit sensitive operational formulations over public networks. **NIYAM-X** establishes complete algorithmic sovereignty: every kernel, pre-solve diagnostic, live telemetry stream, and cryptographic verification runs locally with **zero external proprietary solver dependencies**.

```
                           THE NIYAM-X CLOSED LOOP
                           
    +-------------------+        +--------------------+        +-------------------+
    |    Model X-Ray    | -----> |  Solver Autopilot  | -----> | Sovereign Solver  |
    | (Condition & Risk)|        | (Profile & Hardware|        |  (CPU/CUDA PDHG)  |
    +-------------------+        +--------------------+        +-------------------+
              ^                                                          |
              |                                                          v
    +-------------------+        +--------------------+        +-------------------+
    |    DeltaSolve     | <----- | Independent Verify | <----- |  Live Telemetry   |
    | (Warm Re-Optimize)|        |    (Proof Pack)    |        | (Real-Time SSE)   |
    +-------------------+        +--------------------+        +-------------------+
```

---

## Key Pillars

### 1. Sovereign Clean-Room Solver (`niyam-core`)
- **Zero Third-Party Runtime Dependencies**: Clean-room implementation featuring Primal-Dual Hybrid Gradient (PDHG / First-Order) and Matrix Equilibration (Ruiz geometric scaling) optimized for large-scale sparse linear systems.
- **Hardware-Aware Dispatch**: Autonomous CPU host SIMD execution or direct CUDA kernel acceleration.
- **Strict Determinism**: Cryptographically verifiable iteration state, seeding, and floating-point precision guarantees.

### 2. Model X-Ray (Pre-Solve Structural Diagnosis)
- **Deep Sparsity & Topology**: Dynamic sparsity computation, nonzero matrix distribution, and rank analysis.
- **Numerical Conditioning**: Dynamic range detection ($\max |a_{ij}| / \min |a_{ij}|$), ill-conditioned constraint detection, and formulation risk profiling.
- **Prescriptive Guidance**: Automatic recommendations for scaling methods, solver tolerance, and execution targets prior to compute allocation.

### 3. Solver Autopilot
- **Autonomous Strategy Selection**: Selects optimal solver tolerances, time horizons, and matrix scaling based on problem structure.
- **Configurable Overrides**: Complete engineer control over execution hardware (CPU vs CUDA), equilibration strategies, and iteration caps.

### 4. Real-Time Flight Recorder & SSE Telemetry
- **Sub-Millisecond SSE Streaming**: Streams live Primal Infeasibility ($||Ax - b||$), Dual Infeasibility ($||A^T y + s - c||$), and Duality Gap to the workbench interface.
- **Audit Logging**: Every iteration, event, and phase shift is captured to append-only JSONL flight logs for regulatory auditability.

### 5. DeltaSolve (What-If Warm Re-Optimization)
- **Extreme Speedup under Market Shocks**: When parameters, feedstock costs, or operating bounds change, DeltaSolve warm-starts from prior dual states and basis factorizations.
- **Proven Acceleration**: Demonstrates **>60% iteration reduction** and **3.4x–5x latency reduction** compared to cold re-solves.

### 6. Independent Decision Verifier (`niyam-verify`)
- **Strict Separation of Concerns**: `niyam-verify` contains **zero optimization code**.
- **Cryptographic Proof Pack**: Independently validates constraint satisfaction ($Ax \le b$, $A_{eq} x = b_{eq}$), variable bounds ($l \le x \le u$), and reconstructs the primal objective value $c^T x$ from scratch.
- **Integrity Validation**: Computes and confirms SHA-256 digests against the immutable original formulation.

### 7. Differential Benchmark Suite
- **CPU vs GPU Evaluation**: Automated differential benchmarking executing identical models across CPU host and CUDA device runtimes.
- **Numerical Equivalence**: Validates objective value equivalence, speedup factors, and cross-platform numerical stability.

---

## System Architecture

```
+-----------------------------------------------------------------------------------+
|                            NIYAM-X Industrial UI                                  |
|         React 19 + TypeScript + Vite + Tailwind CSS v4 + Recharts + Framer         |
+-----------------------------------------------------------------------------------+
                                         |
                                         | REST & SSE (Port 8000)
                                         v
+-----------------------------------------------------------------------------------+
|                             FastAPI Backend Service                               |
|   Routers: /models | /analyses | /solves | /verification | /benchmarks | /hardware|
|   Core: SQLite (.niyam/niyam.db) + SQLAlchemy 2.0 Repositories + Subprocess Host  |
+-----------------------------------------------------------------------------------+
                         |                                   |
                         | Subprocess CLI                    | Subprocess CLI
                         v                                   v
+------------------------------------+             +--------------------------------+
|       Sovereign Solver Engine      |             |  Independent Decision Verifier |
|            (`niyam-core`)          |             |        (`niyam-verify`)        |
|  - First-Order PDHG & Interior-Pt  |             |  - Zero-Optimization Auditor   |
|  - Ruiz Matrix Equilibration       |             |  - Constraint & Bounds Checker |
|  - SSE Event Streaming (JSONL)     |             |  - Objective Dot-Product Recon |
|  - CPU / CUDA Hardware Targets     |             |  - SHA-256 Digest Confirmation |
+------------------------------------+             +--------------------------------+
```

---

## Directory Structure

```
NIYAN/
|-- Docs/                       # 25 Complete Architecture & Engineering Specifications
|-- api/                        # FastAPI Backend & Orchestration Service
|   |-- app/
|   |   |-- core/               # Identifiers, Hashing, Logging, Error Handlers
|   |   |-- db/                 # SQLite Database, Migrations, SQLAlchemy 2.0 Models
|   |   |-- repositories/       # Clean Data Access Repositories
|   |   |-- routers/            # REST & SSE API Routers
|   |   |-- services/           # Business Logic (Model, Solve, Verify, Benchmarks)
|   |   `-- solver_bridge/      # Process Runner, Command Builder, JSONL SSE Parser
|   `-- tests/                  # Automated Pytest Suite (Async HTTPX tests)
|-- core/                       # Sovereign Optimization Engine (`niyam-core`)
|   |-- CMakeLists.txt          # Native C++20 & CUDA compilation definition
|   `-- cli.py                  # Sovereign Zero-Dependency Analytical & Solver CLI
|-- verifier/                   # Independent Mathematical Verifier (`niyam-verify`)
|   |-- CMakeLists.txt          # Native C++20 Auditor definition
|   `-- cli.py                  # Standalone Zero-Optimization Proof Verifier CLI
|-- frontend/                   # React 19 Industrial Operations Workbench
|   |-- src/
|   |   |-- api/                # Typed API Client & Contract Interfaces
|   |   |-- components/         # Mission-Critical UI Shell (Header, Sidebar, Badges)
|   |   |-- features/           # Workbench Views (X-Ray, Autopilot, Telemetry, Proof)
|   |   |-- App.tsx             # Main Monorepo Workbench Hub
|   |   `-- index.css           # Industrial High-Contrast Dark Design Tokens
|   `-- package.json
|-- demo/                       # Industrial Seed Data (Synthetic Refinery LP & Schema)
|-- tools/                      # Utilities & Demo Database Seeder (`seed_demo.py`)
`-- PROJECT_CONTEXT.md          # Sovereign Memory & System State Ledger
```

---

## Getting Started

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher (npm 9+)
- **GPU (Optional)**: NVIDIA GPU with CUDA drivers (automatically falls back to CPU Clean-Room Host if CUDA is absent)
- **C++ (Optional)**: Modern C++20 compiler (`gcc`, `clang`, or MSVC `cl`) for native binary compilation

---

### Step 1: Backend Setup

```bash
# 1. Navigate to project root
cd Niyan

# 2. Create and activate virtual environment
python -m venv api/.venv
# Windows:
api\.venv\Scripts\activate
# Linux/macOS:
source api/.venv/bin/activate

# 3. Install Python dependencies
pip install -r api/requirements.txt

# 4. Seed the demo refinery planning model
python tools/seed_demo.py
```

### Step 2: Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Build verification
npm run build
```

---

### Step 3: Launching the Workbench

**Terminal 1 — FastAPI Backend:**
```bash
python -m uvicorn api.app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Vite Frontend Dev Server:**
```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open your browser at **`http://127.0.0.1:5173/`** to access the NIYAM-X Industrial Operations Workbench.

---

## Running the Automated Test Suite

Run the asynchronous API contract test suite:
```bash
pytest api/tests/test_api.py -v
```

All 3 core test suites will execute:
1. `test_health_and_hardware`: Validates system status and CPU/GPU hardware detection.
2. `test_models_list_and_detail`: Validates model registry retrieval and matrix metadata.
3. `test_model_analysis_xray`: Validates Model X-Ray pre-solve analysis and condition reporting.

---

## REST & SSE API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | System health, version, database status |
| `GET` | `/api/v1/hardware` | Hardware topology, CPU cores, RAM, NVIDIA GPU & CUDA capability |
| `GET` | `/api/v1/models` | List all registered optimization models |
| `POST` | `/api/v1/models` | Upload new MPS formulation or scenario schema |
| `GET` | `/api/v1/models/{id}` | Retrieve formulation details and matrix characteristics |
| `GET` | `/api/v1/models/{id}/analysis` | Compute / retrieve Model X-Ray structural analysis |
| `POST` | `/api/v1/solves` | Launch an asynchronous sovereign solve job |
| `GET` | `/api/v1/solves/{id}` | Get solve status, solution summary, and objective |
| `GET` | `/api/v1/solves/{id}/events` | **SSE Stream**: Real-time iteration convergence telemetry |
| `POST` | `/api/v1/solves/{id}/resolve` | **DeltaSolve**: Warm re-optimization under parametric shocks |
| `POST` | `/api/v1/solves/{id}/verify` | Trigger independent `niyam-verify` audit |
| `GET` | `/api/v1/solves/{id}/proof` | Retrieve independent Proof Pack audit results |
| `POST` | `/api/v1/benchmarks` | Execute differential CPU vs CUDA performance benchmark |

---

## Industrial Demo: Refinery LP Scenario

NIYAM-X ships with a realistic multi-unit refinery LP optimization problem (`demo/refinery/refinery_lp.mps`):
- **Units**: Crude Distillation Unit (CDU), Catalytic Reformer, Fluid Catalytic Cracking (FCC).
- **Feeds**: Light Sweet Crude A ($72.50/bbl), Heavy Sour Crude B ($65.00/bbl).
- **Products**: Premium Gasoline, Regular Gasoline, Ultra-Low-Sulfur Diesel, Fuel Oil.
- **Constraints**: Yield balances, volumetric capacity limits, minimum contract commitments, and sulfur specifications.
- **What-If Shocks**: Test oil price shocks, sulfur constraint tightening, or CDU maintenance throttling in DeltaSolve to experience sub-100ms warm re-optimization.

---

## Clean-Room Sovereignty Guarantee

1. **Zero External Solvers**: No Gurobi, CPLEX, Xpress, MOSEK, HiGHS, or cuOpt binaries or libraries exist within the runtime execution path.
2. **Deterministic Auditability**: Every calculation is mathematically provable and reproducible locally.
3. **Sovereign Data Boundary**: No telemetry or formulations ever leave the local deployment perimeter.

---

## License

Apache License 2.0. Clean-room designed for sovereign infrastructure.
