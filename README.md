# Autonomous Support Engine

Multi-agent customer support system with:
- SOP-based routing
- RAG grounding (no hallucination)
- Self-critique loop
- Confidence-based escalation

## Setup

```bash
git clone <repo>
cd autonomous-support-engine
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn app:app --reload
```

## Run Simulation

```bash
python simulate.py
```

Generates: `metrics.csv` (performance data)

## Run Dashboard

```bash
streamlit run dashboard.py
```

## Features

- Deterministic workflows (billing, login, API)
- No hallucination (context-only responses)
- Critic loop improves answers
- Metrics: resolution rate, latency, revisions

## Architecture

Router → Knowledge (RAG) → Responder → Critic → Supervisor

## Goal

Not a chatbot. A system that processes tickets, validates responses, escalates when uncertain. 

Agents DO NOT decide freely

SOP decides → Agents execute

SOP I WILL BE DEFINING IN THIS:-

✅ SOP 1: Refund Not Received
✅ SOP 2: Login Issue (Auth)
