# app/run_basic_tests.py

from typing import Literal

from tts_service import speak
from stt_service import record_audio, speech_to_text
from rag_pipeline import build_rag_context_for_question

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

LANG_NAMES = {
    "ko": "Korean",
    "en": "English",
    "ja": "Japanese",
    "zh": "Chinese",
    "fr": "French",
    "es": "Spanish",
    "vi": "Vietnamese",
    "th": "Thai",
}

# ─────────────────────────────────────────────
#  언어별 고정 멘트 (하드코딩)
# ─────────────────────────────────────────────
PHRASES = {
    # TTS 테스트용
    "tts_test": {
        "ko": "안녕하세요, 저는 도리입니다. TTS 테스트 중입니다.",
        "en": "Hello, I am Dori. This is a TTS test.",
        "ja": "こんにちは、ドリです。TTSテスト中です。",
        "zh": "你好，我是多莉。现在正在进行语音测试。",
        "fr": "Bonjour, je suis Dori. Ceci est un test de synthèse vocale.",
        "es": "Hola, soy Dori. Esta es una prueba de síntesis de voz.",
        "vi": "Xin chào, tôi là Dori. Đây là bài kiểm tra TTS.",
        "th": "สวัสดี ฉันคือโดริ นี่คือการทดสอบเสียงพูด TTS",
    },
    # 웨이크워드 인식 후 첫 멘트
    "wake_ack": {
        "ko": "네, 무엇을 도와드릴까요?",
        "en": "Yes, how can I help you?",
        "ja": "はい、どのようにお手伝いしましょうか？",
        "zh": "好的，请问有什么可以帮您？",
        "fr": "Oui, que puis-je faire pour vous ?",
        "es": "Sí, ¿en qué puedo ayudarte?",
        "vi": "Vâng, tôi có thể giúp gì cho bạn?",
        "th": "ฉันช่วยอะไรคุณได้บ้าง?",
    },
    # Q&A 시작: 질문 있는지 물어보기
    "ask_any_question": {
        "ko": "이 장소에 대해 궁금한 점이 있으신가요?",
        "en": "Do you have any questions about this place?",
        "ja": "この場所について何か質問はありますか？",
        "zh": "关于这个地方，您有什么想问的吗？",
        "fr": "Avez-vous des questions sur cet endroit ?",
        "es": "¿Tienes alguna pregunta sobre este lugar?",
        "vi": "Bạn có câu hỏi nào về địa điểm này không?",
        "th": "คุณมีคำถามเกี่ยวกับสถานที่นี้ไหม?",
    },
    # 질문이 없을 때 다음 장소로
    "no_question_move_on": {
        "ko": "질문이 없으시면 다음 장소로 이동하겠습니다.",
        "en": "If you have no questions, I will move to the next spot.",
        "ja": "ご質問がなければ、次の場所へ移動します。",
        "zh": "如果您没有问题的话，我将带您前往下一个地点。",
        "fr": "S'il n'y a pas de question, je vous emmène au prochain point.",
        "es": "Si no hay preguntas, iré al siguiente punto.",
        "vi": "Nếu bạn không có câu hỏi, tôi sẽ di chuyển đến điểm tiếp theo.",
        "th": "ถ้าไม่มีคำถาม ฉันจะพาไปยังจุดถัดไปนะ",
    },
    # (옵션) 질문을 들었지만, 아직 답변 생성은 안 붙어있을 때
    "dummy_answer": {
        "ko": "질문은 잘 들었습니다. 지금은 답변 생성 기능을 준비 중입니다.",
        "en": "I heard your question. For now, the answer-generation function is still under development.",
        "ja": "ご質問はしっかり聞き取りました。現在、回答生成機能を準備中です。",
        "zh": "我已经听到您的问题，目前回答生成功能还在开发中。",
        "fr": "J'ai bien entendu votre question. Pour le moment, la génération de réponse est encore en cours de développement.",
        "es": "He escuchado tu pregunta. Por ahora, la función de generación de respuestas sigue en desarrollo.",
        "vi": "Tôi đã nghe câu hỏi của bạn. Hiện tại chức năng tạo câu trả lời vẫn đang được phát triển.",
        "th": "ฉันได้ยินคำถามของคุณแล้ว ตอนนี้ระบบสร้างคำตอบยังอยู่ระหว่างการพัฒนา",
    },
    # Q&A 마무리 멘트
    "end_qa": {
        "ko": "알겠습니다. 이제 다음 단계로 넘어가겠습니다.",
        "en": "Got it. I will move on to the next step.",
        "ja": "わかりました。それでは次のステップに進みます。",
        "zh": "好的，我现在带您进入下一步。",
        "fr": "Très bien. Je passe à l'étape suivante.",
        "es": "De acuerdo. Pasemos al siguiente paso.",
        "vi": "Được rồi. Chúng ta sẽ chuyển sang bước tiếp theo.",
        "th": "เข้าใจแล้ว ต่อไปเราจะไปขั้นตอนถัดไปกันนะ",
    },
}


