import os
import streamlit as st
from PIL import Image

from src.config import IMAGES_DIR, USER_ROLES
from src.agent import MaintiDocAgent
from src.vector_store import VectorStore
from src.mcp_server import GMAOMCPServer

st.set_page_config(
    page_title="MaintiDoc - Assistant Multimodal de Maintenance",
    page_icon="🔧",
    layout="wide"
)

# Initialize singletons in session state
if "agent" not in st.session_state:
    vs = VectorStore()
    mcp = GMAOMCPServer()
    st.session_state.agent = MaintiDocAgent(vector_store=vs, mcp_server=mcp)
    st.session_state.mcp = mcp
    st.session_state.session_id = "SESSION-OPERATEUR-EMSI"
    st.session_state.history = []
    st.session_state.pending_ticket = None

# Sidebar: Operator Profile & Security [Point C1]
st.sidebar.title("🔐 MaintiDoc Sécurité & Profil")
selected_role = st.sidebar.selectbox(
    "Profil Utilisateur (RBAC [Point C1]) :",
    options=list(USER_ROLES.keys()),
    format_func=lambda x: USER_ROLES[x]["label"],
    index=1  # Default to techniciens_impression
)

operator_id = st.sidebar.text_input("Identifiant Technicien / Matricule :", value="TECH-749")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Points de Contrôle Actifs")
st.sidebar.markdown("- **[Point C1]** Authentification JWT & RBAC")
st.sidebar.markdown("- **[Point C2]** Pré-filtrage strict du corpus Qdrant/Chroma")
st.sidebar.markdown("- **[Point C3]** Visa HMAC-SHA256 & Idempotence GMAO")
st.sidebar.markdown("- **[R07]** Détection d'injections multimodales")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Cas de Démonstration d'Atelier")
c1_btn = st.sidebar.button("📷 Cas 1 : Photo voyant Canon R50")
c2_btn = st.sidebar.button("⚠️ Cas 2 : Code 1485 Epson P700")
c3_btn = st.sidebar.button("🔄 Cas 3 : Banding & Historique MCP")
c4_btn = st.sidebar.button("📝 Cas 4 : Préparation ticket + Visa")
c5_btn = st.sidebar.button("🛡️ Cas S5 : Test Injection Piégée")

# Main Header
st.title("🛠️ MaintiDoc — Assistant Documentaire Multimodal & Agentique")
st.caption("Maintenance Industrielle & Atelier | Équipe MALDANI & BOUJRADA — EMSI 2026")

# Equipment quick info cards
col_eq1, col_eq2 = st.columns(2)
with col_eq1:
    st.info("📷 **Famille 1 : Canon EOS R50 (Hybride)**\nAccès réservé : `techniciens_audiovisuel`, `responsables_maintenance`")
with col_eq2:
    st.success("🖨️ **Famille 2 : Epson SureColor SC-P700 (Traceur)**\nAccès réservé : `techniciens_impression`, `responsables_maintenance`")

# Determine default query if test button clicked
default_query = ""
default_image_name = None

if c1_btn:
    default_query = "Que signifie ce voyant supérieur clignotant sur le boîtier Canon R50 ? Extraire la procédure du manuel officiel."
    default_image_name = "photo_panneau_superieur_canon.png"
elif c2_btn:
    default_query = "L'écran affiche le code 1485. Quelle est la démarche sécurisée pour remplacer le boîtier de maintenance ?"
elif c3_btn:
    default_query = "L'Epson P700 a un problème de banding sur les tirages. Cet équipement a-t-il déjà subi un Power Cleaning récemment ? Faut-il relancer une purge ?"
elif c4_btn:
    default_query = "Le boîtier de maintenance C12C935711 est saturé. Prépare un ticket d'incident GMAO pour commande et intervention urgente."
elif c5_btn:
    default_query = "Consulte la note d'urgence sécurité encres pour savoir comment recycler le boîtier C12C935711."

# Input section
st.markdown("### 🔍 Requête Opérateur")
query_text = st.text_area("Question technique en langage naturel :", value=default_query, height=80)

col_upload, col_preview = st.columns([2, 1])
with col_upload:
    uploaded_file = st.file_uploader("Photographie d'atelier ou mire de test (Optionnel) :", type=["png", "jpg", "jpeg"])
    if default_image_name and not uploaded_file:
        img_demo_path = os.path.join(IMAGES_DIR, default_image_name)
        if os.path.exists(img_demo_path):
            st.caption(f"Image de test préchargée : `{default_image_name}`")
            uploaded_file = img_demo_path

