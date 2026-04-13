def critic_agent(state):

    draft = state.current_draft or ""
    context = " ".join(state.retrieved_context).lower()

    # Check if draft contains words not in context (basic hallucination detection)
    draft_words = set(draft.lower().split())
    context_words = set(context.split())
    factual = draft_words.issubset(context_words) or any(word in context for word in draft_words)

    scores = {
        "factual_accuracy": factual,
        "tone": len(draft) > 40,
        "completeness": "please" in draft.lower() or "next" in draft.lower() or "information" in draft.lower()
    }

    feedback = []

    if not scores["factual_accuracy"]:
        feedback.append("Answer contains info not in context")

    if not scores["tone"]:
        feedback.append("Tone is too blunt, add empathy.")

    if not scores["completeness"]:
        feedback.append("Add clear next steps.")

    result = {
        "scores": scores,
        "feedback": " ".join(feedback)
    }

    state.critic_scores = scores
    state.critic_history.append(result)   # 🔥 LOG IT

    return state
