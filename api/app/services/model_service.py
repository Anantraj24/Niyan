from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session
from api.app.core.ids import model_id, version_id
from api.app.core.hashing import compute_sha256_bytes
from api.app.core.errors import NotFoundException, ValidationException
from api.app.db.models import ModelRecord, ModelVersionRecord, ScenarioSchemaRecord
from api.app.repositories.model_repository import ModelRepository
from api.app.services.artifact_service import ArtifactService
from api.app.schemas.models import ModelImportResponse, ModelSummary, ModelDetail, ModelVersionSummary

class ModelService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModelRepository(db)

    def import_model(
        self,
        file_bytes: bytes,
        filename: str,
        display_name: Optional[str] = None,
        dataset_kind: str = "user"
    ) -> ModelImportResponse:
        if not file_bytes:
            raise ValidationException("File content cannot be empty")

        ext = Path(filename).suffix.lstrip(".").lower()
        if not ext:
            ext = "mps"

        m_id = model_id()
        v_id = version_id()
        name = display_name or Path(filename).stem.replace("_", " ").title()
        sha = compute_sha256_bytes(file_bytes)
        size = len(file_bytes)

        # Store artifact file
        version_dir = ArtifactService.get_model_version_dir(m_id, v_id)
        source_path = version_dir / f"model.{ext}"
        with open(source_path, "wb") as f:
            f.write(file_bytes)

        # Create database records
        model_rec = ModelRecord(
            id=m_id,
            display_name=name,
            dataset_kind=dataset_kind,
            current_version_id=v_id
        )
        self.repo.create_model(model_rec)

        version_rec = ModelVersionRecord(
            id=v_id,
            model_id=m_id,
            format=ext,
            source_path=str(source_path),
            sha256=sha,
            size_bytes=size
        )
        self.repo.create_version(version_rec)

        return ModelImportResponse(
            model_id=m_id,
            version_id=v_id,
            display_name=name,
            format=ext,
            sha256=sha,
            dataset_kind=dataset_kind,
            size_bytes=size,
            created_at=model_rec.created_at
        )

    def list_models(self) -> List[ModelSummary]:
        records = self.repo.list_models()
        results = []
        for r in records:
            results.append(
                ModelSummary(
                    model_id=r.id,
                    display_name=r.display_name,
                    dataset_kind=r.dataset_kind,
                    current_version_id=r.current_version_id,
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                    version_count=len(r.versions) if r.versions else 1
                )
            )
        return results

    def get_model(self, m_id: str) -> ModelDetail:
        record = self.repo.get_model(m_id)
        if not record:
            raise NotFoundException("Model", m_id)

        latest_ver = None
        if record.current_version_id:
            ver = self.repo.get_version(record.current_version_id)
            if ver:
                latest_ver = ModelVersionSummary(
                    version_id=ver.id,
                    format=ver.format,
                    sha256=ver.sha256,
                    size_bytes=ver.size_bytes,
                    created_at=ver.created_at
                )

        return ModelDetail(
            model_id=record.id,
            display_name=record.display_name,
            dataset_kind=record.dataset_kind,
            current_version=latest_ver,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    def get_scenario_schema(self, m_id: str) -> Optional[ScenarioSchemaRecord]:
        return self.repo.get_scenario_schema(m_id)
