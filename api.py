"""
DataOps Copilot API.

Run:
    uvicorn api:app --reload

Endpoints:
    POST /investigate   {"request": "..."}      -> agent investigation summary + evidence
    POST /remediate      {"confirm": true}       -> runs quarantine + cleaned dataset + verification
    GET  /quality/status                         -> raw evidence, no narrative
    GET  /metrics                                -> in-memory audit log / custom metrics buffer
    GET  /health
"""
import os

from fastapi import FastAPI
from pydantic import BaseModel

from agent.agent import DataOpsAgent
from dataops import quality, observability

app = FastAPI(title="DataOps Copilot API", version="0.1.0")
agent = DataOpsAgent()


class InvestigateRequest(BaseModel):
    request: str


class RemediateRequest(BaseModel):
    confirm: bool = False


@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm_backend": os.environ.get("LLM_BACKEND", "none"),
        "mock_backend": os.environ.get("USE_MOCK_BACKEND", "true"),
    }


@app.get("/metrics")
def metrics():
    return {"metrics": observability.METRICS_BUFFER[-100:]}


@app.get("/quality/status")
def quality_status():
    return quality.overall_status()


@app.post("/investigate")
def investigate(body: InvestigateRequest):
    return agent.investigate(body.request)


@app.post("/remediate")
def remediate(body: RemediateRequest):
    return agent.remediate(confirm=body.confirm)
