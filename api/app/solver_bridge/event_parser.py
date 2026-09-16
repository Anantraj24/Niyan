import json
from typing import Optional, Dict, Any
from api.app.solver_bridge.protocol import SolverEvent

class EventParser:
    @staticmethod
    def parse_line(line: str) -> Optional[SolverEvent]:
        line = line.strip()
        if not line or not line.startswith("{"):
            return None
        try:
            data = json.loads(line)
            if "type" in data and "seq" in data:
                return SolverEvent(**data)
            return None
        except Exception:
            return None

    @staticmethod
    def to_sse(event: SolverEvent) -> str:
        """Format a SolverEvent as Server-Sent Event text."""
        event_name = event.type
        data_json = json.dumps({
            "seq": event.seq,
            "timestamp_ms": event.timestamp_ms,
            **event.data
        })
        return f"id: {event.seq}\nevent: {event_name}\ndata: {data_json}\n\n"
