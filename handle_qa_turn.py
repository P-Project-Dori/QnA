# multilingual_orchestrator.py

from typing import Literal
from rag_pipeline import build_spot_intro_text
from translation_service import translate, LanguageCode
from tts_service import speak


def speak_spot_intro(spot_code: str, user_lang: LanguageCode):
    """
    - DB에서 영어 안내 스크립트 가져오기
    - 사용자 언어로 번역
    - TTS로 읽기
    """
    text_en = build_spot_intro_text(spot_code)  # 영어
    text_user = translate(text_en, src="en", tgt=user_lang)
    speak(text_user, lang=user_lang)

from stt_service import speech_to_text
from translation_service import translate
from rag_pipeline import build_llm_prompt_for_qa
from llm_client import call_llm


def handle_qa_turn(
    audio_bytes: bytes,
    user_lang: LanguageCode,
    spot_code: str,
    place_id: str = "gyeongbokgung",
):
    """
    한 번의 Q&A 턴 처리:
      - 음성 → (STT) → user_lang 텍스트
      - user_lang 질문 → 영어로 번역
      - 영어 질문 → RAG + LLM → 영어 답변
      - 영어 답변 → user_lang 번역
      - user_lang 답변 → TTS
    """
    # 1. 음성 → 텍스트 (user_lang)
    question_user = speech_to_text(audio_bytes, lang=user_lang)

    # (혹시 공백이면 그냥 종료할 수도 있음)
    question_user = question_user.strip()
    if not question_user:
        return

    # 2. user_lang → 영어
    question_en = translate(question_user, src=user_lang, tgt="en")

    # 3. 영어 RAG + LLM
    prompt = build_llm_prompt_for_qa(
        spot_code=spot_code,
        user_question=question_en,
        place_id=place_id,
        language="en",
    )
    answer_en = call_llm(prompt).strip()

    # 4. 영어 → user_lang
    answer_user = translate(answer_en, src="en", tgt=user_lang)

    # 5. TTS
    speak(answer_user, lang=user_lang)
