# translation_service.py

from typing import Literal
from llm_client import call_llm

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ko": "Korean",
    "ja": "Japanese",
    "zh": "Chinese",
    "fr": "French",
    "es": "Spanish",
    "vi": "Vietnamese",
    "th": "Thai",
}


def _build_translation_prompt(text: str, src: LanguageCode, tgt: LanguageCode) -> str:
    """
    일반적인 문장 번역용 프롬프트 (안내 멘트, 답변 등).
    """
    if src == tgt:
        return text

    src_name = SUPPORTED_LANGUAGES[src]
    tgt_name = SUPPORTED_LANGUAGES[tgt]

    return (
        "You are a professional multilingual tour guide translator.\n"
        f"Translate the following text from {src_name} to {tgt_name}.\n"
        "Do not add explanations, comments, or extra sentences.\n"
        "Preserve place names and proper nouns.\n\n"
        "[Source]\n"
        f"{text}\n\n"
        f"[Translation in {tgt_name}]\n"
    )


def _build_question_to_en_prompt(text: str, src: LanguageCode) -> str:
    """
    질문을 영어로 바꿀 때 사용하는 좀 더 안전한 프롬프트.
    """
    if src == "en":
        return text

    src_name = SUPPORTED_LANGUAGES[src]

    return (
        "You are a translator assistant.\n"
        f"Translate the following user question from {src_name} to English.\n"
        "Keep the meaning exactly the same.\n"
        "Do not answer the question. Output only the translated question.\n\n"
        "[User Question]\n"
        f"{text}\n\n"
        "[English Question]\n"
    )


def _build_answer_from_en_prompt(text: str, tgt: LanguageCode) -> str:
    """
    영어 답변을 사용자 언어로 번역할 때 사용하는 프롬프트.
    """
    if tgt == "en":
        return text

    tgt_name = SUPPORTED_LANGUAGES[tgt]

    return (
        "You are a tour guide translator.\n"
        "Translate the following answer from English to "
        f"{tgt_name} using a polite and friendly tone.\n"
        "Do not add extra sentences.\n\n"
        "[Answer in English]\n"
        f"{text}\n\n"
        f"[Answer in {tgt_name}]\n"
    )


def translate(text: str, src: LanguageCode, tgt: LanguageCode) -> str:
    """
    일반 텍스트 번역(안내 멘트, 설명 등)에 사용.
    """
    if src == tgt:
        return text

    prompt = _build_translation_prompt(text, src, tgt)
    result = call_llm(prompt)
    return result.strip()


def translate_question_to_en(user_question: str, src: LanguageCode) -> str:
    """
    사용자 질문을 영어로 번역.
    """
    if src == "en":
        return user_question

    prompt = _build_question_to_en_prompt(user_question, src)
    result = call_llm(prompt)
    return result.strip()


def translate_answer_from_en(answer_en: str, tgt: LanguageCode) -> str:
    """
    영어 답변을 사용자 언어로 번역.
    """
    if tgt == "en":
        return answer_en

    prompt = _build_answer_from_en_prompt(answer_en, tgt)
    result = call_llm(prompt)
    return result.strip()
