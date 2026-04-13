def router_agent(state):
    prompt = f"""
    Classify this issue into:
    [billing, refund, tech, login]

    Text: {state.user_input}
    """

    result = call_llm(prompt)

    state.issue_category = result.lower()
    state.active_sop = f"{state.issue_category}_workflow"
    state.routing_confidence_score = 0.8

    return state