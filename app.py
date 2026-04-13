
def execute(state):
    if state.status == "Escalated":
        state.confidence_score = 0.3
    else:
        state.status = "Auto-Resolved"
        state.confidence_score = 0.9

    return state


@app.post("/process_ticket/{ticket_id}")
async def process_ticket(ticket_id: str):
    state = ticket_db[ticket_id]

    state = router_agent(state)
    state = knowledge_agent(state)
    state = run_responder_loop(state)
    state = execute(state)

    ticket_db[ticket_id] = state
    return state

    