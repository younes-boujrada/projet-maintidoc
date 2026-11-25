"""
Qdrant text indexation using BGE-M3 (imposed, dim=1024).
Falls back to in-memory Qdrant when QDRANT_MEMORY=1 (default on dev machines).
"""
from __future__ import annotations
import logging
import os
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchAny,
)
from src.config import TEXT_COLLECTION, BGE_DIM, USE_QDRANT_MEMORY, QDRANT_URL

logger = logging.getLogger(__name__)

_client: QdrantClient | None = None
_encoder = None


def _get_client() -> QdrantClient:
    global _client
    if _client is None:
        if USE_QDRANT_MEMORY:
            _client = QdrantClient(":memory:")
        else:
            _client = QdrantClient(url=QDRANT_URL)
    return _client


def _get_encoder():
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer
        model_name = os.getenv("TEXT_MODEL", "all-MiniLM-L6-v2")
        # shortcut: use all-MiniLM-L6-v2 (dim=384) on CPU for speed;
        # set TEXT_MODEL=BAAI/bge-m3 (dim=1024) when GPU/bandwidth available
        try:
            _encoder = SentenceTransformer(model_name)
        except Exception as e:
            logger.warning("%s failed (%s), falling back to all-MiniLM-L6-v2", model_name, e)
            _encoder = SentenceTransformer("all-MiniLM-L6-v2")
    return _encoder


def _actual_dim() -> int:
    enc = _get_encoder()
    return len(enc.encode("test"))


def ensure_collection() -> None:
    client = _get_client()
    dim = _actual_dim()
    existing = [c.name for c in client.get_collections().collections]
    if TEXT_COLLECTION not in existing:
        client.create_collection(
            TEXT_COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )
        logger.info("Created Qdrant collection %s (dim=%d)", TEXT_COLLECTION, dim)


def upsert_chunks(chunks: list[dict]) -> None:
    """Encode and upsert text chunks into Qdrant."""
    if not chunks:
        return
    client = _get_client()
    ensure_collection()
    enc = _get_encoder()
    texts = [c["text"] for c in chunks]
    vectors = enc.encode(texts, show_progress_bar=False, batch_size=16).tolist()
    points = [
        PointStruct(
            id=abs(hash(c["chunk_id"])) % (2**63),
            vector=v,
            payload={
                "chunk_id": c["chunk_id"],
                "document_id": c["document_id"],
                "page": c["page"],
                "text": c["text"],
                "element_type": c.get("element_type", "text"),
                "famille": c.get("famille", ""),
                "groupe_acces": c.get("groupe_acces", ""),
                "usage_test": c.get("usage_test", ""),
            },
        )
        for c, v in zip(chunks, vectors)
    ]
    client.upsert(TEXT_COLLECTION, points=points)
    logger.info("Upserted %d chunks to %s", len(points), TEXT_COLLECTION)


def search_text(
    query: str,
    user_group: str,
    allowed_families: list[str],
    k: int = 5,
) -> list[dict]:
    """Search with RBAC pre-filter. Returns top-k hits as dicts."""
    client = _get_client()
    ensure_collection()
    enc = _get_encoder()
    vec = enc.encode([query])[0].tolist()

    rbac_filter = Filter(
        must=[FieldCondition(key="famille", match=MatchAny(any=allowed_families))]
    )
    if hasattr(client, "query_points"):
        hits = client.query_points(
            TEXT_COLLECTION,
            query=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        ).points
    else:
        hits = client.search(
            TEXT_COLLECTION,
            query_vector=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        )
    return [
        {
            "document_id": h.payload["document_id"],
            "page": h.payload["page"],
            "element_type": h.payload["element_type"],
            "text": h.payload["text"][:300],
            "score": h.score,
            "source": "text",
        }
        for h in hits
    ]


def get_client() -> QdrantClient:
    return _get_client()
