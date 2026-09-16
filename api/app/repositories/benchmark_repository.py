from typing import Optional
from sqlalchemy.orm import Session
from api.app.db.models import BenchmarkRunRecord, BenchmarkResultRecord

class BenchmarkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_benchmark_run(self, record: BenchmarkRunRecord) -> BenchmarkRunRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_benchmark_run(self, benchmark_id: str) -> Optional[BenchmarkRunRecord]:
        return self.db.query(BenchmarkRunRecord).filter(BenchmarkRunRecord.id == benchmark_id).first()

    def add_result(self, record: BenchmarkResultRecord) -> BenchmarkResultRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_benchmark_run(self, record: BenchmarkRunRecord) -> BenchmarkRunRecord:
        self.db.commit()
        self.db.refresh(record)
        return record
