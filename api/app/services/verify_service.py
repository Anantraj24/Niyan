import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.orm import Session
from api.app.core.ids import verification_id
from api.app.core.errors import NotFoundException, SolverProcessException
from api.app.db.models import VerificationRecord
from api.app.repositories.solve_repository import SolveRepository
from api.app.repositories.verification_repository import VerificationRepository
from api.app.solver_bridge.command_builder import CommandBuilder
from api.app.schemas.verification import VerificationResponse

class VerifyService:
    def __init__(self, db: Session):
        self.db = db
        self.solve_repo = SolveRepository(db)
        self.verify_repo = VerificationRepository(db)

    async def verify_solve(self, solve_id: str) -> VerificationResponse:
        job = self.solve_repo.get_solve(solve_id)
        if not job:
            raise NotFoundException("SolveJob", solve_id)

        solve_dir = Path(job.artifact_dir)
        solution_path = solve_dir / "solution.json"
        proof_path = solve_dir / "proof.json"
        output_path = solve_dir / "verification.json"

        if not solution_path.exists():
            raise SolverProcessException("Cannot verify: solution.json does not exist for this solve.")

        model_path = job.model_version.source_path

        cmd = CommandBuilder.build_verify_cmd(
            model_path=model_path,
            solution_path=str(solution_path),
            proof_path=str(proof_path),
            output_path=str(output_path)
        )

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0 or not output_path.exists():
            err_msg = stderr.decode("utf-8", errors="replace") if stderr else "Verification process failed"
            raise SolverProcessException(f"Verification execution error: {err_msg}")

        with open(output_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)

        v_id = verification_id()
        verdict = v_data.get("verdict", "VERIFIED")

        record = VerificationRecord(
            id=v_id,
            solve_id=solve_id,
            state="COMPLETED",
            verdict=verdict,
            max_primal_violation=v_data.get("max_primal_violation", 0.0),
            max_bound_violation=v_data.get("max_bound_violation", 0.0),
            max_integrality_violation=v_data.get("max_integrality_violation", 0.0),
            objective_error=v_data.get("objective_error", 0.0),
            model_hash_match=v_data.get("model_hash_match", True),
            artifact_path=str(output_path),
            created_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc)
        )
        self.verify_repo.create_verification(record)

        return VerificationResponse(
            verification_id=v_id,
            solve_id=solve_id,
            state="COMPLETED",
            verdict=verdict,
            max_primal_violation=record.max_primal_violation,
            max_bound_violation=record.max_bound_violation,
            max_integrality_violation=record.max_integrality_violation,
            objective_error=record.objective_error,
            model_hash_match=record.model_hash_match,
            created_at=record.created_at,
            completed_at=record.completed_at
        )

    def get_verification(self, solve_id: str) -> Optional[VerificationResponse]:
        record = self.verify_repo.get_verification_by_solve(solve_id)
        if not record:
            return None

        return VerificationResponse(
            verification_id=record.id,
            solve_id=record.solve_id,
            state=record.state,
            verdict=record.verdict,
            max_primal_violation=record.max_primal_violation,
            max_bound_violation=record.max_bound_violation,
            max_integrality_violation=record.max_integrality_violation,
            objective_error=record.objective_error,
            model_hash_match=record.model_hash_match,
            error_message=record.error_message,
            created_at=record.created_at,
            completed_at=record.completed_at
        )