def get_phrase(key: str, lang: LanguageCode) -> str:
    """
    고정 멘트를 언어에 맞게 가져오는 헬퍼.
    - 해당 언어 문구가 없으면 영어(en)로 fallback.
    """
    entry = PHRASES.get(key, {})
    if lang in entry:
        return entry[lang]
    if "en" in entry:
        return entry["en"]
    return key


# ─────────────────────────────────────────────
#  언어 선택
# ─────────────────────────────────────────────
def select_language() -> LanguageCode:
    """
    콘솔에서 언어를 선택하게 하는 간단한 메뉴.
    """
    print("=== 언어 선택 (Language Select) ===")
    for code, name in LANG_NAMES.items():
        print(f"- {code}: {name}")
    print()

    while True:
        choice = input("사용할 언어 코드를 입력하세요 (예: ko, en) : ").strip()
        if choice in LANG_NAMES:
            print(f"[LANG] {choice} ({LANG_NAMES[choice]}) 선택됨.\n")
            return choice  # type: ignore
        print("[LANG] 지원하지 않는 코드입니다. 다시 입력해주세요.")


# ─────────────────────────────────────────────
#  TEST 1: TTS 테스트
# ─────────────────────────────────────────────
def test_tts(user_lang: LanguageCode):
    """
    TTS가 잘 되는지 간단히 테스트.
    """
    print("=== [TEST 1] TTS 테스트 ===")
    text = get_phrase("tts_test", user_lang)
    print(f"[TTS] 다음 문장을 읽습니다: {text!r}")
    speak(text, lang=user_lang)
    print("[TTS] 재생 완료.\n")


# ─────────────────────────────────────────────
#  TEST 2: 웨이크워드 테스트 (처음 1번만)
# ─────────────────────────────────────────────
def test_wakeword_via_stt(user_lang: LanguageCode):
    """
    마이크로 'hey dori'를 말하면, STT로 인식해서
    소문자로 변환 후 'dori'가 들어가면 웨이크워드 성공으로 간주.
    (단순 버전)
    """
    print("=== [TEST 2] 웨이크워드 (hey dori) STT 테스트 ===")
    print("3초 동안 'hey dori' 라고 말해보세요. (영어 발음 권장)")
    input("준비되면 엔터를 눌러 녹음을 시작합니다...")

    audio = record_audio(seconds=3.0, sample_rate=16000)
    text = speech_to_text(audio_bytes=audio, lang="en", sample_rate=16000)

    print(f"[STT] 인식 결과: {text!r}")

    if text and "dori" in text.lower():
        print("[WAKEWORD] 인식 성공! (wakeword detected)\n")
        phrase = get_phrase("wake_ack", user_lang)
        speak(phrase, lang=user_lang)
    else:
        print("[WAKEWORD] 'hey dori'를 인식하지 못했습니다. (이번 데모에서는 한 번만 테스트합니다)\n")


