# embedding_client.py
from sentence_transformers import SentenceTransformer
import numpy as np

# 전역 캐싱 (성능 ↑)
_model = None

def load_embedding_model():
    global _model
    if _model is None:
        print("🔵 Loading embedding model: intfloat/e5-small-v2 ...")
        _model = SentenceTransformer(
            "intfloat/e5-small-v2",
            trust_remote_code=True
        )
    return _model


def embed_query(text: str) -> np.ndarray:
    """
    e5-small-v2 query embedding
    """
    model = load_embedding_model()
    formatted = f"query: {text}"
    return model.encode(
        formatted,
        normalize_embeddings=True
    )


def embed_passage(text: str) -> np.ndarray:
    """
    e5-small-v2 passage embedding
    """
    model = load_embedding_model()
    formatted = f"passage: {text}"
    return model.encode(
        formatted,
        normalize_embeddings=True
    )
