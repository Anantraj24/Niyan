from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ModelImportResponse(BaseModel):
    model_id: str
    version_id: str
    display_name: str
    format: str
    sha256: str
    dataset_kind: str
    size_bytes: int
    created_at: datetime

class ModelVersionSummary(BaseModel):
    version_id: str
    format: str
    sha256: str
    size_bytes: int
    created_at: datetime

class ModelSummary(BaseModel):
    model_id: str
    display_name: str
    dataset_kind: str
    current_version_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    version_count: int = 1

class ModelDetail(BaseModel):
    model_id: str
    display_name: str
    dataset_kind: str
    current_version: Optional[ModelVersionSummary] = None
    created_at: datetime
    updated_at: datetime
