# main_tour_loop.py

import time
from tour_route import TOUR_ROUTE
from stt_service import listen_for_seconds
from tts_service import speak
from llm_client import call_llm
from wakeword_service import is_wakeword, wakeword_label

# ─────────────────────────────────────────────
#  언어별 고정 멘트 & 스크립트
# ─────────────────────────────────────────────
PHRASES = {
    "arrived": {
        "ko": "{spot_name}에 도착했습니다.",
        "en": "We have arrived at {spot_name}.",
    },
    "next_move": {
        "ko": "다음 장소로 이동합니다.",
        "en": "Moving to the next spot.",
    },
    "tour_start_welcome": {
        "ko": "안녕하세요! 도리 투어에 오신 것을 환영합니다.",
        "en": "Hello! Welcome to the Dori tour.",
    },
    "tour_start_move": {
        "ko": "그럼 이제 첫 번째 장소로 이동하겠습니다.",
        "en": "Let's move to the first spot.",
    },
    "tour_end": {
        "ko": "모든 투어가 끝났습니다. 함께해주셔서 감사합니다!",
        "en": "The tour is finished. Thank you for joining!",
    },
    "intro_arrival": {
        "ko": "다음 장소에 도착했습니다.",
        "en": "We have reached the next spot.",
    },
    "qa_intro": {
        "ko": "설명이 끝났습니다. 질문이 있으신가요? 있으시면 말씀해주세요. 없으시면 ‘패스’라고 말해주셔도 좋아요.",
        "en": "That concludes the explanation. Do you have any questions? If not, you can say 'pass'.",
    },
    "qa_silence": {
        "ko": "말씀이 없으셔서 다음 장소로 이동하겠습니다.",
        "en": "No response, so we'll move to the next spot.",
    },
    "qa_pass": {
        "ko": "알겠습니다. 다음 장소로 이동할게요.",
        "en": "Okay. We will move to the next spot.",
    },
    "qa_more": {
        "ko": "추가로 궁금하신 점 있으신가요?",
        "en": "Any other questions?",
    },
    "photo_intro": {
        "ko": "이곳은 경회루입니다. 사진이 아주 잘 나오는 장소예요!",
        "en": "This is Gyeonghoeru. It's a great place for photos!",
    },
    "photo_prompt": {
        "ko": "사진을 찍어드릴까요? 준비되시면 ‘찍어줘’라고 말해주세요.",
        "en": "Shall I take a photo for you? Say 'take a photo' when ready.",
    },
    "photo_shot": {
        "ko": "좋아요! 3초 뒤에 찍을게요. 하나, 둘, 셋… 찰칵!",
        "en": "Great! I'll take it in 3 seconds. One, two, three... click!",
    },
    "photo_saved": {
        "ko": "사진이 저장되었습니다! 나중에 받아가실 수 있어요.",
        "en": "Photo saved! You can get it later.",
    },
    "photo_skip": {
        "ko": "말씀이 없으셔서 사진 촬영은 생략할게요.",
        "en": "No response, so I'll skip the photo.",
    },
}


# 간단한 spot 설명 스크립트 (하드코딩, ko/en만)
SPOT_SCRIPTS = {
    "ko": {
        "gwanghwamun": [
            "광화문은 경복궁의 정문으로, 조선 왕조의 위엄을 상징합니다.",
            "임진왜란과 한국전쟁을 거치며 여러 차례 훼손과 복원을 반복했습니다.",
        ],
        "heungnyemun": [
            "흥례문은 광화문을 지나 경복궁으로 들어오는 두 번째 문입니다.",
            "왕실 의식이 진행될 때 신하들이 대기하던 공간과 맞닿아 있습니다.",
        ],
        "geunjeongmun": [
            "근정문은 근정전 앞마당으로 들어가는 문으로, 공식 조회의 입구였습니다.",
        ],
        "geunjeongjeon": [
            "근정전은 국왕이 정사를 보던 정전으로, 경복궁의 중심 건물입니다.",
            "이곳에서 즉위식과 외국 사신 접견 같은 국가 의례가 열렸습니다.",
        ],
        "sujeongjeon": [
            "수정전은 왕과 신하들이 학문과 정치에 대해 토론하던 장소였습니다.",
        ],
        "gyeonghoeru": [
            "경회루는 연못 위에 세워진 누각으로, 연회와 외국 사신 접대를 위해 사용되었습니다.",
        ],
    },
    "en": {
        "gwanghwamun": [
            "Gwanghwamun is the main gate of Gyeongbokgung Palace, symbolizing the authority of the Joseon dynasty.",
            "It was damaged and restored multiple times through the Imjin War and the Korean War.",
        ],
        "heungnyemun": [
            "Heungnyemun is the second gate after Gwanghwamun when entering Gyeongbokgung.",
            "It connects to spaces where officials waited during royal ceremonies.",
        ],
        "geunjeongmun": [
            "Geunjeongmun is the gate leading to the main courtyard of Geunjeongjeon, used for official audiences.",
        ],
        "geunjeongjeon": [
            "Geunjeongjeon is the main throne hall where the king handled state affairs.",
            "Coronations and receptions for foreign envoys took place here.",
        ],
        "sujeongjeon": [
            "Sujeongjeon was a hall where the king and officials discussed studies and politics.",
        ],
        "gyeonghoeru": [
            "Gyeonghoeru is a pavilion built over a pond, used for banquets and receptions of foreign envoys.",
        ],
    },
}


