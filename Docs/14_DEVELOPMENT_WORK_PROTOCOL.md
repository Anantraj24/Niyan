# NIYAM-X — Engineering & Development Protocol

## 1. Purpose

Maintain rigorous architectural discipline, prevent scope creep, and ensure repeatable, high-reliability development across the NIYAM-X platform.

## 2. Context Loading Protocol

At the start of any new feature or module work:

Core Reference Documents:
- `00_START_HERE.md` — Project mission, architectural boundaries, and conventions
- `01_PRODUCT_BRAIN.md` — Optimization engine thesis and mathematical modules
- `02_SYSTEM_ARCHITECTURE.md` — Monolith structure, IPC bridges, and process boundaries
- `14_DEVELOPMENT_WORK_PROTOCOL.md` — This engineering protocol

Reference task-specific documents only as needed for the feature area. Avoid scanning irrelevant subsystems unless tracing cross-cutting bugs.

## 3. File Ownership & Boundary Rules

Consult `15_FILE_OWNERSHIP_MAP.md`.

Modify only files within your assigned subsystem:
- Frontend features (`frontend/src/features/`, `frontend/src/components/`)
- API and business logic (`api/app/routers/`, `api/app/services/`)
- Optimization core & verification (`core/`, `verifier/`)

Do not cross subsystem boundaries without coordinating schema contracts.

## 4. Pre-Implementation Review

Before writing code for complex tasks, confirm:
- Target objective and user requirement
- Design specifications and contract definitions
- Specific files to be touched
- Potential regressions or numerical accuracy risks

## 5. Implementation Rules

Strict engineering guidelines:
- Zero unapproved external dependencies
- Do not refactor unrelated modules in a feature branch
- Do not modify canonical optimization domain terms
- Keep API schemas strictly synchronized with contract specifications
- Ensure database schema updates maintain forward/backward compatibility
- Preserve native protocol test fixtures

## 6. Contract Modifications

If an architectural contract change is required:
1. Document the rationale in `20_ADR_LOG.md` (Architecture Decision Record).
2. Detail the current state, proposed change, business justification, and migration path.
3. Update corresponding schema contracts and documentation in the same pull request.

## 7. Quality & Completion Criteria

Every pull request must document:
- Changed files and rationale
- Unit and integration tests executed
- Build and bundle verification status
- Cryptographic verifier integrity confirmation
- Updated documentation

## 8. Sovereign Clean-Room & Reliability Standard

- Mocks are restricted to unit test suites.
- The production user interface must always reflect actual live solver state and telemetry.
- If backend services or hardware acceleration are offline, present explicit diagnostics rather than simulated fallbacks.
- Sovereign clean-room principle: Zero proprietary third-party commercial solver dependencies in runtime.

## 9. Stop & Clarification Conditions

Halt and clarify before proceeding if:
- Mathematical formulations or numerical tolerances are ambiguous
- API specifications conflict with existing database records
- Verifier audit requirements are unclear
- A requested change violates the clean-room sovereign rule
