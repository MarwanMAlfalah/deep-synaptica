# Deep Synaptica

> **Make AI show its work.**\
> Turning black boxes into glass boxes.

Deep Synaptica is an agentic AI observability and evaluation platform.\
It transforms opaque AI systems into transparent, measurable, and
debuggable workflows by exposing every internal step of reasoning, tool
usage, latency, and outputs.

This project is designed as a research-grade infrastructure for: - AI
agent tracing\
- Run-level observability\
- Evaluation pipelines\
- Transparent experimentation

------------------------------------------------------------------------

## 🧠 What is Deep Synaptica?

Deep Synaptica is **not just an application**.\
It is a **system for evaluating AI systems themselves**.

Instead of building "another AI product", you are building: \> A
platform that inspects, measures, and explains how AI products think and
act.

------------------------------------------------------------------------

## 🏗 Architecture

    deep-synaptica/
    │
    ├── services/
    │   ├── api/         → FastAPI backend (runs, logs, health, tracing access)
    │   └── agent/       → Agent runtime (LLM logic + tracing hooks)
    │
    ├── apps/
    │   └── dashboard/   → Next.js 16 frontend (UI for observability)
    │
    └── README.md

Logical flow:

    User → Dashboard → API → Agent → Tracer → JSON Logs → API → Dashboard

------------------------------------------------------------------------

## ⚙️ Tech Stack

  Layer         Technology
  ------------- ---------------------------------
  Frontend      Next.js 16, TypeScript
  Backend API   FastAPI, Uvicorn
  Agent Core    Python 3.10+, Groq API
  Tracing       Custom JSON-based tracing
  Storage       JSONL logs (file-based for MVP)
  CI/CD         GitHub Actions
  Runtime       Node.js 20+, Python 3.10+

------------------------------------------------------------------------

## 🚀 Local Installation

### 1️⃣ Clone Repository

``` bash
git clone https://github.com/MarwanMAlfalah/deep-synaptica.git
cd deep-synaptica
```

### 2️⃣ Setup Python (Agent + API)

``` bash
cd services
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the API:

``` bash
cd api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Test:

``` bash
curl http://127.0.0.1:8000/health
```

### 3️⃣ Setup Dashboard (Frontend)

``` bash
cd ../../apps/dashboard
npm install
npm run dev
```

Open:

    http://localhost:3000

------------------------------------------------------------------------

## 🌐 API Endpoints

    GET    /health
    GET    /runs
    POST   /runs
    GET    /runs/{run_id}

------------------------------------------------------------------------

## ▶ Create a Run

``` bash
curl -X POST http://127.0.0.1:8000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 3-day Python learning plan",
    "meta": {}
  }'
```

------------------------------------------------------------------------

## 📜 License

MIT License.
