import time
from typing import Any, Dict, Optional
from dotenv import load_dotenv

from .groq_client import groq_chat
from .tracing.tracer import Tracer

load_dotenv()

SYSTEM = "You are a helpful AI tutor. Be clear, structured, and concise."


def run(prompt: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    meta = meta or {}
    tracer = Tracer(agent_version="v0.1")

    goal = prompt.strip()

    # Step 1: PLAN
    prompt_plan = f"Create a 7-day learning plan for: {goal}. Provide day-by-day bullets."
    t0 = time.time()
    plan = groq_chat(system=SYSTEM, prompt=prompt_plan)
    tracer.step(step_type="PLAN", prompt=prompt_plan, response=plan, latency_ms=int((time.time()-t0)*1000))

    # Step 2: EXPLAIN
    prompt_explain = f"Explain the plan briefly and give key tips. Plan:\n{plan}"
    t0 = time.time()
    explain = groq_chat(system=SYSTEM, prompt=prompt_explain)
    tracer.step(step_type="EXPLAIN", prompt=prompt_explain, response=explain, latency_ms=int((time.time()-t0)*1000))

    # Step 3: TODO
    prompt_todo = f"Give a compact checklist for execution. Plan:\n{plan}"
    t0 = time.time()
    todo = groq_chat(system=SYSTEM, prompt=prompt_todo)
    tracer.step(step_type="TODO", prompt=prompt_todo, response=todo, latency_ms=int((time.time()-t0)*1000))

    return tracer.finish(final_response=todo)

# ✅ Alias for compatibility: some code imports main()
def main(prompt: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return run(prompt, meta)

if __name__ == "__main__":
    main()
