# DataOps Copilot

An AI-powered data engineering assistant that detects, investigates, and
remediates data-quality and pipeline issues — built around Google Agent
Development Kit (ADK), Model Context Protocol (MCP), MCP Toolbox for
Databases, and Google Cloud data services (BigQuery, Cloud Storage, Pub/Sub,
Dataform).

**Core principle:** the AI investigates using evidence returned by
deterministic tools. It never invents findings — every number in its output
traces back to a real query against the data.

## Tool checklist

| Category | Status | Where |
| --- | --- | --- |
| Gemini API | Code path written, needs your API key to verify | `agent/agent.py` (`LLM_BACKEND=gemini`) |
| Gemini Agent Platform / Google ADK | Code path written, needs your API key to verify | `agent/agent.py::_investigate_with_adk` (`Agent`, `InMemoryRunner`) |
| MCP Toolbox for Databases | ✅ tool definitions verified | `mcp/tools.yaml` |
| BigQuery | Code path written; loader included, needs your project to verify | `dataops/bigquery.py`, `synthetic/load_to_bigquery.py` |
| Cloud Storage | Code path written, needs your project to verify | `dataops/storage.py` |
| Pub/Sub | Code path written, needs your project to verify | `dataops/pubsub.py` |
| Dataform | Code path written, needs your project to verify | `dataops/dataform.py` |
| Cloud Run | Manifests written, needs deploy to verify | `deploy/cloudrun-api.yaml`, `deploy/cloudrun-ui.yaml` |
| Cloud Monitoring | Code path written, needs your project to verify | `dataops/observability.py::record_metric` |
| Cloud Logging | Code path written, needs your project to verify | `dataops/observability.py::log_event` |
| IAM | Script written, needs your project to verify | `deploy/setup_iam.sh` |
| Python / SQL | ✅ verified locally | throughout `dataops/*.py` |
| FastAPI | ✅ verified locally | `api.py` |
| Streamlit | ✅ verified locally | `streamlit_app.py` |
| Docker | Verified to build; not deployed to Cloud Run yet | `Dockerfile`, `Dockerfile.streamlit`, `docker-compose.yml` |
| GitHub | ✅ CI workflow included | `.github/workflows/ci.yml` |

Everything marked **✅ verified locally** has actually been run end-to-end
against the SQLite/local mock in this repo (no cloud credentials needed —
see Quickstart). Everything marked **"needs your project to verify"** is
real, correct google-cloud-* client code that has *not yet been executed
against a live GCP project* — I don't have GCP credentials to test it here.
Follow **Going to production** below to run it against your own project
before you demo/submit, so you can honestly say it's been exercised for real.

## Quickstart (no cloud credentials required)

This repo runs out of the box against a local mock backend: a SQLite
database standing in for BigQuery, and local files standing in for GCS.
Swapping in real GCP is a one-line env change (see **Going to production**).

```bash
pip install -r requirements.txt

# generate a synthetic customer dataset with injected quality issues
python synthetic/generate_data.py

# run the full investigate -> remediate -> verify pipeline
python -m dataops.run_pipeline

# or serve the API
uvicorn api:app --reload
# then: curl http://localhost:8000/quality/status

# or launch the Streamlit UI on top of the API (in a second terminal)
pip install streamlit requests
streamlit run streamlit_app.py
```

### Or with Docker

```bash
docker compose up --build
# API:       http://localhost:8000/docs
# Streamlit: http://localhost:8501
```

Run the test suite:

```bash
pytest tests/ -v
```

## What the synthetic dataset contains

700 base customer rows, with:
- 35 rows with a NULL `customer_id`
- 50 rows with a malformed `email`
- 40 duplicate rows (exact clones re-inserted)
- a handful of rows older than the 7-day freshness threshold

`dataops/quality.py`'s checks are validated against these exact counts in
`tests/test_quality.py`.

## Architecture

```
Data Engineer/User -> DataOps Copilot (ADK agent) -> MCP Toolbox
    -> BigQuery / Cloud Storage / Pub/Sub / Dataform
    -> Deterministic Data Quality Checks
    -> Investigation & Remediation
    -> AI Investigation Summary
```

- **`agent/`** — the agent orchestrator (`agent.py`) and system prompt
  (`prompts.py`). Two backends: `LLM_BACKEND=none` (deterministic, offline,
  used by default and by the demo) and `LLM_BACKEND=anthropic` (a real
  tool-calling loop against Claude — a drop-in slot for Google ADK +
  Gemini/Vertex in production).
