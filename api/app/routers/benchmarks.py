from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.app.db.session import get_db
from api.app.services.benchmark_service import BenchmarkService
from api.app.schemas.benchmarks import CreateBenchmarkRequest, BenchmarkResponse

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])

@router.post("", response_model=BenchmarkResponse, status_code=status.HTTP_201_CREATED)
async def run_benchmark(req: CreateBenchmarkRequest, db: Session = Depends(get_db)):
    service = BenchmarkService(db)
    return await service.run_benchmark(req)

@router.get("/{benchmark_id}", response_model=BenchmarkResponse)
def get_benchmark(benchmark_id: str, db: Session = Depends(get_db)):
    service = BenchmarkService(db)
    return service.get_benchmark(benchmark_id)
