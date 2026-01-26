import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

LOG_DIR = os.getenv("TRACE_DIR", os.path.join(os.getcwd(), "..", "..", "data", "logs"))

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class Tracer:
    def __init__(self, agent_version: str = "v0.1"):
        self.run_id = str(uuid.uuid4())
        self.agent_version = agent_version
        self.steps = []
        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_path = os.path.join(LOG_DIR, f"{self.run_id}.jsonl")

    def log_step(
        self,
        step_type: str,
        prompt: str,
        response: str,
        latency_ms: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        payload = {
            "run_id": self.run_id,
            "agent_version": self.agent_version,
            "step_type": step_type,
            "prompt": prompt,
            "response": response,
            "latency_ms": latency_ms,
            "meta": meta or {},
            "error": error,
            "created_at": _now_iso(),
        }
        self.steps.append(payload)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
