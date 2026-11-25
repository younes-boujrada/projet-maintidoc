"""
Ingest script: reads inventaire.csv, extracts + chunks all corpus docs,
upserts into Qdrant text and image collections.
Usage: python scripts/ingest.py [--corpus corpus/] [--ocr pytesseract|pymupdf]
"""
from __future__ import annotations
import argparse, csv, logging, sys, time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run(corpus_dir: Path, ocr_tool: str) -> None:
    from src.ingestion.extraction import extract_pdf, extract_image_caption
    from src.ingestion.chunker import chunk_text
    from src.indexation.text_index import upsert_chunks, ensure_collection
    from src.indexation.image_index import upsert_images, ensure_collection as ec_img

    ensure_collection()
    ec_img()

    inventaire_path = corpus_dir / "inventaire.csv"
    rows = list(csv.DictReader(open(inventaire_path, encoding="utf-8")))

    total_chunks = 0
    image_records = []
    t0 = time.perf_counter()

    for row in rows:
        doc_id = row["document_id"]
        famille = row["famille"]
        groupe = row["groupe_acces"]
        fmt = row["format"]
        usage = row["usage_test"]

        meta = {
            "famille": famille,
            "groupe_acces": groupe,
            "usage_test": usage,
        }

        if fmt == "image":
            img_path = corpus_dir / "images" / (doc_id + ".png")
            if img_path.exists():
                caption = extract_image_caption(img_path)
                image_records.append({
                    "img_path": str(img_path),
                    "document_id": doc_id,
                    "famille": famille,
                    "groupe_acces": groupe,
                    "caption": caption,
                })
                # also index as text chunk for text-only search
                chunks = chunk_text(caption, doc_id, 1, {**meta, "element_type": "image"})
                upsert_chunks(chunks)
                total_chunks += len(chunks)
                logger.info("Indexed image %s", doc_id)
            continue

        # PDF path
        pdf_path = corpus_dir / "documents" / (doc_id + ".pdf")
        if not pdf_path.exists():
            pdf_path = corpus_dir / "documents" / (doc_id + ".md")
        if not pdf_path.exists():
            logger.warning("Missing file for %s, skipping", doc_id)
            continue

        is_scanned = fmt == "pdf_scanne"
        pages = extract_pdf(pdf_path, is_scanned=is_scanned, ocr_tool=ocr_tool)

        for p in pages:
            chunks = chunk_text(p["text"], doc_id, p["page"], {**meta, "element_type": p["element_type"]})
            upsert_chunks(chunks)
            total_chunks += len(chunks)

        logger.info("Indexed %s (%d pages, %s)", doc_id, len(pages), fmt)

    # index images in image collection
    if image_records:
        from src.indexation.image_index import upsert_images
        upsert_images(image_records)

    elapsed = round(time.perf_counter() - t0, 1)
    logger.info("Done: %d chunks, %d images in %.1fs", total_chunks, len(image_records), elapsed)
    print(f"\n✓ Ingestion terminée : {total_chunks} chunks texte, {len(image_records)} images en {elapsed}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=str(ROOT / "corpus"))
    parser.add_argument("--ocr", choices=["pytesseract", "pymupdf"], default="pytesseract")
    args = parser.parse_args()
    run(Path(args.corpus), args.ocr)