# ─────────────────────────────────────────────
#  TEST 3: Q&A 흐름 (질문 여부 + RAG 컨텍스트 확인)
# ─────────────────────────────────────────────
def test_qa_with_rag(user_lang: LanguageCode):
    """
    Q&A 흐름 (질문 여부 + 음성 질문 + RAG 컨텍스트 확인)을
    선택한 언어 기반으로 시연.
    - 도리가: '질문 있으신가요?' (user_lang)
    - 사용자가 해당 언어로 질문
    - STT → 질문 텍스트 출력
    - RAG 컨텍스트 일부 출력
    - 도리가: '지금은 답변 생성 준비 중' + '다음 단계로 넘어갈게요'
    """
    print("=== [TEST 3] Q&A + RAG 데모 ===")

    # 1) 도리가 "질문 있으신가요?" 라고 해당 언어로 묻기
    ask_text = get_phrase("ask_any_question", user_lang)
    speak(ask_text, lang=user_lang)

    if user_lang == "ko":
        print("👉 이제 한국어로 경복궁에 대해 궁금한 점을 말해보세요.")
        print("   예: '경복궁은 언제 지어졌나요?'")
    elif user_lang == "en":
        print("👉 Now ask a question about Gyeongbokgung in English.")
        print("   e.g. 'When was Gyeongbokgung Palace built?'")
    elif user_lang == "ja":
        print("👉 景福宮について日本語で質問してみてください。")
        print("   例: 「景福宮はいつ建てられましたか？」")
    elif user_lang == "zh":
        print("👉 现在请用中文提出一个关于景福宫的问题。")
        print("   例如：“景福宫是什么时候建造的？”")
    else:
        print("👉 선택한 언어로 경복궁에 대해 궁금한 점을 말해보세요.")

    input("준비되면 엔터를 눌러 녹음을 시작합니다 (5초)...")

    # 2) 음성 녹음 & STT (선택한 언어 코드 그대로 사용)
    audio = record_audio(seconds=5.0, sample_rate=16000)
    question = speech_to_text(audio_bytes=audio, lang=user_lang, sample_rate=16000)

    print(f"[STT] 인식된 질문: {question!r}")

    if not question:
        # 질문이 없거나 인식 실패 → 다음 장소로 이동 멘트
        move_on_text = get_phrase("no_question_move_on", user_lang)
        speak(move_on_text, lang=user_lang)
        print("[RAG] 질문을 인식하지 못했습니다. (질문 없음으로 처리)\n")
        return

    # 3) RAG 컨텍스트 조회 (현재는 영어 knowledge_docs 기준)
    print("[RAG] 컨텍스트를 조회하는 중입니다...")
    context = build_rag_context_for_question(
        question=question,
        place_id="gyeongbokgung",
        language="en",  # knowledge_docs가 영어 기준이라 일단 en 고정
    )

    if not context:
        print("[RAG] 관련 컨텍스트를 찾지 못했습니다.\n")
    else:
        print("\n[RAG] 이 질문에 대해 참고할 지식 일부입니다:")
        print("--------------------------------------------------")
        print(context[:600])
        print("--------------------------------------------------\n")

    # 4) 아직 LLM 연결 전이므로, 데모용 멘트로 마무리
    dummy = get_phrase("dummy_answer", user_lang)
    speak(dummy, lang=user_lang)

    end_qa = get_phrase("end_qa", user_lang)
    speak(end_qa, lang=user_lang)


# ─────────────────────────────────────────────
#  메인
# ─────────────────────────────────────────────
def main():
    print("########################################")
    print("#   DORI 기본 기능 테스트 (No LLM)     #")
    print("########################################\n")

    user_lang = select_language()

    # 1) TTS 테스트
    test_tts(user_lang)

    # 2) 웨이크워드 테스트 (한 번)
    test_wakeword_via_stt(user_lang)

    # 3) Q&A + RAG 흐름 (질문 여부 → RAG 컨텍스트)
    test_qa_with_rag(user_lang)

    print("=== 모든 기본 테스트가 종료되었습니다. ===")


if __name__ == "__main__":
    main()
