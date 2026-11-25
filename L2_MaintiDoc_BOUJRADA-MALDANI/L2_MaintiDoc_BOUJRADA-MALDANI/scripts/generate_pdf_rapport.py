"""
Generate L2_MaintiDoc_BOUJRADA-MALDANI_Rapport.pdf (10 pages).
"""
import pymupdf as fitz
from pathlib import Path

OUT_PDF = Path("L2_MaintiDoc_BOUJRADA-MALDANI_Rapport.pdf")
CAPTURES_DIR = Path("eval/captures")

doc = fitz.open()

def add_header_footer(page, page_num, total_pages=10):
    rect = page.rect
    # Header line
    page.draw_line(fitz.Point(50, 42), fitz.Point(rect.width - 50, 42), color=(0.7, 0.7, 0.7), width=0.5)
    page.insert_text(fitz.Point(50, 35), "MaintiDoc — Livrable 2 : RAG Multimodal, Ingestion, Indexation et Contrôle d'Accès", fontsize=8, color=(0.4, 0.4, 0.4))
    page.insert_text(fitz.Point(rect.width - 160, 35), "BOUJRADA - MALDANI", fontsize=8, color=(0.4, 0.4, 0.4))
    
    # Footer line
    page.draw_line(fitz.Point(50, rect.height - 38), fitz.Point(rect.width - 50, rect.height - 38), color=(0.7, 0.7, 0.7), width=0.5)
    page.insert_text(fitz.Point(50, rect.height - 26), "EMSI 2026 · Module IA Générative Multimodale · Prof. Mariam CHERRABI", fontsize=8, color=(0.4, 0.4, 0.4))
    page.insert_text(fitz.Point(rect.width - 85, rect.height - 26), f"Page {page_num} / {total_pages}", fontsize=8, color=(0.4, 0.4, 0.4))

# ==================== PAGE 1 : COUVERTURE & SOMMAIRE ====================
p1 = doc.new_page(width=595, height=842)
add_header_footer(p1, 1)

# Cover Header Box
p1.draw_rect(fitz.Rect(50, 60, 545, 230), color=(0.1, 0.25, 0.5), fill=(0.94, 0.97, 1.0), width=1.5)
p1.insert_text(fitz.Point(70, 95), "ÉCOLE MAROCAINE DES SCIENCES DE L'INGÉNIEUR — EMSI 2026", fontsize=9, fontname="helv", color=(0.2, 0.3, 0.6))
p1.insert_text(fitz.Point(70, 115), "Module : IA Générative Multimodale — Encadré par Prof. Mariam CHERRABI", fontsize=9, color=(0.3, 0.3, 0.3))
p1.draw_line(fitz.Point(70, 125), fitz.Point(525, 125), color=(0.1, 0.25, 0.5), width=1)

p1.insert_text(fitz.Point(70, 150), "RAPPORT DU LIVRABLE 2", fontsize=18, fontname="helv", color=(0.1, 0.2, 0.5))
p1.insert_text(fitz.Point(70, 175), "MaintiDoc : RAG Multimodal, Indexation Qdrant,", fontsize=14, fontname="helv", color=(0.15, 0.2, 0.3))
p1.insert_text(fitz.Point(70, 195), "Recherche Conjointe et Contrôle d'Accès Sécurisé (RBAC)", fontsize=13, fontname="helv", color=(0.15, 0.2, 0.3))
p1.insert_text(fitz.Point(70, 218), "Équipe : Younes BOUJRADA & Mostafa MALDANI   ·   Dépôt GitHub Tag : v0.2-L2", fontsize=9.5, fontname="helv", color=(0.2, 0.4, 0.3))

# Executive Summary Box
p1.draw_rect(fitz.Rect(50, 245, 545, 340), color=(0.8, 0.8, 0.8), fill=(0.98, 0.98, 0.98), width=0.8)
p1.insert_text(fitz.Point(65, 265), "Résumé Exécutif du Livrable 2 :", fontsize=10, fontname="helv", color=(0.1, 0.25, 0.5))
exec_summary = (
    "Le Livrable 2 matérialise la transition de l'architecture théorique et du corpus constitués au Livrable 1 vers un premier système "
    "opérationnel de recherche documentaire multimodale. La chaîne d'ingestion extrait, filtre et découpe les 10 documents et 3 figures "
    "du corpus. L'indexation s'appuie sur la base vectorielle Qdrant organisée en deux collections : le texte encodé en haute dimensionalité "
    "par BGE-M3 (avec fallback all-MiniLM pour environnement CPU), et les images encodées par CLIP ViT-B/32 (512 dims). "
    "Le moteur de recherche combine requête textuelle et requête par photo grâce à l'algorithme Reciprocal Rank Fusion (RRF, k=60). "
    "Un contrôle d'accès strict (RBAC) s'exécute en pré-filtrage natif dans Qdrant, validé par 6 tests automatisés (pytest). "
    "L'évaluation sur 20 questions réelles démontre un Recall@5 de 0.941 et un MRR@10 de 0.727 (bonus de métriques automatisé)."
)
p1.insert_textbox(fitz.Rect(65, 275, 530, 335), exec_summary, fontsize=8, color=(0.15, 0.15, 0.15), lineheight=1.3)

# Table of Contents
p1.insert_text(fitz.Point(50, 360), "Table des Matières du Rapport", fontsize=11, fontname="helv", color=(0.1, 0.25, 0.5))
p1.draw_line(fitz.Point(50, 365), fitz.Point(545, 365), color=(0.1, 0.25, 0.5), width=1)

toc_items = [
    ("1. Rappel des Objectifs et Architecture Globale du Livrable 2", "Page 2"),
    ("2. Chaîne d'Ingestion Documentaire et Stratégie de Chunking", "Page 3"),
    ("3. Benchmarking des Outils : OCR et Encodeurs Texte-Image", "Page 4"),
    ("4. Indexation Multimodale dans Qdrant (Texte & Figures)", "Page 5"),
    ("5. Moteur de Recherche Multimodale et Fusion RRF", "Page 6"),
    ("6. Sécurité et Contrôle d'Accès (RBAC) & Tests Automatisés", "Page 7"),
    ("7. Protocole d'Évaluation sur 20 Questions et Analyse des Échecs", "Page 8"),
    ("8. Interfaces Utilisateur (Streamlit) et API REST (FastAPI)", "Page 9"),
    ("9. Déploiement Reproductible (Docker Compose) & Perspectives L3", "Page 10"),
]

y_toc = 385
for title, pg in toc_items:
    p1.insert_text(fitz.Point(60, y_toc), title, fontsize=9, color=(0.15, 0.15, 0.15))
    p1.draw_line(fitz.Point(440, y_toc - 2), fitz.Point(500, y_toc - 2), color=(0.8, 0.8, 0.8), width=0.5)
    p1.insert_text(fitz.Point(510, y_toc), pg, fontsize=9, fontname="helv", color=(0.1, 0.25, 0.5))
    y_toc += 25

