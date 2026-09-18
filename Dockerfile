# ==============================================================================
# NIYAM-X — Sovereign Optimization Workbench Multi-Stage Production Dockerfile
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build the React 19 Frontend
# ------------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /build

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Python / Sovereign Core Runtime
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NIYAM_HOME=/app/.niyam \
    PORT=10000

WORKDIR /app

# Install curl for healthchecks (lightweight, zero bloat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY api/requirements.txt ./api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy backend, core solver, verifier, demo assets, and developer tools
COPY api/ ./api/
COPY core/ ./core/
COPY verifier/ ./verifier/
COPY demo/ ./demo/
COPY tools/ ./tools/

# Copy compiled frontend assets from Stage 1 into the location expected by FastAPI
COPY --from=frontend-builder /build/dist ./frontend/dist

# Initialize directory structure and seed demo models
RUN mkdir -p .niyam/artifacts && \
    python tools/seed_demo.py && \
    python tools/import_mps.py -f demo/energy_grid/energy_grid_lp.mps -n "5-Bus Electric Power Dispatch" -s demo/energy_grid/scenario_schema.json --dataset-kind industrial

EXPOSE 10000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/api/v1/health || exit 1

# Start sovereign FastAPI server serving both API and Frontend SPA (respecting dynamic PORT if assigned by Render/Cloud Run)
CMD ["sh", "-c", "python -m uvicorn api.app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
