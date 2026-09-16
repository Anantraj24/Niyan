import os
from pathlib import Path
from fastapi import APIRouter
from api.app.config import settings
from api.app.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def get_health():
    solver_path = Path(settings.niyam_solver_path)
    verify_path = Path(settings.niyam_verify_path)
    
    return HealthResponse(
        status="ok",
        api_version=settings.app_version,
        solver_available=solver_path.exists(),
        verifier_available=verify_path.exists()
    )
