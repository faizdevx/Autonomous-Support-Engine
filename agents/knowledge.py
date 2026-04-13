"""Knowledge agent using RAG retrieval."""

from rag.retriever import retrieve_documents


def knowledge_agent(state):
    category = state.issue_category

    results = retrieve_documents(
        query=state.user_input,
        category=category,
        k=5
    )

    state.retrieved_context = [doc.page_content for doc in results]

    # Fake score (later can use cosine similarity)
    state.retrieval_score = 0.9 if results else 0.0

    return state
