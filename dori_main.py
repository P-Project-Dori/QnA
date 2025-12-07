# dori_main.py

import time
from typing import Literal

from wakeword_service import start_wakeword_listener
from main_tour_loop import run_tour
from tts_service import speak

# translation_service.py와 동일한 언어 코드 타입
LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

# TODO:
#  - 실제로는 웹 예약 정보에서 사용자가 선택한 언어를 가져오면 됨.
#  - 지금은 데모용으로 한국어로 고정.
USER_LANG: LanguageCode = "ko"
PLACE_ID = "gyeongbokgung"


def on_wakeword_detected():
    """
    웨이크워드("Hey, Dori")가 감지되었을 때 호출되는 콜백.
    여기서 간단한 인사 멘트를 하고, 투어를 시작한다.
    """
    print("[ENTRY] Wakeword detected! Starting tour...")

    # 1) 인사 멘트
    if USER_LANG == "ko":
        greeting = "안녕하세요, 저는 도리입니다. 지금부터 경복궁 안내를 시작하겠습니다."
    else:
        greeting = "Hello, I am Dori. I will now start the tour of Gyeongbokgung Palace."

    speak(greeting, lang=USER_LANG)

    # 2) 메인 투어 실행
    run_tour(
        user_lang=USER_LANG,
        place_id=PLACE_ID,
        qa_record_seconds=10.0,  # 요구사항: 10초 대기
        max_qa_turns=3,          # 스팟당 최대 3번까지 Q&A
    )

    # 3) 투어 종료 후 한 마디 더 (원하면)
    if USER_LANG == "ko":
        bye_msg = "투어가 모두 끝났습니다. 도리와 함께해 주셔서 감사합니다."
    else:
        bye_msg = "The tour has finished. Thank you for joining Dori."

    speak(bye_msg, lang=USER_LANG)
    print("[ENTRY] Tour finished.")


def main():
    """
    전체 엔트리 포인트.
    - 웨이크워드 리스너를 시작하고
    - 사용자가 'Hey Dori'를 말할 때까지 대기.
    """
    print("==============================================")
    print(" DORI - Multilingual Tour Guide Robot (Demo) ")
    print("==============================================")
    print()
    print(f"[ENTRY] Selected language = {USER_LANG}, place_id = {PLACE_ID}")
    print("[ENTRY] Waiting for wakeword... (console에서는 'hey' 입력으로 테스트)")
    print()

    # 웨이크워드 리스너 시작
    # (이 함수는 별도 스레드에서 'hey' 입력을 기다리는 구조라고 가정)
    start_wakeword_listener(on_wakeword_detected)

    # 메인 스레드는 그냥 살아있기만 하면 됨.
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[ENTRY] KeyboardInterrupt: 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
