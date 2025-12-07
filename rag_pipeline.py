# rag_pipeline.py

from faiss_retriever import FaissRetriever
from db_utils import get_scripts_for_spot_code


retriever = FaissRetriever(
    model_name="intfloat/e5-small-v2, thenlper/gte-small",
    top_k=5,
)


def build_spot_intro_text(spot_code: str, language: str = "en") -> str:
    """
    스팟 도착 시 TTS로 읽어줄 소개 멘트 (scripts 기반)
    현재는 scripts.text_en을 사용하고, language 파라미터는 향후 번역 레이어에서 사용 예정.
    """
    scripts = get_scripts_for_spot_code(spot_code)
    paragraphs = [s["text_en"] for s in scripts]
    return "\n\n".join(paragraphs)


def build_rag_context_for_question(
    question: str,
    place_id: str = "gyeongbokgung",
    language: str = "en",
) -> str:
    """
    사용자의 질문과 place_id를 기반으로,
    FAISS에서 관련 knowledge_docs를 찾고 context 텍스트를 구성.
    """
    docs = retriever.retrieve(
        question=question,
        place_id=place_id,
        language=language,
    )

    if not docs:
        return ""

    parts = []
    for d in docs:
        prefix = ""
        if d.get("source_type"):
            prefix += f"[source: {d['source_type']}] "
        if d.get("source_ref"):
            prefix += f"[ref: {d['source_ref']}] "
        parts.append(prefix + d["text"])

    return "\n\n".join(parts)


def build_llm_prompt_for_qa(
    spot_code: str,
    user_question: str,
    place_id: str = "gyeongbokgung",
    language: str = "en",
) -> str:
    """
    LLM에게 넘길 전체 프롬프트를 생성.
    """
    context = build_rag_context_for_question(
        question=user_question,
        place_id=place_id,
        language=language,
    )

    system_part = (
        "You are a tour guide robot for Gyeongbokgung Palace. "
        "Answer the visitor's question based ONLY on the given context. "
        "If the information is not in the context, honestly say that you do not know.\n"
    )

    prompt = (
        f"{system_part}\n"
        f"[Context Start]\n{context}\n[Context End]\n\n"
        f"[User Question]\n{user_question}\n\n"
        f"[Answer]\n"
    )
    return prompt
