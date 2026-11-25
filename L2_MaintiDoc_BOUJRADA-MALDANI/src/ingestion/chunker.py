"""
Chunker: splits page text into overlapping paragraphs.
Strategy: paragraph-aware split, 300 tokens target, 50-token overlap.
shortcut: token count approximated as len(text)//4; use tiktoken for exact counts.
"""
from __future__ import annotations

CHUNK_CHARS = 1200   # ≈300 tokens
OVERLAP_CHARS = 200  # ≈50 tokens


def chunk_text(text: str, doc_id: str, page: int, metadata: dict) -> list[dict]:
    """Split text into overlapping chunks, preserving paragraph boundaries when possible."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()] if text.strip() else []

    chunks: list[dict] = []
    buf = ""
    chunk_idx = 0

    for para in paragraphs:
        if len(buf) + len(para) + 2 <= CHUNK_CHARS:
            buf = (buf + "\n\n" + para).strip()
        else:
            if buf:
                chunks.append(_make_chunk(buf, doc_id, page, chunk_idx, metadata))
                chunk_idx += 1
                buf = buf[-OVERLAP_CHARS:] + "\n\n" + para
            else:
                buf = para

    if buf.strip():
        chunks.append(_make_chunk(buf, doc_id, page, chunk_idx, metadata))

    # single chunk for very short pages
    if not chunks and text.strip():
        chunks.append(_make_chunk(text.strip(), doc_id, page, 0, metadata))

    return chunks


def _make_chunk(text: str, doc_id: str, page: int, idx: int, meta: dict) -> dict:
    return {
        "chunk_id": f"{doc_id}_p{page}_c{idx}",
        "document_id": doc_id,
        "page": page,
        "text": text,
        **meta,
    }
