"""
Zip the whole maintidoc project (clean archive without __pycache__, .git, large temp dirs).
"""
import zipfile, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP_OUT = ROOT / "maintidoc_full_project.zip"

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", "venv", ".venv", "qdrant_local"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".zip"}

count = 0
total_size = 0

with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # filter directories in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.endswith("_db")]
        
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXCLUDE_EXTS and f != "test_doc.pdf":
                continue
            
            filepath = Path(dirpath) / f
            rel_path = filepath.relative_to(ROOT)
            
            zf.write(filepath, arcname=str(rel_path))
            count += 1
            total_size += filepath.stat().st_size

print(f"✓ Archive complète créée : {ZIP_OUT.name} ({count} fichiers, {ZIP_OUT.stat().st_size:,} octets)")
