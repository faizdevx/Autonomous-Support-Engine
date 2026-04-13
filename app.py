
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db.memory import get_ticket, save_ticket
from services.ticket_processor import process_ticket
from models.state import TicketState

app = FastAPI(title="Autonomous Support Engine")

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask(query: Query):
    state = TicketState(
        ticket_id="demo",
        user_input=query.text
    )

    final = process_ticket(state)

    return {
        "response": final.current_draft,
        "status": final.status,
        "confidence": final.confidence_score,
        "revisions": final.revision_count,
        "logs": {
            "drafts": final.drafts,
            "critic": final.critic_history
        }
    }

@app.post("/process_ticket/{ticket_id}", response_model=TicketState)
async def process_ticket_endpoint(ticket_id: str):
    try:
        state = get_ticket(ticket_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Ticket not found")

    state = process_ticket(state)
    save_ticket(state)
    return state
