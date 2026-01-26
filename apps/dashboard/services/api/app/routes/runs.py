from fastapi import APIRouter, HTTPException
import os, json, glob, sys
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from agent.run import run_agent

# --- paths ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TRACE_DIR = os.getenv("TRACE_DIR", os.path.join(ROOT, "data", "logs"))

# IMPORTANT: allow importing "agent" package from services/agent
AGENT_SERVICE_DIR = os.path.join(ROOT, "services", "agent")
if AGENT_SERVICE_DIR not in sys.path:
    sys.path.insert(0, AGENT_SERVICE_DIR)

try:
    from agent.run import run as run_agent
except Exception as e:
    run_agent = None
    print("Failed to import agent.run.run:", e)

router = APIRouter(prefix="/runs", tags=["runs"])


def _list_runs() -> List[Dict[str, Any]]:
    runs: List[Dict[str, Any]] = []
    for path in sorted(glob.glob(os.path.join(TRACE_DIR, "*.jsonl")), reverse=True):
        run_id = os.path.splitext(os.path.basename(path))[0]
        step_count = 0
        total_latency_ms = 0
        status = "SUCCESS"
        agent_version = "v0.1"
        created_at = None

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    if "step_type" in obj:
                        step_count += 1
                        total_latency_ms += int(obj.get("latency_ms") or 0)
                    if obj.get("type") == "run":
                        created_at = obj.get("created_at") or created_at
                        status = obj.get("status") or status
                        agent_version = obj.get("agent_version") or agent_version
        except Exception:
            pass

        runs.append({
            "run_id": run_id,
            "agent_version": agent_version,
            "created_at": created_at,
            "step_count": step_count,
            "total_latency_ms": total_latency_ms,
            "status": status,
            "trace_file": os.path.basename(path),
        })
    return runs


@router.get("")
def runs_index() -> Dict[str, Any]:
    if not os.path.isdir(TRACE_DIR):
        return {"trace_dir": TRACE_DIR, "count": 0, "runs": []}
    items = _list_runs()
    return {"trace_dir": TRACE_DIR, "count": len(items), "runs": items}


@router.get("/{run_id}")
def run_details(run_id: str) -> Dict[str, Any]:
    path = os.path.join(TRACE_DIR, f"{run_id}.jsonl")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Not Found")

    steps: List[Dict[str, Any]] = []
    run_meta: Dict[str, Any] = {
        "run_id": run_id,
        "trace_file": os.path.basename(path),
        "status": "SUCCESS",
        "agent_version": "v0.1",
    }

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("type") == "run":
                run_meta.update(obj)
            else:
                steps.append(obj)

    run_meta["step_count"] = len(steps)
    run_meta["total_latency_ms"] = sum(int(s.get("latency_ms") or 0) for s in steps)
    return {"run": run_meta, "steps": steps}


class RunCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    meta: Optional[Dict[str, Any]] = None


@router.post("")
def create_run(body: RunCreateRequest):
    if run_agent is None:
        raise HTTPException(
            status_code=500,
            detail="Agent runner not wired yet (failed to import agent.run.run)"
        )

    try:
        return run_agent(prompt=body.prompt, meta=body.meta or {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
