from __future__ import annotations

import pandas as pd
from time import perf_counter

from backend.core.config import ROOT_DIR, get_settings
from backend.models.schemas import SimulationRow, SimulationSummary, TicketState
from backend.services.orchestrator import ORCHESTRATOR
from backend.utils.ids import generate_request_id, generate_ticket_id


QUERIES = [
    "The food was bad and I want a refund",
    "My refund has not arrived yet",
    "I was charged twice for the same order",
    "I cannot log in because the OTP never arrived",
    "My account is locked after multiple sign-in attempts",
    "I need help with an unsupported enterprise request",
]


def run_simulation() -> tuple[list[SimulationRow], SimulationSummary]:
    settings = get_settings()
    rows: list[SimulationRow] = []

    for index in range(settings.simulation.runs):
        query = QUERIES[index % len(QUERIES)]
        state = TicketState(
            request_id=generate_request_id(),
            ticket_id=generate_ticket_id(),
            user_input=query,
        )
        started = perf_counter()
        final_state = ORCHESTRATOR.process(state)
        latency_ms = round((perf_counter() - started) * 1000, 3)
        rows.append(
            SimulationRow(
                request_id=final_state.request_id,
                ticket_id=final_state.ticket_id,
                query=query,
                status=final_state.status,
                sop_id=final_state.sop_id,
                latency_ms=latency_ms,
                confidence_score=final_state.confidence_score,
                revision_count=final_state.revision_count,
                success=final_state.status == "Auto-Resolved",
                before_response=final_state.response_before_critique,
                after_response=final_state.final_response,
                retrieved_context_count=len(final_state.retrieved_context),
            )
        )

    summary = SimulationSummary(
        runs=len(rows),
        resolution_rate=sum(1 for row in rows if row.status == "Auto-Resolved") / len(rows),
        escalation_rate=sum(1 for row in rows if row.status == "Escalated") / len(rows),
        avg_latency_ms=sum(row.latency_ms for row in rows) / len(rows),
        avg_revisions=sum(row.revision_count for row in rows) / len(rows),
        success_rate=sum(1 for row in rows if row.success) / len(rows),
    )
    return rows, summary


def write_outputs(rows: list[SimulationRow], summary: SimulationSummary) -> None:
    settings = get_settings()
    csv_path = ROOT_DIR / settings.simulation.output_csv
    json_path = ROOT_DIR / settings.simulation.output_json
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row.model_dump() for row in rows]).to_csv(csv_path, index=False)
    json_path.write_text(summary.model_dump_json(indent=2), encoding="utf-8")


if __name__ == "__main__":
    simulation_rows, simulation_summary = run_simulation()
    write_outputs(simulation_rows, simulation_summary)
    print(f"Simulation runs: {simulation_summary.runs}")
    print(f"Resolution rate: {simulation_summary.resolution_rate:.2%}")
    print(f"Escalation rate: {simulation_summary.escalation_rate:.2%}")
    print(f"Average latency: {simulation_summary.avg_latency_ms:.2f} ms")
