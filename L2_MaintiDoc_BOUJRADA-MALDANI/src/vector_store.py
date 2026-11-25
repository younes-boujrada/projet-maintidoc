import os
from typing import List, Dict, Any, Optional
from PIL import Image
import chromadb
from src.config import DB_DIR, COLLECTION_NAME, USER_ROLES
from src.embeddings import encode_text, encode_image


class VectorStore:
    def __init__(self, persist_dir: str = str(DB_DIR)):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def count(self) -> int:
        return self.collection.count()

    def add_element(
        self,
        element_id: str,
        document_text: str,
        metadata: Dict[str, Any],
        embedding: List[float]
    ):
        """Adds a text chunk or visual element to the vector collection."""
        self.collection.upsert(
            ids=[element_id],
            documents=[document_text],
            metadatas=[metadata],
            embeddings=[embedding]
        )

    def query(
        self,
        query_text: Optional[str] = None,
        query_image: Optional[Any] = None,
        user_role: Optional[str] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Multimodal search with STRICT Point [C2] RBAC Pre-Filtering.
        Metadata filtering is enforced before cosine similarity search.
        """
        if not query_text and not query_image:
            raise ValueError("Query must contain text or an image.")

        # Compute query embedding
        if query_image is not None:
            q_emb = encode_image(query_image)
        else:
            q_emb = encode_text(query_text)

        # Build Point [C2] RBAC Filter
        where_clause = None
        if user_role and user_role in USER_ROLES:
            if user_role == "responsables_maintenance":
                # Superviseur has universal access
                where_clause = None
            elif user_role == "operateurs_invites":
                # Guests restricted to basic public/normal usage
                where_clause = {"usage_test": "normal"}
            else:
                # Technicians restricted strictly to their access group
                where_clause = {"groupes_acces": user_role}

        total_count = self.collection.count()
        if total_count == 0:
            return []

        n_results = min(k, total_count)
        query_kwargs = {
            "query_embeddings": [q_emb],
            "n_results": n_results
        }
        if where_clause:
            query_kwargs["where"] = where_clause

        try:
            results = self.collection.query(**query_kwargs)
        except Exception as e:
            # If where condition matched 0 documents in ChromaDB
            return []

        formatted = []
        if results and results.get("ids") and results["ids"][0]:
            ids = results["ids"][0]
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            for idx, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
                similarity = max(0.0, 1.0 - dist)
                formatted.append({
                    "ref": f"S{idx}",
                    "chunk_id": cid,
                    "document_id": meta.get("document_id", "inconnu"),
                    "page": meta.get("page", 1),
                    "element_type": meta.get("element_type", "procedure_paragraph"),
                    "famille_equipement": meta.get("famille_equipement", ""),
                    "equipment_id": meta.get("equipment_id", ""),
                    "groupes_acces": meta.get("groupes_acces", ""),
                    "has_visual_element": meta.get("has_visual_element", False),
                    "linked_image_id": meta.get("linked_image_id", None),
                    "usage_test": meta.get("usage_test", "normal"),
                    "content": doc,
                    "similarity": similarity
                })

        return formatted
