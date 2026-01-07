# dori_main.py

import time
from typing import Literal

from wakeword_service import start_wakeword_listener
from main_tour_loop import run_tour, start_dori_tour
from tts_service import speak

# translation_service.py와 동일한 언어 코드 타입
LanguageCode = Literal["en", "ko"]

PLACE_ID = "gyeongbokgung"


def on_wakeword_detected(detected_lang: str = "en"):
    """
    웨이크워드("Hey, Dori")가 감지되었을 때 호출되는 콜백.
    여기서 간단한 인사 멘트를 하고, 투어를 시작한다.
    """
    global USER_LANG
    # Whisper 감지 언어 기준으로 ko/en 설정 (기타는 en 기본)
    if detected_lang and detected_lang.startswith("ko"):
        USER_LANG = "ko"
    else:
        USER_LANG = "en"

    print("[ENTRY] Wakeword detected! Starting tour...")

    # 1) 인사 멘트
    if USER_LANG == "ko":
        greeting = "안녕하세요, 저는 도리입니다. 지금부터 경복궁 안내를 시작하겠습니다."
    else:
        greeting = "Hello, I am Dori. I will now start the tour of Gyeong-bok-gung Palace."

    speak(greeting, lang=USER_LANG)

    # 2) 메인 투어 실행
    start_dori_tour(lang=USER_LANG)

    print("[ENTRY] Tour finished.")


def main():
    """
    전체 엔트리 포인트.
    - 웨이크워드 리스너를 시작하고
    - 사용자가 'Hey Dori'를 말할 때까지 대기.
    """
    from config import ENABLE_RAG
    
    print("==============================================")
    print(" DORI - Multilingual Tour Guide Robot (Demo) ")
    print("==============================================")
    print()
    print(f"📚 RAG Status: {'ENABLED' if ENABLE_RAG else 'DISABLED'}")
    print(f"   (Toggle in config.py: ENABLE_RAG = {ENABLE_RAG})")
    print()
    global USER_LANG

    while True:
        USER_LANG = "en"  # default before detection
        print(f"[ENTRY] Waiting for wakeword... (voice, auto language detection)")
        print()

        # 웨이크워드 리스너 시작 (언어 자동 감지)
        start_wakeword_listener(on_wakeword_detected, use_voice=True, lang=USER_LANG)

        # 메인 스레드는 투어 종료까지 유지, 종료 후 다시 대기
        try:
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            print("\n[ENTRY] KeyboardInterrupt: 프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()
