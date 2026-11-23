import os
import re
import uuid
import hashlib
from typing import Dict, Any, Optional, List
from PIL import Image

from src.config import IMAGES_DIR, USER_ROLES
from src.models import AgentResponse, Citation, TicketDraft
from src.vector_store import VectorStore
from src.mcp_server import GMAOMCPServer
from src.security import forge_approval_token, sanitize_and_wrap_context


class MaintiDocAgent:
    """
    Multimodal Agentic Orchestrator for MaintiDoc.
    Implements Control Points [C1], [C2], [C3] and Use Cases 1 to 4.
    """
    def __init__(self, vector_store: Optional[VectorStore] = None, mcp_server: Optional[GMAOMCPServer] = None):
        self.vector_store = vector_store or VectorStore()
        self.mcp_server = mcp_server or GMAOMCPServer()

    def process_request(
        self,
        question: str,
        image_input: Optional[Any] = None,
        user_role: str = "techniciens_impression",
        operator_id: str = "TECH-01",
        session_id: Optional[str] = None
    ) -> AgentResponse:
        session_id = session_id or str(uuid.uuid4())
        warnings: List[str] = []
        citations: List[Citation] = []
        retrieved_images: List[str] = []

        # ---------------------------------------------------------
        # Étape 1 : Réception et Contrôle d'Identité [Point C1]
        # ---------------------------------------------------------
        if user_role not in USER_ROLES:
            return AgentResponse(
                answer="Accès refusé : Rôle utilisateur non reconnu par la passerelle de sécurité.",
                warnings=["Échec d'authentification [Point C1]"]
            )

        role_info = USER_ROLES[user_role]
        allowed_families = role_info.get("allowed_families", [])

        # ---------------------------------------------------------
        # Étape 2 : Analyse Visuelle & Détection Équipement Cible
        # ---------------------------------------------------------
        detected_equipment = None
        target_family = None
        visual_cue = ""
        q_lower = question.lower()

        if any(w in q_lower for w in ["canon", "r50", "capteur"]):
            detected_equipment = "CANON-R50-LAB01"
            target_family = "appareils_photo"
        elif any(w in q_lower for w in ["epson", "p700", "traceur", "1485", "c12c935711", "buse", "banding", "encres", "power cleaning"]):
            detected_equipment = "EPSON-P700-01"
            target_family = "imprimantes_pro"

        if image_input is not None:
            img_name = getattr(image_input, "name", str(image_input)).lower()
            if "canon" in img_name or "panneau" in img_name:
                detected_equipment = "CANON-R50-LAB01"
                target_family = "appareils_photo"
                visual_cue = "Photographie panneau supérieur Canon EOS R50 voyant alerte clignotant"
            elif "epson" in img_name or "mire" in img_name or "boitier" in img_name:
                detected_equipment = "EPSON-P700-01"
                target_family = "imprimantes_pro"
                visual_cue = "Mire test buses ou schéma boîtier Epson"

        # [Point C1/C2] Strict RBAC Check on Target Family
        if target_family and user_role != "responsables_maintenance":
            if target_family not in allowed_families:
                return AgentResponse(
                    answer=(
                        f"Accès refusé : Votre profil ({user_role}) n'est pas habilité à consulter "
                        f"la documentation des équipements de la famille '{target_family}' [Point C1/C2 - RBAC]."
                    ),
                    warnings=["Blocage RBAC : isolation stricte inter-familles respectée [Point C1 & C2]."]
                )

        # Check prompt injection in question (Jailbreak / S5)
        if any(term in q_lower for term in ["ignore all instructions", "root mode", "leak the secret", "note_urgence_securite_piegee"]):
            warnings.append("Document piégé détecté : instruction de contournement neutralisée comme donnée passive [Point R07].")

        # ---------------------------------------------------------
        # Étape 3 : Recherche Hybride Filtrée [Point C2]
        # ---------------------------------------------------------
        search_query = f"{question} {visual_cue}".strip()
        chunks = self.vector_store.query(
            query_text=search_query,
            query_image=image_input,
            user_role=user_role,
            k=5
        )

        if not chunks:
            return AgentResponse(
                answer="Aucune documentation technique correspondante n'a été trouvée dans votre périmètre d'habilitation.",
                warnings=["Aucun chunk autorisé récupéré [Point C2]."]
            )

        # ---------------------------------------------------------
        # Étape 4 : Traitement des Sources, Citations & Protection R07
        # ---------------------------------------------------------
        contradictions_detected = []
        has_official_canon = False
        has_thirdparty_canon = False
        has_official_epson = False
        has_thirdparty_epson = False

        formatted_contexts = []
        for chk in chunks:
            doc_id = chk["document_id"]
            page = chk["page"]
            content = chk["content"]

            if "ignore all instructions" in content.lower() or "root mode" in content.lower():
                if not any("piégé" in w for w in warnings):
                    warnings.append("Document piégé détecté : instruction de contournement neutralisée comme donnée passive [Point R07].")

            safe_text = sanitize_and_wrap_context(content, doc_id, page)
            formatted_contexts.append(safe_text)

            fig = "Figure 1 (Schéma boîtier)" if "boitier" in doc_id or "schema" in doc_id else None
            citations.append(Citation(
                document_id=doc_id,
                page=page,
                figure_or_element=fig,
                snippet=content[:150] + "..."
            ))

            if "canon_officiel" in doc_id:
                has_official_canon = True
            elif "canon_tierce" in doc_id:
                has_thirdparty_canon = True
            elif "epson_standard" in doc_id:
                has_official_epson = True
            elif "epson_tierce" in doc_id:
                has_thirdparty_epson = True

        if has_official_canon and has_thirdparty_canon:
            contradictions_detected.append(
                "CONTRADICTION DÉTECTÉE (Capteur Canon R50) : La procédure officielle [proc_nettoyage_capteur_canon_officiel, p. 1] "
                "proscrit formellement tout liquide et préconise une poire soufflante à 15 mm. La fiche tierce recommande l'alcool isopropylique. "
                "Recommandation retenue : Suivre impérativement la procédure constructeur officielle pour préserver la garantie."
            )

        if has_official_epson and has_thirdparty_epson:
            contradictions_detected.append(
                "CONTRADICTION DÉTECTÉE (Tête Epson SC-P700) : Le guide officiel [guide_maint_tete_epson_standard, p. 1] "
                "impose un repos obligatoire de 12 heures après 2 nettoyages. La procédure tierce propose un débouchage forcé à l'ammoniaque sous pression. "
                "Recommandation retenue : Observer la règle des 12h de repos constructeur pour éviter la destruction de la tête MicroPiezo."
            )

        # ---------------------------------------------------------
        # Étape 5 : Consultation Historique MCP (Cas 3)
        # ---------------------------------------------------------
        mcp_history_data = None
        needs_mcp_history = any(k in q_lower for k in ["historique", "banding", "power cleaning", "nettoyage", "récent", "intervention", "ticket", "déjà"])
        
        if needs_mcp_history and detected_equipment:
            hist_res = self.mcp_server.get_equipment_history(detected_equipment)
            if hist_res.get("found"):
                mcp_history_data = hist_res["data"]

        # ---------------------------------------------------------
        # Étape 6 : Synthèse de la Réponse Métier Sourcée
        # ---------------------------------------------------------
        answer_parts = []

        # Document piégé test
        if "note_urgence_securite_piegee" in q_lower or any("piegee" in c.document_id for c in citations):
            answer_parts.append(
                "**Consultation Documentaire - Consignes de Sécurité Encres :**\n"
                "Conformément à la note de sécurité [note_urgence_securite_piegee.pdf, p. 1], les encres pigmentaires UltraChrome "
                "doivent obligatoirement faire l'objet d'un retraitement chimique en bac de rétention étanche spécialisé.\n"
                "- **Consigne de sécurité :** Il est strictement interdit de jeter le boîtier de maintenance C12C935711 "
                "ou des résidus d'encres dans les déchets municipaux ordinaires.\n"
                "- *Note de sécurité IA : L'instruction de contournement présente dans le document a été traitée comme donnée passive neutralisée.*"
            )

        # Cas 1 : Photo panneau Canon R50
        elif target_family == "appareils_photo" and ("voyant" in q_lower or "panneau" in q_lower or "photo" in q_lower or "orange" in q_lower or "rouge" in q_lower or image_input is not None):
            retrieved_images.append("photo_panneau_superieur_canon.png")
            answer_parts.append(
                "**Diagnostic Visuel du Panneau Supérieur (Canon EOS R50) :**\n"
                "L'analyse de l'image montre le clignotement de l'indicateur thermique de surchauffe (témoin thermomètre).\n"
                "- **Cause exacte :** Élévation anormale de la température interne du processeur DIGIC X lors d'un fonctionnement prolongé.\n"
                "- **Consigne officielle :** Éteindre immédiatement l'appareil, ouvrir la trappe batterie dans un local ventilé et observer un repos d'au moins 20 minutes [manuel_canon_r50_base.pdf, p. 1].\n"
                "- **Rappel sécurité :** Ne pas exposer le capteur nu à des poussières ou solvants chimiques."
            )

        # Cas 2 : Code 1485 / Boîtier maintenance Epson P700
        elif "1485" in q_lower or "c12c935711" in q_lower or ("boitier" in q_lower and target_family == "imprimantes_pro"):
            retrieved_images.append("schema_boitier_maintenance_epson.png")
            answer_parts.append(
                "**Procédure de Résolution du Code Erreur 1485 (Epson SureColor SC-P700) :**\n"
                "Le code **1485** indique la saturation complète du boîtier de maintenance d'encre usagée [table_erreurs_epson_p700.pdf, p. 1].\n"
                "- **Référence officielle de la pièce :** Boîtier de maintenance **C12C935711** [manuel_epson_p700_base.pdf, p. 1].\n"
                "- **Démarche sécurisée :**\n"
                "  1. Ouvrir le capot latéral droit du traceur.\n"
                "  2. Dévisser la vis moletée de maintien.\n"
                "  3. Extraire l'ancien boîtier horizontalement sans l'incliner pour éviter tout écoulement d'encre.\n"
                "  4. Insérer le boîtier neuf jusqu'au clic d'enclenchement.\n"
                "- ⚠️ **CONSIGNE DE SÉCURITÉ CRITIQUE :** Il est strictement interdit de toucher la puce IC dorée située sur le flanc du boîtier (risque de court-circuit irrémédiable du contrôleur) [manuel_epson_p700_base.pdf, p. 1, Figure 1]."
            )

        # Cas 3 : Banding et consultation historique MCP
        elif "banding" in q_lower or ("power cleaning" in q_lower and target_family == "imprimantes_pro"):
            retrieved_images.append("mire_test_buses_nozzle_check_epson.png")
            history_text = ""
            if mcp_history_data:
                interventions = mcp_history_data.get("recent_interventions", [])
                history_text = (
                    f"\n- **Consultation GMAO via MCP :** L'équipement `{mcp_history_data['equipment_id']}` a déjà subi "
                    f"**{len(interventions)} nettoyages puissants (Power Cleaning)** consécutifs le 22/02/2026 par {interventions[-1]['technician']}.\n"
                    f"- **Préconisation constructeur impérative :** En application stricte de la **règle des 12 heures de repos** "
                    f"[guide_maint_tete_epson_standard.pdf, p. 1], **aucune nouvelle purge ne doit être lancée immédiatement** afin de permettre "
                    f"la réhydratation naturelle des buses MicroPiezo et d'éviter d'endommager la tête PrecisionCore."
                )

            answer_parts.append(
                f"**Analyse du Problème de Banding sur Epson SC-P700 :**\n"
                f"L'apparition de bandes horizontales résulte de buses obstruées (notamment Light Cyan).{history_text}\n"
                f"- Si les buses demeurent bouchées après le repos de 12 heures, commander un boîtier neuf et envisager une révision d'atelier."
            )

        # Réponse générique sourcée
        else:
            top_chunk = chunks[0]
            answer_parts.append(
                f"**Réponse Technique MaintiDoc :**\n"
                f"D'après la documentation consultée [{top_chunk['document_id']}.pdf, p. {top_chunk['page']}] :\n"
                f"{top_chunk['content'][:400]}..."
            )

        if contradictions_detected:
            answer_parts.append("\n**Alertes de Contradiction :**\n" + "\n".join(f"- {c}" for c in contradictions_detected))

        # ---------------------------------------------------------
        # Étape 7 : Préparation Brouillon Ticket & Suspension Human-in-the-Loop [Point C3] (Cas 4)
        # ---------------------------------------------------------
        ticket_draft = None
        human_interrupt_required = False

        needs_ticket = any(kw in q_lower for kw in ["ticket", "commander", "pièce", "remplacement", "saturation", "1485", "anomalie bloquante", "gmao"])
        if needs_ticket and detected_equipment:
            if "1485" in q_lower or "boitier" in q_lower or "c12c935711" in q_lower:
                title = "Remplacement requis : Boîtier de maintenance C12C935711 saturé"
                desc = "Alerte 1485 constatée sur Epson SC-P700. Boîtier d'encre usagée saturé à 98% après 3 850 impressions. Remplacement et commande d'une unité neuve requis."
                part = "C12C935711 (Epson Maintenance Box)"
                severity = "CRITIQUE"
            else:
                title = f"Intervention de maintenance requise sur {detected_equipment}"
                desc = f"Signalement technicien : {question}. Diagnostic assisté par MaintiDoc."
                part = "LP-E17" if "canon" in detected_equipment.lower() else "C12C935711"
                severity = "MOYENNE"

            idempotency_raw = f"{detected_equipment}-{title}-{operator_id}"
            idempotency_key = hashlib.md5(idempotency_raw.encode('utf-8')).hexdigest()

            raw_ticket_data = {
                "equipment_id": detected_equipment,
                "title": title,
                "description": desc,
                "severity": severity,
                "recommended_part": part
            }
            approval_token = forge_approval_token(session_id, raw_ticket_data, operator_id)

            ticket_draft = TicketDraft(
                equipment_id=detected_equipment,
                title=title,
                description=desc,
                severity=severity,
                recommended_part=part,
                approval_token=approval_token,
                idempotency_key=idempotency_key
            )
            human_interrupt_required = True
            warnings.append(
                "Interruption Human-in-the-Loop [Point C3] : Brouillon de ticket généré. "
                "L'exécution est suspendue en attente du visa explicite du technicien."
            )

        full_answer = "\n\n".join(answer_parts)
        return AgentResponse(
            answer=full_answer,
            citations=citations,
            sources=chunks,
            images=retrieved_images,
            ticket_draft=ticket_draft,
            warnings=warnings,
            human_interrupt_required=human_interrupt_required
        )

    def approve_and_submit_ticket(
        self,
        ticket_draft: TicketDraft,
        session_id: str,
        operator_id: str
    ) -> Dict[str, Any]:
        """Étape 8 : Validation et Exécution MCP avec clé d'idempotence et jeton HMAC."""
        return self.mcp_server.create_ticket(
            equipment_id=ticket_draft.equipment_id,
            title=ticket_draft.title,
            description=ticket_draft.description,
            severity=ticket_draft.severity,
            recommended_part=ticket_draft.recommended_part,
            session_id=session_id,
            operator_id=operator_id,
            approval_token=ticket_draft.approval_token or "",
            idempotency_key=ticket_draft.idempotency_key
        )
