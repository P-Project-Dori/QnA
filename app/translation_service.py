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
    자연스럽고 자연스러운 번역을 위해 개선됨.
    """
    if src == tgt:
        return text

    src_name = SUPPORTED_LANGUAGES[src]
    tgt_name = SUPPORTED_LANGUAGES[tgt]

    return (
        "You are a professional multilingual tour guide translator.\n"
        f"Translate the following tour guide script from {src_name} to {tgt_name}.\n\n"
        "TRANSLATION GUIDELINES:\n"
        "- Translate naturally and fluently, as if speaking to a tourist\n"
        "- Preserve all place names, proper nouns, and historical terms exactly\n"
        "- Maintain the original tone and style (informative but friendly)\n"
        "- Do not add explanations, comments, or extra sentences\n"
        "- Keep the same sentence structure when possible\n"
        "- Ensure the translation sounds natural in the target language\n\n"
        "[Source Text]\n"
        f"{text}\n\n"
        f"[Natural Translation in {tgt_name}]\n"
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
    자연스럽고 정확한 번역을 위해 개선됨.
    """
    if tgt == "en":
        return text

    tgt_name = SUPPORTED_LANGUAGES[tgt]

    return (
        "You are a professional tour guide translator.\n"
        f"Translate the following answer from English to {tgt_name}.\n\n"
        "TRANSLATION GUIDELINES:\n"
        "- Use a polite, friendly, and natural tone\n"
        "- Preserve all place names, proper nouns, and historical terms exactly\n"
        "- Keep the meaning and nuance exactly the same\n"
        "- Make it sound natural in the target language\n"
        "- Do not add extra sentences or explanations\n"
        "- Maintain the same level of formality\n\n"
        "[Answer in English]\n"
        f"{text}\n\n"
        f"[Natural Translation in {tgt_name}]\n"
    )


def translate(text: str, src: LanguageCode, tgt: LanguageCode) -> str:
    """
    일반 텍스트 번역(안내 멘트, 설명 등)에 사용.
    자연스럽고 정확한 번역을 위해 개선된 프롬프트 사용.
    """
    if src == tgt:
        return text

    prompt = _build_translation_prompt(text, src, tgt)
    # Slightly higher token limit for better translation quality
    result = call_llm(prompt, temperature=0.3, max_tokens=256)
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
    자연스럽고 정확한 번역을 위해 개선된 프롬프트 사용.
    """
    if tgt == "en":
        return answer_en

    prompt = _build_answer_from_en_prompt(answer_en, tgt)
    # Slightly higher token limit for better translation quality
    result = call_llm(prompt, temperature=0.3, max_tokens=256)
    return result.strip()
