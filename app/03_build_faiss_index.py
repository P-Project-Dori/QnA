# 03_build_faiss_index.py

import numpy as np
import faiss

from db_utils import get_all_knowledge_docs
from embedding_client import embed_passage


INDEX_PATH = "faiss_index_en.bin"
IDS_PATH = "faiss_ids_en.npy"


def main():
    print("📥 Loading knowledge_docs (language='en')...")
    docs = get_all_knowledge_docs(language="en")

    if not docs:
        print("⚠️ No knowledge_docs found. Did you run 02_seed_knowledge_docs.py?")
        return

    texts = [d["text"] for d in docs]
    ids = np.array([d["id"] for d in docs], dtype="int64")

    print(f"🧠 Computing embeddings with: intfloat/e5-small-v2")
    embeddings = []
    for text in texts:
        vec = embed_passage(text)
        embeddings.append(vec)
    emb_mat = np.array(embeddings, dtype="float32")

    dim = emb_mat.shape[1]
    print(f"📐 Embedding dimension: {dim}")

    index = faiss.IndexFlatIP(dim)
    index.add(emb_mat)

    faiss.write_index(index, INDEX_PATH)
    np.save(IDS_PATH, ids)

    print(f"✅ FAISS index saved to {INDEX_PATH}")
    print(f"✅ Doc IDs saved to {IDS_PATH}")


if __name__ == "__main__":
    main()













