"""Business orchestration for ticket processing flows."""

from agents.router import router_agent
from agents.knowledge import knowledge_agent
from services.feedback_service import run_responder_loop
from services.supervisor_service import supervisor_agent
from models.state import TicketState


def process_ticket(state: TicketState) -> TicketState:
    state = router_agent(state)

    if state.status == "Escalated":
        return supervisor_agent(state)

    state = knowledge_agent(state)
    state = run_responder_loop(state)
    return supervisor_agent(state)
