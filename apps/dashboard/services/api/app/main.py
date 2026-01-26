from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import runs

from app.routes import health, runs

app = FastAPI(title="Deep Synaptica API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(runs.router)
