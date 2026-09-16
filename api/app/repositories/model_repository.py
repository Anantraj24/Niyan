from typing import List, Optional
from sqlalchemy.orm import Session
from api.app.db.models import ModelRecord, ModelVersionRecord, AnalysisRecord, ScenarioSchemaRecord

class ModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_model(self, record: ModelRecord) -> ModelRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def create_version(self, record: ModelVersionRecord) -> ModelVersionRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_model(self, model_id: str) -> Optional[ModelRecord]:
        return self.db.query(ModelRecord).filter(ModelRecord.id == model_id).first()

    def list_models(self) -> List[ModelRecord]:
        return self.db.query(ModelRecord).order_by(ModelRecord.created_at.desc()).all()

    def get_version(self, version_id: str) -> Optional[ModelVersionRecord]:
        return self.db.query(ModelVersionRecord).filter(ModelVersionRecord.id == version_id).first()

    def get_latest_version(self, model_id: str) -> Optional[ModelVersionRecord]:
        return (
            self.db.query(ModelVersionRecord)
            .filter(ModelVersionRecord.model_id == model_id)
            .order_by(ModelVersionRecord.created_at.desc())
            .first()
        )

    def save_analysis(self, record: AnalysisRecord) -> AnalysisRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_latest_analysis(self, version_id: str) -> Optional[AnalysisRecord]:
        return (
            self.db.query(AnalysisRecord)
            .filter(AnalysisRecord.model_version_id == version_id)
            .order_by(AnalysisRecord.created_at.desc())
            .first()
        )

    def save_scenario_schema(self, record: ScenarioSchemaRecord) -> ScenarioSchemaRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_scenario_schema(self, model_id: str) -> Optional[ScenarioSchemaRecord]:
        return self.db.query(ScenarioSchemaRecord).filter(ScenarioSchemaRecord.model_id == model_id).first()
