from __future__ import annotations

from fastapi import FastAPI, HTTPException

from backend.core.config import get_settings
from backend.db.memory import get_ticket, save_ticket
from backend.models.schemas import QueryRequest, QueryResponse, TicketState
from backend.services.orchestrator import ORCHESTRATOR
from backend.utils.ids import generate_request_id, generate_ticket_id


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Deterministic SOP-based multi-agent support system with observability.",
    version="2.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest) -> QueryResponse:
    state = TicketState(
        request_id=generate_request_id(),
        ticket_id=request.ticket_id or generate_ticket_id(),
        user_input=request.text,
    )
    final_state = ORCHESTRATOR.process(state)
    save_ticket(final_state)
    return QueryResponse(
        request_id=final_state.request_id,
        ticket_id=final_state.ticket_id,
        status=final_state.status,
        sop_id=final_state.sop_id,
        issue_category=final_state.issue_category,
        final_answer=final_state.final_response,
        confidence_score=final_state.confidence_score,
        revision_count=final_state.revision_count,
        before_response=final_state.response_before_critique,
        after_response=final_state.final_response,
        critique_feedback=final_state.critique.feedback if final_state.critique else [],
        retrieved_context=final_state.retrieved_context,
        traces=final_state.traces,
    )


@app.get("/tickets/{ticket_id}", response_model=TicketState)
def read_ticket(ticket_id: str) -> TicketState:
    try:
        return get_ticket(ticket_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Ticket not found") from exc
