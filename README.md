# Autonomous Support Engine

Deterministic multi-agent support system for refund and login workflows. The pipeline is fixed, retrieval-backed, and observable end to end.

## Quick Start

```bash
pip install -r requirements.txt
python scripts/seed_data.py
uvicorn app:app --reload
```

In a second terminal:

```bash
streamlit run app_ui.py
```

Optional metrics run:

```bash
python scripts/simulate.py
streamlit run dashboard.py
```

## What It Does

- Enforces a fixed orchestration path: `Router -> Knowledge -> Responder -> Critic -> Supervisor`
- Supports 2 deterministic SOPs:
  - `refund_not_received`
  - `login_issue`
- Answers from retrieved context only
- Tracks before-vs-after critique revisions
- Writes structured traces to JSONL and SQLite
- Ships with a clean Streamlit operator UI and metrics dashboard

## Architecture

```text
User / UI
    |
    v
FastAPI API
    |
    v
SupportOrchestrator
    |
    +--> Router       -> match deterministic SOP
    +--> Knowledge    -> retrieve top-k context chunks
    +--> Responder    -> build SOP-bound draft
    +--> Critic       -> score + revise draft
    +--> Supervisor   -> resolve or escalate
    |
    +--> Structured Logs (JSONL + SQLite)
    +--> Simulation Metrics (CSV + JSON)
```

## Folder Structure

```text
backend/
  api/
  core/
  agents/
  services/
  rag/
  models/
  db/
  utils/
frontend/
  streamlit_app.py
  dashboard.py
scripts/
  simulate.py
  seed_data.py
data/
  synthetic_support_dataset.json
configs/
  config.yaml
logs/
app.py
app_ui.py
dashboard.py
simulate.py
requirements.txt
README.md
```

## SOPs

### SOP 1: Refund Not Received

Required data:
- `order_id`
- `refund_request_date`
- `payment_method`

Steps:
- Confirm the request is refund-related.
- Retrieve billing refund context.
- Respond only with retrieved refund guidance.
- Ask for the required operational data.

Escalate when:
- No refund context is retrieved.
- The user requests a policy exception.
- Required refund details are missing.

### SOP 2: Login Issue

Required data:
- `email`
- `last_login_attempt_at`
- `device_or_browser`

Steps:
- Confirm the request is login-related.
- Retrieve login troubleshooting context.
- Respond only with retrieved login guidance.
- Ask for the required operational data.

Escalate when:
- No login context is retrieved.
- The issue implies security review or lockout without context support.
- Required login details are missing.

## Frontend

The Streamlit app shows:

- Final answer
- Confidence score
- Revision count
- Before vs after critique output
- Retrieved context
- Per-agent traces

Screenshot placeholders:

- `docs/screenshots/chat.png`
- `docs/screenshots/dashboard.png`

## Observability

Generated files:

- `logs/agent_runs.jsonl`
- `logs/agent_runs.db`
- `logs/simulation_metrics.csv`
- `logs/simulation_summary.json`

Each agent trace includes:

- `request_id`
- `agent_name`
- `input`
- `output`
- `latency_ms`
- `confidence`
- `revision_count`

## Configuration

Primary config lives in [configs/config.yaml](configs/config.yaml).

Environment overrides:

- `SUPPORT_API_URL`
- `ASE_CONFIG_PATH`
- `ASE_ENV`

Optional local env file:

- Copy `.env.example` to `.env` and adjust values as needed.

## API

Key endpoints:

- `GET /health`
- `POST /ask`
- `GET /tickets/{ticket_id}`

Interactive docs:

- `http://localhost:8000/docs`

## Docker

```bash
docker build -t autonomous-support-engine .
docker run -p 8000:8000 autonomous-support-engine
```

## Demo Queries

- `The food was bad and I want a refund`
- `My refund has not arrived yet`
- `I cannot log in because the OTP never arrived`
- `My account is locked after multiple sign-in attempts`

## Project Value

- Predictable support automation for narrow SOPs
- Retrieval-backed outputs instead of freeform answers
- Faster debugging through explicit traces and revision tracking
- Lightweight local setup for demos, experiments, and extensions
