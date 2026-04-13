def responder_agent(state):
    context = "\n".join(state.retrieved_context)

    prompt = f"""
    Answer the user using ONLY this context:

    {context}

    Question: {state.user_input}
    """

    state.current_draft = call_llm(prompt)
    return state