"""
Générateur du Rapport Officiel PDF Haute Définition : MaintiDoc
Construit un rapport paginé au format standard A4 (595 x 842 pt)
avec PyMuPDF, intégrant toutes les captures d'écran, diagrammes,
tableaux, cartouches de conformité, en-têtes et numérotation de page.
"""

import os
import pymupdf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
DIAG_DIR = os.path.join(BASE_DIR, "..", "..", "docs", "diagrammes")
OUTPUT_PDF = os.path.join(BASE_DIR, "Rapport_MaintiDoc_RAG_Multimodal_Agentique.pdf")
ROOT_OUTPUT_PDF = os.path.join(BASE_DIR, "..", "..", "Rapport_MaintiDoc_RAG_Multimodal_Agentique.pdf")

W_A4, H_A4 = 595.3, 841.9  # Standard A4 points

C_NAVY = (13/255, 35/255, 58/255)
C_BLUE = (13/255, 71/255, 161/255)
C_RED = (255/255, 75/255, 75/255)
C_DARK = (38/255, 39/255, 48/255)
C_MUTED = (108/255, 117/255, 125/255)
C_LIGHT_BG = (248/255, 249/255, 251/255)
C_BORDER = (220/255, 224/255, 230/255)
C_GREEN = (27/255, 94/255, 32/255)


def add_header_footer(page, page_num, total_pages):
    if page_num == 1:
        return  # No header/footer on cover
    
    # Header
    page.draw_line(pymupdf.Point(36, 36), pymupdf.Point(W_A4 - 36, 36), color=C_BORDER, width=0.6)
    page.insert_text(
        pymupdf.Point(36, 28),
        "MAINTIDOC — ASSISTANT MULTIMODAL & AGENTIQUE",
        fontsize=7.5,
        color=C_BLUE,
        fontname="helv"
    )
    page.insert_text(
        pymupdf.Point(W_A4 - 230, 28),
        "RAPPORT TECHNIQUE & VALIDATION",
        fontsize=7.5,
        color=C_MUTED,
        fontname="helv"
    )

    # Footer
    page.draw_line(pymupdf.Point(36, H_A4 - 36), pymupdf.Point(W_A4 - 36, H_A4 - 36), color=C_BORDER, width=0.6)
    page.insert_text(
        pymupdf.Point(36, H_A4 - 24),
        "EMSI 2026 — Module IA Générative Multimodale | Équipe MALDANI & BOUJRADA",
        fontsize=7.5,
        color=C_MUTED,
        fontname="helv"
    )
    page_str = f"Page {page_num} sur {total_pages}"
    page.insert_text(
        pymupdf.Point(W_A4 - 95, H_A4 - 24),
        page_str,
        fontsize=7.5,
        color=C_BLUE,
        fontname="helv"
    )


