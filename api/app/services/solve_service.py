import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator, Optional, Dict, Any
from sqlalchemy.orm import Session
from api.app.core.ids import solve_id, version_id
from api.app.core.errors import NotFoundException, ValidationException
from api.app.core.logging import logger
from api.app.db.session import SessionLocal
from api.app.db.models import SolveJobRecord, ModelVersionRecord
from api.app.repositories.model_repository import ModelRepository
from api.app.repositories.solve_repository import SolveRepository
from api.app.repositories.verification_repository import VerificationRepository
from api.app.solver_bridge.command_builder import CommandBuilder
from api.app.solver_bridge.process_runner import ProcessRunner
from api.app.solver_bridge.event_parser import EventParser
from api.app.services.artifact_service import ArtifactService
from api.app.schemas.solves import (
    SolveConfig, CreateSolveResponse, SolveStatusResponse, ResolveRequest, ResolveResponse
)

# Solve concurrency limiter
_SOLVE_SEMAPHORE = asyncio.Semaphore(1)

class SolveService:
    def __init__(self, db: Session):
        self.db = db
        self.model_repo = ModelRepository(db)
        self.solve_repo = SolveRepository(db)
        self.verify_repo = VerificationRepository(db)

    def create_solve(
        self,
        model_id: str,
        ver_id: Optional[str] = None,
        config: Optional[SolveConfig] = None,
        parent_solve_id: Optional[str] = None,
        warm_start_requested: bool = False,
        custom_model_path: Optional[str] = None
    ) -> CreateSolveResponse:
        model = self.model_repo.get_model(model_id)
        if not model:
            raise NotFoundException("Model", model_id)

        target_version_id = ver_id or model.current_version_id
        if not target_version_id:
            raise NotFoundException("ModelVersion", "None")

        version = self.model_repo.get_version(target_version_id)
        if not version:
            raise NotFoundException("ModelVersion", target_version_id)

        cfg = config or SolveConfig()
        s_id = solve_id()
        solve_dir = ArtifactService.get_solve_dir(s_id)

        model_path = custom_model_path or version.source_path

        job = SolveJobRecord(
            id=s_id,
            model_version_id=target_version_id,
            parent_solve_id=parent_solve_id,
            state="QUEUED",
            backend_requested=cfg.backend,
            scaling_requested=cfg.scaling,
            warm_start_requested=warm_start_requested,
            time_limit_sec=cfg.time_limit_sec,
            iteration_limit=cfg.iteration_limit,
            tolerance=cfg.tolerance,
            artifact_dir=str(solve_dir)
        )
        self.solve_repo.create_solve(job)

        # Launch background execution task
        asyncio.create_task(
            self._execute_solve_job(
                s_id=s_id,
                model_path=str(model_path),
                solve_dir=solve_dir,
                cfg=cfg,
                parent_solve_id=parent_solve_id
            )
        )

        return CreateSolveResponse(
            solve_id=s_id,
            state="QUEUED",
            events_url=f"/api/v1/solves/{s_id}/events"
        )

    async def _execute_solve_job(
        self,
        s_id: str,
        model_path: str,
        solve_dir: Path,
        cfg: SolveConfig,
        parent_solve_id: Optional[str] = None
    ):
        async with _SOLVE_SEMAPHORE:
            # Create independent session for background worker
            bg_db = SessionLocal()
            try:
                repo = SolveRepository(bg_db)
                job = repo.get_solve(s_id)
                if not job:
                    return

                job.state = "RUNNING"
                job.started_at = datetime.now(timezone.utc)
                repo.update_solve(job)

                solution_path = solve_dir / "solution.json"
                proof_path = solve_dir / "proof.json"

                warm_state_path = None
                if parent_solve_id:
                    parent_dir = ArtifactService.get_solve_dir(parent_solve_id)
                    parent_sol = parent_dir / "solution.json"
                    if parent_sol.exists():
                        warm_state_path = str(parent_sol)

                cmd = CommandBuilder.build_solve_cmd(
                    model_path=model_path,
                    output_path=str(solution_path),
                    proof_path=str(proof_path),
                    backend=cfg.backend,
                    scaling=cfg.scaling,
                    time_limit=cfg.time_limit_sec,
                    iteration_limit=cfg.iteration_limit,
                    tolerance=cfg.tolerance,
                    warm_state_path=warm_state_path
                )

                async for event in ProcessRunner.run_solver_process(s_id, cmd, solve_dir):
                    if event.type == "autopilot.selected":
                        job.backend_used = event.data.get("backend")
                        job.scaling_used = event.data.get("scaling")
                    elif event.type == "solver.completed":
                        job.solver_status = event.data.get("solver_status", "COMPLETED")
                        job.objective = event.data.get("objective")
                        job.iterations = event.data.get("iterations")
                        job.solve_time_ms = event.data.get("elapsed_ms")
                        job.primal_residual = event.data.get("primal_residual")
                        job.dual_residual = event.data.get("dual_residual")
                        job.warm_start_used = event.data.get("warm_start_used", False)
                        if "backend" in event.data:
                            job.backend_used = event.data.get("backend")
                    elif event.type == "solver.failed":
                        job.error_code = event.data.get("code", "SOLVER_FAILED")
                        job.error_message = event.data.get("message", "Solve process failed")

                # If solution file exists, extract summary data if not already populated
                if solution_path.exists():
                    try:
                        with open(solution_path, "r", encoding="utf-8") as sf:
                            sdata = json.load(sf)
                            if not job.solver_status:
                                job.solver_status = sdata.get("status", "OPTIMAL")
                            if job.objective is None:
                                job.objective = sdata.get("objective")
                    except Exception:
                        pass

                job.state = "COMPLETED" if job.solver_status != "NUMERICAL_FAILURE" else "FAILED"
                job.completed_at = datetime.now(timezone.utc)
                repo.update_solve(job)

            except Exception as e:
                logger.error(f"Error in background solve {s_id}: {e}", exc_info=True)
                if job:
                    job.state = "FAILED"
                    job.error_message = str(e)
                    job.completed_at = datetime.now(timezone.utc)
                    repo.update_solve(job)
            finally:
                bg_db.close()

    def get_solve_status(self, s_id: str) -> SolveStatusResponse:
        job = self.solve_repo.get_solve(s_id)
        if not job:
            raise NotFoundException("SolveJob", s_id)

        v_record = self.verify_repo.get_verification_by_solve(s_id)
        v_state = v_record.state if v_record else "NOT_RUN"
        v_verdict = v_record.verdict if v_record else None

        return SolveStatusResponse(
            solve_id=job.id,
            model_id=job.model_version.model_id if job.model_version else "",
            version_id=job.model_version_id,
            parent_solve_id=job.parent_solve_id,
            state=job.state,
            solver_status=job.solver_status,
            backend=job.backend_used or job.backend_requested,
            scaling=job.scaling_used or job.scaling_requested,
            warm_start=job.warm_start_used,
            objective=job.objective,
            iterations=job.iterations,
            solve_time_ms=job.solve_time_ms,
            primal_residual=job.primal_residual,
            dual_residual=job.dual_residual,
            verification_state=v_state,
            verification_verdict=v_verdict,
            error_code=job.error_code,
            error_message=job.error_message,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at
        )

    def resolve(self, parent_s_id: str, req: ResolveRequest) -> ResolveResponse:
        parent = self.solve_repo.get_solve(parent_s_id)
        if not parent:
            raise NotFoundException("SolveJob", parent_s_id)

        # Build patched model for DeltaSolve
        parent_version = self.model_repo.get_version(parent.model_version_id)
        if not parent_version:
            raise NotFoundException("ModelVersion", parent.model_version_id)

        child_s_id = solve_id()
        child_dir = ArtifactService.get_solve_dir(child_s_id)
        patched_model_path = child_dir / "patched_model.json"

        # Apply parameter changes / delta modifications
        patch_info = {
            "base_model_path": parent_version.source_path,
            "parent_solve_id": parent_s_id,
            "changes": req.changes.model_dump(exclude_none=True)
        }
        with open(patched_model_path, "w", encoding="utf-8") as f:
            json.dump(patch_info, f, indent=2)

        cfg = req.config or SolveConfig()

        job = SolveJobRecord(
            id=child_s_id,
            model_version_id=parent.model_version_id,
            parent_solve_id=parent_s_id,
            state="QUEUED",
            backend_requested=cfg.backend,
            scaling_requested=cfg.scaling,
            warm_start_requested=True,
            time_limit_sec=cfg.time_limit_sec,
            iteration_limit=cfg.iteration_limit,
            tolerance=cfg.tolerance,
            artifact_dir=str(child_dir)
        )
        self.solve_repo.create_solve(job)

        asyncio.create_task(
            self._execute_solve_job(
                s_id=child_s_id,
                model_path=str(patched_model_path),
                solve_dir=child_dir,
                cfg=cfg,
                parent_solve_id=parent_s_id
            )
        )

        return ResolveResponse(
            solve_id=child_s_id,
            parent_solve_id=parent_s_id,
            state="QUEUED",
            warm_start_requested=True,
            events_url=f"/api/v1/solves/{child_s_id}/events"
        )

    async def stream_solve_events(self, s_id: str) -> AsyncGenerator[str, None]:
        job = self.solve_repo.get_solve(s_id)
        if not job:
            yield "event: error\ndata: {\"message\": \"Job not found\"}\n\n"
            return

        events_file = Path(job.artifact_dir) / "events.jsonl"

        # If job already completed, replay events from events.jsonl file
        if job.state in ("COMPLETED", "FAILED", "CANCELLED") and events_file.exists():
            with open(events_file, "r", encoding="utf-8") as f:
                for line in f:
                    event = EventParser.parse_line(line)
                    if event:
                        yield EventParser.to_sse(event)
            return

        # If job is running or starting, subscribe to live broadcast queue
        queue = ProcessRunner.register_listener(s_id)
        try:
            # Yield initial connect event
            yield f"id: 0\nevent: stream.connected\ndata: {{\"solve_id\": \"{s_id}\"}}\n\n"
            
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    if event is None:
                        # End of stream signaled
                        break
                    yield EventParser.to_sse(event)
                except asyncio.TimeoutError:
                    # Heartbeat comment to keep connection alive
                    yield ": heartbeat\n\n"
        finally:
            ProcessRunner.unregister_listener(s_id, queue)
