"""
Reciprocal Rank Fusion (RRF) — standard k=60 constant.
"""
from __future__ import annotations
from collections import defaultdict


def rrf_fuse(ranked_lists: list[list[dict]], k: int = 60) -> list[dict]:
    """
    Fuse multiple ranked result lists using RRF.
    Each item must have a unique key: (document_id, page, element_type).
    Returns merged list sorted by fused score descending.
    """
    scores: dict[tuple, float] = defaultdict(float)
    best: dict[tuple, dict] = {}

    for ranked in ranked_lists:
        for rank, item in enumerate(ranked, start=1):
            key = (item["document_id"], item.get("page"), item.get("element_type"))
            scores[key] += 1.0 / (rank + k)
            if key not in best:
                best[key] = item

    merged = []
    for key, score in sorted(scores.items(), key=lambda x: -x[1]):
        entry = {**best[key], "rrf_score": round(score, 6)}
        merged.append(entry)

    return merged
