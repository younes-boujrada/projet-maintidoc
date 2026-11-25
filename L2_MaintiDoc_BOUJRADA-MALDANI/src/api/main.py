"""
FastAPI search endpoint.
Run: uvicorn src.api.main:app --reload
"""
from __future__ import annotations
import os
os.environ.setdefault("QDRANT_MEMORY", "1")

from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile, shutil
from pathlib import Path
from src.acces.rbac import get_allowed_families
from src.recherche.search import search as do_search

app = FastAPI(title="MaintiDoc API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}


@app.post("/search")
async def search(
    query: str = Form(...),
    utilisateur: str = Form(...),
    text_only: bool = Form(False),
    photo: UploadFile | None = File(None),
):
    allowed = get_allowed_families(utilisateur)
    if not allowed:
        raise HTTPException(status_code=403, detail=f"Groupe '{utilisateur}' non autorisé")

    img_path: str | None = None
    tmp_dir: str | None = None
    if photo:
        tmp_dir = tempfile.mkdtemp()
        img_path = str(Path(tmp_dir) / photo.filename)
        with open(img_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)

    try:
        results = do_search(
            query_text=query,
            user_group=utilisateur,
            query_image=img_path,
            k=5,
            text_only=text_only,
        )
    finally:
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    return {"query": query, "utilisateur": utilisateur, "results": results}
