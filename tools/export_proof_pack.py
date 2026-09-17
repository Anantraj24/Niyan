#!/usr/bin/env python3
"""
NIYAM-X — Independent Proof Pack Exporter
Extracts and packages an immutable, zero-optimizer cryptographic Proof Pack
for regulatory compliance, third-party audit, or mathematical certification.
"""

import argparse
import json
import sys
import zipfile
from pathlib import Path

# Add workspace root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from api.app.db.session import SessionLocal, init_db
from api.app.services.verify_service import VerifyService
from api.app.repositories.solve_repository import SolveRepository
from api.app.repositories.model_repository import ModelRepository


def main():
    parser = argparse.ArgumentParser(
        description="Export an independent mathematical Proof Pack from NIYAM-X."
    )
    parser.add_argument("--solve-id", "-s", required=True, help="Job ID of the solved model (slv_...).")
    parser.add_argument("--output", "-o", default=None, help="Output zip file path.")

    args = parser.parse_args()

    init_db()
    db = SessionLocal()
    try:
        verify_service = VerifyService(db)
        solve_repo = SolveRepository(db)
        model_repo = ModelRepository(db)

        solve = solve_repo.get_solve(args.solve_id)
        if not solve:
            print(f"[ERROR] Solve job not found: {args.solve_id}")
            sys.exit(1)

        proof = verify_service.get_verification(args.solve_id)
        if not proof:
            print(f"[ERROR] No verification proof found for job {args.solve_id}. Run verify first.")
            sys.exit(1)

        version = model_repo.get_version(solve.model_version_id)
        model = model_repo.get_model(version.model_id) if version else None
        model_name = model.display_name if model else solve.model_version_id

        output_path = Path(args.output or f"proof_pack_{args.solve_id}.zip").resolve()

        # Build certificate manifest
        certificate = {
            "platform": "NIYAM-X Sovereign Mathematical Optimization",
            "standard": "SOVEREIGN-PROOF-PACK-V1",
            "solve_id": args.solve_id,
            "verification_id": proof.verification_id,
            "model_id": version.model_id if version else None,
            "model_name": model_name,
            "model_sha256": version.sha256 if version else "unknown",
            "hash_matches": proof.model_hash_match,
            "verdict": proof.verdict,
            "max_primal_violation": proof.max_primal_violation,
            "max_bound_violation": proof.max_bound_violation,
            "max_integrality_violation": proof.max_integrality_violation,
            "objective_error": proof.objective_error,
            "engine_guarantee": "Clean-Room Zero-Optimizer Independent Verification",
            "verified_at": proof.completed_at.isoformat() if proof.completed_at else None
        }

        # Create zip bundle
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("CERTIFICATE.json", json.dumps(certificate, indent=2))
            
            # Add solution JSON if it exists
            sol_path = WORKSPACE_ROOT / ".niyam" / "artifacts" / "solves" / args.solve_id / "solution.json"
            if sol_path.exists():
                zf.write(sol_path, arcname="solution.json")

            # Add proof JSON if it exists
            prf_path = WORKSPACE_ROOT / ".niyam" / "artifacts" / "solves" / args.solve_id / "proof.json"
            if prf_path.exists():
                zf.write(prf_path, arcname="proof_details.json")

        print(f"[SUCCESS] Sovereign Proof Pack exported successfully:")
        print(f"  Destination: {output_path}")
        print(f"  Verdict:     {proof.verdict}")
        print(f"  SHA-256:     {version.sha256 if version else 'unknown'}")
        print(f"  Max Infeas:  {proof.max_primal_violation:.2e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