- **`dataops/`** — the deterministic tools themselves: quality checks
  (`quality.py`), remediation (`incidents.py`), freshness/verification
  (`monitoring.py`), and thin wrappers over BigQuery/GCS/Pub-Sub/Dataform
  that fall back to local mocks when `USE_MOCK_BACKEND=true`.
- **`mcp/tools.yaml`** — MCP Toolbox tool definitions exposing the
  `dataops/*.py` functions to the agent.
- **`dataops/observability.py`** — Cloud Logging (structured audit trail of
  every investigation/remediation) and Cloud Monitoring (custom metrics:
  issue counts, remediation counts) — falls back to stdout logging + an
  in-memory buffer in mock mode.
- **`synthetic/generate_data.py`** — builds the demo dataset described above.
- **`api.py`** — FastAPI wrapper: `/investigate`, `/remediate`,
  `/quality/status`, `/metrics`, `/health`.
- **`streamlit_app.py`** — chat UI over the API: ask for an investigation,
  read the evidence-grounded summary, confirm and trigger remediation.
- **`Dockerfile`** / **`Dockerfile.streamlit`** / **`docker-compose.yml`** —
  containerizes the API and UI for local demo or Cloud Run deployment.
- **`deploy/`** — `cloudrun-api.yaml` / `cloudrun-ui.yaml` (Cloud Run service
  manifests) and `setup_iam.sh` (creates the runtime service account and
  binds least-privilege roles for every GCP service used).
- **`.github/workflows/ci.yml`** — GitHub Actions: installs deps, regenerates
  the synthetic dataset, runs `pytest`, and smoke-tests the full pipeline on
  every push/PR.

## Going to production

1. Set `USE_MOCK_BACKEND=false` and provide `GCP_PROJECT_ID`, `GCS_BUCKET`,
   `PUBSUB_TOPIC` — `dataops/bigquery.py`, `storage.py`, `pubsub.py`,
   `dataform.py`, and `observability.py` already contain the real GCP client
   code paths (BigQuery, Cloud Storage, Pub/Sub, Dataform, Cloud Monitoring,
   Cloud Logging). All SQL in `dataops/quality.py` / `incidents.py` is
   written to run unchanged on both SQLite (mock) and BigQuery Standard SQL
   (schema lookups go through `client.get_schema()`, not `PRAGMA`; boolean
   predicates use `WHERE FALSE` not `WHERE 0`; parameters use `@name` style).
2. Load real data into BigQuery:
   ```bash
   export GCP_PROJECT_ID=your-project-id
   pip install google-cloud-bigquery
   python synthetic/generate_data.py        # writes synthetic/customer_data.csv
   python synthetic/load_to_bigquery.py      # creates the dataset/table and loads it
   ```
3. Point `mcp/tools.yaml`'s `bigquery_prod` source at your real
   project/dataset, and run it behind an actual MCP Toolbox server instead of
   the in-process Python bindings.
4. Set `LLM_BACKEND=gemini` and `GOOGLE_API_KEY` (or Vertex AI application
   default credentials) to run the real Google ADK + Gemini agent in
   `agent/agent.py::_investigate_with_adk` — the same `TOOL_REGISTRY`,
   mutation-confirmation gating, and evidence-only-response contract used by
   the offline demo carry over unchanged. `pip install google-adk google-genai`.
5. Run `bash deploy/setup_iam.sh` (with `GCP_PROJECT_ID` exported) to create
   the `dataops-copilot-sa` service account with least-privilege roles across
   BigQuery, Cloud Storage, Pub/Sub, Dataform, Cloud Monitoring, Cloud
   Logging, and Vertex AI.
6. Deploy to Cloud Run:
   ```bash
   gcloud run deploy dataops-copilot-api --source . \
     --service-account dataops-copilot-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com \
     --set-env-vars USE_MOCK_BACKEND=false,LLM_BACKEND=gemini,GCP_PROJECT_ID=$GCP_PROJECT_ID
   gcloud run deploy dataops-copilot-ui --source . --dockerfile Dockerfile.streamlit \
     --set-env-vars DATAOPS_API_URL=<api service URL>
   ```
   See `deploy/cloudrun-api.yaml` / `deploy/cloudrun-ui.yaml` for the
   declarative manifests.

## Security notes

- Never commit secrets — use `.env` (see `.env.example`) or a secret manager.
- Local binaries (e.g. `toolbox.exe`), virtual environments, and generated
  runtime artifacts (`mock_warehouse.db`, `storage_mock/`) are excluded via
  `.gitignore`.
- Restrict MCP allowed origins/hosts in production rather than using
  wildcard access.
