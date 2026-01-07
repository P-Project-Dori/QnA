# faiss_retriever.py

import faiss
import numpy as np
import json
from embedding_client import embed_query

class FaissRetriever:
    def __init__(self, index_path="faiss_index_en.bin", ids_path="faiss_ids_en.npy", top_k=5):
        print("🔵 Loading FAISS index ...")
        self.index = faiss.read_index(index_path)
        self.doc_ids = np.load(ids_path, allow_pickle=True)
        self.top_k = top_k
        self.dim = self.index.d

    def _fit_dim(self, vec: np.ndarray) -> np.ndarray:
        """
        Adjust embedding dimension to match FAISS index:
        - Truncate if vector is larger than index dimension
        - Zero-pad if smaller
        """
        if vec.shape[0] == self.dim:
            return vec
        if vec.shape[0] > self.dim:
            return vec[: self.dim]
        padded = np.zeros(self.dim, dtype=vec.dtype)
        padded[: vec.shape[0]] = vec
        return padded

    def search(self, question: str):
        """
        Search FAISS index and return knowledge_doc IDs.
        Returns: list of integer document IDs
        """
        query_emb_raw = embed_query(question).astype("float32")
        query_emb = self._fit_dim(query_emb_raw)[None, :]
        scores, idxs = self.index.search(query_emb, self.top_k)

        # Extract document IDs from the stored array
        doc_ids = []
        for idx in idxs[0]:
            # self.doc_ids is an array of integers (knowledge_doc.id)
            doc_id = int(self.doc_ids[idx])
            doc_ids.append(doc_id)

        return doc_ids
