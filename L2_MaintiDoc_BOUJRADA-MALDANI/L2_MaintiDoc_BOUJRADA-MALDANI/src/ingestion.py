import os
import csv
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image
import fitz  # PyMuPDF

from src.config import DOCS_DIR, IMAGES_DIR, INVENTAIRE_PATH
from src.embeddings import encode_text, encode_image
from src.vector_store import VectorStore
from src.models import IndexedChunkMetadata


def compute_file_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def ingest_corpus(vector_store: VectorStore = None) -> int:
    """Ingests the technical documents and visual diagrams into the Vector Store."""
    if vector_store is None:
        vector_store = VectorStore()

    if not os.path.exists(INVENTAIRE_PATH):
        raise FileNotFoundError(f"Inventaire CSV not found at {INVENTAIRE_PATH}")

    total_chunks = 0
    with open(INVENTAIRE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc_id = row["document_id"]
            famille = row["famille"]
            doc_format = row["format"]
            groupe_acces = row["groupe_acces"]
            usage_test = row["usage_test"]
            equipment_id = "Canon EOS R50" if famille == "appareils_photo" else "Epson SC-P700"

            if doc_format in ["pdf_texte", "pdf_scanne"]:
                pdf_path = os.path.join(DOCS_DIR, f"{doc_id}.pdf")
                if not os.path.exists(pdf_path):
                    # Check markdown fallback
                    md_path = os.path.join(DOCS_DIR, f"{doc_id}.md")
                    if os.path.exists(md_path):
                        sha = compute_file_sha256(md_path)
                        text = Path(md_path).read_text(encoding="utf-8")
                        cid = f"chk_{doc_id}_p01_c01"
                        meta = IndexedChunkMetadata(
                            chunk_id=cid,
                            document_id=doc_id,
                            version="v1.0 (2026-01)",
                            page=1,
                            element_type="procedure_paragraph",
                            famille_equipement=famille,
                            equipment_id=equipment_id,
                            groupes_acces=groupe_acces,
                            source_sha256=sha,
                            has_visual_element=False,
                            usage_test=usage_test
                        ).model_dump()
                        full_content = f"[{doc_id}] {text}"
                        emb = encode_text(full_content)
                        vector_store.add_element(cid, full_content, meta, emb)
                        total_chunks += 1
                    continue

                sha = compute_file_sha256(pdf_path)
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text("text").strip()
                    if not text:
                        text = f"[Contenu scanné OCR {doc_id} Page {page_num + 1}]"

                    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
                    if not paragraphs:
                        paragraphs = [text]

                    for p_idx, para in enumerate(paragraphs, start=1):
                        cid = f"chk_{doc_id}_p{page_num+1:02d}_c{p_idx:02d}"
                        meta = IndexedChunkMetadata(
                            chunk_id=cid,
                            document_id=doc_id,
                            version="v1.0 (2026-01)",
                            page=page_num + 1,
                            element_type="procedure_paragraph" if "proc" in doc_id or "guide" in doc_id else "code_table",
                            famille_equipement=famille,
                            equipment_id=equipment_id,
                            groupes_acces=groupe_acces,
                            source_sha256=sha,
                            has_visual_element=False,
                            usage_test=usage_test
                        ).model_dump()

                        full_para = f"[{doc_id}] {para}"
                        emb = encode_text(full_para)
                        vector_store.add_element(cid, full_para, meta, emb)
                        total_chunks += 1
                doc.close()

            elif doc_format == "image":
                img_path = os.path.join(IMAGES_DIR, f"{doc_id}.png")
                if not os.path.exists(img_path):
                    continue

                sha = compute_file_sha256(img_path)
                cid = f"chk_{doc_id}_img_01"
                description = f"[{doc_id}] Image technique / Photographie de panneau pour {doc_id} ({equipment_id})"
                meta = IndexedChunkMetadata(
                    chunk_id=cid,
                    document_id=doc_id,
                    version="v1.0 (2026-01)",
                    page=1,
                    element_type="schema" if "schema" in doc_id or "mire" in doc_id else "photo",
                    famille_equipement=famille,
                    equipment_id=equipment_id,
                    groupes_acces=groupe_acces,
                    source_sha256=sha,
                    has_visual_element=True,
                    linked_image_id=str(img_path),
                    usage_test=usage_test
                ).model_dump()

                emb = encode_image(img_path)
                vector_store.add_element(cid, description, meta, emb)
                total_chunks += 1

    return total_chunks


if __name__ == "__main__":
    vs = VectorStore()
    cnt = ingest_corpus(vs)
    print(f"Ingestion complete: {cnt} chunks indexed in ChromaDB.")
