# MaintiDoc — Assistant Documentaire Multimodal et Agentique pour la Maintenance Industrielle & Atelier

> **Module :** IA Générative Multimodale (Prof. Mariam CHERRABI) — EMSI 2026  
> **Équipe :** MALDANI Mostafa & BOUJRADA Younes  
> **Équipements Cibles :** Famille 1 : Canon EOS R50 (Hybride) | Famille 2 : Epson SureColor SC-P700 (Traceur)

---

## 📌 Architecture Implémentée

MaintiDoc est structuré en modules découplés selon les spécifications du Livrable 1 :

- **`corpus/`** : 38 documents techniques, photographies et schémas d'atelier, répertoriés dans `inventaire.csv`.
- **`src/config.py`** : Configuration des rôles RBAC, chemins et constantes de sécurité.
- **`src/models.py`** : Modèles Pydantic stricts pour les métadonnées indexées, les citations sourcées et les tickets GMAO.
- **`src/security.py`** : 
  - `[Point C1]` Contrôle d'accès RBAC.
  - `[Point C3]` Jeton cryptographique d'approbation humaine HMAC-SHA256.
  - `[R07]` Balisage XML étanche `<context_document>` pour neutraliser les injections de prompt (Jailbreak S5).
- **`src/embeddings.py`** : Moteur d'embeddings multimodaux (texte et image).
- **`src/vector_store.py`** : Base vectorielle ChromaDB avec pré-filtrage dur `[Point C2]` par groupe d'accès utilisateur.
- **`src/ingestion.py`** : Pipeline d'extraction PyMuPDF, découpage sémantique, hachage SHA-256 et indexation.
- **`src/mcp_server.py`** : Serveur MCP de GMAO exposant `get_equipment_history` et `create_ticket` avec clé d'idempotence et validation du visa opérateur.
- **`src/agent.py`** : Orchestrateur agentique multimodal intégrant les 4 cas d'usage atelier et la suspension Human-in-the-Loop.
- **`app.py`** : Application web interactive Streamlit avec simulation des profils et validation des tickets.
- **`tests/test_maintidoc.py`** : Suite de tests automatisés validant les 5 critères de réussite.

---

## 🚀 Démarrage Rapide

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Génération du corpus et Ingestion vectorielle
```bash
python generate_corpus.py
python -m src.ingestion
```

### 3. Lancement des tests unitaires
```bash
python -m unittest tests/test_maintidoc.py
```

### 4. Lancement de l'IHM Opérateur Streamlit
```bash
streamlit run app.py
```

---

## 🎯 Cas d'Usage Couverts
1. **Cas 1 :** Identification d'anomalie par photographie de panneau (surchauffe Canon R50).
2. **Cas 2 :** Résolution guidée d'un code d'erreur bloquant (code 1485, boîtier C12C935711, interdiction puce IC dorée).
3. **Cas 3 :** Consultation historique matériel via MCP (banding Epson P700, détection de 2 nettoyages préalables, application de la règle des 12h de repos).
4. **Cas 4 :** Préparation de ticket GMAO avec interruption Human-in-the-loop, visa HMAC-SHA256 et protection contre les doublons par clé d'idempotence.
