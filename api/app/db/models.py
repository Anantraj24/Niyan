from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from api.app.db.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class ModelRecord(Base):
    __tablename__ = "models"

    id = Column(String(32), primary_key=True, index=True)
    display_name = Column(String(255), nullable=False)
    dataset_kind = Column(String(64), nullable=False)  # synthetic, public, user
    current_version_id = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    versions = relationship("ModelVersionRecord", back_populates="model", cascade="all, delete-orphan")
    scenario_schema = relationship("ScenarioSchemaRecord", back_populates="model", uselist=False)

class ModelVersionRecord(Base):
    __tablename__ = "model_versions"

    id = Column(String(32), primary_key=True, index=True)
    model_id = Column(String(32), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, index=True)
    format = Column(String(16), nullable=False)  # mps, json, lp
    source_path = Column(String(512), nullable=False)
    normalized_path = Column(String(512), nullable=True)
    sha256 = Column(String(64), nullable=False, index=True)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    model = relationship("ModelRecord", back_populates="versions")
    analyses = relationship("AnalysisRecord", back_populates="model_version", cascade="all, delete-orphan")
    solves = relationship("SolveJobRecord", back_populates="model_version", cascade="all, delete-orphan")

class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id = Column(String(32), primary_key=True, index=True)
    model_version_id = Column(String(32), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_json = Column(Text, nullable=False)  # Stored JSON string
    risk_level = Column(String(16), nullable=False)  # LOW, MEDIUM, HIGH
    autopilot_json = Column(Text, nullable=False)  # Stored JSON string
    created_at = Column(DateTime, default=utc_now, nullable=False)

    model_version = relationship("ModelVersionRecord", back_populates="analyses")

class SolveJobRecord(Base):
    __tablename__ = "solve_jobs"

    id = Column(String(32), primary_key=True, index=True)
    model_version_id = Column(String(32), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_solve_id = Column(String(32), ForeignKey("solve_jobs.id", ondelete="SET NULL"), nullable=True, index=True)
    state = Column(String(32), nullable=False, index=True)  # QUEUED, STARTING, RUNNING, COMPLETED, FAILED, CANCELLED
    solver_status = Column(String(32), nullable=True)  # OPTIMAL, FEASIBLE, TIME_LIMIT, ITERATION_LIMIT, INFEASIBLE, NUMERICAL_FAILURE
    backend_requested = Column(String(16), nullable=False)  # auto, cpu, cuda
    backend_used = Column(String(16), nullable=True)
    scaling_requested = Column(String(16), nullable=False)  # auto, none, basic, robust
    scaling_used = Column(String(16), nullable=True)
    warm_start_requested = Column(Boolean, default=False, nullable=False)
    warm_start_used = Column(Boolean, default=False, nullable=False)
    time_limit_sec = Column(Float, nullable=True)
    iteration_limit = Column(Integer, nullable=True)
    tolerance = Column(Float, nullable=True)
    objective = Column(Float, nullable=True)
    iterations = Column(Integer, nullable=True)
    solve_time_ms = Column(Integer, nullable=True)
    primal_residual = Column(Float, nullable=True)
    dual_residual = Column(Float, nullable=True)
    artifact_dir = Column(String(512), nullable=False)
    error_code = Column(String(64), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    model_version = relationship("ModelVersionRecord", back_populates="solves")
    verifications = relationship("VerificationRecord", back_populates="solve_job", cascade="all, delete-orphan")

class VerificationRecord(Base):
    __tablename__ = "verifications"

    id = Column(String(32), primary_key=True, index=True)
    solve_id = Column(String(32), ForeignKey("solve_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    state = Column(String(32), nullable=False)  # QUEUED, RUNNING, COMPLETED, FAILED
    verdict = Column(String(32), nullable=True)  # VERIFIED, VERIFICATION_FAILED
    max_primal_violation = Column(Float, nullable=True)
    max_bound_violation = Column(Float, nullable=True)
    max_integrality_violation = Column(Float, nullable=True)
    objective_error = Column(Float, nullable=True)
    model_hash_match = Column(Boolean, nullable=True)
    artifact_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    solve_job = relationship("SolveJobRecord", back_populates="verifications")

class BenchmarkRunRecord(Base):
    __tablename__ = "benchmark_runs"

    id = Column(String(32), primary_key=True, index=True)
    state = Column(String(32), nullable=False)  # QUEUED, RUNNING, COMPLETED, FAILED
    config_json = Column(Text, nullable=False)
    artifact_dir = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    results = relationship("BenchmarkResultRecord", back_populates="benchmark_run", cascade="all, delete-orphan")

class BenchmarkResultRecord(Base):
    __tablename__ = "benchmark_results"

    id = Column(String(32), primary_key=True, index=True)
    benchmark_run_id = Column(String(32), ForeignKey("benchmark_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    model_version_id = Column(String(32), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    solver_name = Column(String(64), nullable=False)
    backend = Column(String(16), nullable=True)
    valid = Column(Boolean, nullable=False, default=False)
    runtime_ms = Column(Integer, nullable=True)
    objective = Column(Float, nullable=True)
    primal_residual = Column(Float, nullable=True)
    dual_residual = Column(Float, nullable=True)
    solver_status = Column(String(32), nullable=True)
    details_json = Column(Text, nullable=True)

    benchmark_run = relationship("BenchmarkRunRecord", back_populates="results")

class ScenarioSchemaRecord(Base):
    __tablename__ = "scenario_schemas"

    id = Column(String(32), primary_key=True, index=True)
    model_id = Column(String(32), ForeignKey("models.id", ondelete="CASCADE"), nullable=False, unique=True)
    schema_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    model = relationship("ModelRecord", back_populates="scenario_schema")
