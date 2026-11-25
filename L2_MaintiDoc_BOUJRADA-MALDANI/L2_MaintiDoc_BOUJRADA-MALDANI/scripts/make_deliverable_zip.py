"""
Assemble L2_MaintiDoc_BOUJRADA-MALDANI.zip according to section 3 of consignes.
"""
import zipfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM_DIR = "L2_MaintiDoc_BOUJRADA-MALDANI"
ZIP_NAME = f"{TEAM_DIR}.zip"
ZIP_PATH = ROOT / ZIP_NAME

# File mappings relative to TEAM_DIR inside the zip
files_to_zip = [
    # Root files of deliverable
    (ROOT / "L2_MaintiDoc_BOUJRADA-MALDANI_Rapport.pdf", f"{TEAM_DIR}/L2_MaintiDoc_BOUJRADA-MALDANI_Rapport.pdf"),
    (ROOT / "L2_MaintiDoc_BOUJRADA-MALDANI_Veille.pdf", f"{TEAM_DIR}/L2_MaintiDoc_BOUJRADA-MALDANI_Veille.pdf"),
    (ROOT / "L2_MaintiDoc_BOUJRADA-MALDANI_LienGitHub.txt", f"{TEAM_DIR}/L2_MaintiDoc_BOUJRADA-MALDANI_LienGitHub.txt"),
    (ROOT / "README.md", f"{TEAM_DIR}/README.md"),
    
    # Resultats directory
    (ROOT / "eval/questions_test.csv", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/questions_test.csv"),
    (ROOT / "eval/resultats_evaluation.csv", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/resultats_evaluation.csv"),
    (ROOT / "corpus/inventaire.csv", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/inventaire.csv"),
    (ROOT / "docs/veille/sources_veille.csv", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/sources_veille.csv"),
    (ROOT / "eval/benchmark_outils.csv", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/benchmark_outils.csv"),
    
    # Captures
    (ROOT / "eval/captures/recherche_texte.png", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/captures/recherche_texte.png"),
    (ROOT / "eval/captures/recherche_photo.png", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/captures/recherche_photo.png"),
    (ROOT / "eval/captures/acces_refuse.png", f"{TEAM_DIR}/{TEAM_DIR}_Resultats/captures/acces_refuse.png"),
]

# Verify all files exist
missing = [str(src) for src, _ in files_to_zip if not src.exists()]
if missing:
    raise FileNotFoundError(f"Missing required deliverable files: {missing}")

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for src, arcname in files_to_zip:
        zf.write(src, arcname)
        print(f"  + {arcname} ({src.stat().st_size:,} bytes)")

print(f"\n✓ Archive ZIP créée avec succès : {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes)")
