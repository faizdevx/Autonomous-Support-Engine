from llm.hf_model import call_llm

SOP_REGISTRY = {
    "billing_refund": "refund_workflow",
    "auth_login": "login_workflow"
}

CATEGORY_MAPPING = {
    "billing_refund": "billing",
    "auth_login": "login"
}


def router_agent(state):
    prompt = f"""
    Classify into:
    [billing_refund, auth_login]

    Text: {state.user_input}
    """

    result = call_llm(prompt).strip().lower()

    if result not in SOP_REGISTRY:
        state.status = "Escalated"
        return state

    state.issue_category = CATEGORY_MAPPING.get(result, result)
    state.active_sop = SOP_REGISTRY[result]
    state.routing_confidence_score = 0.9
    return state
