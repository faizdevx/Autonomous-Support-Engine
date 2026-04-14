from __future__ import annotations

from backend.core.config import get_settings
from backend.models.schemas import RetrievedChunk
from backend.rag.repository import load_knowledge_base


def _score_document(query: str, document: dict[str, object]) -> float:
    query_tokens = set(query.lower().split())
    haystack = " ".join(
        [
            str(document.get("title", "")).lower(),
            str(document.get("content", "")).lower(),
            " ".join(str(tag).lower() for tag in document.get("tags", [])),
        ]
    )
    overlap = sum(1 for token in query_tokens if token in haystack)
    return float(overlap)


def retrieve_context(query: str, category: str | None) -> tuple[list[RetrievedChunk], float]:
    settings = get_settings()
    scored: list[tuple[float, dict[str, object]]] = []
    for item in load_knowledge_base():
        if category and item.get("category") != category:
            continue
        score = _score_document(query, item)
        if score >= settings.rag.min_score:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    matches = scored[: settings.rag.top_k]
    chunks = [
        RetrievedChunk(
            rank=index + 1,
            score=score,
            category=str(item.get("category", "")),
            title=str(item.get("title", "")),
            content=str(item.get("content", "")),
            tags=[str(tag) for tag in item.get("tags", [])],
        )
        for index, (score, item) in enumerate(matches)
    ]
    average_score = sum(chunk.score for chunk in chunks) / len(chunks) if chunks else 0.0
    return chunks, average_score
