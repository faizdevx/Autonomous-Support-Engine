from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st


METRICS_PATH = Path("logs/simulation_metrics.csv")
SUMMARY_PATH = Path("logs/simulation_summary.json")

st.set_page_config(page_title="ASE Metrics", page_icon="AE", layout="wide")
st.title("Autonomous Support Engine Metrics")

if not METRICS_PATH.exists():
    st.warning("Run `python scripts/simulate.py` to generate dashboard data.")
    st.stop()

df = pd.read_csv(METRICS_PATH)
summary = {}
if SUMMARY_PATH.exists():
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Resolution Rate", f"{summary.get('resolution_rate', (df['status'] == 'Auto-Resolved').mean()) * 100:.1f}%")
col2.metric("Escalation Rate", f"{summary.get('escalation_rate', (df['status'] == 'Escalated').mean()) * 100:.1f}%")
col3.metric("Avg Latency", f"{summary.get('avg_latency_ms', df['latency_ms'].mean()):.1f} ms")
col4.metric("Avg Revisions", f"{summary.get('avg_revisions', df['revision_count'].mean()):.2f}")

chart_left, chart_right = st.columns(2)
with chart_left:
    st.subheader("Status Distribution")
    st.bar_chart(df["status"].value_counts())
with chart_right:
    st.subheader("Latency by Ticket")
    st.line_chart(df.set_index("ticket_id")["latency_ms"])

st.subheader("Simulation Runs")
st.dataframe(df, use_container_width=True)
