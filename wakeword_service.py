# wakeword_service.py

from typing import Callable
import threading
import time

WakeWordCallback = Callable[[], None]


def _listener_loop(on_detect: WakeWordCallback):
    """
    매우 단순한 테스트용 wakeword 루프.
    콘솔에서 'hey'라고 입력하면 웨이크워드 감지로 간주하고 on_detect()를 호출.
    """
    print("[WakeWord] 테스트 모드 시작. 콘솔에 'hey'를 입력하면 도리가 깨어납니다.")
    while True:
        text = input("[WakeWord] 입력 (hey/q): ").strip().lower()
        if text == "hey":
            print("[WakeWord] 'Hey, Dori' 감지됨 → 콜백 호출")
            on_detect()
        elif text == "q":
            print("[WakeWord] 종료")
            break
        else:
            print("[WakeWord] 인식하지 못했어요. (hey / q 중 입력)")


def start_wakeword_listener(on_detect: WakeWordCallback):
    """
    간단한 테스트용 구현:
      - 별도 스레드에서 콘솔 입력을 기다리다가
      - 'hey'가 입력되면 on_detect() 콜백 호출

    나중에 실제 음성 기반 웨이크워드 엔진(Porcupine 등)으로 교체하면 됨.
    """
    thread = threading.Thread(
        target=_listener_loop,
        args=(on_detect,),
        daemon=True,
    )
    thread.start()
