# rag_pipeline.py

from faiss_retriever import FaissRetriever

retriever = FaissRetriever(
    index_path="faiss_index_en.bin",
    ids_path="faiss_ids_en.npy",
    top_k=5,
)

def build_rag_context(question: str, spot_code=None):
    """
    RAG용 컨텍스트 생성
    1) FAISS로 문서 검색
    2) spot_code 필터링 (있을 경우)
    """
    docs = retriever.search(question)

    if spot_code:
        # 안전하게 dict 형태만 필터링
        docs = [d for d in docs if isinstance(d, dict) and d.get("spot_code") == spot_code]

    # text_en 추출도 dict만 대상으로 안전하게 처리
    texts = []
    for d in docs:
        if isinstance(d, dict) and "text_en" in d:
            texts.append(d["text_en"])
    context_blob = "\n\n".join(texts)

    return context_blob
