import os
import shutil
from pathlib import Path
from api.app.config import settings

class ArtifactService:
    @staticmethod
    def get_model_version_dir(model_id: str, version_id: str) -> Path:
        p = settings.artifacts_dir / "models" / model_id / version_id
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def get_solve_dir(solve_id: str) -> Path:
        p = settings.artifacts_dir / "solves" / solve_id
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def get_benchmark_dir(benchmark_id: str) -> Path:
        p = settings.artifacts_dir / "benchmarks" / benchmark_id
        p.mkdir(parents=True, exist_ok=True)
        return p
