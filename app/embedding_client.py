# embedding_client.py
from sentence_transformers import SentenceTransformer
import numpy as np
import torch

# 전역 캐싱 (성능 ↑)
_model = None

def load_embedding_model():
    global _model
    if _model is None:
        print("🔵 Loading embedding model: intfloat/e5-small-v2 ...")
        try:
            # CUDA 사용 가능 시 자동 사용, 메모리 부족 시 CPU로 폴백
            device = "cuda" if torch.cuda.is_available() else "cpu"
            _model = SentenceTransformer(
                "intfloat/e5-small-v2",
                trust_remote_code=True,
                device=device
            )
        except Exception as e:
            # CUDA 오류 시 CPU로 강제 전환
            print(f"⚠️  CUDA 로딩 실패, CPU로 전환: {e}")
            _model = SentenceTransformer(
                "intfloat/e5-small-v2",
                trust_remote_code=True,
                device="cpu"
            )
    return _model


def embed_query(text: str) -> np.ndarray:
    """
    e5-small-v2 query embedding
    오류 발생 시 예외를 상위로 전달 (build_rag_context에서 처리)
    """
    try:
        model = load_embedding_model()
        formatted = f"query: {text}"
        return model.encode(
            formatted,
            normalize_embeddings=True
        )
    except RuntimeError as e:
        # CUDA 메모리 오류 등 RuntimeError 발생 시 CPU로 재시도
        if "cuda" in str(e).lower() or "cublas" in str(e).lower():
            print(f"⚠️  CUDA 오류 감지, CPU로 재시도: {e}")
            global _model
            _model = None  # 모델 재로딩을 위해 캐시 초기화
            # CPU로 강제 로딩
            _model = SentenceTransformer(
                "intfloat/e5-small-v2",
                trust_remote_code=True,
                device="cpu"
            )
            model = _model
            formatted = f"query: {text}"
            return model.encode(
                formatted,
                normalize_embeddings=True
            )
        else:
            # 다른 RuntimeError는 그대로 전달
            raise


def embed_passage(text: str) -> np.ndarray:
    """
    e5-small-v2 passage embedding
    오류 발생 시 예외를 상위로 전달
    """
    try:
        model = load_embedding_model()
        formatted = f"passage: {text}"
        return model.encode(
            formatted,
            normalize_embeddings=True
        )
    except RuntimeError as e:
        # CUDA 메모리 오류 등 RuntimeError 발생 시 CPU로 재시도
        if "cuda" in str(e).lower() or "cublas" in str(e).lower():
            print(f"⚠️  CUDA 오류 감지, CPU로 재시도: {e}")
            global _model
            _model = None  # 모델 재로딩을 위해 캐시 초기화
            # CPU로 강제 로딩
            _model = SentenceTransformer(
                "intfloat/e5-small-v2",
                trust_remote_code=True,
                device="cpu"
            )
            model = _model
            formatted = f"passage: {text}"
            return model.encode(
                formatted,
                normalize_embeddings=True
            )
        else:
            # 다른 RuntimeError는 그대로 전달
            raise
