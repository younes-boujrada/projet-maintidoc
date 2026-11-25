"""
Document extraction: PyMuPDF for text PDFs, OCR fallback for scanned docs.
Benchmarks pytesseract vs EasyOCR and picks best for scanned pages.
"""
from __future__ import annotations
import csv, io, time, logging
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

# ── OCR helpers ──────────────────────────────────────────────────────────────

def _ocr_pytesseract(img_bytes: bytes) -> tuple[str, float]:
    """Return (text, seconds). Returns ('', elapsed) on import error."""
    try:
        import pytesseract
        from PIL import Image
        t0 = time.perf_counter()
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img, lang="fra+eng")
        return text, time.perf_counter() - t0
    except Exception as e:
        logger.warning("pytesseract failed: %s", e)
        return "", 0.0


def _ocr_easyocr(img_bytes: bytes) -> tuple[str, float]:
    """Return (text, seconds). Returns ('', elapsed) on import error."""
    try:
        import easyocr
        import numpy as np
        from PIL import Image
        t0 = time.perf_counter()
        reader = easyocr.Reader(["fr", "en"], gpu=False, verbose=False)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        result = reader.readtext(np.array(img), detail=0)
        return " ".join(result), time.perf_counter() - t0
    except Exception as e:
        logger.warning("easyocr failed: %s", e)
        return "", 0.0


def benchmark_ocr(pdf_path: Path) -> dict[str, Any]:
    """
    Run both OCR tools on first page of pdf_path.
    Returns dict with tool names as keys, each having keys: text, time, char_count.
    """
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    doc.close()

    results: dict[str, Any] = {}
    for name, fn in [("pytesseract", _ocr_pytesseract), ("easyocr", _ocr_easyocr)]:
        text, elapsed = fn(img_bytes)
        results[name] = {"text": text[:200], "time": round(elapsed, 2), "char_count": len(text)}
    return results


# ── Main extraction ──────────────────────────────────────────────────────────

def extract_pdf(pdf_path: Path, is_scanned: bool = False, ocr_tool: str = "pymupdf") -> list[dict]:
    """
    Extract pages from a PDF. Each page → dict with keys:
      page, text, element_type ('text'|'ocr'), width, height
    For scanned docs: use ocr_tool ('pytesseract'|'easyocr').
    """
    doc = fitz.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc):
        base_text = page.get_text("text").strip()
        if is_scanned or len(base_text) < 30:
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            if ocr_tool == "easyocr":
                text, _ = _ocr_easyocr(img_bytes)
            else:
                text, _ = _ocr_pytesseract(img_bytes)
            if not text:
                text = base_text  # fallback to native text
            element_type = "ocr"
        else:
            text = base_text
            element_type = "text"
        pages.append({
            "page": i + 1,
            "text": text,
            "element_type": element_type,
            "width": page.rect.width,
            "height": page.rect.height,
        })
    doc.close()
    return pages


def extract_image_caption(img_path: Path) -> str:
    """Generate a text descriptor for an image (used for text-based image indexing)."""
    name = img_path.stem.replace("_", " ")
    return f"Image technique : {name}"
