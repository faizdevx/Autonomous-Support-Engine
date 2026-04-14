from __future__ import annotations

from backend.core.sops import match_sop
from backend.models.schemas import TicketState


def run_router(state: TicketState) -> dict[str, object]:
    sop = match_sop(state.user_input)
    if sop is None:
        return {
            "status": "Escalated",
            "issue_category": None,
            "sop_id": None,
            "required_data": [],
            "escalation_conditions": ["No deterministic SOP matched the request."],
        }

    return {
        "status": "Routed",
        "issue_category": sop.category,
        "sop_id": sop.sop_id,
        "required_data": list(sop.required_data),
        "escalation_conditions": list(sop.escalation_conditions),
        "steps": list(sop.steps),
    }
