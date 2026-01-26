<<<<<<< HEAD
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
=======
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
>>>>>>> da47f2a (Update readme)
