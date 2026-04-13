"""Supervisor logic for final ticket decisioning."""

from services.feedback_service import compute_confidence


def supervisor_agent(state):
    state.confidence_score = compute_confidence(state)

    if state.confidence_score < 0.7 or state.status == "Escalated":
        state.status = "Escalated"
        state.handoff_summary = f"Issue unresolved: {state.user_input}"
    else:
        state.status = "Auto-Resolved"

    return state
