
from fastapi import FastAPI, HTTPException

from db.memory import get_ticket, save_ticket
from services.ticket_processor import process_ticket
from models.state import TicketState

app = FastAPI(title="Autonomous Support Engine")


@app.post("/process_ticket/{ticket_id}", response_model=TicketState)
async def process_ticket_endpoint(ticket_id: str):
    try:
        state = get_ticket(ticket_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Ticket not found")

    state = process_ticket(state)
    save_ticket(state)
    return state
