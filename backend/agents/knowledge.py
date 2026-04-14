from __future__ import annotations

from backend.models.schemas import TicketState
from backend.rag.retriever import retrieve_context


def run_knowledge(state: TicketState) -> dict[str, object]:
    chunks, average_score = retrieve_context(state.user_input, state.issue_category)
    return {
        "retrieved_context": [chunk.model_dump() for chunk in chunks],
        "retrieval_score": average_score,
        "retrieved_context_preview": [chunk.content for chunk in chunks],
        "retrieval_top_k": len(chunks),
    }
