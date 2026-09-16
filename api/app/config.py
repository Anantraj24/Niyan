import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NIYAM_", env_file=".env", extra="ignore")

    app_name: str = "NIYAM-X Workbench API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # Storage & Workspace
    niyam_home: Path = WORKSPACE_ROOT / ".niyam"
    niyam_db_url: str = f"sqlite:///{WORKSPACE_ROOT / '.niyam' / 'niyam.db'}"
    artifacts_dir: Path = WORKSPACE_ROOT / ".niyam" / "artifacts"
    
    # Native Solvers & CLI
    # Defaults to python cli bridge if native binaries not compiled
    niyam_solver_path: str = str(WORKSPACE_ROOT / "core" / "cli.py")
    niyam_verify_path: str = str(WORKSPACE_ROOT / "verifier" / "cli.py")
    
    # Runtime Config
    enable_cuda: bool = True
    max_concurrent_solves: int = 1
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

settings = Settings()

# Ensure runtime directories exist
settings.niyam_home.mkdir(parents=True, exist_ok=True)
settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
(settings.artifacts_dir / "models").mkdir(parents=True, exist_ok=True)
(settings.artifacts_dir / "solves").mkdir(parents=True, exist_ok=True)
(settings.artifacts_dir / "benchmarks").mkdir(parents=True, exist_ok=True)
