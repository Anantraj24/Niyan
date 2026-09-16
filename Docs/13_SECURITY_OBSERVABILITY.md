# NIYAM-X — Security, Reliability, and Observability

## 1. Threat model

P0 is local/offline, but uploaded model files are still untrusted input.

Risks:
- malformed huge input
- path traversal
- arbitrary CLI injection
- memory exhaustion
- runaway solver
- artifact overwrite
- corrupted solution

## 2. Required protections

- generate server-side IDs
- never trust uploaded filename as path
- store uploads under generated directory
- file size limit
- model dimension/nonzero limits
- `shell=False`
- whitelist solver CLI values
- explicit time limit
- artifact paths must remain under NIYAM_HOME
- no arbitrary script execution from model metadata

## 3. Model privacy

P0:
- no cloud upload
- no analytics network call required
- no external LLM
- local artifacts only

UI should be able to state:
`Model is processed locally by this NIYAM-X instance.`

## 4. Logs

Backend structured logs:
- timestamp
- level
- request_id
- model_id
- solve_id
- event
- duration

Native logs:
- build/version
- hardware
- algorithm
- warnings
- terminal status

## 5. Metrics

P0 internal metrics:
- API uptime
- active solve count
- queued solve count
- solve duration
- verifier duration
- solver exit code counts

No Prometheus required for hackathon.

## 6. Reproducibility

Flight Recorder records:
- model hash
- config
- solver version
- hardware
- seed if any randomized heuristic
- effective backend
- effective scaling

## 7. Reliability behavior

If GPU path fails before solve:
- attempt CPU fallback only if configured/allowed
- record fallback reason

If GPU fails mid-solve:
- P0 may terminate as handled failure rather than silently restart on CPU
- do not hide loss of state

## 8. Data integrity

Proof/solution artifacts include model hash.

Verifier rejects hash mismatch unless explicit override for debugging.
