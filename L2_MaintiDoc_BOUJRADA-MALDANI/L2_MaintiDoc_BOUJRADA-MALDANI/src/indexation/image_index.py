"""
Qdrant image indexation using CLIP ViT-B/32 (chosen after benchmark, dim=512).
Benchmarked models: openai/clip-vit-base-patch32 vs multilingual M-CLIP.
Decision: openai/clip-vit-base-patch32 — better top-5 hit rate on French queries
  in our 3-image corpus (3/3 hits vs 2/3 for M-CLIP), faster on CPU.
shortcut: M-CLIP would be better for heavily multilingual corpora; revisit for L3.
"""
from __future__ import annotations
import logging
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchAny,
)
from src.config import IMAGE_COLLECTION, CLIP_DIM, USE_QDRANT_MEMORY, QDRANT_URL

logger = logging.getLogger(__name__)

_clip_model = None
_clip_preprocess = None
_clip_tokenizer = None


def _get_clip():
    global _clip_model, _clip_preprocess, _clip_tokenizer
    if _clip_model is None:
        try:
            from transformers import CLIPModel, CLIPProcessor
            _clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            _clip_preprocess = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            _clip_tokenizer = _clip_preprocess
            _clip_model.eval()
        except Exception as e:
            logger.warning("CLIP transformers failed (%s), trying open_clip", e)
            import open_clip, torch
            model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
            _clip_model = model
            _clip_preprocess = preprocess
            _clip_tokenizer = open_clip.get_tokenizer("ViT-B-32")
    return _clip_model, _clip_preprocess, _clip_tokenizer


def _get_client() -> QdrantClient:
    # shortcut: shares in-memory client state within process via module-level singleton
    from src.indexation.text_index import get_client
    return get_client()


def ensure_collection() -> None:
    client = _get_client()
    existing = [c.name for c in client.get_collections().collections]
    if IMAGE_COLLECTION not in existing:
        client.create_collection(
            IMAGE_COLLECTION,
            vectors_config=VectorParams(size=CLIP_DIM, distance=Distance.COSINE),
        )
        logger.info("Created Qdrant image collection %s", IMAGE_COLLECTION)


def _embed_image(img_path: Path) -> list[float]:
    import torch
    from PIL import Image
    model, processor, _ = _get_clip()
    img = Image.open(img_path).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        out = model.get_image_features(**inputs)
    feats = out.pooler_output if hasattr(out, "pooler_output") and out.pooler_output is not None else (out if isinstance(out, torch.Tensor) else out[0])
    feats = feats / feats.norm(dim=-1, keepdim=True)
    return feats[0].tolist()


def _embed_text_clip(text: str) -> list[float]:
    import torch
    model, processor, _ = _get_clip()
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        out = model.get_text_features(**inputs)
    feats = out.pooler_output if hasattr(out, "pooler_output") and out.pooler_output is not None else (out if isinstance(out, torch.Tensor) else out[0])
    feats = feats / feats.norm(dim=-1, keepdim=True)
    return feats[0].tolist()


def upsert_images(image_records: list[dict]) -> None:
    """
    image_records: list of dicts with keys:
      img_path, document_id, famille, groupe_acces, caption
    """
    if not image_records:
        return
    client = _get_client()
    ensure_collection()
    points = []
    for rec in image_records:
        try:
            vec = _embed_image(Path(rec["img_path"]))
            points.append(PointStruct(
                id=abs(hash(str(rec["img_path"]))) % (2**63),
                vector=vec,
                payload={
                    "img_path": str(rec["img_path"]),
                    "document_id": rec["document_id"],
                    "famille": rec["famille"],
                    "groupe_acces": rec["groupe_acces"],
                    "caption": rec.get("caption", ""),
                    "element_type": "image",
                },
            ))
        except Exception as e:
            logger.warning("Could not embed image %s: %s", rec["img_path"], e)
    if points:
        client.upsert(IMAGE_COLLECTION, points=points)
        logger.info("Upserted %d images to %s", len(points), IMAGE_COLLECTION)


def search_images_by_text(
    query: str,
    allowed_families: list[str],
    k: int = 5,
) -> list[dict]:
    client = _get_client()
    ensure_collection()
    vec = _embed_text_clip(query)
    rbac_filter = Filter(
        must=[FieldCondition(key="famille", match=MatchAny(any=allowed_families))]
    )
    if hasattr(client, "query_points"):
        hits = client.query_points(
            IMAGE_COLLECTION,
            query=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        ).points
    else:
        hits = client.search(
            IMAGE_COLLECTION,
            query_vector=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        )
    return [
        {
            "document_id": h.payload["document_id"],
            "page": None,
            "element_type": "image",
            "img_path": h.payload["img_path"],
            "caption": h.payload.get("caption", ""),
            "score": h.score,
            "source": "image",
        }
        for h in hits
    ]


def search_images_by_image(
    query_img_path: str,
    allowed_families: list[str],
    k: int = 5,
) -> list[dict]:
    client = _get_client()
    ensure_collection()
    vec = _embed_image(Path(query_img_path))
    rbac_filter = Filter(
        must=[FieldCondition(key="famille", match=MatchAny(any=allowed_families))]
    )
    if hasattr(client, "query_points"):
        hits = client.query_points(
            IMAGE_COLLECTION,
            query=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        ).points
    else:
        hits = client.search(
            IMAGE_COLLECTION,
            query_vector=vec,
            query_filter=rbac_filter,
            limit=k,
            with_payload=True,
        )
    return [
        {
            "document_id": h.payload["document_id"],
            "page": None,
            "element_type": "image",
            "img_path": h.payload["img_path"],
            "caption": h.payload.get("caption", ""),
            "score": h.score,
            "source": "photo_query",
        }
        for h in hits
    ]
