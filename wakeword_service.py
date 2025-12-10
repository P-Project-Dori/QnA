# wakeword_service.py

from typing import Callable
import threading
import time

from stt_service import listen_for_seconds

WakeWordCallback = Callable[[], None]

# 허용 표현 (소문자 비교). 약간의 철자/발음 흔들림을 허용하기 위해 부분 매칭 사용.
WAKEWORD_COOLDOWN = 2.0  # 중복 인식 방지 간격(초)


def _wakewords_for_lang(lang: str):
    lang = lang.lower()
    if lang.startswith("ko"):
        # 한국어: '도리야' 인식 용이하도록 변형 추가
        return [
            "도리야",
            "도리 아",
            "doriya",
            "dori ya",
            "dori-ya",
        ]
    # 기본: 영어/기타
    return [
        "hey dori",
        "hey, dori",
        "hey dory",
        "hey, dory",
        "hey tori",
        "dori",
        "dory",
        "tori",
    ]


def is_wakeword(text: str, lang: str) -> bool:
    """
    단순 민감도 향상 로직:
    - 소문자/공백/구두점 제거 후 부분 문자열 검사
    - 언어별 wakeword 리스트에 있는 키워드가 포함되어 있으면 true
    """
    if not text:
        return False
    norm = text.lower().strip()
    for ch in [",", ".", "?", "!", "'", '"']:
        norm = norm.replace(ch, "")
    for w in _wakewords_for_lang(lang):
        candidate = w.replace(",", "").replace(".", "").lower()
        if candidate in norm:
            return True
    return False


def wakeword_label(lang: str) -> str:
    return "도리야" if lang.lower().startswith("ko") else "hey dori"


def _voice_listener_loop(on_detect: WakeWordCallback, lang: str):
    """
    마이크로 'hey dori'를 듣고 감지하면 콜백 실행.
    Google STT를 사용하므로 GCP 자격증명이 필요합니다.
    """
    print(f"[WakeWord] 음성 모드 시작: '{wakeword_label(lang)}'를 말하면 도리가 깨어납니다. (q를 입력하면 종료)")
    last_trigger = 0.0
    while True:
        text = listen_for_seconds(lang="en", seconds=3)
        if text:
            normalized = text.lower().strip()
            print(f"[WakeWord] STT captured: {normalized}")
            now = time.time()
            if now - last_trigger < WAKEWORD_COOLDOWN:
                time.sleep(0.2)
                continue
            if is_wakeword(normalized, lang):
                print("[WakeWord] 'Hey, Dori' 감지됨 → 콜백 호출")
                on_detect()
                last_trigger = now
                continue
        else:
            print("[WakeWord] (무음 또는 인식 실패)")

        # 짧게 쉼
        time.sleep(0.2)


def start_wakeword_listener(on_detect: WakeWordCallback, use_voice: bool = True, lang: str = "en"):
    """
    웨이크워드 리스너 시작.
    - use_voice=True: 마이크 STT로 'hey dori' 감지
    - use_voice=False: 이전 콘솔 입력 방식 (백업용)
    """
    if use_voice:
        target = _voice_listener_loop
    else:
        target = _console_listener_loop

    thread = threading.Thread(
        target=target,
        args=(on_detect, lang),
        daemon=True,
    )
    thread.start()


# 백업: 기존 콘솔 입력 모드 (개발 편의를 위해 유지)
def _console_listener_loop(on_detect: WakeWordCallback):
    print("[WakeWord] 콘솔 모드 시작. 'hey' 입력 시 깨우기, 'q' 종료.")
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
