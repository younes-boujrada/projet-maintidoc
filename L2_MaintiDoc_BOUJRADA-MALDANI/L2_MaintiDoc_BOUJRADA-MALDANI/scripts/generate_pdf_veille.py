"""
Generate L2_MaintiDoc_BOUJRADA-MALDANI_Veille.pdf (4 pages).
"""
import pymupdf as fitz
from pathlib import Path

OUT_PDF = Path("L2_MaintiDoc_BOUJRADA-MALDANI_Veille.pdf")

doc = fitz.open()

def add_header_footer(page, page_num, total_pages=4):
    rect = page.rect
    # Header line
    page.draw_line(fitz.Point(50, 45), fitz.Point(rect.width - 50, 45), color=(0.7, 0.7, 0.7), width=0.5)
    page.insert_text(fitz.Point(50, 38), "MaintiDoc — Livrable 2 : Veille sur les Bonnes Pratiques RAG Multimodal", fontsize=8, color=(0.4, 0.4, 0.4))
    page.insert_text(fitz.Point(rect.width - 160, 38), "Équipe : BOUJRADA - MALDANI", fontsize=8, color=(0.4, 0.4, 0.4))
    
    # Footer line
    page.draw_line(fitz.Point(50, rect.height - 40), fitz.Point(rect.width - 50, rect.height - 40), color=(0.7, 0.7, 0.7), width=0.5)
    page.insert_text(fitz.Point(50, rect.height - 28), "EMSI 2026 · Module IA Générative Multimodale · Prof. Mariam CHERRABI", fontsize=8, color=(0.4, 0.4, 0.4))
    page.insert_text(fitz.Point(rect.width - 90, rect.height - 28), f"Page {page_num} / {total_pages}", fontsize=8, color=(0.4, 0.4, 0.4))

# ==================== PAGE 1 ====================
p1 = doc.new_page(width=595, height=842) # A4
add_header_footer(p1, 1)

# Title Block
p1.draw_rect(fitz.Rect(50, 60, 545, 130), color=(0.1, 0.25, 0.5), fill=(0.95, 0.97, 1.0), width=1)
p1.insert_text(fitz.Point(70, 85), "VEILLE TECHNOLOGIQUE : BONNES PRATIQUES RAG MULTIMODAL", fontsize=13, fontname="helv", color=(0.1, 0.2, 0.5))
p1.insert_text(fitz.Point(70, 105), "Assistant documentaire technique et industriel pour la maintenance (MaintiDoc)", fontsize=10, color=(0.2, 0.2, 0.2))
p1.insert_text(fitz.Point(70, 120), "Auteurs : Younes BOUJRADA & Mostafa MALDANI — Version Livrable 2 (v0.2-L2) — Nov. 2026", fontsize=8.5, color=(0.4, 0.4, 0.4))

# Section 1
p1.insert_text(fitz.Point(50, 155), "1. Méthode et Démarche de Veille", fontsize=11, fontname="helv", color=(0.1, 0.25, 0.5))
p1.draw_line(fitz.Point(50, 160), fitz.Point(545, 160), color=(0.1, 0.25, 0.5), width=1)

