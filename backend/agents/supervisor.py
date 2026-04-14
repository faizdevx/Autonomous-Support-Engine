from __future__ import annotations

from backend.models.schemas import TicketState


def run_supervisor(state: TicketState) -> dict[str, object]:
    critique = state.critique
    route_score = 1.0 if state.sop_id else 0.0
    retrieval_score = 1.0 if state.retrieved_context else 0.0
    critique_score = (
        sum(
            [
                1.0 if critique and critique.factual_accuracy else 0.0,
                1.0 if critique and critique.tone else 0.0,
                1.0 if critique and critique.completeness else 0.0,
            ]
        )
        / 3.0
        if critique
        else 0.0
    )
    confidence = round((route_score + retrieval_score + critique_score) / 3.0, 2)
    should_escalate = not state.sop_id or not state.retrieved_context or confidence < 0.7
    return {
        "status": "Escalated" if should_escalate else "Auto-Resolved",
        "confidence_score": confidence,
        "final_response": state.critique.after_response if state.critique else state.response_before_critique,
        "resolution_reason": (
            "Escalated due to missing deterministic support context."
            if should_escalate
            else "Resolved through deterministic SOP flow."
        ),
    }
