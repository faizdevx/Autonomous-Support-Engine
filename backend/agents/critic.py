from __future__ import annotations

from backend.models.schemas import TicketState


def run_critic(state: TicketState) -> dict[str, object]:
    before = state.response_before_critique
    tone = "please" in before.lower() or "i checked" in before.lower()
    completeness = bool(state.retrieved_context) or "do not have enough verified" in before.lower()
    factual_accuracy = bool(before)

    feedback: list[str] = []
    after = before

    if not tone:
        feedback.append("Add empathy and a clear ownership statement.")
        after = f"I understand the frustration here. {after}"

    if state.retrieved_context and "Please reply with" not in after:
        feedback.append("Add the required operational data for the SOP.")
        after = f"{after} Please reply with the required account details so we can verify the next step."

    if not state.retrieved_context and "escalate" not in after.lower():
        feedback.append("Make the fallback escalation path explicit.")
        after = f"{after} We will escalate this once the required details are provided."

    return {
        "critique": {
            "factual_accuracy": factual_accuracy,
            "tone": tone,
            "completeness": completeness,
            "feedback": feedback,
            "before_response": before,
            "after_response": after,
        },
        "revision_count": 1 if after != before else 0,
        "final_response_candidate": after,
    }
