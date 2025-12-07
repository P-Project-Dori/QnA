# main_tour_loop.py

from typing import Literal

from tour_route import TOUR_ROUTE
from multilingual_orchestrator import speak_spot_intro, handle_single_qa_turn
from tts_service import speak

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]


# 간단한 멘트 사전 (필요하면 나중에 번역 서비스와 연동 가능)
MESSAGES = {
    "ask_question": {
        "ko": "질문이 있으신가요? 10초 동안 질문해 주세요.",
        "en": "Do you have any questions? Please ask within the next 10 seconds.",
    },
    "no_question": {
        "ko": "질문이 없으시면, 다음 장소로 이동하겠습니다.",
        "en": "If you don’t have any questions, I will move to the next spot.",
    },
    "moving_to_spot": {
        "ko": "다음 안내 지점으로 이동하겠습니다.",
        "en": "I will move to the next spot.",
    },
    "photo_intro": {
        "ko": "이곳은 사진이 잘 나오는 포토 스팟입니다. 잠시 후 사진을 찍어드릴게요.",
        "en": "This is a great photo spot. I will take a picture for you soon.",
    },
    "photo_done": {
        "ko": "사진 촬영이 완료되었습니다.",
        "en": "The photo has been taken.",
    },
    "tour_finish": {
        "ko": "이제 오늘의 투어를 마치겠습니다. 도리와 함께해 주셔서 감사합니다.",
        "en": "The tour is now finished. Thank you for joining Dori.",
    },
}


def get_message(key: str, user_lang: LanguageCode) -> str:
    """
    언어별 멘트를 가져오는 헬퍼.
    해당 언어에 정의가 없으면 영어로 fallback.
    """
    table = MESSAGES.get(key, {})
    return table.get(user_lang, table.get("en", ""))


# 실제 로봇 이동/제어 부분은 나중에 Unitree SDK와 연결
def move_robot_to_spot(spot_code: str):
    """
    TODO: 여기에 Unitree Go2 자율주행 코드 연동.
    지금은 데모용으로 콘솔 출력만 한다.
    """
    print(f"[MOVE] 로봇이 스팟 '{spot_code}'로 이동합니다...")


# 실제 카메라 촬영/저장은 나중에 구현
def take_photo_for_user(spot_code: str):
    """
    TODO: 여기서 카메라로 사진 촬영하고 파일 저장/공유 로직 구현.
    지금은 데모용으로 콘솔 출력만 한다.
    """
    print(f"[PHOTO] 스팟 '{spot_code}'에서 사진을 촬영합니다...")


def run_tour(
    user_lang: LanguageCode = "ko",
    place_id: str = "gyeongbokgung",
    qa_record_seconds: float = 10.0,
    max_qa_turns: int = 3,
):
    """
    도리 투어 메인 루프.

    - TOUR_ROUTE에 정의된 순서대로 스팟을 순회
    - 각 스팟에서:
        1) (옵션) 이동 안내 멘트
        2) 스팟 소개 멘트 (다국어 TTS)
        3) 10초 대기 Q&A 루프
        4) 포토 스팟이면 사진 촬영 로직

    매개변수:
      - user_lang: 사용자가 선택한 언어 코드
      - place_id: DB 상 place_id (기본값 'gyeongbokgung')
      - qa_record_seconds: 각 질문 대기 시간(초) → 요구사항대로 10초
      - max_qa_turns: 스팟당 최대 Q&A 반복 횟수
    """
    print(f"[TOUR] 투어 시작 (lang={user_lang}, place_id={place_id})")

    for idx, spot in enumerate(TOUR_ROUTE, start=1):
        spot_code = spot["spot_code"]
        spot_name_en = spot["name_en"]
        is_photo_spot = spot["is_photo_spot"]

        print(f"\n[TOUR] ==== 스팟 {idx}: {spot_code} ({spot_name_en}) ====")

        # 1) 로봇 이동 (실제 구현은 move_robot_to_spot 안에)
        move_robot_to_spot(spot_code)

        # 이동 안내 TTS (원하면 주석 해제해서 사용)
        move_msg = get_message("moving_to_spot", user_lang)
        if move_msg:
            speak(move_msg, lang=user_lang)

        # 2) 스팟 소개 멘트 (DB 기반 scripts → 번역 → TTS)
        speak_spot_intro(spot_code, user_lang)

        # 3) Q&A 루프
        qa_count = 0
        while qa_count < max_qa_turns:
            ask_msg = get_message("ask_question", user_lang)
            if ask_msg:
                speak(ask_msg, lang=user_lang)

            # 여기서 10초 동안 사용자 음성을 듣고,
            # 질문이 없으면 handle_single_qa_turn은 ""(빈 문자열)을 반환하도록 구현돼 있다고 가정.
            answer_user = handle_single_qa_turn(
                user_lang=user_lang,
                spot_code=spot_code,
                place_id=place_id,
                record_seconds=qa_record_seconds,
            )

            if not answer_user:
                # 질문이 없거나 STT로 인식된 내용이 없는 경우 → Q&A 종료
                break

            qa_count += 1
            # 질문이 있었고 답변도 완료된 상태 → 반복 여부는 max_qa_turns로 제한

        if qa_count == 0:
            # 한 번도 질문이 없었을 때만 "질문이 없으시면..." 멘트
            no_q_msg = get_message("no_question", user_lang)
            if no_q_msg:
                speak(no_q_msg, lang=user_lang)

        # 4) 포토 스팟이면 사진 로직
        if is_photo_spot:
            photo_intro = get_message("photo_intro", user_lang)
            if photo_intro:
                speak(photo_intro, lang=user_lang)

            # TODO: 여기서 "사진 찍어드릴까요?" → STT로 yes/no 받는 로직을 추가할 수도 있음.
            # 일단은 무조건 사진 한 번 찍어주는 것으로 처리.
            take_photo_for_user(spot_code)

            photo_done = get_message("photo_done", user_lang)
            if photo_done:
                speak(photo_done, lang=user_lang)

    # 전체 루트 종료 후 마무리 멘트
    finish_msg = get_message("tour_finish", user_lang)
    if finish_msg:
        speak(finish_msg, lang=user_lang)

    print("[TOUR] 투어 종료")
