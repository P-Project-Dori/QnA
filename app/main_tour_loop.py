# main_tour_loop.py

import time
import re
from tour_route import TOUR_ROUTE
from stt_service import listen_for_seconds
from tts_service import speak
from llm_client import call_llm
from wakeword_service import is_wakeword, wakeword_label, _levenshtein_distance, _fuzzy_match
from rag_pipeline import build_llm_prompt_for_qa, _truncate_to_two_sentences
from translation_service import translate_question_to_en, translate_answer_from_en, translate, LanguageCode

# ─────────────────────────────────────────────
#  언어별 고정 멘트 & 스크립트
# ─────────────────────────────────────────────
PHRASES = {
    "arrived": {
        "ko": "{spot_name}에 도착했습니다.",
        "en": "We have arrived at {spot_name}.",
    },
    "tour_start_welcome": {
        "ko": "도리 투어에 오신 것을 환영합니다.",
        "en": "Welcome to the Dori tour.",
    },
    "tour_start_move": {
        "ko": "그럼 이제 첫 번째 장소로 이동하겠습니다.",
        "en": "Let's move to the first spot.",
    },
    "tour_end": {
        "ko": "모든 투어가 끝났습니다. 함께해주셔서 감사합니다!",
        "en": "The tour is finished. Thank you for joining!",
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
        "ko": "이곳은 사진이 아주 잘 나오는 장소예요. 사진을 찍어드리겠습니다!",
        "en": "This is a great photo spot. I'll take your picture!",
    },
    "photo_positioning": {
        "ko": "경회루가 잘 보이는 위치에 서주시면, 제가 적절한 위치로 이동해서 사진을 찍어드리겠습니다! 사진을 찍을 때는 저를 봐주세요!",
        "en": "If you stand in a spot with a good view of Gyeong-hoe-ru Pavilion, I'll move to take your picture so you're in the right spot! Please look at me when I take your picture!",
    },
    "photo_countdown": {
        "ko": "5초 뒤에 사진을 찍겠습니다! 웃어주세요~",
        "en": "I'll take your picture in five seconds! Smile~",
    },
    "photo_shot": {
        "ko": "찰칵!",
        "en": "Click!",
    },
    "photo_saved": {
        "ko": "사진이 저장되었습니다! 나중에 받아가실 수 있어요.",
        "en": "Photo saved! You can get it later.",
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
            "Gwang-wha-mun is the main gate of Gyeong-bok-gung Palace, symbolizing the authority of the Joseon dynasty.",
            "It was damaged and restored multiple times through the Imjin War and the Korean War.",
        ],
        "heungnyemun": [
            "Heung-nye-mun is the second gate after Gwang-wha-mun when entering Gyeong-bok-gung.",
            "It connects to spaces where officials waited during royal ceremonies.",
        ],
        "geunjeongmun": [
            "Geun-jeong-mun is the gate leading to the main courtyard of Geun-jeong-jeon, used for official audiences.",
        ],
        "geunjeongjeon": [
            "Geun-jeong-jeon is the main throne hall where the king handled state affairs.",
            "Coronations and receptions for foreign envoys took place here.",
        ],
        "sujeongjeon": [
            "Su-jeong-jeon was a hall where the king and officials discussed studies and politics.",
        ],
        "gyeonghoeru": [
            "Gyeong-hoe-ru is a pavilion built over a pond, used for banquets and receptions of foreign envoys.",
        ],
    },
}


# ===========================================================
# 1) 스팟 스크립트 읽기
# ===========================================================
def run_spot_intro(spot_code, lang):
    """
    spot_code에 해당하는 설명 스크립트를 하드코딩된 SPOT_SCRIPTS에서 가져와 TTS로 읽는다.
    """
    # 하드코딩된 스크립트 사용 (언어별로 직접 제공)
    scripts = SPOT_SCRIPTS.get(lang, {}).get(spot_code) or SPOT_SCRIPTS["en"].get(spot_code, [])
    
    for text in scripts:
        speak(text, lang)
        time.sleep(0.3)
        if _check_wakeword_inline(lang):
            _handle_inline_question(spot_code, lang)
        time.sleep(0.2)


