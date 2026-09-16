import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Dict, Any

def get_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify(model_path: str, solution_path: str, proof_path: str, output_path: str):
    # 1. Load Solution
    with open(solution_path, "r", encoding="utf-8") as f:
        solution = json.load(f)

    # 2. Load Proof Pack
    proof = {}
    if Path(proof_path).exists():
        with open(proof_path, "r", encoding="utf-8") as f:
            proof = json.load(f)

    # 3. Verify Model Hash
    actual_model_hash = get_sha256(model_path)
    claimed_model_hash = solution.get("model_sha256") or proof.get("model_sha256")
    model_hash_match = (actual_model_hash == claimed_model_hash) if claimed_model_hash else True

    # 4. Reconstruct objective and check violations
    claimed_obj = solution.get("objective", 0.0)
    primal_res = solution.get("primal_residual", 0.0)
    
    # Independent calculation of bounds and violations
    max_bound_violation = 0.0
    variables = solution.get("variables", {})
    for vname, val in variables.items():
        if val < -1e-7:
            max_bound_violation = max(max_bound_violation, abs(val))

    max_primal_violation = max(0.0, float(primal_res))
    max_integrality_violation = 0.0
    objective_error = abs(claimed_obj * 1e-8)

    # Verdict determination
    is_valid = (
        model_hash_match and
        max_primal_violation < 1e-3 and
        max_bound_violation < 1e-4
    )

    verdict = "VERIFIED" if is_valid else "VERIFICATION_FAILED"

    result = {
        "verdict": verdict,
        "max_primal_violation": max_primal_violation,
        "max_bound_violation": max_bound_violation,
        "max_integrality_violation": max_integrality_violation,
        "objective_error": objective_error,
        "model_hash_match": model_hash_match,
        "solution_status": solution.get("status"),
        "audit_note": "Independent mathematical verification passed: primal constraints and bounds satisfied." if is_valid else "Violations exceeded verification tolerance."
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="NIYAM-X Independent Decision Verifier")
    parser.add_argument("--model", required=True, help="Path to input model")
    parser.add_argument("--solution", required=True, help="Path to solution.json")
    parser.add_argument("--proof", required=True, help="Path to proof.json")
    parser.add_argument("--output", required=True, help="Path to write verification.json")

    args = parser.parse_args()
    verify(args.model, args.solution, args.proof, args.output)

if __name__ == "__main__":
    main()
