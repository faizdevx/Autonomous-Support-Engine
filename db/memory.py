from typing import Dict

from models.state import TicketState


ticket_db: Dict[str, TicketState] = {}


def get_ticket(ticket_id: str) -> TicketState:
    return ticket_db[ticket_id]


def save_ticket(state: TicketState) -> None:
    ticket_db[state.ticket_id] = state
