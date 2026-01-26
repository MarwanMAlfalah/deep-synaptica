import time
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from agent.groq_client import groq_chat
from agent.tracing.tracer import Tracer

load_dotenv()

SYSTEM = "You are a helpful AI tutor. Be clear, structured, and concise."

def run(prompt: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:

    meta = meta or {}
    tracer = Tracer(agent_version="v0.1")

    goal = prompt.strip()

    # Step 1: Plan
    prompt_plan = f"Create a 7-day learning plan for: {goal}. Provide day-by-day bullets."
    t0 = time.time()
    plan = groq_chat([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt_plan},
    ])
    latency = int((time.time() - t0) * 1000)
    tracer.log_step("PLAN", prompt_plan, plan, latency_ms=latency, meta=meta)

    # Step 2: Micro-lesson
    prompt_lesson = "Teach Day 1 lesson (very short). End with 1 question to check understanding."
    t0 = time.time()
    lesson = groq_chat([
        {"role": "system", "content": SYSTEM},
        {"role": "assistant", "content": plan},
        {"role": "user", "content": prompt_lesson},
    ])
    latency = int((time.time() - t0) * 1000)
    tracer.log_step("LESSON", prompt_lesson, lesson, latency_ms=latency, meta=meta)

    # Step 3: Exercise
    prompt_ex = "Create a small exercise for Day 1 and provide the expected answer briefly."
    t0 = time.time()
    exercise = groq_chat([
        {"role": "system", "content": SYSTEM},
        {"role": "assistant", "content": lesson},
        {"role": "user", "content": prompt_ex},
    ])
    latency = int((time.time() - t0) * 1000)
    tracer.log_step("EXERCISE", prompt_ex, exercise, latency_ms=latency, meta=meta)

    # المهم: نرجّع نتيجة للـ API
    return {
        "run_id": tracer.run_id,
        "trace_file": getattr(tracer, "log_path", None),
        "status": "SUCCESS",
        "agent_version": "v0.1",
    }
    def run_agent(prompt: str, meta: dict | None = None):
        """
        Adapter function so API can call a stable entrypoint.
        """
        return run(prompt, meta)

def main():
    result = run("Learn Python basics in 7 days")
    print("✅ Run created:", result["run_id"])
    print("📄 Trace saved to:", result["trace_file"])

if __name__ == "__main__":
    main()
