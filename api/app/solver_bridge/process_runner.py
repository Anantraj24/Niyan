import asyncio
import os
from pathlib import Path
from typing import AsyncGenerator, List, Dict, Optional
from api.app.core.logging import logger
from api.app.solver_bridge.event_parser import EventParser
from api.app.solver_bridge.protocol import SolverEvent

class ProcessRunner:
    _active_processes: Dict[str, asyncio.subprocess.Process] = {}
    _event_queues: Dict[str, List[asyncio.Queue]] = {}

    @classmethod
    def register_listener(cls, solve_id: str) -> asyncio.Queue:
        q = asyncio.Queue()
        if solve_id not in cls._event_queues:
            cls._event_queues[solve_id] = []
        cls._event_queues[solve_id].append(q)
        return q

    @classmethod
    def unregister_listener(cls, solve_id: str, q: asyncio.Queue):
        if solve_id in cls._event_queues:
            try:
                cls._event_queues[solve_id].remove(q)
            except ValueError:
                pass
            if not cls._event_queues[solve_id]:
                del cls._event_queues[solve_id]

    @classmethod
    def broadcast_event(cls, solve_id: str, event: Optional[SolverEvent]):
        if solve_id in cls._event_queues:
            for q in cls._event_queues[solve_id]:
                q.put_nowait(event)

    @classmethod
    async def cancel_solve(cls, solve_id: str) -> bool:
        proc = cls._active_processes.get(solve_id)
        if proc and proc.returncode is None:
            try:
                proc.terminate()
                await asyncio.sleep(0.5)
                if proc.returncode is None:
                    proc.kill()
                return True
            except Exception as e:
                logger.error(f"Error terminating process for {solve_id}: {e}")
        return False

    @classmethod
    async def run_solver_process(
        cls,
        solve_id: str,
        cmd: List[str],
        artifact_dir: Path
    ) -> AsyncGenerator[SolverEvent, None]:
        log_path = artifact_dir / "stdout.log"
        stderr_path = artifact_dir / "stderr.log"
        events_jsonl_path = artifact_dir / "events.jsonl"

        logger.info(f"Launching solver subprocess for {solve_id}: {' '.join(cmd)}")
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        cls._active_processes[solve_id] = proc

        with open(log_path, "w", encoding="utf-8") as f_log, \
             open(events_jsonl_path, "w", encoding="utf-8") as f_events:
            try:
                while True:
                    line_bytes = await proc.stdout.readline()
                    if not line_bytes:
                        break
                    line = line_bytes.decode("utf-8", errors="replace")
                    f_log.write(line)
                    f_log.flush()

                    event = EventParser.parse_line(line)
                    if event:
                        f_events.write(line)
                        f_events.flush()
                        cls.broadcast_event(solve_id, event)
                        yield event
            finally:
                cls._active_processes.pop(solve_id, None)
                # broadcast None to signal end of stream
                cls.broadcast_event(solve_id, None)

        _, stderr_bytes = await proc.communicate()
        if stderr_bytes:
            with open(stderr_path, "wb") as f_err:
                f_err.write(stderr_bytes)
        
        logger.info(f"Solver subprocess {solve_id} exited with return code {proc.returncode}")
