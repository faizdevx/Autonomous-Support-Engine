"""Feedback and self-correction loop services."""

from agents.critic import critic_agent
from agents.responder import responder_agent


def run_responder_loop(state):
    while state.revision_count < 2:

        state = responder_agent(state)
        state = critic_agent(state)

        if all(state.critic_scores.values()):
            return state

        # 🔥 Inject feedback into next iteration
        last_feedback = state.critic_history[-1]["feedback"]

        state.user_input += f"\nImprove based on: {last_feedback}"

        state.revision_count += 1

    state.status = "Escalated"
    return state


def compute_confidence(state):
    retrieval = state.retrieval_score or 0
    critic_pass = bool(state.critic_scores) and all(state.critic_scores.values())
    llm_confidence = 0.9 if critic_pass else 0.4
    return (retrieval + llm_confidence) / 2


def generate_improvement_log(state):
    logs = []

    for i in range(len(state.drafts)):
        logs.append({
            "iteration": i,
            "draft": state.drafts[i],
            "critic": state.critic_history[i] if i < len(state.critic_history) else None
        })

    return logs


def get_improvement_metrics(state):
    return {
        "total_revisions": state.revision_count,
        "improved": state.revision_count > 0,
        "final_pass": all(state.critic_scores.values())
    }
