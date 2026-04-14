from __future__ import annotations

from backend.core.sops import SOP_REGISTRY
from backend.models.schemas import TicketState


def run_responder(state: TicketState) -> dict[str, object]:
    sop = SOP_REGISTRY[state.sop_id]
    if not state.retrieved_context:
        before = sop.missing_context_template
        return {
            "response_before_critique": before,
            "final_response_candidate": before,
        }

    context_summary = " ".join(chunk.content for chunk in state.retrieved_context[:2])
    before = sop.resolution_template.format(context_summary=context_summary)
    return {
        "response_before_critique": before,
        "final_response_candidate": before,
    }
