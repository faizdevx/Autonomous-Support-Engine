import streamlit as st
import requests

st.set_page_config(page_title="Agentic AI System", layout="wide")

st.title("🤖 Agentic Support System")

query = st.text_input("Ask your issue")

if st.button("Submit"):

    res = requests.post(
        "http://localhost:8000/ask",
        json={"text": query}
    )

    data = res.json()

    st.subheader("💬 Response")
    st.write(data["response"])

    st.subheader("📊 Status")
    st.write(f"**Status:** {data['status']}")
    st.write(f"**Confidence:** {data['confidence']}")
    st.write(f"**Revisions:** {data['revisions']}")

    st.subheader("🧠 Reasoning")

    for i, draft in enumerate(data["logs"]["drafts"]):
        st.markdown(f"**Iteration {i}**")
        st.write(draft)

        if i < len(data["logs"]["critic"]):
            critic = data["logs"]["critic"][i]
            st.write(f"**Critic Scores:** {critic['scores']}")
            st.write(f"**Feedback:** {critic['feedback']}")