# Veille : Bonnes Pratiques RAG Multimodal

**L2_MaintiDoc_BOUJRADA-MALDANI_Veille**
Équipe : MALDANI Mostafa & BOUJRADA Younes — EMSI 2026

---

## 1. Méthode de veille

Cette veille a été conduite sur la période novembre 2026, en combinant :
- Lecture de documentation officielle (Qdrant, LlamaIndex, PyMuPDF)
- Consultation d'articles de référence (arXiv, ACM DL, ICML)
- Comparaison des pratiques sur des projets similaires de RAG industriel

Les sources ont été sélectionnées pour leur pertinence directe avec notre architecture (Qdrant + BGE-M3 + CLIP), leur actualité (≥2020) et leur vérifiabilité (tous accès publics).

---

## 2. Fiches thématiques

### Fiche 1 — Découpage de documents (Chunking)

**Enjeu :** La qualité du RAG dépend fortement de la granularité des chunks. Un chunk trop grand dilue l'information ; trop petit, il perd le contexte.

**Pratiques identifiées :**

- **Taille recommandée :** 256 à 512 tokens pour les documents techniques structurés (paragraphes courts, tableaux de codes d'erreur). Pour des manuels narratifs, 512–1024 tokens conservent mieux le contexte [S5].
- **Chevauchement (overlap) :** Un overlap de 10–15 % de la taille du chunk évite de couper une procédure en deux chunks distincts. Dans notre implémentation : 1200 caractères (~300 tokens) avec 200 caractères de chevauchement (~50 tokens).
- **Découpage structure-aware :** Identifier les délimiteurs naturels (titres Markdown, sauts de page PDF, numéros de procédure) avant de découper. PyMuPDF permet de récupérer les blocs de texte avec leur type (`text`, `image`, `table`) [S7].
- **Métadonnées enrichies :** Chaque chunk doit porter : `document_id`, `page`, `element_type`, `famille`, `groupe_acces`. Ces métadonnées sont indispensables pour le filtrage RBAC côté Qdrant [S1].

**Décision dans MaintiDoc :** Stratégie paragraphe-aware avec overlap 200 chars, metadata complète en payload Qdrant.

---

### Fiche 2 — Recherche hybride (dense + sparse)

**Enjeu :** La recherche purement vectorielle (dense) peut manquer des termes techniques exacts (codes d'erreur `0x97`, noms de pièces). La recherche par mots-clés (sparse/BM25) les trouve mais ignore la sémantique.

**Pratiques identifiées :**

- **Fusion BM25 + dense :** La combinaison des deux par RRF (Reciprocal Rank Fusion) est la pratique la plus répandue pour des corpus techniques [S6]. RRF avec `k=60` : `score = Σ 1/(rank_i + 60)`.
- **BGE-M3 :** Ce modèle est particulièrement adapté car il supporte nativement les trois modes : dense (1024-dim), sparse (lexical weights) et ColBERT (multi-vector). Dans notre implémentation, nous utilisons uniquement le mode dense faute de temps CPU, mais le mode sparse est disponible via `FlagEmbedding` [S2].
- **Re-ranking :** Un cross-encoder de re-ranking (ex. `BAAI/bge-reranker-v2-m3`) appliqué aux top-20 résultats améliore significativement le MRR. Reporté à L3.

**Décision dans MaintiDoc :** RRF entre recherche texte (BGE-M3 dense) et recherche image (CLIP) — deux listes fusionnées, top-5 retournés.

---

### Fiche 3 — Recherche multimodale (texte + image)

**Enjeu :** Dans un contexte de maintenance technique, le technicien dispose souvent d'une photo du problème (pièce défectueuse, panneau de contrôle, schéma) et non d'une description textuelle précise.

**Pratiques identifiées :**

- **CLIP (Contrastive Language-Image Pre-Training) [S3] :** Encode texte et image dans un espace commun 512-dim. Permet de rechercher des images par requête texte en français ET de trouver des images similaires à une photo query. Limite : entraîné principalement sur de l'anglais ; les requêtes françaises sont moins précises qu'en anglais.
- **ColPali :** Approche plus récente (2024) qui encode directement les pages PDF comme images via un VLM (PaliGemma). Très efficace sur les documents riches en tableaux et schémas. Non retenu pour L2 : nécessite GPU et modèle >7B paramètres.
- **Descripteurs textuels pour images :** Générer une légende automatique (`caption`) pour chaque image et l'indexer dans la collection texte permet la recherche texte-image sans encoder l'image. Fallback utilisé dans MaintiDoc pour les 3 images du corpus.
- **Fusion multimodale :** RRF appliqué sur 3 listes : texte dense, texte→image (CLIP text query), image→image (CLIP photo query). Résultats ordonnés par score RRF.

**Décision dans MaintiDoc :** CLIP ViT-B/32 (openai, 512-dim) + RRF 3 listes. Photo query optionnelle via upload Streamlit ou paramètre API.

---

### Fiche 4 — Contrôle d'accès et métadonnées (RBAC)

**Enjeu :** Dans un GMAO industriel, un technicien d'atelier ne doit pas accéder aux procédures d'un autre service. Le contrôle doit être appliqué *avant* la recherche (pre-filter) et non après (post-filter) pour éviter les fuites d'information par inférence.

**Pratiques identifiées :**

- **Pre-filter vs post-filter :** Un post-filter appliqué après recherche expose potentiellement des embeddings d'un document interdit (un adversaire pourrait inférer son contenu par similarité). Qdrant supporte nativement le filtrage en payload avant la recherche vectorielle via `Filter(must=[FieldCondition(...)])` [S1].
- **Stockage du groupe d'accès en payload :** Chaque point Qdrant porte `famille` et `groupe_acces`. Le filtre RBAC utilise `MatchAny(any=allowed_families)` — robuste aux extensions futures (ajout d'une nouvelle famille ne requiert qu'un re-index partiel).
- **HMAC pour les liens directs :** Les URLs de téléchargement de documents originaux sont signées par HMAC-SHA256. Un token invalide = accès refusé, même si l'URL est connue.
- **Audit trail :** Chaque requête devrait loguer `(user_group, query, timestamp, families_accessed)` pour auditabilité RGPD. Reporté à L3 (PostgreSQL logs).

**Décision dans MaintiDoc :** Pre-filter Qdrant + HMAC tokens + 6 tests pytest automatiques. PostgreSQL audit log reporté à L3.

---

## 3. Tableau de synthèse

| Pratique RAG | Source | Statut dans MaintiDoc | Commentaire |
|---|---|---|---|
| Chunking paragraphe-aware avec overlap | [S5] | ✅ Appliquée | 1200 chars / 200 overlap |
| Métadonnées RBAC en payload Qdrant | [S1] | ✅ Appliquée | famille + groupe_acces |
| RBAC pre-filter (avant recherche) | [S1] | ✅ Appliquée | FieldCondition + MatchAny |
| BGE-M3 embeddings multilingues | [S2] | ✅ Appliquée | fallback all-MiniLM sur CPU |
| RRF fusion multi-listes | [S6] | ✅ Appliquée | k=60, 2–3 listes |
| CLIP ViT-B/32 recherche image | [S3] | ✅ Appliquée | openai pretrained |
| BGE-M3 mode sparse (lexical) | [S2] | ⏳ Reportée (L3) | nécessite FlagEmbedding GPU |
| Re-ranking cross-encoder | [S5] | ⏳ Reportée (L3) | bge-reranker-v2-m3 |
| ColPali (page-as-image) | — | ❌ Écartée (L2) | nécessite GPU 7B+ |
| PostgreSQL audit log | [S1] | ⏳ Reportée (L3) | docker-compose prêt |
| HMAC signature URLs | — | ✅ Appliquée | SHA256, maintidoc_secret |
| Évaluation Recall@5 + MRR@10 | — | ✅ Appliquée | script evaluer_recherche.py |

---

## 4. Sources

| ID | Référence |
|---|---|
| [S1] | Qdrant. *Filtering and Payload*. Documentation officielle, 2024. https://qdrant.tech/documentation/concepts/filtering/ |
| [S2] | Chen et al. / BAAI. *BGE-M3: Multi-Functionality Mixed-Language Representation*. arXiv:2309.07597, 2024. https://arxiv.org/abs/2309.07597 |
| [S3] | Radford et al. / OpenAI. *Learning Transferable Visual Models From Natural Language Supervision*. ICML 2021. https://arxiv.org/abs/2103.00020 |
| [S4] | Lewis et al. / Meta AI. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. https://arxiv.org/abs/2005.11401 |
| [S5] | LlamaIndex. *Advanced RAG Techniques*. Documentation officielle, 2024. https://docs.llamaindex.ai/en/stable/optimizing/advanced_retrieval/ |
| [S6] | Cormack, Clarke, Buettcher. *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods*. SIGIR 2009. https://dl.acm.org/doi/10.1145/1571941.1572114 |
| [S7] | Artifex Software. *PyMuPDF Documentation – Text Extraction*. 2024. https://pymupdf.readthedocs.io/ |
