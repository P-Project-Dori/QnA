from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    """
    - 여러 개일 때는 각 모델에서 나온 임베딩을 L2 normalize 한 뒤
      feature dimension 방향으로 concat 해서 사용.
      (index 만들 때와 질의할 때 항상 동일한 설정을 사용해야 함)
    """
    def __init__(self, model_name: str = "intfloat/e5-small-v2, thenlper/gte-small"):
        self.model_name = model_name
        # "a, b" 형태도 허용
        names = [n.strip() for n in model_name.split(",")]
        self.models = [SentenceTransformer(n) for n in names]

    def _encode(self, texts: List[str], is_query: bool, show_progress_bar: bool):
        # e5 계열에서 추천하는 "query: " / "passage: " 프리픽스 사용
        # gte-small에도 크게 문제 없이 동작하므로 그대로 사용
        if is_query:
            processed = [f"query: {t}" for t in texts]
        else:
            processed = [f"passage: {t}" for t in texts]

        all_embs = []
        for m in self.models:
            e = m.encode(
                processed,
                normalize_embeddings=True,
                show_progress_bar=show_progress_bar,
            )
            all_embs.append(e)

        if len(all_embs) == 1:
            return all_embs[0]

        # (N, d1), (N, d2) -> (N, d1 + d2)
        return np.concatenate(all_embs, axis=1)

    def embed_passages(self, texts: List[str]):
        """문서/패시지용 임베딩"""
        return self._encode(texts, is_query=False, show_progress_bar=True)

    def embed_queries(self, texts: List[str]):
        """질문용 임베딩"""
        return self._encode(texts, is_query=True, show_progress_bar=False)
