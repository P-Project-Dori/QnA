# multilingual_orchestrator.py

from typing import Literal

from translation_service import (
    LanguageCode,
    translate,
    translate_question_to_en,
    translate_answer_from_en,
)
from tts_service import speak
from stt_service import record_audio, speech_to_text
from rag_pipeline import (
    build_spot_intro_text,
    # build_rag_context_for_question,  # 필요하면 사용할 수 있음
    build_llm_prompt_for_qa,
)
from llm_client import call_llm


def speak_spot_intro(spot_code: str, user_lang: LanguageCode):
    """
    1) 영어 스크립트 생성 (DB 기반)
    2) 사용자 언어로 번역
    3) Google TTS로 읽기
    """
    # 1. 영어 안내 멘트 (이미 rag_pipeline에서 구현되어 있다고 가정)
    text_en = build_spot_intro_text(spot_code, language="en")

    # 2. 번역 (영어 → 사용자 언어)
    text_user = translate(text_en, src="en", tgt=user_lang)

    # 3. 음성 출력
    speak(text_user, lang=user_lang)


def handle_single_qa_turn(
    user_lang: LanguageCode,
    spot_code: str,
    place_id: str = "gyeongbokgung",
    record_seconds: float = 5.0,
) -> str:
    """
    한 번의 Q&A 턴(질문 1개 → 답변 1개)을 처리.

    흐름:
      1) 마이크에서 record_seconds 동안 녹음
      2) STT로 사용자 언어 텍스트 추출
      3) 사용자 언어 질문 → 영어로 번역
      4) 영어 질문 + RAG 컨텍스트로 LLM QA
      5) 영어 답변 → 사용자 언어로 번역
      6) TTS로 읽기

    반환값:
      - 최종 사용자 언어 답변 텍스트 (로그용)
    """
    # 1) 음성 녹음
    audio_bytes = record_audio(seconds=record_seconds, sample_rate=16000)

    # 2) STT (사용자 언어 텍스트)
    question_user = speech_to_text(audio_bytes, lang=user_lang, sample_rate=16000)
    question_user = question_user.strip()
    print(f"[Q&A] STT ({user_lang}) → '{question_user}'")

    if not question_user:
        # 아무 말도 안 했으면 그냥 빈 문자열 반환
        return ""

    # 3) 사용자 언어 질문 → 영어
    question_en = translate_question_to_en(question_user, src=user_lang)
    print(f"[Q&A] Translated to EN → '{question_en}'")

    # 4) RAG + LLM (영어)
    prompt = build_llm_prompt_for_qa(
        spot_code=spot_code,
        user_question=question_en,
        place_id=place_id,
        language="en",
    )
    answer_en = call_llm(prompt).strip()
    print(f"[Q&A] LLM answer (EN) → '{answer_en}'")

    # 5) 영어 답변 → 사용자 언어
    answer_user = translate_answer_from_en(answer_en, tgt=user_lang)
    print(f"[Q&A] Translated answer ({user_lang}) → '{answer_user}'")

    # 6) TTS
    speak(answer_user, lang=user_lang)

    return answer_user
