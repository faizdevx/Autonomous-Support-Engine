from __future__ import annotations

from time import perf_counter

from backend.agents.critic import run_critic
from backend.agents.knowledge import run_knowledge
from backend.agents.responder import run_responder
from backend.agents.router import run_router
from backend.agents.supervisor import run_supervisor
from backend.core.logging import LOGGER
from backend.models.schemas import AgentTrace, CritiqueResult, RetrievedChunk, TicketState


class SupportOrchestrator:
    def _trace(
        self,
        state: TicketState,
        agent_name: str,
        agent_input: dict[str, object],
        agent_output: dict[str, object],
        started_at: float,
    ) -> None:
        trace = AgentTrace(
            request_id=state.request_id,
            agent_name=agent_name,
            input=agent_input,
            output=agent_output,
            latency_ms=round((perf_counter() - started_at) * 1000, 3),
            confidence=state.confidence_score,
            revision_count=state.revision_count,
        )
        state.traces.append(trace)
        LOGGER.write(trace)

    def process(self, state: TicketState) -> TicketState:
        started = perf_counter()
        router_output = run_router(state)
        self._trace(state, "router", {"user_input": state.user_input}, router_output, started)
        state.status = str(router_output["status"])
        state.issue_category = router_output.get("issue_category")  # type: ignore[assignment]
        state.sop_id = router_output.get("sop_id")  # type: ignore[assignment]
        state.required_data = list(router_output.get("required_data", []))
        state.escalation_conditions = list(router_output.get("escalation_conditions", []))
        if not state.sop_id:
            state.final_response = (
                "This request does not match a supported deterministic SOP yet. "
                "Please escalate it to a human agent."
            )
            state.resolution_reason = "No SOP match."
            return state

        started = perf_counter()
        knowledge_output = run_knowledge(state)
        self._trace(
            state,
            "knowledge",
            {"user_input": state.user_input, "issue_category": state.issue_category},
            knowledge_output,
            started,
        )
        state.retrieved_context = [
            RetrievedChunk.model_validate(chunk) for chunk in knowledge_output["retrieved_context"]
        ]
        state.retrieval_score = float(knowledge_output["retrieval_score"])
        state.retrieved_context_preview = list(knowledge_output["retrieved_context_preview"])
        state.retrieval_top_k = int(knowledge_output["retrieval_top_k"])

        started = perf_counter()
        responder_output = run_responder(state)
        self._trace(
            state,
            "responder",
            {"sop_id": state.sop_id, "retrieved_context_count": len(state.retrieved_context)},
            responder_output,
            started,
        )
        state.response_before_critique = str(responder_output["response_before_critique"])

        started = perf_counter()
        critic_output = run_critic(state)
        self._trace(
            state,
            "critic",
            {"response_before_critique": state.response_before_critique},
            critic_output,
            started,
        )
        state.critique = CritiqueResult.model_validate(critic_output["critique"])
        state.revision_count = int(critic_output["revision_count"])

        started = perf_counter()
        supervisor_output = run_supervisor(state)
        self._trace(
            state,
            "supervisor",
            {"retrieval_score": state.retrieval_score, "revision_count": state.revision_count},
            supervisor_output,
            started,
        )
        state.status = str(supervisor_output["status"])
        state.confidence_score = float(supervisor_output["confidence_score"])
        state.final_response = str(supervisor_output["final_response"])
        state.resolution_reason = str(supervisor_output["resolution_reason"])
        return state


ORCHESTRATOR = SupportOrchestrator()
