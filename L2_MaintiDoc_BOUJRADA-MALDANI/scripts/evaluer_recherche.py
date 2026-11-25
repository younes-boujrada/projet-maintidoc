"""
Evaluation script: runs 20 questions in text-only vs text+image configs.
Computes Recall@5 and MRR@10 (bonus metrics).
Writes eval/resultats_evaluation.csv.

Usage: python scripts/evaluer_recherche.py
  (requires corpus already ingested: python scripts/ingest.py)
"""
from __future__ import annotations
import csv, os, sys, logging
from pathlib import Path

os.environ.setdefault("QDRANT_MEMORY", "1")
logging.basicConfig(level=logging.WARNING)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

EVAL_DIR = ROOT / "eval"
QUESTIONS_CSV = EVAL_DIR / "questions_test.csv"
RESULTS_CSV = EVAL_DIR / "resultats_evaluation.csv"


def rank_of_hit(results: list[dict], expected_ids: list[str]) -> int | None:
    """Return 1-based rank of first hit whose document_id is in expected_ids, or None."""
    for i, r in enumerate(results, start=1):
        if any(eid in r["document_id"] for eid in expected_ids):
            return i
    return None


def run_evaluation():
    from scripts.ingest import run as run_ingest
    from src.indexation.text_index import get_client, TEXT_COLLECTION, ensure_collection
    ensure_collection()
    client = get_client()
    try:
        count = client.get_collection(TEXT_COLLECTION).points_count
    except Exception:
        count = 0
    if not count:
        print("Index vide, exécution de l'ingestion...")
        run_ingest(ROOT / "corpus", "pymupdf")

    from src.recherche.search import search

    questions = list(csv.DictReader(open(QUESTIONS_CSV, encoding="utf-8")))

    out_rows = [["question_id", "config", "rank_found", "hit_at_5", "reciprocal_rank"]]
    summary: dict[str, dict] = {
        "text_only": {"hits": 0, "rr_sum": 0.0, "total": 0},
        "text_image": {"hits": 0, "rr_sum": 0.0, "total": 0},
    }

    failure_analyses = []

    for q in questions:
        qid = q["question_id"]
        query = q["question"]
        user = q["utilisateur"]
        expected_raw = q["elements_attendus"]
        qtype = q["type_question"]
        photo = q.get("photo", "").strip() or None

        # skip access-denied questions for metric computation
        if "accès refusé" in expected_raw or "aucun" in expected_raw.lower():
            for config in ["text_only", "text_image"]:
                out_rows.append([qid, config, "N/A (accès refusé)", False, 0.0])
            continue

        expected_ids = [e.strip().split()[0] for e in expected_raw.split() if e.strip()]

        for config, text_only_flag in [("text_only", True), ("text_image", False)]:
            try:
                img_path = str(ROOT / photo) if photo and not text_only_flag else None
                results = search(query, user_group=user, query_image=img_path,
                                 k=5, text_only=text_only_flag)
            except Exception as e:
                logging.warning("Search failed for %s/%s: %s", qid, config, e)
                results = []

            rank = rank_of_hit(results, expected_ids)
            hit5 = rank is not None and rank <= 5
            rr = (1.0 / rank) if rank and rank <= 10 else 0.0

            out_rows.append([qid, config, rank if rank else "miss", hit5, round(rr, 4)])
            summary[config]["hits"] += int(hit5)
            summary[config]["rr_sum"] += rr
            summary[config]["total"] += 1

            if not hit5 and len(failure_analyses) < 3:
                failure_analyses.append({
                    "question_id": qid,
                    "config": config,
                    "query": query,
                    "expected": expected_raw,
                    "got": [r["document_id"] for r in results[:3]],
                })

    with open(RESULTS_CSV, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(out_rows)

    print("\n=== RÉSULTATS D'ÉVALUATION ===\n")
    print(f"{'Config':<15} {'Recall@5':>10} {'MRR@10':>10} {'Questions':>10}")
    print("-" * 50)
    for config, s in summary.items():
        total = s["total"] or 1
        recall = s["hits"] / total
        mrr = s["rr_sum"] / total
        print(f"{config:<15} {recall:>10.3f} {mrr:>10.3f} {total:>10}")

    print(f"\n✓ Résultats écrits dans {RESULTS_CSV}")
    print(f"\n--- 3 Analyses d'échec ---")
    for fa in failure_analyses:
        print(f"\n[{fa['question_id']}] {fa['config']}")
        print(f"  Query   : {fa['query'][:80]}")
        print(f"  Attendu : {fa['expected'][:60]}")
        print(f"  Obtenu  : {fa['got']}")

    return summary


if __name__ == "__main__":
    run_evaluation()
