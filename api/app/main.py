from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.app.config import settings
from api.app.core.logging import setup_logging, logger
from api.app.core.errors import NiyamException
from api.app.db.session import init_db

from api.app.routers import (
    health,
    hardware,
    models,
    analyses,
    solves,
    verification,
    benchmarks
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing NIYAM-X SQLite database...")
    init_db()
    logger.info(f"NIYAM-X Workbench API v{settings.app_version} started successfully.")
    yield
    logger.info("Shutting down NIYAM-X Workbench API.")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler conforming to Docs/06_API_CONTRACTS.md Section 11
@app.exception_handler(NiyamException)
async def niyam_exception_handler(request: Request, exc: NiyamException):
    req_id = f"req_{uuid.uuid4().hex[:8]}"
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": req_id
            }
        }
    )

# Mount Routers
prefix = settings.api_prefix
app.include_router(health.router, prefix=prefix)
app.include_router(hardware.router, prefix=prefix)
app.include_router(models.router, prefix=prefix)
app.include_router(analyses.router, prefix=prefix)
app.include_router(solves.router, prefix=prefix)
app.include_router(verification.router, prefix=prefix)
app.include_router(benchmarks.router, prefix=prefix)

# Mount Production Frontend (if built)
from pathlib import Path
from fastapi.staticfiles import StaticFiles

dist_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "app": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
            "api_prefix": prefix
        }

