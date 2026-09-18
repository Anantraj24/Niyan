import json
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from api.app.db.session import get_db
from api.app.core.errors import NotFoundException
from api.app.services.model_service import ModelService
from api.app.schemas.models import ModelImportResponse, ModelSummary, ModelDetail

router = APIRouter(prefix="/models", tags=["Models"])

@router.post("/import", response_model=ModelImportResponse, status_code=status.HTTP_201_CREATED)
async def import_model(
    file: UploadFile = File(...),
    display_name: Optional[str] = Form(None),
    dataset_kind: str = Form("user"),
    db: Session = Depends(get_db)
):
    content = await file.read()
    service = ModelService(db)
    return service.import_model(
        file_bytes=content,
        filename=file.filename or "model.mps",
        display_name=display_name,
        dataset_kind=dataset_kind
    )

@router.get("", response_model=List[ModelSummary])
def list_models(db: Session = Depends(get_db)):
    service = ModelService(db)
    return service.list_models()

@router.get("/{model_id}", response_model=ModelDetail)
def get_model(model_id: str, db: Session = Depends(get_db)):
    service = ModelService(db)
    return service.get_model(model_id)

@router.get("/{model_id}/schema")
def get_scenario_schema(model_id: str, db: Session = Depends(get_db)):
    service = ModelService(db)
    rec = service.get_scenario_schema(model_id)
    if not rec:
        raise NotFoundException("ScenarioSchema", model_id)
    return json.loads(rec.schema_json)

