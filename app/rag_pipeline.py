# rag_pipeline.py

from faiss_retriever import FaissRetriever
from db_utils import get_scripts_for_spot_code, get_knowledge_docs_by_ids
from config import ENABLE_RAG

# ============================================================================
# RAG Retriever Initialization
# ============================================================================
# FAISS retriever is initialized here but will only be used when ENABLE_RAG = True
# When RAG is disabled, this retriever won't be called, saving resources
# ============================================================================
retriever = FaissRetriever(
    index_path="faiss_index_en.bin",
    ids_path="faiss_ids_en.npy",
    top_k=5,
)


def build_rag_context(question: str, spot_code=None):
    """
    RAG용 컨텍스트 생성
    
    Args:
        question: 사용자 질문
        spot_code: 스팟 코드 (필터링용, 현재 미구현)
    
    Returns:
        RAG 컨텍스트 문자열 (RAG가 비활성화되어 있거나 오류 발생 시 빈 문자열)
    
    Process:
        1) ENABLE_RAG 플래그 확인
        2) FAISS로 문서 검색 (knowledge_doc IDs 반환)
        3) DB에서 실제 문서 가져오기
        4) spot_code 필터링 (있을 경우, 향후 구현)
    
    Error Handling:
        - RAG 오류 발생 시 빈 문자열 반환하여 LLM-only 모드로 자동 전환
        - CUDA 메모리 오류, 임베딩 모델 오류 등 모든 예외 처리
    """
    # ========================================================================
    # RAG TOGGLE CHECK: If RAG is disabled, return empty context
    # ========================================================================
    if not ENABLE_RAG:
        print("ℹ️  [RAG] RAG is disabled (ENABLE_RAG = False)")
        return ""
    
    # ========================================================================
    # RAG ENABLED: Proceed with context retrieval (with error handling)
    # ========================================================================
    try:
        # FAISS 검색으로 knowledge_doc IDs 얻기
        doc_ids = retriever.search(question)
        print(f"🔍 [RAG] Retrieved {len(doc_ids)} document IDs: {doc_ids}")
        
        # DB에서 실제 문서 가져오기
        if not doc_ids:
            print("⚠️  [RAG] No documents found for query")
            return ""
        
        docs = get_knowledge_docs_by_ids(doc_ids)
        print(f"🔍 [RAG] Retrieved {len(docs)} documents from database")

        # spot_code 필터링이 필요한 경우
        # spot_id로 필터링하려면 spots 테이블과 조인 필요
        # 현재는 모든 검색된 문서를 사용 (향후 spot_code 필터링 개선 가능)
        # TODO: spot_code로 필터링하려면 spots 테이블 조인 필요

        # text 필드 추출 (knowledge_docs는 'text' 필드 사용)
        texts = []
        for d in docs:
            if isinstance(d, dict) and "text" in d:
                texts.append(d["text"])
        
        context_blob = "\n\n".join(texts)
        print(f"📝 [RAG] Context length: {len(context_blob)} characters")
        return context_blob
    
    except Exception as e:
        # RAG 오류 발생 시 LLM-only 모드로 자동 전환
        print(f"⚠️  RAG 오류 발생 (LLM-only 모드로 전환): {type(e).__name__}: {e}")
        return ""


def build_spot_intro_text(spot_code: str, language: str = "en") -> str:
    """
    DB에서 spot_code에 해당하는 스크립트를 가져와서 하나의 텍스트로 합침.
    """
    scripts = get_scripts_for_spot_code(spot_code)
    
    if not scripts:
        return ""
    
    # text_en 필드에서 텍스트 추출
    texts = [s["text_en"] for s in scripts]
    return " ".join(texts)


def _truncate_to_two_sentences(text: str) -> str:
    """
    답변을 최대 2문장으로 제한하는 안전장치.
    """
    import re
    if not text or not text.strip():
        return text
    
    # 문장 구분자로 분리 (. ! ?)
    # 패턴: 문장 끝 구분자(. ! ?)와 그 뒤의 공백을 포함
    sentences = re.split(r'([.!?]+\s*)', text)
    
    # 구분자와 문장을 다시 결합하여 최대 2문장만 추출
    result = []
    i = 0
    while i < len(sentences) and len(result) < 2:
        sentence_part = sentences[i].strip()
        if sentence_part:
            # 다음 요소가 구분자면 결합
            if i + 1 < len(sentences):
                full_sentence = sentence_part + sentences[i + 1]
                result.append(full_sentence.strip())
                i += 2
            else:
                result.append(sentence_part)
                i += 1
        else:
            i += 1
    
    if result:
        return ' '.join(result).strip()
    return text.strip()