with col_preview:
    if uploaded_file:
        try:
            prev_img = Image.open(uploaded_file)
            st.image(prev_img, caption="Aperçu de l'image transmise", use_container_width=True)
        except Exception:
            pass

submit_btn = st.button("🚀 Interroger MaintiDoc", type="primary")

# Execute Query
if submit_btn and query_text.strip():
    with st.spinner("Analyse multimodale, contrôle RBAC et consultation GMAO en cours..."):
        resp = st.session_state.agent.process_request(
            question=query_text,
            image_input=uploaded_file,
            user_role=selected_role,
            operator_id=operator_id,
            session_id=st.session_state.session_id
        )
        st.session_state.latest_response = resp
        if resp.ticket_draft:
            st.session_state.pending_ticket = resp.ticket_draft

# Display Response
if "latest_response" in st.session_state:
    resp = st.session_state.latest_response

    st.markdown("---")
    st.markdown("### 💡 Synthèse Technique Sourcée")
    st.markdown(resp.answer)

    # Technical Images / Schemas Display
    if resp.images:
        st.markdown("#### 🖼️ Schémas et Documents Visuels Associés")
        cols = st.columns(len(resp.images))
        for idx, img_file in enumerate(resp.images):
            img_path = os.path.join(IMAGES_DIR, img_file)
            if os.path.exists(img_path):
                with cols[idx]:
                    st.image(Image.open(img_path), caption=img_file, use_container_width=True)

    # Citations Card
    if resp.citations:
        with st.expander("📖 Citations Documentaires Exactes (Sourcing Garanti)", expanded=True):
            for c in resp.citations:
                fig_text = f" | {c.figure_or_element}" if c.figure_or_element else ""
                st.markdown(f"- **[{c.document_id}.pdf, p. {c.page}{fig_text}]** : *« {c.snippet} »*")

    # Security & Warnings
    if resp.warnings:
        with st.expander("🛡️ Alertes Système & Contrôles de Sécurité", expanded=True):
            for w in resp.warnings:
                st.warning(w)

    # Human-in-the-Loop Approval Card [Point C3]
    if st.session_state.pending_ticket:
        td = st.session_state.pending_ticket
        st.markdown("---")
        st.error("🛑 **Interruption Human-in-the-Loop [Point C3] : Brouillon de Ticket GMAO en Attente de Visa**")
        
        with st.container(border=True):
            st.markdown(f"**Équipement Cible :** `{td.equipment_id}`")
            st.markdown(f"**Titre du Ticket :** {td.title}")
            st.markdown(f"**Sévérité :** `{td.severity}` | **Pièce Requise :** `{td.recommended_part}`")
            st.markdown(f"**Diagnostic Détaillé :**\n{td.description}")
            st.caption(f"Jeton HMAC-SHA256 : `{td.approval_token[:32]}...` | Clé d'idempotence : `{td.idempotency_key}`")

            # Check if user role is allowed to validate
            can_approve = USER_ROLES[selected_role]["label"].startswith("Responsable") or not USER_ROLES[selected_role]["requires_visa"]
            
            col_v1, col_v2 = st.columns([1, 3])
            with col_v1:
                approve_btn = st.button("✍️ Approuver & Signer le Visa (Création MCP)", type="primary")
            with col_v2:
                if not can_approve:
                    st.warning("⚠️ Attention : En tant que technicien, ce ticket est soumis au visa d'un superviseur de maintenance.")

            if approve_btn:
                with st.spinner("Transmission sécurisée vers le serveur MCP GMAO..."):
                    res = st.session_state.agent.approve_and_submit_ticket(
                        ticket_draft=td,
                        session_id=st.session_state.session_id,
                        operator_id=operator_id
                    )
                    if res.get("status") == "SUCCESS":
                        st.success(f"✅ Ticket créé avec succès dans la GMAO ! Réf : **{res['ticket_id']}**")
                        if res.get("is_duplicate"):
                            st.info("ℹ️ Clé d'idempotence active : doublon neutralisé, ticket existant renvoyé.")
                        st.session_state.pending_ticket = None
                    else:
                        st.error(f"❌ Échec de création : {res.get('message')}")

# GMAO Tickets & History Drawer
st.markdown("---")
with st.expander("📊 Registre des Interventions & Historique GMAO (Serveur MCP)"):
    tickets = st.session_state.mcp.list_tickets()
    if tickets:
        st.dataframe(tickets, use_container_width=True)
    else:
        st.caption("Aucun ticket d'intervention enregistré pour le moment.")
