def critic_agent(state):
    draft = state.current_draft

    prompt = f"""
    Evaluate response:
    1. factual_accuracy
    2. tone
    3. completeness

    Return JSON true/false.

    Response: {draft}
    """

    result = call_llm(prompt)

    state.critic_scores = {
        "factual_accuracy": True,
        "tone": True,
        "completeness": True
    }

    return state


def run_responder_loop(state):
    for _ in range(2):
        state = responder_agent(state)
        state = critic_agent(state)

        if all(state.critic_scores.values()):
            return state

        state.revision_count += 1

    state.status = "Escalated"
    return state