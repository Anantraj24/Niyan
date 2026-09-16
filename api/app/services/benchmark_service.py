import asyncio
import time
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from api.app.core.ids import benchmark_id
from api.app.core.errors import NotFoundException
from api.app.db.models import BenchmarkRunRecord, BenchmarkResultRecord
from api.app.repositories.model_repository import ModelRepository
from api.app.repositories.benchmark_repository import BenchmarkRepository
from api.app.services.artifact_service import ArtifactService
from api.app.services.solve_service import SolveService
from api.app.schemas.solves import SolveConfig
from api.app.schemas.benchmarks import (
    CreateBenchmarkRequest, BenchmarkResponse, BenchmarkResultItem
)

class BenchmarkService:
    def __init__(self, db: Session):
        self.db = db
        self.model_repo = ModelRepository(db)
        self.benchmark_repo = BenchmarkRepository(db)
        self.solve_service = SolveService(db)

    async def run_benchmark(self, req: CreateBenchmarkRequest) -> BenchmarkResponse:
        b_id = benchmark_id()
        bench_dir = ArtifactService.get_benchmark_dir(b_id)

        run_rec = BenchmarkRunRecord(
            id=b_id,
            state="RUNNING",
            config_json=req.model_dump_json(),
            artifact_dir=str(bench_dir),
            created_at=datetime.now(timezone.utc)
        )
        self.benchmark_repo.create_benchmark_run(run_rec)

        results_list: List[BenchmarkResultItem] = []

        for m_id in req.model_ids:
            model = self.model_repo.get_model(m_id)
            if not model:
                continue

            v_id = model.current_version_id
            if not v_id:
                continue

            for backend in req.backends:
                start_time = time.perf_counter()
                
                # Execute solve for this backend
                create_res = self.solve_service.create_solve(
                    model_id=m_id,
                    ver_id=v_id,
                    config=SolveConfig(backend=backend, time_limit_sec=15)
                )

                # Wait for solve to finish
                final_status = None
                for _ in range(60):
                    await asyncio.sleep(0.5)
                    st = self.solve_service.get_solve_status(create_res.solve_id)
                    if st.state in ("COMPLETED", "FAILED"):
                        final_status = st
                        break

                elapsed_ms = int((time.perf_counter() - start_time) * 1000)

                valid = final_status.state == "COMPLETED" if final_status else False
                obj = final_status.objective if final_status else None
                pres = final_status.primal_residual if final_status else None
                dres = final_status.dual_residual if final_status else None
                s_stat = final_status.solver_status if final_status else "TIMEOUT"

                res_item = BenchmarkResultItem(
                    solver="NIYAM",
                    backend=backend,
                    model_id=m_id,
                    valid=valid,
                    runtime_ms=final_status.solve_time_ms or elapsed_ms if final_status else elapsed_ms,
                    objective=obj,
                    primal_residual=pres,
                    dual_residual=dres,
                    solver_status=s_stat
                )
                results_list.append(res_item)

                res_rec = BenchmarkResultRecord(
                    id=f"{b_id}_{m_id}_{backend}",
                    benchmark_run_id=b_id,
                    model_version_id=v_id,
                    solver_name="NIYAM",
                    backend=backend,
                    valid=valid,
                    runtime_ms=res_item.runtime_ms,
                    objective=obj,
                    primal_residual=pres,
                    dual_residual=dres,
                    solver_status=s_stat
                )
                self.benchmark_repo.add_result(res_rec)

        run_rec.state = "COMPLETED"
        run_rec.completed_at = datetime.now(timezone.utc)
        self.benchmark_repo.update_benchmark_run(run_rec)

        return BenchmarkResponse(
            benchmark_id=b_id,
            state="COMPLETED",
            results=results_list,
            created_at=run_rec.created_at,
            completed_at=run_rec.completed_at
        )

    def get_benchmark(self, b_id: str) -> BenchmarkResponse:
        rec = self.benchmark_repo.get_benchmark_run(b_id)
        if not rec:
            raise NotFoundException("BenchmarkRun", b_id)

        items = []
        for r in rec.results:
            items.append(
                BenchmarkResultItem(
                    solver=r.solver_name,
                    backend=r.backend,
                    model_id=r.model_version_id,
                    valid=r.valid,
                    runtime_ms=r.runtime_ms,
                    objective=r.objective,
                    primal_residual=r.primal_residual,
                    dual_residual=r.dual_residual,
                    solver_status=r.solver_status
                )
            )

        return BenchmarkResponse(
            benchmark_id=rec.id,
            state=rec.state,
            results=items,
            created_at=rec.created_at,
            completed_at=rec.completed_at
        )
