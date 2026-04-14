from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    rank: int
    score: float
    category: str
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)


class CritiqueResult(BaseModel):
    factual_accuracy: bool
    tone: bool
    completeness: bool
    feedback: list[str] = Field(default_factory=list)
    before_response: str
    after_response: str


class AgentTrace(BaseModel):
    request_id: str
    agent_name: str
    input: dict[str, Any]
    output: dict[str, Any]
    latency_ms: float
    confidence: float | None = None
    revision_count: int = 0


class TicketState(BaseModel):
    request_id: str
    ticket_id: str
    user_input: str
    issue_category: str | None = None
    sop_id: str | None = None
    required_data: list[str] = Field(default_factory=list)
    escalation_conditions: list[str] = Field(default_factory=list)
    retrieved_context: list[RetrievedChunk] = Field(default_factory=list)
    retrieval_score: float = 0.0
    retrieval_top_k: int = 0
    response_before_critique: str = ""
    final_response: str = ""
    critique: CritiqueResult | None = None
    confidence_score: float = 0.0
    revision_count: int = 0
    status: str = "Pending"
    resolution_reason: str = ""
    traces: list[AgentTrace] = Field(default_factory=list)
    retrieved_context_preview: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    text: str
    ticket_id: str | None = None


class QueryResponse(BaseModel):
    request_id: str
    ticket_id: str
    status: str
    sop_id: str | None
    issue_category: str | None
    final_answer: str
    confidence_score: float
    revision_count: int
    before_response: str
    after_response: str
    critique_feedback: list[str]
    retrieved_context: list[RetrievedChunk]
    traces: list[AgentTrace]


class SimulationRow(BaseModel):
    request_id: str
    ticket_id: str
    query: str
    status: str
    sop_id: str | None
    latency_ms: float
    confidence_score: float
    revision_count: int
    success: bool
    before_response: str
    after_response: str
    retrieved_context_count: int


class SimulationSummary(BaseModel):
    runs: int
    resolution_rate: float
    escalation_rate: float
    avg_latency_ms: float
    avg_revisions: float
    success_rate: float
