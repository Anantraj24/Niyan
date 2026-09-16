from typing import List, Optional
from sqlalchemy.orm import Session
from api.app.db.models import SolveJobRecord

class SolveRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_solve(self, record: SolveJobRecord) -> SolveJobRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_solve(self, solve_id: str) -> Optional[SolveJobRecord]:
        return self.db.query(SolveJobRecord).filter(SolveJobRecord.id == solve_id).first()

    def list_solves_for_model(self, model_version_id: str) -> List[SolveJobRecord]:
        return (
            self.db.query(SolveJobRecord)
            .filter(SolveJobRecord.model_version_id == model_version_id)
            .order_by(SolveJobRecord.created_at.desc())
            .all()
        )

    def update_solve(self, record: SolveJobRecord) -> SolveJobRecord:
        self.db.commit()
        self.db.refresh(record)
        return record