# ===========================================================
# 1) 스팟 스크립트 읽기
# ===========================================================
def run_spot_intro(spot_code, lang):
    """
    spot_code에 해당하는 설명 스크립트를 DB에서 가져와 TTS로 읽는다.
    """
    scripts = SPOT_SCRIPTS.get(lang, {}).get(spot_code) or SPOT_SCRIPTS["en"].get(spot_code, [])

    speak(PHRASES["intro_arrival"][lang], lang)
    time.sleep(0.3)

    for text in scripts:
        speak(text, lang)
        time.sleep(0.3)

        # 간단한 인터럽트: 말 사이에 웨이크워드 감지 시 Q&A 처리 후 이어서 진행
        if _check_wakeword_inline(lang):
            _handle_inline_question(spot_code, lang)
            # 이어서 남은 스크립트 계속
        time.sleep(0.2)


# ===========================================================
# 2) 스팟 Q&A 세션
# ===========================================================
def run_qa_session(spot_code, lang):
    """
    질문 → RAG → LLM → TTS
    - 질문이 없거나 '패스' 계열 → 자동 이동
    - 질문 있으면 답변하고 "추가 질문 있으신가요?" 반복
    """
    speak(PHRASES["qa_intro"][lang], lang)

    while True:
        print("🎙 STT 대기중... (최대 10초)")
        user_text = listen_for_seconds(lang=lang, seconds=10)

        # --- 10초 동안 아무 말 없으면 ---
        if not user_text:
            speak(PHRASES["qa_silence"][lang], lang)
            return

        normalized = user_text.lower().strip()

        # --- '패스' 계열 발화 처리 ---
        PASS_WORDS = ["패스", "없어", "괜찮아", "pass", "no", "없습니다", "아니오"]
        if any(p in normalized for p in PASS_WORDS):
            speak(PHRASES["qa_pass"][lang], lang)
            return

        # --- 질문 있다고 판단되면 RAG + LLM ---
        print(f"사용자 질문: {normalized}")

        prompt = (
            "You are Dori, a concise multilingual tour guide robot. "
            "Answer the user's question directly and briefly in the user's language. "
            "If unsure, say you do not have that information.\n\n"
            f"[User question ({lang})]\n{normalized}\n\n"
            f"[Answer in {lang}]:"
        )
        answer = call_llm(prompt).strip()

        speak(answer, lang)
        time.sleep(0.3)

        # --- 추가 질문 유도 ---
        speak(PHRASES["qa_more"][lang], lang)


# ===========================================================
# 3) 마지막 스팟 — 사진 촬영 모드
# ===========================================================
def run_photo_mode(lang):
    speak(PHRASES["photo_intro"][lang], lang)
    speak(PHRASES["photo_prompt"][lang], lang)

    user_text = listen_for_seconds(lang=lang, seconds=10)

    if user_text and ("찍어" in user_text or "photo" in user_text.lower()):
        speak(PHRASES["photo_shot"][lang], lang)

        # TODO: 실제 카메라 촬영 코드 연결
        # capture_photo()

        speak(PHRASES["photo_saved"][lang], lang)
    else:
        speak(PHRASES["photo_skip"][lang], lang)


# ===========================================================
# 4) 전체 투어 루프
# ===========================================================
def start_dori_tour(lang="ko"):
    """
    도리의 전체 투어 엔진
    """
    speak(PHRASES["tour_start_welcome"][lang], lang)
    time.sleep(0.3)
    speak(PHRASES["tour_start_move"][lang], lang)
    time.sleep(0.5)

    for spot in TOUR_ROUTE:
        spot_code = spot["spot_code"]
        spot_name = spot.get(f"name_{lang}", spot["name_en"])
        is_photo_spot = spot.get("is_photo_spot", False)

        # 스팟 이름 멘트
        speak(PHRASES["arrived"][lang].format(spot_name=spot_name), lang)

        # 스팟 설명 읽기
        run_spot_intro(spot_code, lang)

        # Q&A
        run_qa_session(spot_code, lang)

        # 사진 스팟이면 사진 모드 실행
        if is_photo_spot:
            run_photo_mode(lang)

        speak(PHRASES["next_move"][lang], lang)
        time.sleep(1)

    speak(PHRASES["tour_end"][lang], lang)


# ===========================================================
# 5) 인라인 웨이크워드 인터럽트 핸들러
# ===========================================================
def _check_wakeword_inline(lang: str) -> bool:
    """
    짧게 STT를 돌려 웨이크워드가 들렸는지 확인.
    - 2초 청취, 선택된 언어 코드 사용
    """
    text = listen_for_seconds(lang=lang, seconds=2)
    if not text:
        return False
    print(f"[WakeWord-inline] captured: {text}")
    return is_wakeword(text, lang)


def _handle_inline_question(spot_code: str, lang: str):
    """
    웨이크워드로 인터럽트된 경우 한 번의 질문에 답하고 스크립트를 이어감.
    """
    speak(PHRASES["qa_intro"][lang], lang)

    user_text = listen_for_seconds(lang=lang, seconds=6)
    if not user_text:
        speak(PHRASES["qa_silence"][lang], lang)
        return

    normalized = user_text.strip()
    print(f"[Q&A-inline] question: {normalized}")

    prompt = (
        "You are Dori, a concise multilingual tour guide robot. "
        "Answer the user's question directly and briefly in the user's language. "
        "If unsure, say you do not have that information.\n\n"
        f"[User question ({lang})]\n{normalized}\n\n"
        f"[Answer in {lang}]:"
    )
    answer = call_llm(prompt).strip()
    speak(answer, lang)

    # 안내 멘트 후 스크립트로 복귀
    speak(PHRASES["qa_more"][lang], lang)


# 별칭: 기존 코드 호환
def run_tour(user_lang="ko", place_id="gyeongbokgung", qa_record_seconds=10.0, max_qa_turns=3):
    """
    Wrapper for legacy import compatibility.
    """
    return start_dori_tour(lang=user_lang)