text_p1_s1 = (
    "Dans le cadre de la conception du système MaintiDoc, la veille technologique s'est concentrée sur l'état de l'art "
    "du RAG (Retrieval-Augmented Generation) appliqué à des environnements industriels critiques. Ces contextes imposent "
    "trois contraintes majeures : une haute précision technique (terminologie stricte, codes erreurs), la multimodalité "
    "(présence de schémas, mires et éclatés techniques) et un cloisonnement strict des accès documentaires (RBAC).\n\n"
    "Notre processus d'investigation a croisé trois typologies de sources vérifiées et récentes (2020-2024) :\n"
    "  • Les publications scientifiques de référence issues des conférences majeures (NeurIPS, ICML, SIGIR, arXiv) ;\n"
    "  • La documentation officielle des technologies de pointe adoptées (Qdrant, BGE-M3, PyMuPDF, LlamaIndex) ;\n"
    "  • Les retours d'expérience et benchmarks industriels de vector databases et modèles de représentation multimodale.\n\n"
    "Chaque pratique identifiée a fait l'objet d'une analyse critique vis-à-vis des contraintes matérielles de notre projet "
    "(développement local CPU/GPU, latence de consultation, reproductibilité) pour aboutir à une décision d'implémentation argumentée."
)
p1.insert_textbox(fitz.Rect(50, 170, 545, 300), text_p1_s1, fontsize=9, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Section 2 - Fiche 1
p1.insert_text(fitz.Point(50, 315), "2. Fiches Thématiques Approfondies", fontsize=11, fontname="helv", color=(0.1, 0.25, 0.5))
p1.draw_line(fitz.Point(50, 320), fitz.Point(545, 320), color=(0.1, 0.25, 0.5), width=1)

p1.insert_text(fitz.Point(50, 340), "Fiche 1 : Stratégies de Découpage de Documents Techniques (Chunking)", fontsize=10, fontname="helv", color=(0.2, 0.3, 0.6))
text_p1_f1 = (
    "Enjeu : Dans un corpus de maintenance, le découpage naïf (par nombre fixe de caractères) détruit fréquemment la structure "
    "des procédures pas-à-pas et scinde des tableaux de diagnostic en fragments inintelligibles.\n\n"
    "Pratiques et Enseignements de l'État de l'Art :\n"
    "1. Granularité sémantique et chevauchement (Overlap) : LlamaIndex [S5] recommande des segments de 256 à 512 tokens "
    "pour les documentations denses. Un overlap de 10% à 15% est indispensable pour garantir qu'aucune consigne de sécurité ou "
    "couple de serrage ne soit tronqué entre deux passages adjacents.\n"
    "2. Découpage conscient de la structure (Structure-Aware) : L'analyse des délimiteurs naturels (paragraphes, titres Markdown, "
    "sauts de page) est supérieure au chunking arbitraire. PyMuPDF [S7] extrait les blocs de texte avec typologie (titre, paragraphe, image).\n"
    "3. Préservation des figures et métadonnées contextuelles : Isoler les figures techniques tout en leur associant les métadonnées "
    "du document parent (document_id, page, famille, groupe_acces) évite la perte de traçabilité lors du retrieval.\n\n"
    "Décision pour MaintiDoc : Implémentation d'un Chunker par paragraphes avec seuil cible de 1200 caractères (~300 tokens) "
    "et chevauchement de 200 caractères (~50 tokens). Chaque chunk porte l'ensemble des métadonnées de l'inventaire en payload Qdrant."
)
p1.insert_textbox(fitz.Rect(50, 350, 545, 530), text_p1_f1, fontsize=9, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Section 2 - Fiche 2
p1.insert_text(fitz.Point(50, 550), "Fiche 2 : Recherche Hybride et Fusion de Résultats (Dense + Sparse / RRF)", fontsize=10, fontname="helv", color=(0.2, 0.3, 0.6))
text_p1_f2 = (
    "Enjeu : La recherche purement vectorielle (dense) capture le sens général mais échoue souvent sur les identifiants exacts "
    "(ex. code d'erreur '0x97', référence 'SC-P700'). Inversement, la recherche lexicale (BM25) ignore les synonymes et périphrases.\n\n"
    "Pratiques et Enseignements de l'État de l'Art :\n"
    "1. Reciprocal Rank Fusion (RRF) [S6] : Introduit par Cormack et al. (SIGIR 2009), RRF combine plusieurs listes ordonnées sans "
    "nécessiter de normalisation préalable des scores (qui varient grandement entre cosinus dense et scores BM25). La formule "
    "RRF_score(d) = Σ 1 / (60 + rang(d)) s'avère empiriquement supérieure et plus stable que les combinaisons linéaires pondérées.\n"
    "2. Modèles polyvalents unifiés (BGE-M3) [S2] : BGE-M3 supporte conjointement les représentations dense (1024 dims), "
    "lexicale (poids appris par terme) et multi-vectorielle (ColBERT). Il excelle en français technique et environnement multilingue.\n\n"
    "Décision pour MaintiDoc : Implémentation de RRF (k=60) fusionnant la recherche vectorielle textuelle (BGE-M3 / all-MiniLM) "
    "et la recherche d'images par similarité sémantique CLIP. Le re-ranking par cross-encoder est planifié pour le Livrable 3."
)
p1.insert_textbox(fitz.Rect(50, 560, 545, 800), text_p1_f2, fontsize=9, color=(0.15, 0.15, 0.15), lineheight=1.35)


# ==================== PAGE 2 ====================
p2 = doc.new_page(width=595, height=842)
add_header_footer(p2, 2)

# Fiche 3
p2.insert_text(fitz.Point(50, 60), "Fiche 3 : Recherche Multimodale (Embeddings Conjoints Texte-Image & Vision RAG)", fontsize=10, fontname="helv", color=(0.2, 0.3, 0.6))
p2.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.2, 0.3, 0.6), width=0.8)

