# faiss_retriever.py

import numpy as np
import faiss
from typing import List, Optional

from embedding_client import EmbeddingClient
from db_utils import get_knowledge_docs_by_ids


INDEX_PATH = "faiss_index_en.bin"
IDS_PATH = "faiss_ids_en.npy"
DEFAULT_EMBEDDING_MODEL = "intfloat/e5-small-v2, thenlper/gte-small"


class FaissRetriever:
    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        index_path: str = INDEX_PATH,
        ids_path: str = IDS_PATH,
        top_k: int = 5,
    ):
        self.model_name = model_name
        self.top_k = top_k

        self.client = EmbeddingClient(model_name=model_name)

        self.index = faiss.read_index(index_path)
        self.ids = np.load(ids_path)

    def retrieve(
        self,
        question: str,
        place_id: Optional[str] = None,
        language: str = "en",
    ) -> List[dict]:
        """
        question을 임베딩한 뒤 FAISS에서 top_k개 문서를 가져오고,
        필요시 place_id로 한 번 더 필터링.
        """
        q_emb = self.client.embed_queries([question])[0]
        query = np.array([q_emb], dtype="float32")

        scores, idxs = self.index.search(query, self.top_k)
        selected_ids = self.ids[idxs[0]]

        docs = get_knowledge_docs_by_ids(selected_ids.tolist())

        if place_id is not None:
            docs = [d for d in docs if d["place_id"] == place_id]

        return docs
