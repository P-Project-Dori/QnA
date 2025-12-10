# build_faiss_index.py

import faiss
import numpy as np
from embedding_client import embed_passage
from db_utils import fetch_all_knowledge_docs  # 너희 DB에 있는 함수라고 가정

INDEX_OUT = "faiss_index_en.bin"
IDS_OUT = "faiss_ids_en.npy"


def build_index():
    docs = fetch_all_knowledge_docs()  
    """
    docs = [
        {
            "id": ...,
            "spot_code": "...",
            "text_en": "...",
        }
    ]
    """

    print(f"🔵 Embedding {len(docs)} knowledge documents...")

    embeddings = []
    id_list = []

    for doc in docs:
        vec = embed_passage(doc["text_en"])
        embeddings.append(vec)
        id_list.append(doc)

    embeddings = np.array(embeddings).astype("float32")

    print("🔵 Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print("🔵 Saving FAISS index...")
    faiss.write_index(index, INDEX_OUT)
    np.save(IDS_OUT, np.array(id_list, dtype=object))

    print("✅ Done.")


if __name__ == "__main__":
    build_index()
