import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus"
DOCS_DIR = CORPUS_DIR / "documents"
IMAGES_DIR = CORPUS_DIR / "images"
INVENTAIRE_PATH = CORPUS_DIR / "inventaire.csv"
DB_DIR = BASE_DIR / "data" / "chroma_db"
GMAO_DB_PATH = BASE_DIR / "data" / "gmao.json"

# RBAC Configuration
USER_ROLES = {
    "techniciens_audiovisuel": {
        "label": "Technicien Audiovisuel (Terrain)",
        "allowed_families": ["appareils_photo"],
        "can_create_ticket_directly": False,
        "requires_visa": True
    },
    "techniciens_impression": {
        "label": "Technicien Impression (Atelier)",
        "allowed_families": ["imprimantes_pro"],
        "can_create_ticket_directly": False,
        "requires_visa": True
    },
    "responsables_maintenance": {
        "label": "Responsable / Superviseur Maintenance",
        "allowed_families": ["appareils_photo", "imprimantes_pro"],
        "can_create_ticket_directly": True,
        "requires_visa": False
    },
    "operateurs_invites": {
        "label": "Opérateur Invité (Stagiaire)",
        "allowed_families": ["appareils_photo", "imprimantes_pro"],
        "can_create_ticket_directly": False,
        "restricted_to_base_manuals": True,
        "requires_visa": True
    }
}

HMAC_SECRET = os.getenv("MAINTIDOC_SECRET", "maintidoc_secret_key_2026")
CLIP_MODEL = "ViT-B-32"
CLIP_PRETRAINED = "laion2b_s34b_b79k"
COLLECTION_NAME = "maintidoc_multimodal"