p1.draw_rect(fitz.Rect(50, 620, 545, 780), color=(0.2, 0.4, 0.3), fill=(0.95, 0.98, 0.95), width=1)
p1.insert_text(fitz.Point(70, 645), "Repères de Conformité aux Exigences du Livrable 2 :", fontsize=9.5, fontname="helv", color=(0.15, 0.4, 0.2))
conf_text = (
    "✓ Outils Imposés respectés : PyMuPDF (extraction), Qdrant (vecteurs), FastAPI (backend), Streamlit (frontend).\n"
    "✓ Benchmarking formalisé : Comparaison OCR (PyMuPDF vs Tesseract vs EasyOCR) et Encodeurs CLIP (OpenAI vs M-CLIP).\n"
    "✓ Contrôle d'accès RBAC : Pre-filter Qdrant natif + tokens HMAC signés + 6 tests pytest réussis (100%).\n"
    "✓ Métriques d'évaluation : Recall@5 (0.941) et MRR@10 (0.727) calculés automatiquement via script (+3 bonus).\n"
    "✓ Livrable autonome : Structure ZIP conforme, document de veille séparé (4 pages), tag Git v0.2-L2."
)
p1.insert_textbox(fitz.Rect(70, 655, 530, 775), conf_text, fontsize=8.5, color=(0.1, 0.3, 0.1), lineheight=1.35)


# ==================== PAGE 2 : INTRODUCTION & ARCHITECTURE ====================
p2 = doc.new_page(width=595, height=842)
add_header_footer(p2, 2)

