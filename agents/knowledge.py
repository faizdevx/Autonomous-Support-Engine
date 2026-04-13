def knowledge_agent(state):
    if "refund" in state.issue_category:
        state.retrieved_context = [
            "Refund takes 7-10 days",
            "Order processed successfully"
        ]
        state.retrieval_score = 0.9

    return state