from __future__ import annotations

import os

import requests
import streamlit as st


API_BASE_URL = os.getenv("SUPPORT_API_URL", "http://localhost:8000")


st.set_page_config(page_title="Autonomous Support Engine", page_icon="AE", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(218, 234, 255, 0.9), transparent 35%),
            linear-gradient(180deg, #f6f2ea 0%, #ffffff 55%, #eef4f8 100%);
    }
    .hero {
        padding: 1.5rem 1.75rem;
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.76);
        border: 1px solid rgba(23, 37, 84, 0.08);
        box-shadow: 0 24px 50px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(15, 23, 42, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.4rem;">Autonomous Support Engine</h1>
        <p style="margin:0;color:#334155;">
            Deterministic SOP routing, retrieval-backed responses, critique tracking, and operator-grade traces.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(f"Backend API: `{API_BASE_URL}`")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Describe the support issue")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(f"{API_BASE_URL}/ask", json={"text": prompt}, timeout=30)
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.RequestException as exc:
            st.error(f"Backend request failed: {exc}")
        else:
            st.markdown(payload["final_answer"])
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            with metrics_col1:
                st.markdown(
                    f"<div class='metric-card'><strong>Status</strong><br>{payload['status']}</div>",
                    unsafe_allow_html=True,
                )
            with metrics_col2:
                st.markdown(
                    f"<div class='metric-card'><strong>Confidence</strong><br>{payload['confidence_score']}</div>",
                    unsafe_allow_html=True,
                )
            with metrics_col3:
                st.markdown(
                    f"<div class='metric-card'><strong>Revisions</strong><br>{payload['revision_count']}</div>",
                    unsafe_allow_html=True,
                )

            tab1, tab2, tab3, tab4 = st.tabs(["Before vs After", "Retrieved Context", "Critique", "Agent Traces"])
            with tab1:
                st.markdown("**Before critique**")
                st.write(payload["before_response"] or "No initial draft.")
                st.markdown("**After critique**")
                st.write(payload["after_response"] or "No revised draft.")
            with tab2:
                for chunk in payload["retrieved_context"]:
                    st.markdown(
                        f"**#{chunk['rank']} {chunk['title']}**  \n"
                        f"Score: `{chunk['score']}` | Category: `{chunk['category']}`"
                    )
                    st.write(chunk["content"])
            with tab3:
                feedback = payload.get("critique_feedback") or ["No critique changes applied."]
                for item in feedback:
                    st.write(f"- {item}")
            with tab4:
                for trace in payload["traces"]:
                    st.json(trace, expanded=False)

            st.session_state.messages.append({"role": "assistant", "content": payload["final_answer"]})