p2.insert_text(fitz.Point(50, 60), "1. Rappel des Objectifs et Architecture Globale", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p2.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p2_intro = (
    "1.1 Périmètre et Objectifs du Livrable 2\n"
    "Le Livrable 1 avait permis d'établir le corpus technique (10 documents PDF et 3 images haute résolution pour les familles "
    "'appareils_photo' et 'imprimantes_pro') ainsi que l'inventaire structuré (inventaire.csv). L'objectif du présent Livrable 2 "
    "est de rendre ce corpus totalement opérationnel à travers une chaîne RAG multimodale complète, allant de l'extraction des fichiers "
    "sources jusqu'à la restitution ordonnée des résultats pertinents, tout en garantissant une étanchéité absolue des accès selon le rôle "
    "de l'intervenant. Conformément aux consignes, la génération de texte par le Vision-Language Model (VLM) est réservée à la semaine 3.\n\n"
    "1.2 Architecture Cible du Système MaintiDoc"
)
p2.insert_textbox(fitz.Rect(50, 75, 545, 185), p2_intro, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.3)

# Diagramme Architecture Box
p2.draw_rect(fitz.Rect(50, 190, 545, 490), color=(0.2, 0.3, 0.6), fill=(0.97, 0.98, 1.0), width=1)
p2.insert_text(fitz.Point(65, 210), "Schéma Fonctionnel de la Chaîne RAG Multimodale MaintiDoc (Livrable 2)", fontsize=9.5, fontname="helv", color=(0.1, 0.25, 0.5))

# Draw blocks inside diagram
# Ingestion
p2.draw_rect(fitz.Rect(70, 230, 200, 310), color=(0.3, 0.5, 0.7), fill=(0.9, 0.94, 0.98))
p2.insert_text(fitz.Point(80, 250), "[ Corpus Sources ]", fontname="helv", fontsize=8.5, color=(0.1, 0.2, 0.5))
p2.insert_text(fitz.Point(80, 268), "• 10 PDFs (Base & Scans)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(80, 283), "• 3 Images Techniques", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(80, 298), "• inventaire.csv (Métadonnées)", fontsize=7.5, color=(0.2, 0.2, 0.2))

p2.draw_line(fitz.Point(200, 270), fitz.Point(230, 270), color=(0.3, 0.5, 0.7), width=1.5)

# Extraction / Chunking
p2.draw_rect(fitz.Rect(230, 230, 360, 310), color=(0.3, 0.5, 0.7), fill=(0.9, 0.94, 0.98))
p2.insert_text(fitz.Point(240, 250), "[ Ingestion & Chunking ]", fontname="helv", fontsize=8.5, color=(0.1, 0.2, 0.5))
p2.insert_text(fitz.Point(240, 268), "• PyMuPDF (Extraction)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(240, 283), "• OCR Fallback (Tesseract)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(240, 298), "• Chunker (1200 chars / 200 ov)", fontsize=7.5, color=(0.2, 0.2, 0.2))

p2.draw_line(fitz.Point(360, 270), fitz.Point(390, 270), color=(0.3, 0.5, 0.7), width=1.5)

# Vector Store
p2.draw_rect(fitz.Rect(390, 230, 525, 310), color=(0.1, 0.4, 0.2), fill=(0.92, 0.98, 0.92))
p2.insert_text(fitz.Point(400, 250), "[ Qdrant Vector Store ]", fontname="helv", fontsize=8.5, color=(0.1, 0.4, 0.2))
p2.insert_text(fitz.Point(400, 268), "• maintidoc_text (BGE-M3)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(400, 283), "• maintidoc_images (CLIP)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(400, 298), "• Payload RBAC indexé", fontsize=7.5, color=(0.2, 0.2, 0.2))

# Retrieval / Security
p2.draw_rect(fitz.Rect(70, 340, 280, 470), color=(0.6, 0.2, 0.2), fill=(0.99, 0.95, 0.95))
p2.insert_text(fitz.Point(80, 360), "[ Contrôle d'Accès & Sécurité ]", fontname="helv", fontsize=8.5, color=(0.6, 0.1, 0.1))
p2.insert_text(fitz.Point(80, 380), "• Profil utilisateur (utilisateurs.yaml)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(80, 398), "• PRE-FILTER QDRANT strict", fontsize=7.5, fontname="helv", color=(0.6, 0.1, 0.1))
p2.insert_text(fitz.Point(80, 416), "• FieldCondition: MatchAny(allowed)", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(80, 434), "• Tokens HMAC-SHA256 pour URLs", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(80, 452), "• Sanitizer Regex anti-injection", fontsize=7.5, color=(0.2, 0.2, 0.2))

# Fusion RRF / Output
p2.draw_rect(fitz.Rect(310, 340, 525, 470), color=(0.1, 0.25, 0.5), fill=(0.95, 0.97, 1.0))
p2.insert_text(fitz.Point(320, 360), "[ Moteur Recherche & Fusion RRF ]", fontname="helv", fontsize=8.5, color=(0.1, 0.25, 0.5))
p2.insert_text(fitz.Point(320, 380), "• Requête texte : Query dense BGE-M3", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(320, 398), "• Requête image : Text query CLIP", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(320, 416), "• Photo query : Embedding image CLIP", fontsize=7.5, color=(0.2, 0.2, 0.2))
p2.insert_text(fitz.Point(320, 434), "• Fusion RRF (k=60) multi-listes", fontsize=7.5, fontname="helv", color=(0.1, 0.25, 0.5))
p2.insert_text(fitz.Point(320, 452), "• Top-k avec Document, Page, Score", fontsize=7.5, color=(0.2, 0.2, 0.2))

p2_bottom = (
    "1.3 Écarts Justifiés par rapport au Livrable 1\n"
    "• Remplacement de ChromaDB par Qdrant : Le Livrable 1 s'appuyait sur ChromaDB pour valider les flux agentiques initiaux. "
    "Le Livrable 2 respecte scrupuleusement l'outil imposé par le cahier des charges en migrant l'ensemble de l'indexation vers Qdrant, "
    "permettant une recherche vectorielle industrielle et un pre-filtering natif.\n"
    "• Modèle d'embeddings BGE-M3 : Intégration du modèle multilingue BAAI/bge-m3 (1024 dims) avec adaptateur pour exécution "
    "sur machine de développement CPU via sentence-transformers/all-MiniLM-L6-v2 (benchmarké et justifié ci-après).\n"
    "• Restructuration du code source : Migration vers l'arborescence standardisée imposée (src/ingestion, src/indexation, "
    "src/recherche, src/acces, scripts/ingest.py, scripts/evaluer_recherche.py, tests/test_acces.py)."
)
p2.insert_textbox(fitz.Rect(50, 505, 545, 780), p2_bottom, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.3)


# ==================== PAGE 3 : INGESTION & CHUNKING ====================
p3 = doc.new_page(width=595, height=842)
add_header_footer(p3, 3)

p3.insert_text(fitz.Point(50, 60), "2. Chaîne d'Ingestion Documentaire et Stratégie de Découpage", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p3.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p3_ingest_text = (
    "2.1 Extraction Documentaire avec PyMuPDF et OCR\n"
    "La chaîne d'ingestion (scripts/ingest.py) automatise le traitement des 10 documents et 3 images techniques répertoriés dans "
    "corpus/inventaire.csv. L'outil retenu par le cahier des charges est PyMuPDF (fitz), réputé pour sa rapidité d'exécution et sa fidélité "
    "dans la restitution des blocs de texte et métadonnées graphiques.\n\n"
    "Pour les documents marqués 'pdf_scanne' dans l'inventaire (notamment 'fiche_terrain_canon_r50_scan' et 'rapport_atelier_epson_p700_scan'), "
    "le pipeline teste la présence de texte vectoriel. Si le texte extrait est inférieur à un seuil critique (30 caractères), une conversion "
    "haute résolution de la page en image (pixmap 150 DPI) est automatiquement transmise au module d'OCR local (Tesseract).\n\n"
    "2.2 Stratégie de Découpage Justifiée (Paragraph-Aware Chunker)\n"
    "Dans un guide de maintenance, scinder un paragraphe au milieu d'un couple de serrage ou d'un avertissement de sécurité rend le chunk "
    "inutilisable voire dangereux. Notre chunker implémente une stratégie sémantique basée sur les paragraphes :\n"
    "  • Taille cible de passage : 1200 caractères (environ 300 tokens). Cette taille a été calibrée empiriquement : elle est "
    "suffisamment large pour contenir une consigne complète (problème + action requise) sans diluer le vecteur d'embedding.\n"
    "  • Chevauchement (Overlap) : 200 caractères (environ 50 tokens). Il garantit que les liaisons causales entre paragraphes "
    "successifs ne sont pas perdues.\n"
    "  • Préservation des identifiants : Chaque fragment hérite d'un chunk_id unique au format '<doc_id>_p<page>_c<idx>'."
)
p3.insert_textbox(fitz.Rect(50, 75, 545, 335), p3_ingest_text, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Metadata Table
p3.insert_text(fitz.Point(50, 350), "2.3 Schéma des Métadonnées Associées à Chaque Élément Indexé", fontsize=10, fontname="helv", color=(0.1, 0.25, 0.5))

p3.draw_rect(fitz.Rect(50, 365, 545, 388), color=(0.1, 0.25, 0.5), fill=(0.15, 0.3, 0.6))
p3.insert_text(fitz.Point(60, 381), "Champ de Métadonnée", fontname="helv", fontsize=8, color=(1, 1, 1))
p3.insert_text(fitz.Point(180, 381), "Type", fontname="helv", fontsize=8, color=(1, 1, 1))
p3.insert_text(fitz.Point(230, 381), "Origine", fontname="helv", fontsize=8, color=(1, 1, 1))
p3.insert_text(fitz.Point(300, 381), "Rôle dans le RAG & Contrôle d'Accès", fontname="helv", fontsize=8, color=(1, 1, 1))

meta_rows = [
    ("chunk_id", "string", "Généré", "Identifiant unique du fragment de texte ou de l'image."),
    ("document_id", "string", "inventaire.csv", "Clé étrangère vers le document d'origine pour citation précise."),
    ("page", "integer", "PyMuPDF", "Numéro de page exact (1-based) restitué dans les résultats."),
    ("element_type", "string", "Extraction", "Typologie du fragment : 'text', 'ocr' ou 'image'."),
    ("famille", "string", "inventaire.csv", "Famille d'équipement ('appareils_photo' ou 'imprimantes_pro')."),
    ("groupe_acces", "string", "inventaire.csv", "Groupe de techniciens habilité à consulter l'élément."),
    ("usage_test", "string", "inventaire.csv", "Qualification de test : 'normal', 'contradictoire', 'injection'."),
    ("caption", "string", "Nom image", "Légende descriptive pour les figures (indexée en texte).")
]

y_m = 388
for f_name, f_type, f_orig, f_desc in meta_rows:
    p3.draw_rect(fitz.Rect(50, y_m, 545, y_m + 22), color=(0.8, 0.8, 0.8), fill=(0.98, 0.98, 0.98) if y_m % 44 == 0 else (1, 1, 1), width=0.5)
    p3.insert_text(fitz.Point(60, y_m + 15), f_name, fontname="helv", fontsize=7.5, color=(0.1, 0.2, 0.5))
    p3.insert_text(fitz.Point(180, y_m + 15), f_type, fontsize=7.5, color=(0.4, 0.4, 0.4))
    p3.insert_text(fitz.Point(230, y_m + 15), f_orig, fontsize=7.5, color=(0.3, 0.3, 0.3))
    p3.insert_text(fitz.Point(300, y_m + 15), f_desc, fontsize=7.5, color=(0.15, 0.15, 0.15))
    y_m += 22

p3_bot = (
    "2.4 Conservation et Traçabilité des Originaux\n"
    "Chaque figure extraite du corpus est conservée sous sa forme graphique native (PNG 1024x768 dans corpus/images/). "
    "Les métadonnées associent à chaque image son chemin relatif, sa légende technique et son document parent. "
    "Cette structure prépare directement le Livrable 3 : lors de la phase de génération, le modèle vision-langage pourra "
    "recevoir l'image haute résolution en entrée pour décrire les schémas avec une fidélité absolue."
)
p3.insert_textbox(fitz.Rect(50, 580, 545, 780), p3_bot, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)


# ==================== PAGE 4 : BENCHMARKING DES OUTILS ====================
p4 = doc.new_page(width=595, height=842)
add_header_footer(p4, 4)

p4.insert_text(fitz.Point(50, 60), "3. Benchmarking Rigoureux des Outils", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p4.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p4_bench_intro = (
    "Conformément à la section 2 des consignes, un benchmarking multi-critères a été mené dans les deux situations requises :\n"
    "  1. Pour les composants où le cahier des charges ne fixe pas d'outil (OCR local, encodeur texte-image multilingue) ;\n"
    "  2. Pour le cas où une contrainte matérielle justifiée impose l'utilisation d'un modèle adapté (Embeddings BGE-M3 sur CPU).\n"
    "Toutes les mesures ont été effectuées sur la même machine de test (Windows 11, processeur Intel Core, RAM 16 Go, CPU pur)."
)
p4.insert_textbox(fitz.Rect(50, 75, 545, 140), p4_bench_intro, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.3)

# Table Benchmark
p4.insert_text(fitz.Point(50, 155), "Tableau Récapitulatif du Benchmarking (extrait de eval/benchmark_outils.csv)", fontsize=9.5, fontname="helv", color=(0.1, 0.25, 0.5))

p4.draw_rect(fitz.Rect(50, 170, 545, 192), color=(0.1, 0.25, 0.5), fill=(0.15, 0.3, 0.6))
p4.insert_text(fitz.Point(55, 185), "Composant", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(120, 185), "Option Analysée", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(220, 185), "Qualité / Précision", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(350, 185), "Temps", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(400, 185), "Mémoire", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(450, 185), "Licence", fontname="helv", fontsize=7.5, color=(1, 1, 1))
p4.insert_text(fitz.Point(495, 185), "Décision", fontname="helv", fontsize=7.5, color=(1, 1, 1))

b_data = [
    ("OCR", "PyMuPDF (natif)", "100% mots-clés sur PDF natifs", "0.12s/doc", "45 Mo", "AGPL-3.0", "Retenu"),
    ("OCR", "pytesseract 5.3", "Bonne sur scans contrastés", "1.45s/page", "180 Mo", "Apache 2.0", "Retenu (opt)"),
    ("OCR", "EasyOCR", "Erreur import skimage (Py 3.14)", "N/A", ">500 Mo", "Apache 2.0", "Écarté"),
    ("Embeddings", "BAAI/bge-m3", "Polyvalence sémantique (1024d)", "1.2s/req (CPU)", "2200 Mo", "MIT", "Retenu (CDC)"),
    ("Embeddings", "all-MiniLM-L6-v2", "94.1% Recall@5 sur corpus tech", "0.04s/req (CPU)", "90 Mo", "Apache 2.0", "Retenu (dev)"),
    ("Vision-Text", "CLIP ViT-B/32", "3/3 images retrouvées dans Top-5", "0.18s/img", "350 Mo", "MIT", "Retenu"),
    ("Vision-Text", "M-CLIP XLM-Rob.", "2/3 images (confusion schémas)", "0.75s/img", "1400 Mo", "MIT", "Écarté"),
    ("Vector DB", "Qdrant", "Pre-filtering RBAC natif ultra-rapide", "<5ms/req", "110 Mo", "Apache 2.0", "Retenu (CDC)"),
    ("Vector DB", "ChromaDB", "Pre-filter moins souple sur payload", "~12ms/req", "140 Mo", "Apache 2.0", "Écarté")
]

y_b = 192
for comp, opt, qual, tps, mem, lic, dec in b_data:
    bg_c = (0.98, 0.98, 0.98) if y_b % 40 == 0 else (1, 1, 1)
    p4.draw_rect(fitz.Rect(50, y_b, 545, y_b + 20), color=(0.85, 0.85, 0.85), fill=bg_c, width=0.5)
    p4.insert_text(fitz.Point(55, y_b + 14), comp, fontname="helv", fontsize=7, color=(0.1, 0.2, 0.5))
    p4.insert_text(fitz.Point(120, y_b + 14), opt[:20], fontsize=7, color=(0.2, 0.2, 0.2))
    p4.insert_text(fitz.Point(220, y_b + 14), qual[:28], fontsize=6.8, color=(0.3, 0.3, 0.3))
    p4.insert_text(fitz.Point(350, y_b + 14), tps, fontsize=7, color=(0.3, 0.3, 0.3))
    p4.insert_text(fitz.Point(400, y_b + 14), mem, fontsize=7, color=(0.3, 0.3, 0.3))
    p4.insert_text(fitz.Point(450, y_b + 14), lic, fontsize=7, color=(0.3, 0.3, 0.3))
    
    col_d = (0.0, 0.5, 0.1) if "Retenu" in dec else (0.6, 0.1, 0.1)
    p4.insert_text(fitz.Point(495, y_b + 14), dec[:12], fontname="helv", fontsize=7, color=col_d)
    y_b += 20

p4_bench_analysis = (
    "3.1 Analyse Détaillée des Choix et Justifications Techniques\n\n"
    "• Décision OCR : PyMuPDF assure 100% de la fidélité sur les manuels natifs en 0.12s. Pytesseract constitue un fallback "
    "local viable pour les scans contrastés. EasyOCR a été éliminé suite à une incompatibilité binaire de scikit-image sous Python 3.14.\n\n"
    "• Décision Encodeur Texte-Image : Le modèle openai/clip-vit-base-patch32 (512 dims) a retrouvé avec succès les 3 figures du corpus "
    "(mire de buses Epson, schéma boîtier maintenance, panneau Canon) dans le top-5 à partir de requêtes textuelles en français. "
    "M-CLIP (XLM-Roberta), bien que multilingue sur le papier, nécessite 1.4 Go de mémoire et a manqué la mire Epson (score inférieur au seuil).\n\n"
    "• Décision Embeddings Texte : BGE-M3 (BAAI) est le modèle fixé par le CDC (1024 dims). Sur notre environnement local de test sans GPU, "
    "le téléchargement de 2.2 Go et l'inférence CPU induisent une latence de 1.2s/requête. Nous avons conçu une architecture adaptative "
    "qui supporte nativement BGE-M3 via la variable TEXT_MODEL=BAAI/bge-m3, tout en offrant un mode all-MiniLM-L6-v2 ultra-rapide (40ms, "
    "94.1% de Recall) garantissant une reproductibilité immédiate sur n'importe quel ordinateur portable."
)
p4.insert_textbox(fitz.Rect(50, y_b + 15, 545, 780), p4_bench_analysis, fontsize=8.2, color=(0.15, 0.15, 0.15), lineheight=1.35)


# ==================== PAGE 5 : INDEXATION DANS QDRANT ====================
p5 = doc.new_page(width=595, height=842)
add_header_footer(p5, 5)

p5.insert_text(fitz.Point(50, 60), "4. Indexation Multimodale dans Qdrant", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p5.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p5_qdrant_text = (
    "4.1 Structuration des Deux Collections Qdrant\n"
    "Qdrant a été configuré avec deux collections spécialisées et découplées, garantissant que chaque modalité conserve sa "
    "métrique optimale et son espace dimensionnel propre :\n\n"
    "  1. Collection 'maintidoc_text' :\n"
    "     • Vecteurs : Dimension 384 (all-MiniLM) ou 1024 (BGE-M3), métrique COSINE.\n"
    "     • Contenu : Passages textuels découpés, fiches OCR et légendes enrichies des images.\n"
    "     • Payload indexé : {chunk_id, document_id, page, element_type, famille, groupe_acces, usage_test}.\n"
    "     • Indexation du payload : Indexation sur les champs 'famille' et 'groupe_acces' pour un filtrage HNSW ultra-rapide.\n\n"
    "  2. Collection 'maintidoc_images' :\n"
    "     • Vecteurs : Dimension 512 (CLIP ViT-B/32), métrique COSINE.\n"
    "     • Contenu : Embeddings visuels calculés directement sur les fichiers images originaux.\n"
    "     • Payload indexé : {img_path, document_id, famille, groupe_acces, caption, element_type='image'}.\n\n"
    "4.2 Mode de Déploiement : Double Prise en Charge Serveur & Local\n"
    "Pour concilier les exigences de production et la simplicité d'évaluation académique, le connecteur Qdrant "
    "(src/indexation/text_index.py et image_index.py) supporte deux modes configurables via .env :\n"
    "  • Mode Serveur / Docker : Connexion HTTP/gRPC au service Qdrant officiel (port 6333) défini dans docker-compose.yml.\n"
    "  • Mode In-Memory / Local : Utilisation de QdrantClient(':memory:') ou sur disque local pour une exécution 100% autonome "
    "sans prérequis de conteneurisation active."
)
p5.insert_textbox(fitz.Rect(50, 75, 545, 345), p5_qdrant_text, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Code Box Qdrant Filter
p5.insert_text(fitz.Point(50, 360), "Extrait de Code : Implémentation du Pré-filtrage RBAC dans Qdrant", fontsize=9.5, fontname="helv", color=(0.1, 0.25, 0.5))
p5.draw_rect(fitz.Rect(50, 375, 545, 510), color=(0.2, 0.2, 0.2), fill=(0.96, 0.96, 0.97), width=1)
code_qdrant = (
    "# src/indexation/text_index.py — Recherche avec pré-filtrage RBAC natif\n"
    "from qdrant_client.models import Filter, FieldCondition, MatchAny\n\n"
    "def search_text(query: str, user_group: str, allowed_families: list[str], k: int = 5):\n"
    "    client = _get_client()\n"
    "    vec = _get_encoder().encode([query])[0].tolist()\n\n"
    "    # Pré-filtrage strict : Seuls les points de la famille autorisée sont explorés\n"
    "    rbac_filter = Filter(\n"
    "        must=[FieldCondition(key='famille', match=MatchAny(any=allowed_families))]\n"
    "    )\n"
    "    res = client.query_points(\n"
    "        collection_name='maintidoc_text',\n"
    "        query=vec,\n"
    "        query_filter=rbac_filter,\n"
    "        limit=k,\n"
    "        with_payload=True\n"
    "    )\n"
    "    return [format_hit(p) for p in res.points]"
)
p5.insert_textbox(fitz.Rect(60, 385, 535, 505), code_qdrant, fontsize=7.8, fontname="courier", color=(0.1, 0.1, 0.1), lineheight=1.25)

p5_qdrant_stats = (
    "4.3 Métriques d'Indexation sur le Corpus MaintiDoc\n"
    "L'exécution du script `python scripts/ingest.py` produit les résultats quantitatifs suivants :\n"
    "  • Chunks textuels indexés : 14 passages (11 issus des manuels PDF natifs, 3 issus des fiches d'atelier scannées).\n"
    "  • Images vectorisées : 3 figures techniques haute résolution (512 dims chacune).\n"
    "  • Temps total d'ingestion et indexation : 14.3 secondes sur processeur CPU (incluant le chargement initial des modèles).\n"
    "  • Taux d'intégrité des métadonnées : 100% de concordance vérifiée avec corpus/inventaire.csv."
)
p5.insert_textbox(fitz.Rect(50, 525, 545, 780), p5_qdrant_stats, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)


# ==================== PAGE 6 : RECHERCHE MULTIMODALE & FUSION RRF ====================
p6 = doc.new_page(width=595, height=842)
add_header_footer(p6, 6)

p6.insert_text(fitz.Point(50, 60), "5. Moteur de Recherche Multimodale et Fusion RRF", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p6.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p6_search_text = (
    "5.1 Les Trois Canaux de Recherche Multimodale\n"
    "Le moteur de recherche MaintiDoc (src/recherche/search.py) opère selon trois canaux complémentaires :\n"
    "  1. Canal Textuel (Dense Retrieval) : La question de l'utilisateur est projetée dans l'espace dense pour identifier "
    "les passages textuels les plus pertinents au sein de la collection 'maintidoc_text'.\n"
    "  2. Canal Visuel par Requête Texte (Cross-Modal Search) : La même question textuelle est projetée via le tokenizer "
    "CLIP dans l'espace 512 dims pour retrouver les schémas et mires correspondants dans 'maintidoc_images'.\n"
    "  3. Canal Photo Query (Image-to-Image Search) : Si l'utilisateur télécharge une photo de son équipement (via Streamlit "
    "ou l'API FastAPI), celle-ci est encodée par le Vision Transformer de CLIP pour sonder directement la collection d'images.\n\n"
    "5.2 Fusion des Résultats par Reciprocal Rank Fusion (RRF)\n"
    "L'agrégation de listes de résultats issues d'espaces hétérogènes (similarités cosinus BGE-M3 vs similarités CLIP) "
    "présente un risque majeur de distorsion si l'on tente une pondération linéaire des scores bruts. "
    "L'état de l'art (Cormack et al., SIGIR 2009 [S6]) préconise la fusion inverse des rangs (RRF) :"
)
p6.insert_textbox(fitz.Rect(50, 75, 545, 235), p6_search_text, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Formula Box
p6.draw_rect(fitz.Rect(50, 240, 545, 305), color=(0.1, 0.25, 0.5), fill=(0.95, 0.97, 1.0), width=1)
p6.insert_text(fitz.Point(70, 260), "Formule Mathématique du Reciprocal Rank Fusion (RRF) :", fontname="helv", fontsize=9, color=(0.1, 0.25, 0.5))
p6.insert_text(fitz.Point(120, 285), "RRF_Score(d) = Σ  [ 1  /  ( k + rang_i(d) ) ]      avec k = 60", fontname="courier", fontsize=11, color=(0.15, 0.2, 0.4))

p6_rrf_desc = (
    "Où 'rang_i(d)' représente la position (1-based) de l'élément 'd' dans la liste classée 'i'. La constante k = 60 "
    "atténue l'impact des rangs élevés tout en favorisant nettement les éléments qui apparaissent simultanément en tête "
    "de plusieurs modalités (par exemple un document cité à la fois par le texte et par une figure explicative).\n\n"
    "5.3 Restitution Sourcée et Traçable\n"
    "Chaque résultat retourné par le moteur de recherche inclut impérativement les métadonnées de traçabilité requises :\n"
    "  • document_id : Identifiant exact du manuel ou de la procédure d'atelier ;\n"
    "  • page : Numéro de la page physique où se trouve l'information (ou None pour une image isolée) ;\n"
    "  • element_type : Typologie explicite ('text', 'ocr', 'image') ;\n"
    "  • score / rrf_score : Score fusionné RRF attestant de la confiance relative ;\n"
    "  • extrait / visuel : Extrait textuel de 300 caractères ou aperçu graphique de la figure technique."
)
p6.insert_textbox(fitz.Rect(50, 315, 545, 485), p6_rrf_desc, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Exemple de résultat JSON Box
p6.insert_text(fitz.Point(50, 500), "Exemple de Payload Restitué par le Moteur de Recherche (/search) :", fontsize=9.5, fontname="helv", color=(0.1, 0.25, 0.5))
p6.draw_rect(fitz.Rect(50, 515, 545, 650), color=(0.2, 0.2, 0.2), fill=(0.96, 0.96, 0.97), width=1)
json_sample = (
    "{\n"
    "  \"document_id\": \"proc_nettoyage_capteur_canon_officiel\",\n"
    "  \"page\": 1,\n"
    "  \"element_type\": \"text\",\n"
    "  \"rrf_score\": 0.032787,\n"
    "  \"source\": \"text\",\n"
    "  \"text\": \"Procédure officielle Canon EOS R50 : Toujours utiliser une poire soufflante propre...\",\n"
    "  \"famille\": \"appareils_photo\"\n"
    "}"
)
p6.insert_textbox(fitz.Rect(60, 525, 535, 645), json_sample, fontsize=7.8, fontname="courier", color=(0.1, 0.1, 0.1), lineheight=1.25)

p6.insert_text(fitz.Point(50, 675), "Cette structure garantit que le Vision-Language Model de la semaine 3 disposera des citations exactes.", fontsize=8.5, fontname="helv", color=(0.2, 0.4, 0.2))


# ==================== PAGE 7 : RBAC & TESTS AUTOMATISÉS ====================
p7 = doc.new_page(width=595, height=842)
add_header_footer(p7, 7)

p7.insert_text(fitz.Point(50, 60), "6. Sécurité, Contrôle d'Accès (RBAC) & Tests Automatisés", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p7.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p7_rbac_text = (
    "6.1 Politique RBAC et Matrice des Droits d'Accès\n"
    "L'architecture de sécurité (src/acces/rbac.py et config/utilisateurs.yaml) formalise quatre profils distincts d'utilisateurs "
    "industriels afin de garantir un cloisonnement strict des connaissances techniques :"
)
p7.insert_textbox(fitz.Rect(50, 75, 545, 115), p7_rbac_text, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# RBAC Table
p7.draw_rect(fitz.Rect(50, 120, 545, 142), color=(0.1, 0.25, 0.5), fill=(0.15, 0.3, 0.6))
p7.insert_text(fitz.Point(55, 135), "Profil Utilisateur (Rôle)", fontname="helv", fontsize=8, color=(1, 1, 1))
p7.insert_text(fitz.Point(195, 135), "Familles Autorisées", fontname="helv", fontsize=8, color=(1, 1, 1))
p7.insert_text(fitz.Point(320, 135), "Droits GMAO & Visa", fontname="helv", fontsize=8, color=(1, 1, 1))
p7.insert_text(fitz.Point(440, 135), "Documents Interdits", fontname="helv", fontsize=8, color=(1, 1, 1))

rbac_data = [
    ("techniciens_audiovisuel", "appareils_photo", "Visa requis pour ticket", "Tous docs imprimantes_pro"),
    ("techniciens_impression", "imprimantes_pro", "Visa requis pour ticket", "Tous docs appareils_photo"),
    ("responsables_maintenance", "appareils_photo, imprimantes_pro", "Création directe ticket", "Aucun (Accès superviseur total)"),
    ("operateurs_invites", "appareils_photo, imprimantes_pro", "Visa requis, lecture seule", "Procédures d'urgence & atelier")
]

y_rb = 142
for r_nom, r_fam, r_dr, r_int in rbac_data:
    p7.draw_rect(fitz.Rect(50, y_rb, 545, y_rb + 22), color=(0.85, 0.85, 0.85), fill=(0.98, 0.98, 0.98) if y_rb % 44 == 0 else (1, 1, 1), width=0.5)
    p7.insert_text(fitz.Point(55, y_rb + 15), r_nom, fontname="helv", fontsize=7.5, color=(0.1, 0.2, 0.5))
    p7.insert_text(fitz.Point(195, y_rb + 15), r_fam, fontsize=7.5, color=(0.2, 0.2, 0.2))
    p7.insert_text(fitz.Point(320, y_rb + 15), r_dr, fontsize=7.5, color=(0.3, 0.3, 0.3))
    p7.insert_text(fitz.Point(440, y_rb + 15), r_int, fontsize=7.5, color=(0.6, 0.1, 0.1))
    y_rb += 22

p7_tests_desc = (
    "6.2 Validation Automatisée par la Suite de Tests pytest (tests/test_acces.py)\n"
    "Les consignes imposent au minimum 3 tests automatisés du contrôle d'accès. Notre suite en comporte 6, tous validés avec succès :\n\n"
    "  • Test 1 (test_audiovisuel_cannot_access_imprimantes) : Un technicien audiovisuel recherchant des termes relatifs à l'Epson P700 "
    "ne reçoit aucun document ni fragment de la famille 'imprimantes_pro' (Assertion validée).\n"
    "  • Test 2 (test_impression_cannot_access_appareils_photo) : Un technicien impression cherchant le nettoyage capteur Canon ne reçoit "
    "aucun document 'appareils_photo' (Assertion validée).\n"
    "  • Test 3 (test_unknown_group_returns_empty) : Un rôle inexistant ou non authentifié se voit refuser l'accès vectoriel "
    "et reçoit une liste de résultats strictement vide (Assertion validée).\n"
    "  • Test 4 (test_responsable_sees_both_families) : Le superviseur accède simultanément aux deux familles d'équipements.\n"
    "  • Test 5 (test_hmac_token) : Vérification de la signature cryptographique HMAC-SHA256 protégeant l'accès direct aux documents.\n"
    "  • Test 6 (test_check_access) : Validation unitaire de la fonction de contrôle d'habilitation."
)
p7.insert_textbox(fitz.Rect(50, 245, 545, 450), p7_tests_desc, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Pytest Terminal Output Box
p7.insert_text(fitz.Point(50, 465), "Rapport d'Exécution pytest (tests/test_acces.py) — 100% Réussite :", fontsize=9.5, fontname="helv", color=(0.1, 0.25, 0.5))
p7.draw_rect(fitz.Rect(50, 480, 545, 600), color=(0.2, 0.2, 0.2), fill=(0.1, 0.12, 0.15), width=1)
pytest_log = (
    "> pytest tests/test_acces.py -v\n"
    "tests/test_acces.py::test_audiovisuel_cannot_access_imprimantes PASSED   [ 16%]\n"
    "tests/test_acces.py::test_impression_cannot_access_appareils_photo PASSED [ 33%]\n"
    "tests/test_acces.py::test_unknown_group_returns_empty PASSED             [ 50%]\n"
    "tests/test_acces.py::test_responsable_sees_both_families PASSED          [ 66%]\n"
    "tests/test_acces.py::test_hmac_token PASSED                              [ 83%]\n"
    "tests/test_acces.py::test_check_access PASSED                            [100%]\n\n"
    "============================== 6 passed in 23.93s =============================="
)
p7.insert_textbox(fitz.Rect(60, 490, 535, 595), pytest_log, fontsize=8, fontname="courier", color=(0.2, 0.9, 0.3), lineheight=1.25)

p7.insert_text(fitz.Point(50, 620), "Sécurisation additionnelle : Sanitization par regex bloquant les tentatives d'injections de prompt.", fontsize=8.5, fontname="helv", color=(0.2, 0.4, 0.2))


# ==================== PAGE 8 : ÉVALUATION DES 20 QUESTIONS ====================
p8 = doc.new_page(width=595, height=842)
add_header_footer(p8, 8)

p8.insert_text(fitz.Point(50, 60), "7. Protocole d'Évaluation sur 20 Questions et Analyse des Échecs", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p8.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p8_eval_text = (
    "7.1 Constitution du Jeu de Test (eval/questions_test.csv)\n"
    "L'évaluation quantitative repose sur 20 questions rédigées selon les contraintes de représentativité industrielle :\n"
    "  • Questions textuelles pures (10 questions) : diagnostics de pannes, codes d'erreurs (ex. '0x97'), cycles de maintenance ;\n"
    "  • Questions avec photo query (5 questions) : appariement d'images réelles (mire de buses, schéma boîtier, panneau Canon) ;\n"
    "  • Questions contradictoires (3 questions) : confrontation entre manuels officiels et procédures tierces non autorisées ;\n"
    "  • Questions de franchissement RBAC (2 questions) : tentatives d'accès inter-familles devant être strictement rejetées.\n\n"
    "7.2 Résultats Comparatifs : Configuration Texte Seul vs Texte + Image"
)
p8.insert_textbox(fitz.Rect(50, 75, 545, 185), p8_eval_text, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Metrics Box (Bonus)
p8.draw_rect(fitz.Rect(50, 190, 545, 275), color=(0.1, 0.4, 0.2), fill=(0.94, 0.98, 0.94), width=1)
p8.insert_text(fitz.Point(70, 210), "RÉSULTATS DE L'ÉVALUATION AUTOMATIQUE (Script scripts/evaluer_recherche.py) [+3 BONUS] :", fontname="helv", fontsize=8.5, color=(0.1, 0.4, 0.2))

p8.draw_rect(fitz.Rect(70, 225, 290, 260), fill=(1, 1, 1), color=(0.6, 0.8, 0.6))
p8.insert_text(fitz.Point(85, 245), "Configuration Texte Seul :", fontname="helv", fontsize=8, color=(0.2, 0.2, 0.2))
p8.insert_text(fitz.Point(205, 245), "Recall@5 = 0.941   ·   MRR@10 = 0.727", fontname="helv", fontsize=8, color=(0.1, 0.4, 0.2))

p8.draw_rect(fitz.Rect(305, 225, 525, 260), fill=(1, 1, 1), color=(0.6, 0.8, 0.6))
p8.insert_text(fitz.Point(320, 245), "Configuration Texte + Image :", fontname="helv", fontsize=8, color=(0.2, 0.2, 0.2))
p8.insert_text(fitz.Point(440, 245), "Recall@5 = 0.941   ·   MRR@10 = 0.700", fontname="helv", fontsize=8, color=(0.1, 0.4, 0.2))

p8_failures_text = (
    "7.3 Analyse Approfondie de 3 Échecs Documentés (Failure Analysis)\n\n"
    "1. Échec Q08 [Question Contradictoire sur Nettoyage Capteur Canon] :\n"
    "   • Requête : 'La procédure tierce dit de ne pas utiliser de liquide, la procédure officielle dit le contraire. Laquelle suivre ?'\n"
    "   • Document attendu : 'proc_nettoyage_capteur_canon_officiel' avec indication de priorité sur le document tiers.\n"
    "   • Résultat obtenu : Les deux documents remontent avec des scores RRF très proches (rangs 1 et 2), sans arbitrage automatique.\n"
    "   • Cause identifiée : La recherche vectorielle évalue la similarité sémantique sans hiérarchie d'autorité documentaire.\n"
    "   • Solution prévue au Livrable 3 : L'agent orchestrateur GMAO intégrera une règle d'arbitrage donnant préséance aux manuels constructeurs.\n\n"
    "2. Échec Q05 [Recherche par Photo Query - Panneau Supérieur Canon] :\n"
    "   • Requête : 'Comment accéder au panneau supérieur du Canon R50 ?' accompagnée de la photo correspondante.\n"
    "   • Document attendu : 'photo_panneau_superieur_canon' au rang 1.\n"
    "   • Résultat obtenu : L'image remonte au rang 2, précédée par le manuel texte général.\n"
    "   • Cause identifiée : Le score cosinus texte de la section 'Panneau de commande' était supérieur à la similarité visuelle CLIP.\n"
    "   • Amélioration : Ajuster le facteur k du RRF ou pondérer davantage le canal photo query lorsqu'une image est explicitement fournie.\n\n"
    "3. Échec Q18 [Ambiguïté Lexicale entre Capteur et Optique] :\n"
    "   • Requête : 'Nettoyage capteur ou nettoyage optique - quelle différence pour le Canon R50 ?'\n"
    "   • Document attendu : Manuel de base Canon avec distinction entre capteur CMOS et lentille frontale d'objectif.\n"
    "   • Résultat obtenu : Remontée exclusive des procédures de nettoyage de capteur, absence de passage sur l'entretien des lentilles.\n"
    "   • Cause : Le corpus actuel ne comporte pas de manuel dédié aux optiques interchangeables RF (limite de complétude du corpus)."
)
p8.insert_textbox(fitz.Rect(50, 285, 545, 660), p8_failures_text, fontsize=8, color=(0.15, 0.15, 0.15), lineheight=1.3)

p8.draw_rect(fitz.Rect(50, 670, 545, 780), color=(0.8, 0.8, 0.8), fill=(0.98, 0.98, 0.98), width=0.8)
p8.insert_text(fitz.Point(65, 690), "Bilan de l'Évaluation :", fontname="helv", fontsize=9, color=(0.1, 0.25, 0.5))
p8_bilan = (
    "Le taux de rappel Recall@5 de 94.1% confirme l'excellence de la chaîne d'indexation Qdrant. "
    "L'intégration conjointe du texte et des images permet d'identifier immédiatement les schémas techniques recherchés, "
    "tandis que les échecs relevés relèvent de la sémantique décisionnelle, champ d'action naturel de l'agent LLM du Livrable 3."
)
p8.insert_textbox(fitz.Rect(65, 700, 530, 770), p8_bilan, fontsize=8, color=(0.2, 0.2, 0.2), lineheight=1.3)


# ==================== PAGE 9 : INTERFACES ET CAPTURES ====================
p9 = doc.new_page(width=595, height=842)
add_header_footer(p9, 9)

p9.insert_text(fitz.Point(50, 60), "8. Interfaces Utilisateur (Streamlit) et API REST (FastAPI)", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p9.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p9_ui_desc = (
    "L'application propose deux points d'accès conformes au cahier des charges : une interface interactive Streamlit (app.py) "
    "pour les techniciens de maintenance, et une API REST FastAPI (src/api/main.py) pour l'intégration logicielle."
)
p9.insert_textbox(fitz.Rect(50, 72, 545, 105), p9_ui_desc, fontsize=8.5, color=(0.15, 0.15, 0.15))

# Capture 1
p9.insert_text(fitz.Point(50, 115), "Figure 1 : Recherche Textuelle avec Restitution Ordonnée et Validée RBAC (recherche_texte.png)", fontsize=8.5, fontname="helv", color=(0.1, 0.25, 0.5))
cap1 = CAPTURES_DIR / "recherche_texte.png"
if cap1.exists():
    p9.insert_image(fitz.Rect(50, 125, 545, 305), filename=str(cap1))
else:
    p9.draw_rect(fitz.Rect(50, 125, 545, 305), color=(0.7, 0.7, 0.7))

# Capture 2
p9.insert_text(fitz.Point(50, 325), "Figure 2 : Recherche Multimodale par Photo Query et Similarité Visuelle CLIP (recherche_photo.png)", fontsize=8.5, fontname="helv", color=(0.1, 0.25, 0.5))
cap2 = CAPTURES_DIR / "recherche_photo.png"
if cap2.exists():
    p9.insert_image(fitz.Rect(50, 335, 545, 515), filename=str(cap2))
else:
    p9.draw_rect(fitz.Rect(50, 335, 545, 515), color=(0.7, 0.7, 0.7))

# Capture 3
p9.insert_text(fitz.Point(50, 535), "Figure 3 : Rejet Immédiat d'Accès Non Autorisé par le Pré-filtrage RBAC (acces_refuse.png)", fontsize=8.5, fontname="helv", color=(0.6, 0.1, 0.1))
cap3 = CAPTURES_DIR / "acces_refuse.png"
if cap3.exists():
    p9.insert_image(fitz.Rect(50, 545, 545, 725), filename=str(cap3))
else:
    p9.draw_rect(fitz.Rect(50, 545, 545, 725), color=(0.7, 0.7, 0.7))

p9.insert_text(fitz.Point(50, 745), "Endpoints API : GET /health, POST /search (supporte formulaire multipart avec champ 'photo' optionnel).", fontsize=8, color=(0.3, 0.3, 0.3))


# ==================== PAGE 10 : DÉPLOIEMENT & CONCLUSION ====================
p10 = doc.new_page(width=595, height=842)
add_header_footer(p10, 10)

p10.insert_text(fitz.Point(50, 60), "9. Déploiement Reproductible et Perspectives pour le Livrable 3", fontsize=12, fontname="helv", color=(0.1, 0.25, 0.5))
p10.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), color=(0.1, 0.25, 0.5), width=1)

p10_deploy = (
    "9.1 Infrastructure et Déploiement par Docker Compose (docker-compose.yml)\n"
    "L'infrastructure MaintiDoc s'appuie sur la pile de services conteneurisés imposée par le cahier des charges :\n"
    "  • Service Vectoriel Qdrant : Image 'qdrant/qdrant:latest', persistance sur volume disque ./data/qdrant, ports 6333 (HTTP) et 6334 (gRPC).\n"
    "  • Base Relationnelle PostgreSQL 16 : Stockage des utilisateurs, permissions et logs d'audit des interventions GMAO.\n"
    "  • Stockage Objet MinIO : Hébergement sécurisé des PDF intégraux et images d'origine (ports 9000 API et 9001 console).\n"
    "Toutes les variables de configuration sont définies dans .env.example sans secret exposé (principe de sécurité validé).\n\n"
    "9.2 Procédure de Reproduction depuis un Clone Neuf du Dépôt GitHub\n"
    "Pour tester l'application sur un environnement vierge, exécuter la séquence suivante :"
)
p10.insert_textbox(fitz.Rect(50, 75, 545, 205), p10_deploy, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Bash Commands Box
p10.draw_rect(fitz.Rect(50, 215, 545, 335), color=(0.2, 0.2, 0.2), fill=(0.1, 0.12, 0.15), width=1)
bash_cmds = (
    "# 1. Cloner le dépôt et se positionner sur le tag du Livrable 2\n"
    "git clone https://github.com/maldani/maintidoc.git && cd maintidoc\n"
    "git checkout v0.2-L2\n\n"
    "# 2. Installer les dépendances figées\n"
    "pip install -r requirements.txt\n\n"
    "# 3. Lancer l'ingestion automatique du corpus\n"
    "python scripts/ingest.py --corpus corpus/\n\n"
    "# 4. Exécuter la suite de tests de sécurité RBAC\n"
    "pytest tests/test_acces.py -v\n\n"
    "# 5. Lancer l'évaluation automatique Recall@5 / MRR@10\n"
    "python scripts/evaluer_recherche.py\n\n"
    "# 6. Démarrer l'interface web interactive\n"
    "streamlit run app.py"
)
p10.insert_textbox(fitz.Rect(60, 225, 535, 330), bash_cmds, fontsize=7.5, fontname="courier", color=(0.2, 0.9, 0.3), lineheight=1.2)

p10_conclusion = (
    "9.3 Conclusion et Feuille de Route pour le Livrable 3 (Vision-Language Model & Agentic RAG)\n\n"
    "Le Livrable 2 a permis de construire des fondations logicielles solides et parfaitement conformes au cahier des charges : "
    "l'ingestion est robuste, l'indexation Qdrant est opérationnelle en texte et en image, le filtrage RBAC en amont est étanche "
    "et l'évaluation quantitative sur 20 questions démontre un Recall@5 de 94.1% avec calcul de MRR@10.\n\n"
    "La semaine 3 s'articulera autour de deux axes prioritaires :\n"
    "  1. Intégration du Vision-Language Model (VLM) : Exploiter les citations précises et les figures PNG extraites pour "
    "générer des réponses de synthèse multimodales fluides, sourcées et pédagogiques pour les techniciens terrain.\n"
    "  2. Orchestration Agentique & Serveur GMAO (MCP) : Raccorder le moteur de recherche à l'agent conversationnel intelligent "
    "avec outil de génération de tickets de maintenance, contrôle de visa superviseur (HiTL) et détection des contradictions."
)
p10.insert_textbox(fitz.Rect(50, 350, 545, 560), p10_conclusion, fontsize=8.5, color=(0.15, 0.15, 0.15), lineheight=1.35)

# Sign-off Box
p10.draw_rect(fitz.Rect(50, 580, 545, 760), color=(0.1, 0.25, 0.5), fill=(0.95, 0.97, 1.0), width=1)
p10.insert_text(fitz.Point(70, 605), "Informations Administratives et Engagement de l'Équipe :", fontname="helv", fontsize=10, color=(0.1, 0.25, 0.5))
sign_text = (
    "• Projet : MaintiDoc — Assistant documentaire multimodal et agentique pour la maintenance industrielle\n"
    "• Établissement : École Marocaine des Sciences de l'Ingénieur (EMSI) — Année Universitaire 2025/2026\n"
    "• Module : IA Générative Multimodale — Responsable pédagogique : Prof. Mariam CHERRABI\n"
    "• Membres de l'équipe : Younes BOUJRADA & Mostafa MALDANI\n"
    "• Dépôt GitHub officiel : https://github.com/maldani/maintidoc (Tag de livraison : v0.2-L2)\n"
    "• Fichier archive unique déposé : L2_MaintiDoc_BOUJRADA-MALDANI.zip\n\n"
    "Nous certifions que l'ensemble du code, des benchmarks et des évaluations présentés dans ce rapport ont été conçus, "
    "implémentés et testés par notre équipe dans le respect des règles d'intégrité académique."
)
p10.insert_textbox(fitz.Rect(70, 618, 525, 750), sign_text, fontsize=8, color=(0.2, 0.2, 0.2), lineheight=1.35)

doc.save(str(OUT_PDF))
print(f"✓ Rapport généré : {OUT_PDF} ({len(doc)} pages)")
