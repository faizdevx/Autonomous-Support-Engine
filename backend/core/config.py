from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


ROOT_DIR = Path(__file__).resolve().parents[2]


class RagConfig(BaseModel):
    top_k: int = 4
    min_score: float = 1.0
    dataset_path: str = "data/synthetic_support_dataset.json"
    persist_directory: str = "chroma_db"
    use_chroma: bool = False


class LoggingConfig(BaseModel):
    json_log_path: str = "logs/agent_runs.jsonl"
    sqlite_path: str = "logs/agent_runs.db"


class FrontendConfig(BaseModel):
    api_base_url: str = "http://localhost:8000"


class SimulationConfig(BaseModel):
    runs: int = 25
    output_csv: str = "logs/simulation_metrics.csv"
    output_json: str = "logs/simulation_summary.json"


class AppConfig(BaseModel):
    environment: str = "development"
    app_name: str = "Autonomous Support Engine"
    rag: RagConfig = Field(default_factory=RagConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    frontend: FrontendConfig = Field(default_factory=FrontendConfig)
    simulation: SimulationConfig = Field(default_factory=SimulationConfig)


def _deep_update(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_update(merged[key], value)
        else:
            merged[key] = value
    return merged


@lru_cache(maxsize=1)
def get_settings() -> AppConfig:
    config_path = Path(os.getenv("ASE_CONFIG_PATH", ROOT_DIR / "configs" / "config.yaml"))
    raw: dict[str, Any] = {}
    if config_path.exists():
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    env_override = {
        "environment": os.getenv("ASE_ENV", raw.get("environment", "development")),
        "frontend": {
            "api_base_url": os.getenv(
                "SUPPORT_API_URL",
                raw.get("frontend", {}).get("api_base_url", "http://localhost:8000"),
            )
        },
    }
    merged = _deep_update(raw, env_override)
    return AppConfig.model_validate(merged)
