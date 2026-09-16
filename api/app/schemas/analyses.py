from typing import Optional, List
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    version_id: Optional[str] = None

class ProfileData(BaseModel):
    variables: int
    constraints: int
    nonzeros: int
    density: float
    coefficient_min_abs: float
    coefficient_max_abs: float
    coefficient_dynamic_range: float
    integer_ratio: float
    binary_ratio: float
    fixed_variables: int
    singleton_rows: int

class RiskIssue(BaseModel):
    code: str
    severity: str  # LOW, MEDIUM, HIGH
    message: str

class RiskData(BaseModel):
    level: str  # LOW, MEDIUM, HIGH
    issues: List[RiskIssue]

class AutopilotData(BaseModel):
    backend: str  # CPU, CUDA
    scaling: str  # NONE, BASIC, ROBUST
    warm_start_eligible: bool
    reasons: List[str]

class AnalysisResponse(BaseModel):
    analysis_id: str
    model_id: str
    version_id: str
    profile: ProfileData
    risk: RiskData
    autopilot: AutopilotData
