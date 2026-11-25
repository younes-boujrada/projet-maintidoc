import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"
DOCS_DIR = CORPUS_DIR / "documents"
IMAGES_DIR = CORPUS_DIR / "images"
INVENTAIRE_PATH = CORPUS_DIR / "inventaire.csv"
DATA_DIR = BASE_DIR / "data"
EVAL_DIR = BASE_DIR / "eval"
GMAO_DB_PATH = DATA_DIR / "gmao.json"

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# shortcut: in-memory Qdrant used when server unavailable; switch to URL for prod
USE_QDRANT_MEMORY = os.getenv("QDRANT_MEMORY", "1") == "1"

TEXT_COLLECTION = "maintidoc_text"
IMAGE_COLLECTION = "maintidoc_images"

# BGE-M3 dim=1024 (imposed), CLIP ViT-B/32 dim=512
BGE_MODEL = "BAAI/bge-m3"
BGE_DIM = 1024
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"  # chosen after benchmark
CLIP_DIM = 512

RBAC = {
    "techniciens_audiovisuel": {
        "label": "Technicien Audiovisuel (Terrain)",
        "allowed_families": ["appareils_photo"],
        "can_create_ticket_directly": False,
        "requires_visa": True,
    },
    "techniciens_impression": {
        "label": "Technicien Impression (Atelier)",
        "allowed_families": ["imprimantes_pro"],
        "can_create_ticket_directly": False,
        "requires_visa": True,
    },
    "responsables_maintenance": {
        "label": "Responsable / Superviseur Maintenance",
        "allowed_families": ["appareils_photo", "imprimantes_pro"],
        "can_create_ticket_directly": True,
        "requires_visa": False,
    },
    "operateurs_invites": {
        "label": "Opérateur Invité (Stagiaire)",
        "allowed_families": ["appareils_photo", "imprimantes_pro"],
        "restricted_to_base_manuals": True,
        "can_create_ticket_directly": False,
        "requires_visa": True,
    },
}
# keep old name for backward compat
USER_ROLES = RBAC

HMAC_SECRET = os.getenv("MAINTIDOC_SECRET", "maintidoc_secret_key_2026")
COLLECTION_NAME = "maintidoc_multimodal"  # legacy ChromaDB name kept for agent.py
