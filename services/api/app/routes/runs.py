from fastapi import APIRouter, HTTPException
import os, json, glob, sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

router = APIRouter()

# --- paths ---
ROOT = Path(__file__).resolve().parents[3]          # services/api/app/routes -> services/api
SERVICES_DIR = ROOT.parent                          # services
AGENT_DIR = SERVICES_DIR / "agent"                  # services/agent

# ✅ make "agent" importable
if str(AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(AGENT_DIR))

TRACE_DIR = os.getenv("TRACE_DIR", str(ROOT / "data" / "logs"))
os.makedirs(TRACE_DIR, exist_ok=True)

# ✅ Stable import (works whether agent exposes run or main)
try:
    from agent.agent.run import run as run_agent
except Exception:
    from agent.agent.run import main as run_agent


class RunCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    meta: Dict[str, Any] = Field(default_factory=dict)

@router.get("/runs")
def list_runs() -> Dict[str, Any]:
    files = sorted(glob.glob(os.path.join(TRACE_DIR, "*.json")), reverse=True)
    runs: List[Dict[str, Any]] = []
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            runs.append({
                "run_id": data.get("run_id") or Path(fp).stem,
                "status": data.get("status", "UNKNOWN"),
                "latency_ms": data.get("latency_ms"),
                "agent_version": data.get("agent_version", "v0.1"),
                "steps": len(data.get("steps", [])),
                "created_at": data.get("created_at"),
            })
        except Exception:
            continue
    return {"total": len(runs), "runs": runs}

@router.get("/runs/{run_id}")
def get_run(run_id: str) -> Dict[str, Any]:
    fp = os.path.join(TRACE_DIR, f"{run_id}.json")
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Not Found")

    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/runs")
def create_run(body: RunCreateRequest) -> Dict[str, Any]:
    try:
        result = run_agent(body.prompt, body.meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    # result expected to include run_id, steps, status...
    run_id = result.get("run_id")
    if not run_id:
        # fallback: create id from filename approach if tracer returns trace_file only
        run_id = result.get("trace_file")
        if run_id:
            run_id = Path(run_id).stem

    # persist if tracer didn't already save
    fp = os.path.join(TRACE_DIR, f"{run_id}.json")
    if run_id and not os.path.exists(fp):
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return result