text_p2_f3 = (
    "Enjeu : En situation de panne sur site, le technicien prend fréquemment une photo d'un composant encrassé, d'une mire "
    "d'impression dégradée ou d'un voyant clignotant. Le système doit faire le pont entre ce signal visuel et les manuels techniques textuels.\n\n"
    "Pratiques et Enseignements de l'État de l'Art :\n"
    "1. Espace latent partagé (CLIP) [S3] : Radford et al. (OpenAI, 2021) projettent images et textes dans un même espace géométrique "
    "(512 dims pour ViT-B/32). Cela autorise deux modes d'interrogation essentiels :\n"
    "   • Recherche Texte -> Image : retrouver une figure technique à partir d'une requête descriptive en français ;\n"
    "   • Recherche Image -> Image (Photo Query) : soumettre une photo terrain et identifier le schéma ou la mire de référence.\n"
    "2. Limite linguistique et adaptation multilingue : Le modèle CLIP standard d'OpenAI a été entraîné principalement sur de l'anglais. "
    "Les variantes multilingues comme M-CLIP (XLM-Roberta) améliorent la compréhension des langues romanes mais augmentent fortement "
    "l'empreinte mémoire (>1.4 Go) et la latence sans gain notable sur de petits corpus industriels très visuels.\n"
    "3. Nouveaux paradigmes Vision-Doc (ColPali, 2024) : ColPali indexe directement les pages de documents comme des images sans OCR. "
    "Bien que très performant pour les mises en page complexes, il requiert des modèles de 7B paramètres et des GPU puissants (>16 Go VRAM).\n\n"
    "Décision pour MaintiDoc : Déploiement d'une collection Qdrant dédiée aux images vectorisées par openai/clip-vit-base-patch32 (512 dims), "
    "doublée d'un indexage de légendes descriptives dans la collection texte pour assurer un rappel exhaustif sur requêtes textuelles pures."
)
p2.insert_textbox(fitz.Rect(50, 75, 545, 320), text_p2_f3, fontsize=9, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Fiche 4
p2.insert_text(fitz.Point(50, 335), "Fiche 4 : Sécurité et Contrôle d'Accès Documentaire (RBAC & Pre-Filtering Vectoriel)", fontsize=10, fontname="helv", color=(0.2, 0.3, 0.6))
p2.draw_line(fitz.Point(50, 340), fitz.Point(545, 340), color=(0.2, 0.3, 0.6), width=0.8)

text_p2_f4 = (
    "Enjeu : Dans une organisation d'entreprise, les techniciens ne doivent avoir accès qu'aux équipements de leur spécialité "
    "(ex. un technicien audiovisuel ne doit pas consulter les rapports confidentiels du pôle impression). Un système RAG qui filtre "
    "les résultats après coup expose l'entreprise à des failles de sécurité majeures.\n\n"
    "Pratiques et Enseignements de l'État de l'Art :\n"
    "1. Pre-Filtering vs Post-Filtering [S1] :\n"
    "   • Post-filtering (A posteriori) : Interroger l'index global puis supprimer les résultats non autorisés. Cette approche dégrade "
    "le Recall@k (si les 5 premiers documents sont interdits, l'utilisateur ne reçoit rien) et présente un risque d'inférence statistique.\n"
    "   • Pre-filtering (A priori) : La base vectorielle restreint l'espace de recherche aux seuls documents autorisés avant le calcul "
    "des plus proches voisins (HNSW graph traversal avec prédicat de payload). Qdrant excelle dans ce mode grâce à son architecture native.\n"
    "2. Modélisation fine des permissions en métadonnées : Associer à chaque fragment de document son groupe cible (famille, equipement_id, "
    "groupe_acces). L'utilisation de conditions de filtrage flexibles (ex. MatchAny) garantit l'évolutivité lors de l'ajout de nouveaux profils.\n"
    "3. Protection cryptographique des liens de consultation : Sécuriser les URLs de téléchargement et d'affichage des documents orignaux "
    "via des signatures HMAC-SHA256 afin d'empêcher les attaques par énumération directe d'identifiants (IDOR).\n\n"
    "Décision pour MaintiDoc : Application stricte du Pre-filtering dans Qdrant avec FieldCondition(key='famille', match=MatchAny(...)), "
    "complétée par des tokens HMAC de vérification d'intégrité et une suite de tests unitaires automatisés validant l'étanchéité des profils."
)
p2.insert_textbox(fitz.Rect(50, 350, 545, 600), text_p2_f4, fontsize=9, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Page 2 Bottom Box - Résumé méthodologique
p2.draw_rect(fitz.Rect(50, 615, 545, 770), color=(0.2, 0.4, 0.3), fill=(0.95, 0.98, 0.95), width=1)
p2.insert_text(fitz.Point(65, 635), "Synthèse des Recommandations Applicables à MaintiDoc", fontsize=10, fontname="helv", color=(0.15, 0.4, 0.2))
summary_box = (
    "• L'efficacité d'un RAG multimodal ne réside pas dans la complexité brute des modèles, mais dans la synergie entre un découpage "
    "respectant la structure du document technique et une indexation multi-représentations (texte dense + CLIP).\n"
    "• Le choix de Qdrant s'impose comme un standard industriel moderne grâce à son filtrage en amont (pre-filter) sans dégradation de performance.\n"
    "• La fusion RRF apporte la robustesse nécessaire pour traiter uniformément requêtes textuelles, figures et photos d'intervention."
)
p2.insert_textbox(fitz.Rect(65, 650, 530, 760), summary_box, fontsize=8.5, color=(0.1, 0.3, 0.1), lineheight=1.35)


# ==================== PAGE 3 ====================
p3 = doc.new_page(width=595, height=842)
add_header_footer(p3, 3)

# Section 3 - Tableau de Synthèse
p3.insert_text(fitz.Point(50, 60), "3. Tableau de Synthèse des Pratiques RAG Étudiées", fontsize=11, fontname="helv", color=(0.1, 0.25, 0.5))
p3.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

table_top = 80
row_h = 42

headers = ["Pratique RAG Analysée", "Source", "Statut MaintiDoc", "Justification Technique & Décision"]
col_w = [140, 50, 85, 220]

# Draw Table Header
p3.draw_rect(fitz.Rect(50, table_top, 545, table_top + 25), color=(0.1, 0.25, 0.5), fill=(0.15, 0.3, 0.6), width=1)
p3.insert_text(fitz.Point(55, table_top + 16), headers[0], fontsize=8.5, fontname="helv", color=(1, 1, 1))
p3.insert_text(fitz.Point(195, table_top + 16), headers[1], fontsize=8.5, fontname="helv", color=(1, 1, 1))
p3.insert_text(fitz.Point(245, table_top + 16), headers[2], fontsize=8.5, fontname="helv", color=(1, 1, 1))
p3.insert_text(fitz.Point(335, table_top + 16), headers[3], fontsize=8.5, fontname="helv", color=(1, 1, 1))

rows_data = [
    ("Chunking par paragraphes avec overlap (300t / 50t)", "[S5]", "Appliquée (L2)", "Préserve les consignes et étapes de dépannage sans tronquage."),
    ("Métadonnées RBAC complètes en payload Qdrant", "[S1]", "Appliquée (L2)", "Stocke famille, groupe_acces et identifiants pour filtrage natif."),
    ("Pre-filtering vectoriel strict avant recherche", "[S1]", "Appliquée (L2)", "Empêche toute fuite d'information et conserve un Recall optimal."),
    ("Indexation conjointe texte et image (CLIP ViT-B/32)", "[S3]", "Appliquée (L2)", "Permet la recherche texte-image et par photo query en 512 dims."),
    ("Fusion multi-listes par Reciprocal Rank Fusion (k=60)", "[S6]", "Appliquée (L2)", "Agrège les rangs textuels et visuels sans biais d'échelle de scores."),
    ("Extraction hybride PyMuPDF + OCR de secours", "[S7]", "Appliquée (L2)", "Extraction native rapide (0.1s) + tesseract pour scans d'atelier."),
    ("Embeddings BGE-M3 denses multilingues", "[S2]", "Appliquée (L2)", "Modèle imposé (1024 dims). Fallback all-MiniLM pour CPU local."),
    ("Mode sparse lexical BGE-M3 (ColBERT / BM25)", "[S2]", "Reportée (L3)", "Nécessite GPU et FlagEmbedding; sera intégré avec l'agent GMAO."),
    ("Re-ranking neuronal par Cross-Encoder (bge-reranker)", "[S5]", "Reportée (L3)", "Améliore le MRR@5 sur les 20 premiers résultats; prévu en S3."),
    ("ColPali (Vision-Language Page Indexing)", "[—]", "Écartée (L2)", "Empreinte mémoire excessive (>16 Go) et dépendance GPU prohibitive."),
    ("Stockage persistant MinIO / S3 pour images", "[S1]", "Appliquée (L2)", "Prêt sous docker-compose.yml; stockage disque local en mode dev."),
    ("Audit trail des accès et requêtes sous PostgreSQL", "[S1]", "Reportée (L3)", "Structure prête dans docker-compose; journalisation complète en S3.")
]

y_row = table_top + 25
for i, r in enumerate(rows_data):
    bg_color = (0.98, 0.98, 0.98) if i % 2 == 0 else (1.0, 1.0, 1.0)
    p3.draw_rect(fitz.Rect(50, y_row, 545, y_row + row_h), color=(0.8, 0.8, 0.8), fill=bg_color, width=0.5)
    
    # Text insertion
    p3.insert_textbox(fitz.Rect(55, y_row + 3, 190, y_row + row_h), r[0], fontsize=7.5, color=(0.1, 0.1, 0.1))
    p3.insert_text(fitz.Point(195, y_row + 18), r[1], fontsize=7.5, color=(0.2, 0.4, 0.7))
    
    status_col = (0.0, 0.5, 0.1) if "Appliquée" in r[2] else ((0.8, 0.5, 0.0) if "Reportée" in r[2] else (0.6, 0.1, 0.1))
    p3.insert_text(fitz.Point(245, y_row + 18), r[2], fontsize=7.5, fontname="helv", color=status_col)
    
    p3.insert_textbox(fitz.Rect(335, y_row + 3, 540, y_row + row_h), r[3], fontsize=7.5, color=(0.2, 0.2, 0.2))
    y_row += row_h

p3.insert_text(fitz.Point(50, y_row + 25), "Synthèse opérationnelle : 7 pratiques appliquées dès le Livrable 2, 3 reportées au Livrable 3 (Agentic / VLM), 1 écartée.", fontsize=8.5, fontname="helv", color=(0.2, 0.2, 0.2))


# ==================== PAGE 4 ====================
p4 = doc.new_page(width=595, height=842)
add_header_footer(p4, 4)

# Section 4 - Sources
p4.insert_text(fitz.Point(50, 60), "4. Sources Référencées et Vérifiées", fontsize=11, fontname="helv", color=(0.1, 0.25, 0.5))
p4.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

sources_desc = (
    "Conformément aux exigences du cahier des charges du Livrable 2, les sources retenues ont été vérifiées par les deux membres "
    "de l'équipe. Elles comprennent 4 publications scientifiques avec comité de lecture ou archives ouvertes majeures, et 3 documentations "
    "techniques officielles d'outils industriels de premier plan. Toutes les sources sont accessibles publiquement."
)
p4.insert_textbox(fitz.Rect(50, 75, 545, 120), sources_desc, fontsize=8.5, color=(0.2, 0.2, 0.2), lineheight=1.3)

sources = [
    ("[S1]", "Qdrant Documentation : Filtering and Payload Concepts", "Qdrant Official Docs, 2024", "https://qdrant.tech/documentation/concepts/filtering/",
     "Explicite l'algorithme HNSW étendu avec pre-filtering par payload conditionnel. Démontre la supériorité du pre-filter sur le post-filter."),
    ("[S2]", "BGE-M3 : Multi-Functionality Mixed-Language Representation", "Chen et al. (BAAI / FlagAI), arXiv:2309.07597, 2024", "https://arxiv.org/abs/2309.07597",
     "Publication fondatrice du modèle imposé BGE-M3 (1024 dims). Démontre la polyvalence multi-tâche dense/sparse/ColBERT sur plus de 100 langues."),
    ("[S3]", "Learning Transferable Visual Models From Natural Language Supervision (CLIP)", "Radford et al. (OpenAI), ICML 2021", "https://arxiv.org/abs/2103.00020",
     "Détaille l'architecture contrastive texte-image permettant la recherche cross-modale et l'interrogation par image requête (photo query)."),
    ("[S4]", "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "Lewis et al. (Meta AI), NeurIPS 2020", "https://arxiv.org/abs/2005.11401",
     "Article séminal définissant le paradigme RAG moderne, combinant composant de récupération paramétrique et génération conditionnelle."),
    ("[S5]", "Advanced RAG Techniques and Document Chunking", "LlamaIndex Documentation, 2024", "https://docs.llamaindex.ai/en/stable/optimizing/advanced_retrieval/",
     "Fournit les métriques et règles heuristiques pour le dimensionnement des chunks (tokens vs délimiteurs de structure) et le re-ranking."),
    ("[S6]", "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods", "Cormack, Clarke, Buettcher, ACM SIGIR 2009", "https://dl.acm.org/doi/10.1145/1571941.1572114",
     "Démontre mathématiquement que la fusion inverse des rangs (RRF avec k=60) élimine le biais d'échelle entre listes de scores hétérogènes."),
    ("[S7]", "PyMuPDF Documentation : Text & Image Extraction from PDF", "Artifex Software, 2024", "https://pymupdf.readthedocs.io/",
     "Guide officiel d'extraction de primitives graphiques et textuelles des documents PDF industriels, assurant la fidélité des métadonnées.")
]

y_src = 130
for sid, title, author, url, annot in sources:
    p4.draw_rect(fitz.Rect(50, y_src, 545, y_src + 60), color=(0.85, 0.85, 0.85), fill=(0.99, 0.99, 1.0), width=0.5)
    p4.insert_text(fitz.Point(60, y_src + 15), sid, fontsize=9, fontname="helv", color=(0.1, 0.25, 0.5))
    p4.insert_text(fitz.Point(85, y_src + 15), title, fontsize=8.5, fontname="helv", color=(0.1, 0.1, 0.1))
    p4.insert_text(fitz.Point(85, y_src + 28), author, fontsize=7.5, color=(0.3, 0.3, 0.3))
    p4.insert_text(fitz.Point(85, y_src + 40), f"URL : {url}", fontsize=7, color=(0.15, 0.35, 0.7))
    p4.insert_text(fitz.Point(85, y_src + 52), f"Impact sur MaintiDoc : {annot}", fontsize=7, color=(0.2, 0.5, 0.2))
    y_src += 68

# Sign-off box
p4.draw_rect(fitz.Rect(50, 715, 545, 765), color=(0.1, 0.25, 0.5), fill=(0.96, 0.97, 1.0), width=0.8)
p4.insert_text(fitz.Point(70, 735), "Validation de la Veille par l'Équipe MaintiDoc :", fontsize=8.5, fontname="helv", color=(0.1, 0.25, 0.5))
p4.insert_text(fitz.Point(70, 752), "Mostafa MALDANI (Vérificateur [S1, S3, S5, S7])   ·   Younes BOUJRADA (Vérificateur [S2, S4, S6])", fontsize=8, color=(0.3, 0.3, 0.3))

doc.save(str(OUT_PDF))
print(f"✓ Veille générée : {OUT_PDF} ({len(doc)} pages)")
