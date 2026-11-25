"""
MaintiDoc – Streamlit UI (L2: multimodal search with Qdrant).
"""
from __future__ import annotations
import os, sys, tempfile, shutil
from pathlib import Path

os.environ.setdefault("QDRANT_MEMORY", "1")
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import streamlit as st

@st.cache_resource
def ensure_indexed():
    from src.indexation.text_index import get_client, TEXT_COLLECTION, ensure_collection
    ensure_collection()
    client = get_client()
    try:
        count = client.get_collection(TEXT_COLLECTION).points_count
    except Exception:
        count = 0
    if not count:
        from scripts.ingest import run as run_ingest
        run_ingest(ROOT / "corpus", "pymupdf")

ensure_indexed()

st.set_page_config(page_title="MaintiDoc", page_icon="🔧", layout="wide")

st.title("🔧 MaintiDoc — Recherche Multimodale")
st.caption("Livrable 2 — MALDANI Mostafa & BOUJRADA Younes — EMSI 2026")

# ── Sidebar: user & config ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    user_group = st.selectbox(
        "Groupe utilisateur",
        ["techniciens_audiovisuel", "techniciens_impression",
         "responsables_maintenance", "operateurs_invites"],
    )
    text_only = st.toggle("Recherche texte uniquement (sans images)", value=False)
    st.divider()
    st.markdown("**Familles autorisées :**")
    from src.acces.rbac import get_allowed_families
    allowed = get_allowed_families(user_group)
    for f in allowed:
        st.markdown(f"- `{f}`")
    if not allowed:
        st.error("Aucun accès configuré pour ce groupe.")

# ── Main: query input ────────────────────────────────────────────────────────
query = st.text_input("🔍 Question / requête texte", placeholder="Ex: Comment nettoyer le capteur Canon R50 ?")
photo_file = st.file_uploader("📷 Photo query (optionnel)", type=["jpg", "jpeg", "png"])

if st.button("Rechercher", type="primary", disabled=not query.strip()):
    if not allowed:
        st.error("⛔ Accès refusé : votre groupe n'a accès à aucune famille de documents.")
        st.stop()

    img_path = None
    tmp_dir = None
    if photo_file and not text_only:
        tmp_dir = tempfile.mkdtemp()
        img_path = str(Path(tmp_dir) / photo_file.name)
        with open(img_path, "wb") as f:
            f.write(photo_file.read())

    with st.spinner("Recherche en cours…"):
        try:
            from src.recherche.search import search
            results = search(
                query_text=query,
                user_group=user_group,
                query_image=img_path,
                k=5,
                text_only=text_only,
            )
        except Exception as e:
            st.error(f"Erreur de recherche : {e}")
            results = []
        finally:
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    if not results:
        st.warning("Aucun résultat. Vérifiez que l'ingestion a été effectuée (`python scripts/ingest.py`).")
    else:
        st.success(f"{len(results)} résultat(s) trouvé(s)")
        for i, r in enumerate(results, 1):
            with st.expander(
                f"#{i} — `{r['document_id']}` p.{r.get('page','—')} "
                f"[{r.get('element_type','?')}] score={r.get('rrf_score', r.get('score', 0)):.4f}",
                expanded=(i <= 2),
            ):
                col1, col2 = st.columns([3, 1])
                with col1:
                    if r.get("text"):
                        st.markdown(f"**Extrait :** {r['text'][:400]}")
                    elif r.get("caption"):
                        st.markdown(f"**Légende :** {r['caption']}")
                with col2:
                    if r.get("img_path") and Path(r["img_path"]).exists():
                        st.image(r["img_path"], caption=r.get("caption", ""), use_container_width=True)
                st.caption(f"Source : `{r.get('source','?')}` — Famille : détectée via RBAC")