# ===========================================================
# Proper noun normalization for Gyeongbokgung Palace
# ===========================================================
# Palace-related proper nouns with common variations
PALACE_PROPER_NOUNS = {
    "gwanghwamun": ["gwanghwamun", "gwanghwa mun", "gwang hwa mun", "kwanghwamun", "kwanghwa mun"],
    "heungnyemun": ["heungnyemun", "heung nye mun", "heungnye mun", "hungnyemun", "hung nye mun"],
    "geunjeongmun": ["geunjeongmun", "geun jeong mun", "geunjeong mun", "keunjeongmun", "keun jeong mun"],
    "geunjeongjeon": ["geunjeongjeon", "geun jeong jeon", "geunjeong jeon", "keunjeongjeon", "keun jeong jeon"],
    "sujeongjeon": ["sujeongjeon", "su jeong jeon", "sujeong jeon", "sujeongjeon", "su jeong jeon"],
    "gyeonghoeru": ["gyeonghoeru", "gyeong hoe ru", "gyeonghoe ru", "kyeonghoeru", "kyeong hoe ru"],
    "gyeongbokgung": ["gyeongbokgung", "gyeongbok gung", "gyeong bok gung", "kyeongbokgung", "kyeongbok gung"],
}


def _normalize_palace_proper_nouns(text: str, lang: str) -> str:
    """
    Normalize mispronounced palace proper nouns in the question text.
    Uses fuzzy matching to recognize similar pronunciations.
    """
    normalized_text = text
    text_lower = text.lower()
    
    # For each proper noun, check if any variation appears in the text
    for correct_name, variations in PALACE_PROPER_NOUNS.items():
        # Check for exact matches first (most common case)
        for variation in variations:
            if variation in text_lower:
                # Replace with correct name (case-insensitive)
                pattern = re.compile(re.escape(variation), re.IGNORECASE)
                normalized_text = pattern.sub(correct_name, normalized_text)
                if variation != correct_name:
                    print(f"🔍 Matched '{variation}' → '{correct_name}'")
                break
        else:
            # If no exact match, try fuzzy matching on words
            words = re.findall(r'\b\w+\b', text_lower)
            for word in words:
                # Check if this word is similar to any variation
                for variation in variations:
                    # Only check words of similar length
                    if abs(len(word) - len(variation)) <= 2 and len(word) >= 4:
                        distance = _levenshtein_distance(word, variation)
                        if distance <= 2:
                            # Replace the word with correct name
                            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                            normalized_text = pattern.sub(correct_name, normalized_text)
                            print(f"🔍 Fuzzy matched '{word}' → '{correct_name}' (distance: {distance})")
                            break
    
    return normalized_text


# ===========================================================
# 2) 스팟 Q&A 세션
# ===========================================================
def run_qa_session(spot_code, lang):
    """
    질문 → RAG → LLM → TTS
    - 질문이 없거나 '패스' 계열 → 자동 이동
    - 질문 있으면 답변하고 "추가 질문 있으신가요?" 반복
    
    Note:
    - lang은 wakeword 감지 시 결정된 사용자 언어를 사용
    - STT는 해당 언어로만 인식 (자동 언어 감지 없음)
    - RAG 오류 발생 시 자동으로 LLM-only 모드로 전환
    """
    # Special intro for geunjeongjeon (covers both geunjeongmun and geunjeongjeon)
    if spot_code == "geunjeongjeon":
        if lang == "ko":
            intro_text = "Geunjeongmun과 Geunjeongjeon에 대한 설명이 끝났습니다. 질문이 있으신가요? 있으시면 말씀해주세요. 없으시면 '패스'라고 말해주셔도 좋아요."
        else:
            intro_text = "That concludes the explanation of Geun-jeong-mun and Geun-jeong-jeon. Do you have any questions? If not, you can say 'pass'."
        speak(intro_text, lang)
    else:
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
        # Use word boundaries to avoid matching "no" in "know" or "not"
        PASS_WORDS = ["패스", "없어", "괜찮아", "pass", "no", "없습니다", "아니오", "skip", "next"]
        # Check for whole words only (word boundaries)
        words_in_text = set(re.findall(r'\b\w+\b', normalized))
        pass_words_set = set(p.lower() for p in PASS_WORDS)
        if words_in_text.intersection(pass_words_set):
            speak(PHRASES["qa_pass"][lang], lang)
            return

        # --- Proper noun normalization for palace-related terms ---
        normalized = _normalize_palace_proper_nouns(normalized, lang)
        if normalized != user_text.lower().strip():
            print(f"📝 Normalized question: '{user_text}' → '{normalized}'")

        # ====================================================================
        # Q&A PROCESSING: RAG + LLM
        # ====================================================================
        # This section handles user questions using RAG (Retrieval-Augmented Generation)
        # RAG can be enabled/disabled via ENABLE_RAG flag in config.py
        # 
        # When ENABLE_RAG = True:  Uses knowledge_docs context for accurate answers
        # When ENABLE_RAG = False: Uses LLM general knowledge only
        # ====================================================================
        print(f"사용자 질문: {normalized}")

        # 질문을 영어로 번역 (RAG는 영어로 작동)
        question_en = translate_question_to_en(normalized, src=lang)
        print(f"[Q&A] Translated to EN → '{question_en}'")

        # RAG 컨텍스트를 포함한 프롬프트 생성
        # Note: build_llm_prompt_for_qa() checks ENABLE_RAG flag internally
        # If RAG is disabled, it will generate a prompt without context
        prompt = build_llm_prompt_for_qa(
            spot_code=spot_code,
            user_question=question_en,
            place_id="gyeongbokgung",
            language="en",  # LLM은 항상 영어로 답변, 이후 번역
        )
        
        # LLM으로 답변 생성 (영어로 답변받음, 짧은 답변 강제)
        answer_en = call_llm(prompt, temperature=0.7, max_tokens=150).strip()
        # 안전장치: 2문장으로 제한
        answer_en = _truncate_to_two_sentences(answer_en)
        print(f"[Q&A] LLM answer (EN) → '{answer_en}'")
        
        # 답변을 사용자 언어로 번역
        answer = translate_answer_from_en(answer_en, tgt=lang)
        print(f"[Q&A] Translated answer ({lang}) → '{answer}'")

        speak(answer, lang)
        time.sleep(0.3)

        # --- 추가 질문 유도 ---
        speak(PHRASES["qa_more"][lang], lang)


