from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TicketState(BaseModel):
    ticket_id: str
    user_input: str

    # Router
    issue_category: Optional[str] = None
    active_sop: Optional[str] = None
    routing_confidence_score: Optional[float] = None

    # Knowledge
    retrieved_context: List[str] = Field(default_factory=list)
    retrieval_score: Optional[float] = None

    # Responder
    current_draft: Optional[str] = None
    revision_count: int = 0
    critic_scores: Dict[str, bool] = Field(default_factory=dict)

    # NEW: store ALL drafts
    drafts: List[str] = Field(default_factory=list)

    # NEW: store ALL critic outputs
    critic_history: List[Dict] = Field(default_factory=list)

    # Final
    status: str = "Pending"
    confidence_score: Optional[float] = None
    handoff_summary: Optional[str] = None
