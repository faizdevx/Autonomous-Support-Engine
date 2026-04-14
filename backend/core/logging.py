from __future__ import annotations

import json
import sqlite3

from backend.core.config import ROOT_DIR, get_settings
from backend.models.schemas import AgentTrace


class StructuredLogger:
    def __init__(self) -> None:
        settings = get_settings()
        self.json_path = ROOT_DIR / settings.logging.json_log_path
        self.sqlite_path = ROOT_DIR / settings.logging.sqlite_path
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_sqlite()

    def _ensure_sqlite(self) -> None:
        with sqlite3.connect(self.sqlite_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_runs (
                    request_id TEXT,
                    agent_name TEXT,
                    agent_input TEXT,
                    agent_output TEXT,
                    latency_ms REAL,
                    confidence REAL,
                    revision_count INTEGER
                )
                """
            )

    def write(self, trace: AgentTrace) -> None:
        payload = trace.model_dump(mode="json")
        with self.json_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")

        with sqlite3.connect(self.sqlite_path) as connection:
            connection.execute(
                """
                INSERT INTO agent_runs (
                    request_id, agent_name, agent_input, agent_output,
                    latency_ms, confidence, revision_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trace.request_id,
                    trace.agent_name,
                    json.dumps(trace.input),
                    json.dumps(trace.output),
                    trace.latency_ms,
                    trace.confidence,
                    trace.revision_count,
                ),
            )


LOGGER = StructuredLogger()
