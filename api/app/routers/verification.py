from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.app.db.session import get_db
from api.app.services.verify_service import VerifyService
from api.app.schemas.verification import VerificationResponse
from api.app.core.errors import NotFoundException

router = APIRouter(tags=["Verification & Proof Pack"])

@router.post("/solves/{solve_id}/verify", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
async def verify_solve(solve_id: str, db: Session = Depends(get_db)):
    service = VerifyService(db)
    return await service.verify_solve(solve_id)

@router.get("/solves/{solve_id}/verification", response_model=VerificationResponse)
def get_verification(solve_id: str, db: Session = Depends(get_db)):
    service = VerifyService(db)
    result = service.get_verification(solve_id)
    if not result:
        raise NotFoundException("Verification for solve", solve_id)
    return result
