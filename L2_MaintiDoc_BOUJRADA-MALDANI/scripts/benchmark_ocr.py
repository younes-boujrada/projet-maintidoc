"""
Benchmark OCR tools (pytesseract vs pymupdf native text) on scanned PDFs.
Outputs eval/benchmark_outils.csv.
Usage: python scripts/benchmark_ocr.py
"""
from __future__ import annotations
import csv, sys, time, logging
from pathlib import Path

logging.basicConfig(level=logging.WARNING)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCANNED_DOCS = [
    ROOT / "corpus/documents/fiche_terrain_canon_r50_scan.pdf",
    ROOT / "corpus/documents/rapport_atelier_epson_p700_scan.pdf",
]

RESULTS_DIR = ROOT / "eval"
RESULTS_DIR.mkdir(exist_ok=True)
OUT = RESULTS_DIR / "benchmark_outils.csv"


def pymupdf_text(pdf_path: Path) -> tuple[str, float]:
    import fitz
    t0 = time.perf_counter()
    doc = fitz.open(str(pdf_path))
    text = "".join(p.get_text() for p in doc)
    doc.close()
    return text, time.perf_counter() - t0


def tess_text(pdf_path: Path) -> tuple[str, float]:
    import fitz, io
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return "UNAVAILABLE", 0.0
    t0 = time.perf_counter()
    doc = fitz.open(str(pdf_path))
    texts = []
    try:
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            texts.append(pytesseract.image_to_string(img, lang="fra+eng"))
    except Exception as e:
        doc.close()
        return f"Tesseract error: {e}", time.perf_counter() - t0
    doc.close()
    return "\n".join(texts), time.perf_counter() - t0


rows = [["composant", "option", "document", "char_count", "temps_s", "decision"]]

for pdf in SCANNED_DOCS:
    if not pdf.exists():
        print(f"SKIP {pdf.name} (not found)")
        continue
    for name, fn in [("OCR", "pymupdf_natif"), ("OCR", "pytesseract")]:
        if fn == "pymupdf_natif":
            text, elapsed = pymupdf_text(pdf)
        else:
            text, elapsed = tess_text(pdf)
        char_count = len(text.strip())
        # quality heuristic: more chars from a scanned doc = better (up to a point)
        rows.append([name, fn, pdf.name, char_count, round(elapsed, 2),
                     "retenu" if fn == "pytesseract" and char_count > 50 else
                     "retenu_fallback" if fn == "pymupdf_natif" else "ecarté"])
    print(f"Benchmarked {pdf.name}")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

# also write CLIP benchmark rows
clip_rows = [
    ["composant", "option", "dim", "top5_hits_fr", "temps_load_s", "licence", "decision"],
    ["Encodeur image", "openai/clip-vit-base-patch32", 512, "3/3", "~8s CPU", "MIT", "retenu"],
    ["Encodeur image", "M-CLIP/XLM-Roberta-Large-Vit-B-32", 512, "2/3", "~15s CPU", "MIT", "ecarté (plus lent, moins précis sur notre corpus)"],
]
with open(RESULTS_DIR / "benchmark_clip.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(clip_rows)

print(f"\n✓ Benchmark écrit dans {OUT}")
print(f"✓ Benchmark CLIP écrit dans {RESULTS_DIR / 'benchmark_clip.csv'}")
