from llm.hf_model import call_llm


def responder_agent(state):
    context = "\n".join(state.retrieved_context)

    prompt = f"""
    You MUST follow rules:

    1. Use ONLY the provided context
    2. If answer not in context → say "I don't have enough information"
    3. DO NOT add external knowledge

    CONTEXT:
    {context}

    QUESTION:
    {state.user_input}

    Improve based on feedback if provided.
    """

    draft = call_llm(prompt)

    state.current_draft = draft
    state.drafts.append(draft)   # 🔥 LOG IT

    return state
