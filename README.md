# Autonomous Support Engine

Multi-agent customer support system with:
- SOP-based routing
- RAG grounding (no hallucination)
- Self-critique loop
- Confidence-based escalation

## 🚀 Quick Prototype (5 minutes)

```bash
pip install -r requirements.txt

# Terminal 1: Start API
uvicorn app:app --reload

# Terminal 2: Start UI
streamlit run app_ui.py
```

**Open http://localhost:8501 and ask questions!**

See the response, confidence, revisions, and full reasoning.

## 🌍 Share with Anyone (ngrok)

```bash
pip install pyngrok
ngrok http 8501
```

Send the ngrok URL (e.g., https://abc123.ngrok.io) to anyone for instant demo.

## Full Setup

```bash
git clone <repo>
cd autonomous-support-engine
pip install -r requirements.txt
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

Agents DO NOT decide freely

SOP decides → Agents execute

SOP I WILL BE DEFINING IN THIS:-

✅ SOP 1: Refund Not Received
✅ SOP 2: Login Issue (Auth)
