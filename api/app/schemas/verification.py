from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VerifyRequest(BaseModel):
    pass

class VerificationResponse(BaseModel):
    verification_id: str
    solve_id: str
    state: str  # QUEUED, RUNNING, COMPLETED, FAILED
    verdict: Optional[str] = None  # VERIFIED, VERIFICATION_FAILED
    max_primal_violation: Optional[float] = None
    max_bound_violation: Optional[float] = None
    max_integrality_violation: Optional[float] = None
    objective_error: Optional[float] = None
    model_hash_match: Optional[bool] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
