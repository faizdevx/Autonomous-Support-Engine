from __future__ import annotations

from backend.models.schemas import TicketState


_TICKET_STORE: dict[str, TicketState] = {}


def save_ticket(state: TicketState) -> None:
    _TICKET_STORE[state.ticket_id] = state


def get_ticket(ticket_id: str) -> TicketState:
    return _TICKET_STORE[ticket_id]
