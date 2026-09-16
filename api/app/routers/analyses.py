from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.app.db.session import get_db
from api.app.services.analysis_service import AnalysisService
from api.app.schemas.analyses import AnalysisRequest, AnalysisResponse
from api.app.core.errors import NotFoundException

router = APIRouter(prefix="/models", tags=["Analysis & X-Ray"])

@router.post("/{model_id}/analyze", response_model=AnalysisResponse)
async def analyze_model(
    model_id: str,
    req: Optional[AnalysisRequest] = None,
    db: Session = Depends(get_db)
):
    service = AnalysisService(db)
    v_id = req.version_id if req else None
    return await service.analyze_model(model_id=model_id, version_id=v_id)

@router.get("/{model_id}/analysis", response_model=AnalysisResponse)
def get_latest_analysis(
    model_id: str,
    version_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = AnalysisService(db)
    analysis = service.get_latest_analysis(model_id=model_id, version_id=version_id)
    if not analysis:
        raise NotFoundException("Analysis for model", model_id)
    return analysis