def create_report():
    doc = pymupdf.open()

    # =========================================================
    # PAGE 1 : COUVERTURE
    # =========================================================
    p1 = doc.new_page(width=W_A4, height=H_A4)
    
    # Top decorative bar
    p1.draw_rect(pymupdf.Rect(0, 0, W_A4, 8), fill=C_RED, color=None)

    # Institution
    p1.insert_text(pymupdf.Point(40, 65), "ÉCOLE MAROCAINE DES SCIENCES DE L'INGÉNIEUR", fontsize=13, fontname="hebo", color=C_NAVY)
    p1.insert_text(pymupdf.Point(40, 83), "Mastère 2 / 5ème Année — Filière Ingénierie Informatique & Intelligence Artificielle", fontsize=9.5, fontname="helv", color=C_MUTED)
    p1.insert_text(pymupdf.Point(40, 97), "Module : IA Générative Multimodale — Année Académique 2026", fontsize=9.5, fontname="helv", color=C_MUTED)

    p1.draw_line(pymupdf.Point(40, 115), pymupdf.Point(W_A4 - 40, 115), color=C_BORDER, width=1)

    # Title
    p1.insert_text(pymupdf.Point(40, 175), "MAINTIDOC", fontsize=34, fontname="hebo", color=C_RED)
    p1.insert_text(pymupdf.Point(40, 208), "Assistant Documentaire Multimodal et Agentique", fontsize=17, fontname="hebo", color=C_NAVY)
    p1.insert_text(pymupdf.Point(40, 230), "pour la Maintenance Industrielle & Atelier", fontsize=17, fontname="hebo", color=C_NAVY)

    # Subtitle
    sub1 = "Rapport Technique d'Implémentation, Sécurité RBAC, Protocole MCP GMAO,"
    sub2 = "Boucle Human-in-the-Loop et Validation Expérimentale Illustrée"
    p1.insert_text(pymupdf.Point(40, 265), sub1, fontsize=10.5, fontname="heit", color=C_MUTED)
    p1.insert_text(pymupdf.Point(40, 280), sub2, fontsize=10.5, fontname="heit", color=C_MUTED)

    # Decorative Card: Project metadata
    p1.draw_rect(pymupdf.Rect(40, 315, W_A4 - 40, 560), fill=C_LIGHT_BG, color=C_BORDER, width=1)

    # Left Column: Team
    p1.insert_text(pymupdf.Point(60, 345), "👨‍💻 ÉQUIPE PROJET (BINÔME)", fontsize=11, fontname="hebo", color=C_BLUE)
    p1.insert_text(pymupdf.Point(60, 370), "• Mostafa MALDANI", fontsize=10, fontname="hebo", color=C_DARK)
    p1.insert_text(pymupdf.Point(70, 386), "Ingénierie & Data Science / Architecture RAG", fontsize=8.5, fontname="helv", color=C_MUTED)
    p1.insert_text(pymupdf.Point(70, 400), "maldanirachid2016@gmail.com", fontsize=8.5, fontname="courier", color=C_DARK)

    p1.insert_text(pymupdf.Point(60, 425), "• Younes BOUJRADA", fontsize=10, fontname="hebo", color=C_DARK)
    p1.insert_text(pymupdf.Point(70, 441), "Systèmes Agentiques, MCP & Vision-Language Models", fontsize=8.5, fontname="helv", color=C_MUTED)
    p1.insert_text(pymupdf.Point(70, 455), "boujrada.younes@emsi.ma", fontsize=8.5, fontname="courier", color=C_DARK)

    # Right Column: Supervision
    p1.insert_text(pymupdf.Point(320, 345), "🎓 ENCADREMENT PÉDAGOGIQUE", fontsize=11, fontname="hebo", color=C_BLUE)
    p1.insert_text(pymupdf.Point(320, 370), "• Prof. Mariam CHERRABI", fontsize=10, fontname="hebo", color=C_DARK)
    p1.insert_text(pymupdf.Point(330, 386), "Enseignante-Chercheuse en IA Générative", fontsize=8.5, fontname="helv", color=C_MUTED)
    p1.insert_text(pymupdf.Point(330, 400), "EMSI Casablanca", fontsize=8.5, fontname="helv", color=C_MUTED)

    p1.insert_text(pymupdf.Point(320, 425), "📅 DATE DE FINALISATION", fontsize=10, fontname="hebo", color=C_BLUE)
    p1.insert_text(pymupdf.Point(330, 441), "Novembre 2026 — Session Officielle", fontsize=8.5, fontname="helv", color=C_DARK)

    # Equipment Badges
    p1.draw_line(pymupdf.Point(60, 475), pymupdf.Point(W_A4 - 60, 475), color=C_BORDER, width=0.8)
    p1.insert_text(pymupdf.Point(60, 498), "ÉQUIPEMENTS COUVERTS PAR LE CORPUS :", fontsize=9.5, fontname="hebo", color=C_NAVY)
    
    p1.insert_text(pymupdf.Point(60, 520), "📷 Famille 1 : Canon EOS R50 (Hybride APS-C, monture RF, batterie LP-E17, alerte surchauffe)", fontsize=8.5, fontname="helv", color=C_DARK)
    p1.insert_text(pymupdf.Point(60, 538), "🖨️ Famille 2 : Epson SureColor SC-P700 (Traceur art pro, encres UltraChrome, code 1485, boîtier C12C935711)", fontsize=8.5, fontname="helv", color=C_DARK)

    # Bottom summary box
    p1.draw_rect(pymupdf.Rect(40, 580, W_A4 - 40, 780), fill=(235/255, 243/255, 255/255), color=(153/255, 193/255, 255/255), width=1)
    p1.insert_text(pymupdf.Point(60, 606), "🛡️ SYNTHÈSE DES 5 OBJECTIFS DE CONFORMITÉ INDUSTRIELLE ATTEINTS :", fontsize=9.5, fontname="hebo", color=C_BLUE)
    pts_cov = [
        "1. Sourcing Documentaire Exact : Citations rigoureuses (manuel officiel, page précise, figure associée).",
        "2. Contrôle d'Accès État de l'Art (RBAC) [C1, C2] : Pré-filtrage ChromaDB interdisant tout accès croisé.",
        "3. Boucle Human-in-the-Loop [Point C3] : Signature HMAC-SHA256 obligatoire avant toute écriture GMAO.",
        "4. Idempotence Réseau Stricte : Clé d'idempotence neutralisant les risques de doublons de tickets d'intervention.",
        "5. Confinement Anti-Jailbreak [R07 / S5] : Balisage XML étanche neutralisant les prompt injections d'atelier."
    ]
    y_c = 630
    for pt in pts_cov:
        p1.insert_text(pymupdf.Point(60, y_c), pt, fontsize=8.5, fontname="helv", color=C_DARK)
        y_c += 24

    # =========================================================
    # PAGE 2 : RÉSUMÉ EXÉCUTIF & ARCHITECTURE GLOBALE
    # =========================================================
    p2 = doc.new_page(width=W_A4, height=H_A4)
    p2.insert_text(pymupdf.Point(36, 60), "1. Résumé Exécutif & Architecture Découplée", fontsize=15, fontname="hebo", color=C_NAVY)

    p2.insert_text(
        pymupdf.Point(36, 85),
        "MaintiDoc est un assistant multimodal d'aide à la décision technique pour la maintenance d'équipements industriels.",
        fontsize=9, fontname="helv", color=C_DARK
    )
    p2.insert_text(
        pymupdf.Point(36, 100),
        "Il traite simultanément des requêtes textuelles d'opérateurs et des photographies de panneaux ou mires de test,",
        fontsize=9, fontname="helv", color=C_DARK
    )
    p2.insert_text(
        pymupdf.Point(36, 115),
        "en garantissant un sourcing constructeur exhaustif, un pré-filtrage RBAC et une suspension Human-in-the-Loop.",
        fontsize=9, fontname="helv", color=C_DARK
    )

    # Insert Architecture Diagram
    diag_path = os.path.join(DIAG_DIR, "diagramme_architecture_globale.png")
    if os.path.exists(diag_path):
        p2.insert_image(pymupdf.Rect(45, 135, W_A4 - 45, 410), filename=diag_path)
        p2.insert_text(
            pymupdf.Point(110, 425),
            "Figure 1.1 : Architecture Globale Découplée (RAG Multimodal, VectorStore, VLM Qwen2.5-VL et Serveur MCP GMAO)",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Table of Modules
    p2.insert_text(pymupdf.Point(36, 455), "Découpage Fonctionnel des Modules (rag_multimodal_agentique/maintidoc/src) :", fontsize=10, fontname="hebo", color=C_BLUE)

    modules = [
        ("src/config.py", "Rôles RBAC, constantes de sécurité et chemins des corpus."),
        ("src/models.py", "Modèles Pydantic stricts (MetadataIndex, Citation, TicketGMAO, AgentResponse)."),
        ("src/security.py", "Fonctions HMAC-SHA256 [C3], vérification RBAC [C1] et confinement XML [R07]."),
        ("src/embeddings.py", "Embeddings unifiés all-MiniLM-L6-v2 et descripteurs sémantiques visuels."),
        ("src/vector_store.py", "Base ChromaDB persistante avec pré-filtrage dur [Point C2] par groupe d'accès."),
        ("src/ingestion.py", "Extraction PyMuPDF, découpage sémantique, calcul SHA-256 et indexation."),
        ("src/mcp_server.py", "Serveur GMAO MCP : get_equipment_history et create_ticket avec clé d'idempotence."),
        ("src/agent.py", "Orchestrateur agentique avec gestion des cas d'usage et suspension Human-in-the-Loop."),
        ("app.py", "Interface interactive Streamlit avec simulation des profils et validation des visas.")
    ]

    p2.draw_rect(pymupdf.Rect(36, 470, W_A4 - 36, 785), fill=C_LIGHT_BG, color=C_BORDER, width=1)
    p2.draw_rect(pymupdf.Rect(36, 470, W_A4 - 36, 492), fill=(225/255, 230/255, 238/255), color=C_BORDER, width=1)
    p2.insert_text(pymupdf.Point(46, 485), "MODULE SOURCE", fontsize=8.5, fontname="hebo", color=C_NAVY)
    p2.insert_text(pymupdf.Point(180, 485), "RÔLE TECHNIQUE & RESPONSABILITÉ DANS MAINTIDOC", fontsize=8.5, fontname="hebo", color=C_NAVY)

    y_m = 512
    for mod_name, mod_desc in modules:
        p2.insert_text(pymupdf.Point(46, y_m), mod_name, fontsize=8, fontname="courier", color=C_BLUE)
        p2.insert_text(pymupdf.Point(180, y_m), mod_desc, fontsize=8, fontname="helv", color=C_DARK)
        p2.draw_line(pymupdf.Point(36, y_m + 8), pymupdf.Point(W_A4 - 36, y_m + 8), color=C_BORDER, width=0.5)
        y_m += 30

    # =========================================================
    # PAGE 3 : CADRE DE SÉCURITÉ & SCREENSHOT 1 (ACCUEIL)
    # =========================================================
    p3 = doc.new_page(width=W_A4, height=H_A4)
    p3.insert_text(pymupdf.Point(36, 60), "2. Cadre de Sécurité Industrielle & Interface Opérateur", fontsize=15, fontname="hebo", color=C_NAVY)

    p3.insert_text(pymupdf.Point(36, 85), "Quatre points de contrôle rigoureux garantissent la conformité industrielle du système :", fontsize=9, fontname="helv", color=C_DARK)
    p3.insert_text(pymupdf.Point(45, 103), "• [Point C1] RBAC : Permissions différenciées (techniciens_audiovisuel, techniciens_impression, superviseurs).", fontsize=8.5, fontname="helv", color=C_DARK)
    p3.insert_text(pymupdf.Point(45, 120), "• [Point C2] Pré-filtrage ChromaDB : Application du filtre where={'famille': autorisee} en amont du calcul de similarité.", fontsize=8.5, fontname="helv", color=C_DARK)
    p3.insert_text(pymupdf.Point(45, 137), "• [Point C3] Visa HMAC-SHA256 : Toute action en écriture (create_ticket) requiert un jeton cryptographique éphémère.", fontsize=8.5, fontname="helv", color=C_DARK)
    p3.insert_text(pymupdf.Point(45, 154), "• [R07 / S5] Neutralisation Injections : Confinement dans des balises <context_document> pour bloquer les jailbreaks.", fontsize=8.5, fontname="helv", color=C_DARK)

    # Insert Screenshot 1
    s1_path = os.path.join(SCREENSHOTS_DIR, "screenshot_01_interface_accueil.png")
    if os.path.exists(s1_path):
        p3.insert_image(pymupdf.Rect(40, 175, W_A4 - 40, 485), filename=s1_path)
        p3.insert_text(
            pymupdf.Point(85, 498),
            "Figure 2.1 : Interface d'accueil Streamlit avec barre latérale RBAC, points de contrôle actifs et cartes matérielles",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Insert Flow Diagram
    diag_flow = os.path.join(DIAG_DIR, "diagramme_flux_requete_agentique.png")
    if os.path.exists(diag_flow):
        p3.insert_image(pymupdf.Rect(50, 520, W_A4 - 50, 775), filename=diag_flow)
        p3.insert_text(
            pymupdf.Point(120, 790),
            "Figure 2.2 : Flux séquentiel de requête agentique avec point d'arrêt Human-in-the-Loop [Point C3]",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # =========================================================
    # PAGE 4 : CAS 1 (CANON R50) & CAS 2 (EPSON P700 CODE 1485)
    # =========================================================
    p4 = doc.new_page(width=W_A4, height=H_A4)
    p4.insert_text(pymupdf.Point(36, 60), "3. Démonstration des Cas d'Atelier (Cas 1 & Cas 2)", fontsize=15, fontname="hebo", color=C_NAVY)

    # Cas 1
    p4.insert_text(pymupdf.Point(36, 85), "3.1 Cas 1 : Diagnostic Visuel d'Alerte Thermique sur Canon EOS R50", fontsize=11, fontname="hebo", color=C_BLUE)
    p4.insert_text(pymupdf.Point(36, 102), "• Requête : Analyse de la photographie du panneau supérieur d'un Canon R50 présentant un voyant rouge clignotant.", fontsize=8.5, fontname="helv", color=C_DARK)
    p4.insert_text(pymupdf.Point(36, 117), "• Diagnostic & Sourcing : Alerte surchauffe détectée. Citation exacte : manuel_canon_r50_base.pdf, page 24, Fig. 4.2.", fontsize=8.5, fontname="helv", color=C_DARK)

    s2_path = os.path.join(SCREENSHOTS_DIR, "screenshot_02_cas1_canon_voyant.png")
    if os.path.exists(s2_path):
        p4.insert_image(pymupdf.Rect(40, 130, W_A4 - 40, 420), filename=s2_path)
        p4.insert_text(
            pymupdf.Point(90, 432),
            "Figure 3.1 : Cas 1 — Reconnaissance multimodale du voyant de surchauffe Canon R50 et citation sourcée p. 24",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Cas 2
    p4.insert_text(pymupdf.Point(36, 455), "3.2 Cas 2 : Résolution Guidée du Code Bloquant 1485 (Epson P700)", fontsize=11, fontname="hebo", color=C_BLUE)
    p4.insert_text(pymupdf.Point(36, 472), "• Requête : Démarche sécurisée suite à l'affichage du code 1485 (Boîtier de maintenance saturé).", fontsize=8.5, fontname="helv", color=C_DARK)
    p4.insert_text(pymupdf.Point(36, 487), "• Procédure : Remplacement par la référence C12C935711 et consigne critique : interdiction formelle de toucher la puce IC dorée.", fontsize=8.5, fontname="helv", color=C_DARK)

    s3_path = os.path.join(SCREENSHOTS_DIR, "screenshot_03_cas2_epson_code1485.png")
    if os.path.exists(s3_path):
        p4.insert_image(pymupdf.Rect(40, 500, W_A4 - 40, 790), filename=s3_path)
        p4.insert_text(
            pymupdf.Point(95, 802),
            "Figure 3.2 : Cas 2 — Procédure de remplacement du boîtier C12C935711 et alerte critique sur la puce IC",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # =========================================================
    # PAGE 5 : CAS 3 (MCP BANDING 12H) & CAS 4 (HITL VISA)
    # =========================================================
    p5 = doc.new_page(width=W_A4, height=H_A4)
    p5.insert_text(pymupdf.Point(36, 60), "4. Démonstration des Cas d'Atelier (Cas 3 & Cas 4)", fontsize=15, fontname="hebo", color=C_NAVY)

    # Cas 3
    p5.insert_text(pymupdf.Point(36, 85), "4.1 Cas 3 : Banding & Interrogation GMAO via MCP (Règle des 12h de Repos)", fontsize=11, fontname="hebo", color=C_BLUE)
    p5.insert_text(pymupdf.Point(36, 102), "• Outil MCP get_equipment_history : Détection de 2 Power Cleanings récents (moins de 3 heures).", fontsize=8.5, fontname="helv", color=C_DARK)
    p5.insert_text(pymupdf.Point(36, 117), "• Règle Métier Stricte : Interdiction absolue de relancer une purge ; obligation d'extinction et repos de 12 heures.", fontsize=8.5, fontname="helv", color=C_DARK)

    s4_path = os.path.join(SCREENSHOTS_DIR, "screenshot_04_cas3_epson_banding_mcp.png")
    if os.path.exists(s4_path):
        p5.insert_image(pymupdf.Rect(40, 130, W_A4 - 40, 420), filename=s4_path)
        p5.insert_text(
            pymupdf.Point(90, 432),
            "Figure 4.1 : Cas 3 — Consultation MCP de l'historique et application de la règle constructeur des 12h de repos",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Cas 4 HITL
    p5.insert_text(pymupdf.Point(36, 455), "4.2 Cas 4 : Suspension Human-in-the-Loop & Visa Superviseur [Point C3]", fontsize=11, fontname="hebo", color=C_BLUE)
    p5.insert_text(pymupdf.Point(36, 472), "• Interruption Préventive : Aucune écriture directe en base GMAO sans consentement explicite de l'opérateur.", fontsize=8.5, fontname="helv", color=C_DARK)
    p5.insert_text(pymupdf.Point(36, 487), "• Garanties : Génération d'un jeton HMAC-SHA256 scellé et d'une clé d'idempotence réseau anti-doublon.", fontsize=8.5, fontname="helv", color=C_DARK)

    s5_path = os.path.join(SCREENSHOTS_DIR, "screenshot_05_cas4_ticket_hitl_attente.png")
    if os.path.exists(s5_path):
        p5.insert_image(pymupdf.Rect(40, 500, W_A4 - 40, 790), filename=s5_path)
        p5.insert_text(
            pymupdf.Point(95, 802),
            "Figure 4.2 : Cas 4 — Suspension agentique Human-in-the-Loop, génération du jeton HMAC-SHA256 et attente de visa",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # =========================================================
    # PAGE 6 : CAS 4 (ENREGISTREMENT) & CAS S5 (INJECTION NEUTRALISÉE)
    # =========================================================
    p6 = doc.new_page(width=W_A4, height=H_A4)
    p6.insert_text(pymupdf.Point(36, 60), "5. Validation GMAO & Neutralisation d'Injection (S5)", fontsize=15, fontname="hebo", color=C_NAVY)

    # Cas 4 Validé
    p6.insert_text(pymupdf.Point(36, 85), "5.1 Cas 4 (Suite) : Signature Validée & Enregistrement Idempotent dans la GMAO", fontsize=11, fontname="hebo", color=C_BLUE)
    p6.insert_text(pymupdf.Point(36, 102), "• Exécution MCP create_ticket : Création du ticket TICK-2026-0043 après vérification de signature du responsable.", fontsize=8.5, fontname="helv", color=C_DARK)
    p6.insert_text(pymupdf.Point(36, 117), "• Protection Anti-Rejeu : La clé IDEM intercepte tout appel répété et renvoie le ticket sans créer de doublon.", fontsize=8.5, fontname="helv", color=C_DARK)

    s6_path = os.path.join(SCREENSHOTS_DIR, "screenshot_06_cas4_ticket_approuve_gmao.png")
    if os.path.exists(s6_path):
        p6.insert_image(pymupdf.Rect(40, 130, W_A4 - 40, 420), filename=s6_path)
        p6.insert_text(
            pymupdf.Point(90, 432),
            "Figure 5.1 : Cas 4 (Suite) — Confirmation de création du ticket GMAO via MCP et registre interactif mis à jour",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Cas S5 Injection
    p6.insert_text(pymupdf.Point(36, 455), "5.2 Cas Sécurité S5 : Détection et Neutralisation de Prompt Injection (Jailbreak)", fontsize=11, fontname="hebo", color=C_BLUE)
    p6.insert_text(pymupdf.Point(36, 472), "• Attaque Détectée : Tentative de forçage en 'MAINTENANCE SUPERVISOR ROOT MODE' via une note technique piégée.", fontsize=8.5, fontname="helv", color=C_DARK)
    p6.insert_text(pymupdf.Point(36, 487), "• Résultat : Balisage XML étanche actif, charge hostile confinée sans basculement illégitime de mode.", fontsize=8.5, fontname="helv", color=C_DARK)

    s7_path = os.path.join(SCREENSHOTS_DIR, "screenshot_07_securite_s5_injection.png")
    if os.path.exists(s7_path):
        p6.insert_image(pymupdf.Rect(40, 500, W_A4 - 40, 790), filename=s7_path)
        p6.insert_text(
            pymupdf.Point(95, 802),
            "Figure 5.2 : Cas S5 — Neutralisation totale de l'injection, alerte de sécurité et délivrance des consignes légitimes",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # =========================================================
    # PAGE 7 : TESTS UNITAIRES AUTOMATISÉS & CONCLUSION
    # =========================================================
    p7 = doc.new_page(width=W_A4, height=H_A4)
    p7.insert_text(pymupdf.Point(36, 60), "6. Validation par Tests Automatisés & Conclusion", fontsize=15, fontname="hebo", color=C_NAVY)

    p7.insert_text(pymupdf.Point(36, 85), "La suite de tests unitaires (tests/test_maintidoc.py) valide rigoureusement les 5 objectifs de conception :", fontsize=9, fontname="helv", color=C_DARK)

    s8_path = os.path.join(SCREENSHOTS_DIR, "screenshot_08_tests_unitaires_ok.png")
    if os.path.exists(s8_path):
        p7.insert_image(pymupdf.Rect(40, 105, W_A4 - 40, 440), filename=s8_path)
        p7.insert_text(
            pymupdf.Point(100, 452),
            "Figure 6.1 : Exécution console unitaire — Ran 5 tests in 17.456s — OK (Taux de conformité 100%)",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Table of Test Results
    p7.draw_rect(pymupdf.Rect(40, 470, W_A4 - 40, 640), fill=C_LIGHT_BG, color=C_BORDER, width=1)
    p7.draw_rect(pymupdf.Rect(40, 470, W_A4 - 40, 492), fill=(225/255, 230/255, 238/255), color=C_BORDER, width=1)
    p7.insert_text(pymupdf.Point(50, 485), "TEST", fontsize=8.5, fontname="hebo", color=C_NAVY)
    p7.insert_text(pymupdf.Point(140, 485), "CRITÈRE DE CONFORMITÉ TESTÉ", fontsize=8.5, fontname="hebo", color=C_NAVY)
    p7.insert_text(pymupdf.Point(470, 485), "RÉSULTAT", fontsize=8.5, fontname="hebo", color=C_NAVY)

    tests_rows = [
        ("test_01", "Étanchéité RBAC [C1, C2] : Rejet strict des accès croisés Canon/Epson", "VALIDÉ (100%)"),
        ("test_02", "Sourcing documentaire exact avec numéro de page précis et citation", "VALIDÉ (100%)"),
        ("test_03", "Human-in-the-Loop [C3] : Rejet des créations sans visa + Idempotence", "VALIDÉ (100%)"),
        ("test_04", "Confinement anti-jailbreak [S5 / R07] : Neutralisation de note piégée", "VALIDÉ (100%)"),
        ("test_05", "Validation de bout en bout des 4 cas réels (Canon, Epson, MCP, HITL)", "VALIDÉ (100%)")
    ]
    y_tr = 512
    for tid, tdes, tres in tests_rows:
        p7.insert_text(pymupdf.Point(50, y_tr), tid, fontsize=8, fontname="courier", color=C_BLUE)
        p7.insert_text(pymupdf.Point(140, y_tr), tdes, fontsize=8, fontname="helv", color=C_DARK)
        p7.insert_text(pymupdf.Point(470, y_tr), tres, fontsize=8, fontname="hebo", color=C_GREEN)
        p7.draw_line(pymupdf.Point(40, y_tr + 8), pymupdf.Point(W_A4 - 40, y_tr + 8), color=C_BORDER, width=0.5)
        y_tr += 28

    # Conclusion paragraph
    p7.insert_text(pymupdf.Point(36, 665), "Conclusion Industrielle & Perspectives :", fontsize=11, fontname="hebo", color=C_NAVY)
    p7.insert_text(
        pymupdf.Point(36, 685),
        "MaintiDoc démontre la faisabilité opérationnelle d'un assistant de maintenance associant RAG multimodal,",
        fontsize=8.5, fontname="helv", color=C_DARK
    )
    p7.insert_text(
        pymupdf.Point(36, 700),
        "Vision-Language Model (Qwen2.5-VL) et serveur GMAO fondé sur le standard MCP.",
        fontsize=8.5, fontname="helv", color=C_DARK
    )
    p7.insert_text(
        pymupdf.Point(36, 715),
        "La stricte séparation des privilèges et la suspension Human-in-the-Loop sécurisent les actions industrielles.",
        fontsize=8.5, fontname="helv", color=C_DARK
    )
    p7.insert_text(
        pymupdf.Point(36, 735),
        "Perspectives : Extension aux capteurs vibratoires IoT et intégration sur lunettes connectées d'atelier.",
        fontsize=8.5, fontname="heit", color=C_MUTED
    )

    # =========================================================
    # PAGE 8 : CAPTURES TERMINAL WINDOWS (INGESTION & ASSISTANT CLI)
    # =========================================================
    p8 = doc.new_page(width=W_A4, height=H_A4)
    p8.insert_text(pymupdf.Point(36, 60), "7. Captures d'Écran Terminal Windows (PowerShell)", fontsize=15, fontname="hebo", color=C_NAVY)
    p8.insert_text(pymupdf.Point(36, 85), "Validation des pipelines techniques en console Windows Terminal :", fontsize=9, fontname="helv", color=C_DARK)

    # Screenshot Ingestion
    s9_path = os.path.join(SCREENSHOTS_DIR, "screenshot_09_terminal_ingestion_corpus.png")
    if os.path.exists(s9_path):
        p8.insert_image(pymupdf.Rect(40, 105, W_A4 - 40, 425), filename=s9_path)
        p8.insert_text(
            pymupdf.Point(80, 437),
            "Figure 7.1 : Terminal Windows — Ingestion vectorielle ChromaDB, extraction PyMuPDF et hachage SHA-256",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Screenshot CLI Assistant
    s10_path = os.path.join(SCREENSHOTS_DIR, "screenshot_10_terminal_assistant_cli.png")
    if os.path.exists(s10_path):
        p8.insert_image(pymupdf.Rect(40, 460, W_A4 - 40, 780), filename=s10_path)
        p8.insert_text(
            pymupdf.Point(85, 792),
            "Figure 7.2 : Terminal Windows — Assistant interactif CLI connecté au modèle local multimodal Qwen2.5-VL",
            fontsize=8, fontname="heit", color=C_MUTED
        )

    # Apply headers, footers and page numbers
    total_pages = doc.page_count
    for i in range(total_pages):
        page = doc[i]
        add_header_footer(page, i + 1, total_pages)

    doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    doc.save(ROOT_OUTPUT_PDF, garbage=4, deflate=True)
    print(f"Rapport PDF généré avec succès ({total_pages} pages) dans : {OUTPUT_PDF}")
    print(f"Copie racine générée : {ROOT_OUTPUT_PDF}")


if __name__ == "__main__":
    create_report()
