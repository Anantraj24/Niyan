from typing import Optional
from sqlalchemy.orm import Session
from api.app.db.models import VerificationRecord

class VerificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_verification(self, record: VerificationRecord) -> VerificationRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_verification_by_solve(self, solve_id: str) -> Optional[VerificationRecord]:
        return (
            self.db.query(VerificationRecord)
            .filter(VerificationRecord.solve_id == solve_id)
            .order_by(VerificationRecord.created_at.desc())
            .first()
        )

    def update_verification(self, record: VerificationRecord) -> VerificationRecord:
        self.db.commit()
        self.db.refresh(record)
        return record
