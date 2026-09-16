from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class CreateBenchmarkRequest(BaseModel):
    model_ids: List[str]
    backends: List[str] = ["CPU", "CUDA"]
    include_reference: bool = False

class BenchmarkResultItem(BaseModel):
    solver: str
    backend: Optional[str] = None
    model_id: Optional[str] = None
    valid: bool
    runtime_ms: Optional[int] = None
    objective: Optional[float] = None
    primal_residual: Optional[float] = None
    dual_residual: Optional[float] = None
    solver_status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class BenchmarkResponse(BaseModel):
    benchmark_id: str
    state: str
    results: List[BenchmarkResultItem]
    created_at: datetime
    completed_at: Optional[datetime] = None
