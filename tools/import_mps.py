#!/usr/bin/env python3
"""
NIYAM-X — Command Line Model Importer
Imports any arbitrary MPS/LP optimization formulation into the local sovereign database,
computes cryptographic SHA-256 digests, and optionally runs Model X-Ray pre-solve analysis.
"""

import argparse
import asyncio
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


async def main():
    parser = argparse.ArgumentParser(
        description="Import an MPS optimization model into NIYAM-X sovereign repository."
    )
    parser.add_argument("--file", "-f", required=True, help="Path to .mps or .lp formulation file.")
    parser.add_argument("--name", "-n", default=None, help="Display name for the model.")
    parser.add_argument("--schema", "-s", default=None, help="Optional JSON scenario schema path.")
    parser.add_argument("--xray", action="store_true", default=True, help="Run Model X-Ray diagnostic immediately.")
    parser.add_argument("--dataset-kind", default="user", choices=["benchmark", "industrial", "synthetic", "user"])

    args = parser.parse_args()
    file_path = Path(args.file).resolve()

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    display_name = args.name or file_path.stem.replace("_", " ").title()

    init_db()
    db = SessionLocal()
    try:
        model_service = ModelService(db)
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        imported = model_service.import_model(
            file_bytes=file_bytes,
            filename=file_path.name,
            display_name=display_name,
            dataset_kind=args.dataset_kind
        )

        print(f"[SUCCESS] Model imported:")
        print(f"  Model ID:     {imported.model_id}")
        print(f"  Version ID:   {imported.version_id}")
        print(f"  Name:         {imported.display_name}")
        print(f"  Format:       {imported.format.upper()}")
        print(f"  Size:         {imported.size_bytes} bytes")
        print(f"  SHA-256:      {imported.sha256}")

        if args.schema:
            schema_p = Path(args.schema).resolve()
            if schema_p.exists():
                with open(schema_p, "r", encoding="utf-8") as sf:
                    sch_json = sf.read()
                sch_rec = ScenarioSchemaRecord(
                    id=scenario_schema_id(),
                    model_id=imported.model_id,
                    schema_json=sch_json
                )
                db.add(sch_rec)
                db.commit()
                print(f"[SUCCESS] Attached scenario parameter schema: {schema_p.name}")

        if args.xray:
            print("[INFO] Running Model X-Ray diagnostic...")
            analysis_service = AnalysisService(db)
            analysis = await analysis_service.analyze_model(model_id=imported.model_id)
            print(f"  Variables:     {analysis.profile.variables}")
            print(f"  Constraints:   {analysis.profile.constraints}")
            print(f"  Nonzeros:      {analysis.profile.nonzeros}")
            print(f"  Dynamic Range: {analysis.profile.coefficient_dynamic_range:.2e}")
            print(f"  Sparsity:      {(1.0 - analysis.profile.density) * 100:.2f}%")
            print(f"  Autopilot:     {analysis.autopilot.backend.upper()} backend, {analysis.autopilot.scaling} scaling")
            print(f"  Risk Level:    {analysis.risk.level} ({len(analysis.risk.issues)} issues)")

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
