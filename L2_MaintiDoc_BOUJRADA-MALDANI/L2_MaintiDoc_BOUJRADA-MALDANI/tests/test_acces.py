"""
Automated RBAC access control tests (pytest).
Tests run against in-memory Qdrant (no server required).
"""
from __future__ import annotations
import os, sys
os.environ["QDRANT_MEMORY"] = "1"  # force in-memory mode
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

import pytest
from src.acces.rbac import get_allowed_families, check_access, verify_token, forge_token
from src.indexation.text_index import ensure_collection, upsert_chunks, search_text
from src.indexation.image_index import ensure_collection as ec_img


@pytest.fixture(autouse=True, scope="module")
def seed_index():
    """Seed Qdrant in-memory with minimal fixture data."""
    ensure_collection()
    ec_img()
    chunks = [
        {
            "chunk_id": "canon_p1_c0",
            "document_id": "manuel_canon_r50_base",
            "page": 1,
            "text": "Manuel Canon EOS R50 : nettoyage du capteur photo",
            "element_type": "text",
            "famille": "appareils_photo",
            "groupe_acces": "techniciens_audiovisuel",
            "usage_test": "normal",
        },
        {
            "chunk_id": "epson_p1_c0",
            "document_id": "manuel_epson_p700_base",
            "page": 1,
            "text": "Manuel Epson SC-P700 : remplacement encre et débouchage buses",
            "element_type": "text",
            "famille": "imprimantes_pro",
            "groupe_acces": "techniciens_impression",
            "usage_test": "normal",
        },
    ]
    upsert_chunks(chunks)
    yield


# ── Test 1: techniciens_audiovisuel ne voit pas les docs imprimantes_pro ─────

def test_audiovisuel_cannot_access_imprimantes():
    results = search_text(
        "débouchage buses Epson",
        user_group="techniciens_audiovisuel",
        allowed_families=get_allowed_families("techniciens_audiovisuel"),
        k=5,
    )
    families = [r["document_id"] for r in results]
    assert all("epson" not in doc_id for doc_id in families), (
        "techniciens_audiovisuel should NOT see Epson docs"
    )


# ── Test 2: techniciens_impression ne voit pas les docs appareils_photo ──────

def test_impression_cannot_access_appareils_photo():
    results = search_text(
        "nettoyage capteur Canon R50",
        user_group="techniciens_impression",
        allowed_families=get_allowed_families("techniciens_impression"),
        k=5,
    )
    assert all("canon" not in r["document_id"] for r in results), (
        "techniciens_impression should NOT see Canon docs"
    )


# ── Test 3: groupe inconnu → liste vide ──────────────────────────────────────

def test_unknown_group_returns_empty():
    results = search_text(
        "capteur Canon",
        user_group="groupe_inexistant",
        allowed_families=get_allowed_families("groupe_inexistant"),
        k=5,
    )
    assert results == [], "Unknown group should get empty results"


# ── Test 4: responsables_maintenance voit les deux familles ──────────────────

def test_responsable_sees_both_families():
    allowed = get_allowed_families("responsables_maintenance")
    assert "appareils_photo" in allowed
    assert "imprimantes_pro" in allowed


# ── Test 5: token HMAC valide / invalide ─────────────────────────────────────

def test_hmac_token():
    token = forge_token("manuel_canon_r50_base")
    assert verify_token("manuel_canon_r50_base", token)
    assert not verify_token("manuel_epson_p700_base", token)


# ── Test 6: check_access helper ──────────────────────────────────────────────

def test_check_access():
    assert check_access("techniciens_audiovisuel", "appareils_photo")
    assert not check_access("techniciens_audiovisuel", "imprimantes_pro")
    assert check_access("responsables_maintenance", "imprimantes_pro")
