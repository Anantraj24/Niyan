from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from api.app.db.session import get_db
from api.app.services.solve_service import SolveService
from api.app.schemas.solves import (
    CreateSolveRequest, CreateSolveResponse, SolveStatusResponse,
    ResolveRequest, ResolveResponse
)

router = APIRouter(prefix="/solves", tags=["Solves & DeltaSolve"])

@router.post("", response_model=CreateSolveResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_solve(req: CreateSolveRequest, db: Session = Depends(get_db)):
    service = SolveService(db)
    return service.create_solve(
        model_id=req.model_id,
        ver_id=req.version_id,
        config=req.config
    )

@router.get("/{solve_id}", response_model=SolveStatusResponse)
def get_solve_status(solve_id: str, db: Session = Depends(get_db)):
    service = SolveService(db)
    return service.get_solve_status(solve_id)

@router.get("/{solve_id}/events")
async def stream_solve_events(solve_id: str, db: Session = Depends(get_db)):
    service = SolveService(db)
    return StreamingResponse(
        service.stream_solve_events(solve_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/{solve_id}/resolve", response_model=ResolveResponse)
async def resolve_deltasolve(solve_id: str, req: ResolveRequest, db: Session = Depends(get_db)):
    service = SolveService(db)
    return service.resolve(parent_s_id=solve_id, req=req)
