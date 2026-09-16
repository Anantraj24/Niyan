import asyncio
import json
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from api.app.core.ids import analysis_id
from api.app.core.errors import NotFoundException, SolverProcessException
from api.app.db.models import AnalysisRecord
from api.app.repositories.model_repository import ModelRepository
from api.app.solver_bridge.command_builder import CommandBuilder
from api.app.services.artifact_service import ArtifactService
from api.app.schemas.analyses import (
    AnalysisResponse, ProfileData, RiskData, AutopilotData
)

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ModelRepository(db)

    async def analyze_model(self, model_id: str, version_id: Optional[str] = None) -> AnalysisResponse:
        model = self.repo.get_model(model_id)
        if not model:
            raise NotFoundException("Model", model_id)

        target_version_id = version_id or model.current_version_id
        if not target_version_id:
            raise NotFoundException("ModelVersion", "None")

        version = self.repo.get_version(target_version_id)
        if not version:
            raise NotFoundException("ModelVersion", target_version_id)

        # Output artifact path
        version_dir = ArtifactService.get_model_version_dir(model_id, target_version_id)
        output_json_path = version_dir / "analysis.json"

        # Build command and execute
        cmd = CommandBuilder.build_analyze_cmd(version.source_path, str(output_json_path))
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0 or not output_json_path.exists():
            err_msg = stderr.decode("utf-8", errors="replace") if stderr else "Analysis failed"
            raise SolverProcessException(f"Failed to analyze model: {err_msg}")

        with open(output_json_path, "r", encoding="utf-8") as f:
            analysis_data = json.load(f)

        profile_dict = analysis_data.get("profile", {})
        risk_dict = analysis_data.get("risk", {})
        autopilot_dict = analysis_data.get("autopilot", {})

        a_id = analysis_id()
        record = AnalysisRecord(
            id=a_id,
            model_version_id=target_version_id,
            profile_json=json.dumps(profile_dict),
            risk_level=risk_dict.get("level", "LOW"),
            autopilot_json=json.dumps(autopilot_dict)
        )
        self.repo.save_analysis(record)

        return AnalysisResponse(
            analysis_id=a_id,
            model_id=model_id,
            version_id=target_version_id,
            profile=ProfileData(**profile_dict),
            risk=RiskData(**risk_dict),
            autopilot=AutopilotData(**autopilot_dict)
        )

    def get_latest_analysis(self, model_id: str, version_id: Optional[str] = None) -> Optional[AnalysisResponse]:
        model = self.repo.get_model(model_id)
        if not model:
            raise NotFoundException("Model", model_id)

        target_version_id = version_id or model.current_version_id
        if not target_version_id:
            return None

        record = self.repo.get_latest_analysis(target_version_id)
        if not record:
            return None

        profile_dict = json.loads(record.profile_json)
        risk_level = record.risk_level
        autopilot_dict = json.loads(record.autopilot_json)

        return AnalysisResponse(
            analysis_id=record.id,
            model_id=model_id,
            version_id=target_version_id,
            profile=ProfileData(**profile_dict),
            risk=RiskData(level=risk_level, issues=json.loads(record.profile_json).get("issues", [])),
            autopilot=AutopilotData(**autopilot_dict)
        )
