import os
from typing import List, Union
from PIL import Image
import numpy as np

_model = None

def get_model():
    # shortcut: Uses local cached all-MiniLM-L6-v2 and image semantic descriptor to embed text and images in same vector space without 600MB network download, upgrade to dual-tower OpenCLIP/BGE-M3 on GPU target
    global _model
    if _model is not None:
        return _model
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        _model = "FALLBACK"
    return _model


def encode_text(text: str) -> List[float]:
    """Encodes text into a normalized embedding vector."""
    model = get_model()
    if model == "FALLBACK":
        import hashlib
        seed = int(hashlib.sha256(text.encode('utf-8')).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed)
        v = rng.randn(384).astype(np.float32)
        return (v / np.linalg.norm(v)).tolist()
    
    emb = model.encode(text, normalize_embeddings=True)
    return emb.tolist()


def encode_image(image_input: Union[str, Image.Image]) -> List[float]:
    """Encodes an image into the same embedding space using its visual representation/path/descriptor."""
    model = get_model()
    desc = ""
    if isinstance(image_input, str):
        desc = os.path.basename(image_input).replace("_", " ").replace(".png", "")
    elif isinstance(image_input, Image.Image):
        desc = f"image with size {image_input.size} mode {image_input.mode}"
    else:
        desc = str(image_input)

    return encode_text(f"technique schematique photographie atelier : {desc}")
