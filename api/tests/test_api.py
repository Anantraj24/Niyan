import sys
import asyncio
import pytest
from pathlib import Path
import httpx

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from api.app.main import app
from api.app.db.session import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()

@pytest.mark.anyio
async def test_health():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["solver_available"] is True
        assert data["verifier_available"] is True

@pytest.mark.anyio
async def test_root_serves_frontend():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/")
        assert res.status_code == 200
        # When frontend/dist is built, it serves text/html; otherwise it serves application/json
        assert "text/html" in res.headers["content-type"] or "application/json" in res.headers["content-type"]

@pytest.mark.anyio
async def test_hardware():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/hardware")
        assert res.status_code == 200
        data = res.json()
        assert "cpu" in data
        assert "gpu" in data
        assert data["cpu"]["logical_cores"] > 0

@pytest.mark.anyio
async def test_models_flow_and_solve():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List models
        res = await ac.get("/api/v1/models")
        assert res.status_code == 200
        models = res.json()
        assert len(models) >= 1
        model_id = models[0]["model_id"]

        # 2. Get model detail & scenario schema
        res = await ac.get(f"/api/v1/models/{model_id}")
        assert res.status_code == 200
        assert res.json()["model_id"] == model_id

        schema_res = await ac.get(f"/api/v1/models/{model_id}/schema")
        if schema_res.status_code == 200:
            assert "parameters" in schema_res.json()

        # 3. Model X-Ray Analysis
        res = await ac.post(f"/api/v1/models/{model_id}/analyze")
        assert res.status_code == 200
        analysis = res.json()
        assert "profile" in analysis
        assert "risk" in analysis
        assert "autopilot" in analysis

        # 4. Create Solve
        res = await ac.post("/api/v1/solves", json={
            "model_id": model_id,
            "config": {
                "backend": "CPU",
                "scaling": "BASIC",
                "time_limit_sec": 10
            }
        })
        assert res.status_code == 202
        solve_data = res.json()
        solve_id = solve_data["solve_id"]
        assert solve_data["state"] == "QUEUED"

        # Wait for solve to finish
        completed = False
        for _ in range(40):
            await asyncio.sleep(0.15)
            st_res = await ac.get(f"/api/v1/solves/{solve_id}")
            assert st_res.status_code == 200
            st = st_res.json()
            if st["state"] in ("COMPLETED", "FAILED"):
                completed = True
                assert st["solver_status"] in ("OPTIMAL", "FEASIBLE")
                assert st["objective"] is not None
                break
        assert completed is True

        # 5. Independent Verification
        v_res = await ac.post(f"/api/v1/solves/{solve_id}/verify")
        assert v_res.status_code == 202
        v_data = v_res.json()
        assert v_data["state"] == "COMPLETED"
        assert v_data["verdict"] == "VERIFIED"
        assert v_data["model_hash_match"] is True

        # 5b. Proof Pack ZIP Export
        exp_res = await ac.get(f"/api/v1/solves/{solve_id}/proof/export")
        assert exp_res.status_code == 200
        assert exp_res.headers["content-type"] == "application/zip"
        assert len(exp_res.content) > 100

        # 6. DeltaSolve re-solve
        delta_res = await ac.post(f"/api/v1/solves/{solve_id}/resolve", json={
            "changes": {
                "parameters": {
                    "CDU_CAP": 105000.0
                }
            },
            "config": {
                "backend": "CPU",
                "time_limit_sec": 10
            }
        })
        assert delta_res.status_code == 200
        delta_data = delta_res.json()
        assert delta_data["parent_solve_id"] == solve_id
        assert delta_data["warm_start_requested"] is True
