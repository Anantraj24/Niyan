from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class SolveConfig(BaseModel):
    backend: str = "AUTO"  # AUTO, CPU, CUDA
    scaling: str = "AUTO"  # AUTO, NONE, BASIC, ROBUST
    time_limit_sec: Optional[float] = 30.0
    iteration_limit: Optional[int] = 100000
    tolerance: Optional[float] = 1e-6

class CreateSolveRequest(BaseModel):
    model_id: str
    version_id: Optional[str] = None
    config: SolveConfig = Field(default_factory=SolveConfig)

class CreateSolveResponse(BaseModel):
    solve_id: str
    state: str  # QUEUED
    events_url: str

class SolveStatusResponse(BaseModel):
    solve_id: str
    model_id: str
    version_id: str
    parent_solve_id: Optional[str] = None
    state: str
    solver_status: Optional[str] = None
    backend: Optional[str] = None
    scaling: Optional[str] = None
    warm_start: bool = False
    objective: Optional[float] = None
    iterations: Optional[int] = None
    solve_time_ms: Optional[int] = None
    primal_residual: Optional[float] = None
    dual_residual: Optional[float] = None
    verification_state: str = "NOT_RUN"
    verification_verdict: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class ResolveChanges(BaseModel):
    objective: Optional[Dict[str, float]] = None
    parameters: Optional[Dict[str, float]] = None
    rhs: Optional[Dict[str, float]] = None
    bounds: Optional[Dict[str, Dict[str, float]]] = None

class ResolveRequest(BaseModel):
    changes: ResolveChanges
    config: Optional[SolveConfig] = None

class ResolveResponse(BaseModel):
    solve_id: str
    parent_solve_id: str
    state: str
    warm_start_requested: bool
    events_url: str