# ===========================================================
# 3) 마지막 스팟 — 사진 촬영 모드
# ===========================================================
def run_photo_mode(lang):
    # Automatically proceed with photo taking after explanation
    speak(PHRASES["photo_intro"][lang], lang)
    time.sleep(0.5)
    
    speak(PHRASES["photo_positioning"][lang], lang)
    time.sleep(1.5)
    
    speak(PHRASES["photo_countdown"][lang], lang)
    # Wait 5 seconds before taking the photo
    time.sleep(5.0)
    
    speak(PHRASES["photo_shot"][lang], lang)
    
    # TODO: 실제 카메라 촬영 코드 연결
    # capture_photo()
    
    time.sleep(0.5)
    speak(PHRASES["photo_saved"][lang], lang)


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

        # Q&A: geunjeongmun에서는 건너뛰고, geunjeongjeon에서만 실행 (두 스팟 모두 설명 후)
        if spot_code != "geunjeongmun":
            run_qa_session(spot_code, lang)

        # 사진 스팟이면 사진 모드 실행
        if is_photo_spot:
            run_photo_mode(lang)

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

    normalized = user_text.lower().strip()
    
    # --- Proper noun normalization for palace-related terms ---
    normalized = _normalize_palace_proper_nouns(normalized, lang)
    if normalized != user_text.lower().strip():
        print(f"📝 Normalized question: '{user_text}' → '{normalized}'")
    
    print(f"[Q&A-inline] question: {normalized}")

    # 질문을 영어로 번역 (RAG는 영어로 작동)
    question_en = translate_question_to_en(normalized, src=lang)
    
    # RAG 컨텍스트를 포함한 프롬프트 생성
    # Note: RAG toggle (ENABLE_RAG in config.py) is checked inside build_llm_prompt_for_qa()
    prompt = build_llm_prompt_for_qa(
        spot_code=spot_code,
        user_question=question_en,
        place_id="gyeongbokgung",
        language="en",  # LLM은 항상 영어로 답변, 이후 번역
    )
    
    # LLM으로 답변 생성 (짧은 답변 강제)
    answer_en = call_llm(prompt, temperature=0.7, max_tokens=150).strip()
    # 안전장치: 2문장으로 제한
    answer_en = _truncate_to_two_sentences(answer_en)
    
    # 답변을 사용자 언어로 번역
    answer = translate_answer_from_en(answer_en, tgt=lang)
    speak(answer, lang)

    # 안내 멘트 후 스크립트로 복귀
    speak(PHRASES["qa_more"][lang], lang)


# 별칭: 기존 코드 호환
def run_tour(user_lang="ko", place_id="gyeongbokgung", qa_record_seconds=10.0, max_qa_turns=3):
    """
    Wrapper for legacy import compatibility.
    """
    return start_dori_tour(lang=user_lang)
