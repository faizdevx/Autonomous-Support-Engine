import streamlit as st
import pandas as pd

st.title("Autonomous Support Engine Dashboard")

# Load data
df = pd.read_csv("metrics.csv")

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    resolution_rate = (df["status"] == "Auto-Resolved").mean()
    st.metric("Resolution Rate", f"{resolution_rate*100:.1f}%")

with col2:
    escalation_rate = (df["status"] == "Escalated").mean()
    st.metric("Escalation Rate", f"{escalation_rate*100:.1f}%")

with col3:
    st.metric("Avg Latency", f"{df['latency'].mean():.2f}s")

with col4:
    improved_rate = df["improved"].mean()
    st.metric("Improved After Critique", f"{improved_rate*100:.1f}%")

st.subheader("📄 Ticket Logs")
st.dataframe(df)

st.subheader("🔍 Revisions Distribution")
st.bar_chart(df["revisions"].value_counts().sort_index())

st.subheader("🎯 Per-Ticket Analysis")
ticket_id = st.selectbox("Select Ticket", df["ticket_id"].tolist())

if ticket_id:
    selected = df[df["ticket_id"] == ticket_id].iloc[0]

    st.write(f"**Status:** {selected['status']}")
    st.write(f"**Latency:** {selected['latency']}s")
    st.write(f"**Revisions:** {selected['revisions']}")
    st.write(f"**Improved:** {selected['improved']}")

    st.write("**Drafts:**")
    drafts = eval(selected["drafts"])  # Convert string back to list
    for i, draft in enumerate(drafts):
        st.write(f"- Iteration {i}: {draft}")

    st.write("**Critic History:**")
    critic_history = eval(selected["critic_history"])
    for i, critic in enumerate(critic_history):
        st.write(f"- Iteration {i}: Scores {critic['scores']}, Feedback: {critic['feedback']}")