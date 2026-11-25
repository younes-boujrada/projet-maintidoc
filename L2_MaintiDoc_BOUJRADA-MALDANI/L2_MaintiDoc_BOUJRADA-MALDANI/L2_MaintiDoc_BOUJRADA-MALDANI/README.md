# MaintiDoc — Livrable 2

**RAG Multimodal : Ingestion, Indexation Qdrant, Recherche et Contrôle d'Accès**
Équipe : MALDANI Mostafa & BOUJRADA Younes — EMSI 2026

---

## Architecture

```
corpus/                     # 10 PDFs + 3 images + inventaire.csv
src/
  ingestion/                # extraction PyMuPDF + OCR + chunking
  indexation/               # Qdrant text (BGE-M3) + image (CLIP)
  recherche/                # search.py + rrf.py
  acces/                    # rbac.py (pre-filter RBAC)
  api/                      # FastAPI POST /search
scripts/
  ingest.py                 # ingestion CLI
  evaluer_recherche.py      # évaluation 20 questions, Recall@5, MRR@10
  benchmark_ocr.py          # benchmark OCR (pytesseract vs pymupdf)
eval/
  questions_test.csv        # 20 questions de test
  resultats_evaluation.csv  # résultats après évaluation
  sources_veille.csv        # 7 sources vérifiées
docs/veille/veille_rag.md   # document de veille 3-4 pages
app.py                      # Streamlit UI
docker-compose.yml          # Qdrant + PostgreSQL + MinIO
```

## Modèles utilisés

| Rôle | Modèle | Dimension | Note |
|------|--------|-----------|------|
| Embeddings texte | `BAAI/bge-m3` (imposé) | 1024 | Fallback `all-MiniLM-L6-v2` (384) sur CPU sans GPU |
| Encodeur image | `openai/clip-vit-base-patch32` | 512 | Choisi après benchmark vs M-CLIP |
| OCR | `pytesseract` (tesseract) | — | Choisi après benchmark vs PyMuPDF natif |

## Lancement rapide

```bash
# 1. Démarrer les services (optionnel, mode mémoire disponible par défaut)
docker-compose up -d

# 2. Ingestion du corpus
python scripts/ingest.py --corpus corpus/

# 3. Lancer l'interface
streamlit run app.py

# 4. API REST
uvicorn src.api.main:app --reload

# 5. Tests RBAC
pytest tests/test_acces.py -v

# 6. Évaluation
python scripts/evaluer_recherche.py
```

## Variables d'environnement

Copier `.env.example` → `.env` et adapter :

```
QDRANT_URL=http://localhost:6333
QDRANT_MEMORY=1          # 1 = in-memory (dev), 0 = serveur
MAINTIDOC_SECRET=...
```

## Benchmarks

### OCR
| Outil | Caractères extraits (scan) | Temps (p/page) | Décision |
|-------|---------------------------|----------------|----------|
| pytesseract | ~800 | ~1.2s | **Retenu** |
| PyMuPDF natif | ~50 (texte fantôme) | ~0.1s | Fallback uniquement |

### Encodeur image (CLIP)
| Modèle | Top-5 hits (3 images, requête FR) | Temps chargement | Décision |
|--------|-----------------------------------|-----------------|----------|
| `openai/clip-vit-base-patch32` | 3/3 | ~8s CPU | **Retenu** |
| `M-CLIP/XLM-Roberta-Large-Vit-B-32` | 2/3 | ~15s CPU | Écarté |

## Contrôle d'accès (RBAC)

| Groupe | Familles autorisées |
|--------|---------------------|
| `techniciens_audiovisuel` | `appareils_photo` |
| `techniciens_impression` | `imprimantes_pro` |
| `responsables_maintenance` | `appareils_photo`, `imprimantes_pro` |
| `operateurs_invites` | `appareils_photo`, `imprimantes_pro` (manuels de base uniquement) |

Pre-filter appliqué **avant** la recherche Qdrant (`FieldCondition` + `MatchAny`).

## Tag GitHub

```
git tag v0.2-L2
git push origin v0.2-L2
```
