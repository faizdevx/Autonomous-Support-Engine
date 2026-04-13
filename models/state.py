class TicketState(BaseModel):
    ticket_id: str
    user_input: str

    # Router
    issue_category: Optional[str]
    active_sop: Optional[str]
    routing_confidence_score: Optional[float]

    # Knowledge
    retrieved_context: List[str] = []
    retrieval_score: Optional[float]

    # Responder
    current_draft: Optional[str]
    revision_count: int = 0
    critic_scores: Optional[dict]

    # Final
    status: str = "Pending"
    confidence_score: Optional[float]