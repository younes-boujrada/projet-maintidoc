"""
Multimodal search: text + visual + photo-query, fused via RRF.
Pre-filter enforces RBAC before Qdrant queries.
"""
from __future__ import annotations
from typing import Optional
from src.acces.rbac import get_allowed_families
from src.indexation.text_index import search_text
from src.indexation.image_index import search_images_by_text, search_images_by_image
from src.recherche.rrf import rrf_fuse


def search(
    query_text: str,
    user_group: str,
    query_image: Optional[str] = None,
    k: int = 5,
    text_only: bool = False,
) -> list[dict]:
    """
    Main search entry point.
    Returns top-k results fused with RRF (or text-only if text_only=True).
    Each result has: document_id, page, element_type, score/rrf_score, source.
    """
    allowed = get_allowed_families(user_group)
    if not allowed:
        return []

    text_hits = search_text(query_text, user_group, allowed, k=k)

    if text_only:
        return [{**h, "rrf_score": h["score"]} for h in text_hits]

    image_text_hits = search_images_by_text(query_text, allowed, k=k)

    lists = [text_hits, image_text_hits]

    if query_image:
        photo_hits = search_images_by_image(query_image, allowed, k=k)
        lists.append(photo_hits)

    return rrf_fuse(lists)[:k]
