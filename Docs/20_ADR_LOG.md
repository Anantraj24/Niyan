# NIYAM-X — Architecture Decision Record Log

Use this file for architecture changes that affect multiple layers.

---

## ADR-001 — Native solver as separate process

Status: Accepted

Decision:
FastAPI launches `niyam` and `niyam-verify` as native processes instead of embedding solver mathematics in Python.

Reason:
- isolation
- clean ownership
- easier debugging
- preserves CLI
- prevents backend from becoming solver

---

## ADR-002 — SQLite + filesystem

Status: Accepted

Decision:
Use SQLite for metadata and filesystem for large artifacts.

Reason:
- local-first
- offline
- simple
- avoids huge blobs/event streams in DB

---

## ADR-003 — SSE for solve telemetry

Status: Accepted

Decision:
Use Server-Sent Events from backend to browser for one-way live solver telemetry.

Reason:
- simpler than WebSockets
- solver progress is primarily server -> client
- reconnect semantics are sufficient

---

## ADR-004 — Deterministic Autopilot

Status: Accepted

Decision:
P0 solver configuration is rule-based, not ML/LLM.

Reason:
- inspectable
- testable
- no training corpus required
- avoids buzzword complexity

---

## ADR-005 — CPU reference, CUDA acceleration

Status: Accepted

Decision:
CPU backend remains the correctness reference. CUDA backend implements equivalent numerical primitives.

Reason:
- testing
- fallback
- trustworthy GPU claims

---

## ADR TEMPLATE

### ADR-XXX — Title

Status: Proposed | Accepted | Rejected | Superseded

Context:

Decision:

Alternatives:

Consequences:

Affected contracts/files:
