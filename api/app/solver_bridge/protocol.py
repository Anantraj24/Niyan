from typing import Any, Dict, Optional
from pydantic import BaseModel

class SolverEvent(BaseModel):
    protocol_version: int = 1
    seq: int
    type: str
    timestamp_ms: int
    data: Dict[str, Any]

class SolverIterationData(BaseModel):
    iteration: int
    elapsed_ms: int
    objective: float
    primal_residual: float
    dual_residual: float

class SolverCompletedData(BaseModel):
    solver_status: str
    objective: float
    iterations: int
    elapsed_ms: int
    primal_residual: float
    dual_residual: float
    backend: str
    scaling: Optional[str] = None
    warm_start_used: bool = False