def _is_potentially_unclear(question: str) -> bool:
    """
    Detect if a question might be unclear or mis-transcribed.
    This helps the LLM handle ASR errors better.
    """
    if not question or len(question.strip()) < 3:
        return True
    
    # Check for common ASR error patterns
    import re
    
    # Very short questions might be incomplete
    words = question.split()
    if len(words) < 2:
        return True
    
    # Check for excessive non-alphanumeric characters
    non_alnum_ratio = len(re.sub(r'[a-zA-Z0-9가-힣\s]', '', question)) / max(len(question), 1)
    if non_alnum_ratio > 0.3:
        return True
    
    # Check for words that look like gibberish (very long words, repeated patterns)
    for word in words:
        if len(word) > 20:  # Unusually long word
            return True
        if re.search(r'(.)\1{4,}', word):  # Excessive character repetition
            return True
    
    return False


def build_llm_prompt_for_qa(
    spot_code: str,
    user_question: str,
    place_id: str = "gyeongbokgung",
    language: str = "en",
) -> str:
    """
    RAG 컨텍스트를 포함한 LLM 프롬프트 생성.
    항상 영어로 답변하도록 요청 (번역은 별도로 처리).
    
    Args:
        spot_code: 스팟 코드
        user_question: 사용자 질문 (영어)
        place_id: 장소 ID
        language: 언어 코드 (현재 미사용, 항상 영어로 답변)
    
    Returns:
        LLM 프롬프트 문자열
        
    Note:
        - ENABLE_RAG가 True이면 RAG 컨텍스트를 포함한 프롬프트 생성
        - ENABLE_RAG가 False이면 컨텍스트 없이 일반 프롬프트 생성
        - Unclear transcriptions are automatically detected and handled
    """
    # Check if question might be unclear
    is_unclear = _is_potentially_unclear(user_question)
    # ========================================================================
    # RAG CONTEXT RETRIEVAL
    # ========================================================================
    # build_rag_context() will return empty string if ENABLE_RAG = False
    # This allows seamless switching between RAG and non-RAG modes
    context = build_rag_context(user_question, spot_code=spot_code)
    
    # ========================================================================
    # PROMPT GENERATION: RAG Mode (with context)
    # ========================================================================
    if context:
        print(f"✅ [RAG] Using RAG mode with context ({len(context)} chars)")
        # RAG is enabled and context was successfully retrieved
        unclear_instruction = ""
        if is_unclear:
            unclear_instruction = (
                "\nIMPORTANT: The user's question may be unclear or mis-transcribed due to speech recognition errors.\n"
                "- If the question doesn't make sense, try to interpret it in the context of Gyeongbokgung Palace.\n"
                "- If you cannot understand the question at all, say: 'I didn't catch that. Could you please repeat your question?'\n"
                "- Otherwise, answer based on what you think the user might be asking about.\n"
            )
        
        prompt = (
            "You are Dori, a multilingual tour guide robot.\n"
            "PREFER the given context to answer the user's question, but if the answer is not in the context, use your general knowledge to answer.\n"
            "CRITICAL RULES:\n"
            "- Answer in exactly 2 sentences or less\n"
            "- Include ONLY the most essential information\n"
            "- Stop immediately after answering - do not add any additional sentences\n"
            "- First try to answer using the provided context\n"
            "- If the answer is not in the context, use your general knowledge to provide an answer\n"
            "- Answer in English"
            + unclear_instruction +
            "\n\n"
            f"[Context]\n{context}\n\n"
            f"[Question]\n{user_question}\n\n"
            "[Answer in English (2 sentences max, essential info only)]:"
        )
    # ========================================================================
    # PROMPT GENERATION: Non-RAG Mode (without context)
    # ========================================================================
    else:
        # Either RAG is disabled (ENABLE_RAG = False) or no context was found
        # In this mode, LLM relies on its general knowledge
        print(f"ℹ️  [RAG] Using non-RAG mode (no context)")
        unclear_instruction = ""
        if is_unclear:
            unclear_instruction = (
                "\nIMPORTANT: The user's question may be unclear or mis-transcribed due to speech recognition errors.\n"
                "- If the question doesn't make sense, try to interpret it in the context of Gyeongbokgung Palace.\n"
                "- If you cannot understand the question at all, say: 'I didn't catch that. Could you please repeat your question?'\n"
                "- Otherwise, answer based on what you think the user might be asking about.\n"
            )
        
        prompt = (
            "You are Dori, a multilingual tour guide robot.\n"
            "CRITICAL RULES:\n"
            "- Answer in exactly 2 sentences or less\n"
            "- Include ONLY the most essential information\n"
            "- Stop immediately after answering - do not add any additional sentences\n"
            "- If you don't know, say only: 'I don't have that information.'\n"
            "- Answer in English"
            + unclear_instruction +
            "\n\n"
            f"[Question]\n{user_question}\n\n"
            "[Answer in English (2 sentences max, essential info only)]:"
        )
    
    return prompt
