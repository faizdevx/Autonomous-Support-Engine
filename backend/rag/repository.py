from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from backend.core.config import ROOT_DIR, get_settings


@lru_cache(maxsize=1)
def load_knowledge_base() -> list[dict[str, Any]]:
    settings = get_settings()
    dataset_path = ROOT_DIR / settings.rag.dataset_path
    with Path(dataset_path).open(encoding="utf-8") as handle:
        return json.load(handle)
