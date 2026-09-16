import sys
from pathlib import Path
from typing import List, Optional
from api.app.config import settings

class CommandBuilder:
    @staticmethod
    def _base_cmd(binary_path: str) -> List[str]:
        p = Path(binary_path)
        if p.suffix.lower() == ".py":
            return [sys.executable, "-u", str(p)]
        return [str(p)]

    @classmethod
    def build_analyze_cmd(cls, model_path: str, output_path: str) -> List[str]:
        cmd = cls._base_cmd(settings.niyam_solver_path)
        cmd.extend([
            "analyze",
            "--model", str(model_path),
            "--output", str(output_path)
        ])
        return cmd

    @classmethod
    def build_solve_cmd(
        cls,
        model_path: str,
        output_path: str,
        proof_path: str,
        backend: str = "auto",
        scaling: str = "auto",
        time_limit: Optional[float] = None,
        iteration_limit: Optional[int] = None,
        tolerance: Optional[float] = None,
        warm_state_path: Optional[str] = None
    ) -> List[str]:
        cmd = cls._base_cmd(settings.niyam_solver_path)
        cmd.extend([
            "solve",
            "--model", str(model_path),
            "--output", str(output_path),
            "--proof", str(proof_path),
            "--backend", backend.lower(),
            "--scaling", scaling.lower(),
            "--events-jsonl"
        ])
        if time_limit is not None:
            cmd.extend(["--time-limit", str(time_limit)])
        if iteration_limit is not None:
            cmd.extend(["--iteration-limit", str(iteration_limit)])
        if tolerance is not None:
            cmd.extend(["--tolerance", str(tolerance)])
        if warm_state_path is not None:
            cmd.extend(["--warm-state", str(warm_state_path)])
        return cmd

    @classmethod
    def build_verify_cmd(
        cls,
        model_path: str,
        solution_path: str,
        proof_path: str,
        output_path: str
    ) -> List[str]:
        cmd = cls._base_cmd(settings.niyam_verify_path)
        cmd.extend([
            "--model", str(model_path),
            "--solution", str(solution_path),
            "--proof", str(proof_path),
            "--output", str(output_path)
        ])
        return cmd
