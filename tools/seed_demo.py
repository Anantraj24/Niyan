import asyncio
import json
import sys
from pathlib import Path

# Add workspace root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from api.app.db.session import SessionLocal, init_db
from api.app.db.models import ScenarioSchemaRecord
from api.app.core.ids import scenario_schema_id
from api.app.services.model_service import ModelService
from api.app.services.analysis_service import AnalysisService

async def seed():
    print("--- NIYAM-X Demo Seeder ---")
    init_db()
    db = SessionLocal()
    try:
        model_service = ModelService(db)
        existing = [m for m in model_service.list_models() if "Refinery" in m.display_name]
        
        if existing:
            print(f"Refinery demo model already seeded: {existing[0].model_id}")
            model_id = existing[0].model_id
        else:
            mps_path = WORKSPACE_ROOT / "demo" / "refinery" / "refinery_lp.mps"
            with open(mps_path, "rb") as f:
                mps_bytes = f.read()

            imported = model_service.import_model(
                file_bytes=mps_bytes,
                filename="refinery_lp.mps",
                display_name="Synthetic Refinery Planning — Medium",
                dataset_kind="synthetic"
            )
            model_id = imported.model_id
            print(f"Successfully imported refinery model: {model_id} (version: {imported.version_id})")

            # Attach scenario schema
            schema_path = WORKSPACE_ROOT / "demo" / "refinery" / "scenario_schema.json"
            if schema_path.exists():
                with open(schema_path, "r", encoding="utf-8") as sf:
                    schema_json = sf.read()
                sch_rec = ScenarioSchemaRecord(
                    id=scenario_schema_id(),
                    model_id=model_id,
                    schema_json=schema_json
                )
                db.add(sch_rec)
                db.commit()
                print("Attached scenario parameter schema.")

            # Run Model X-Ray analysis
            analysis_service = AnalysisService(db)
            analysis = await analysis_service.analyze_model(model_id=model_id)
            print(f"Ran initial Model X-Ray: {analysis.analysis_id}")
            print(f"Variables: {analysis.profile.variables}, Constraints: {analysis.profile.constraints}, Nonzeros: {analysis.profile.nonzeros}")
            print(f"Autopilot Selected: {analysis.autopilot.backend} backend with {analysis.autopilot.scaling} scaling.")

        print("--- Demo Seeding Completed Successfully ---")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed())
