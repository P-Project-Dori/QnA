# wakeword_service.py

from typing import Callable
import threading
import time
import re

from stt_service import listen_for_seconds, listen_for_seconds_with_lang

WakeWordCallback = Callable[[], None]

# 허용 표현 (소문자 비교). 약간의 철자/발음 흔들림을 허용하기 위해 부분 매칭 사용.
WAKEWORD_COOLDOWN = 2.0  # 중복 인식 방지 간격(초)


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings for fuzzy matching."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def _fuzzy_match(text: str, pattern: str, max_distance: int = 2) -> bool:
    """
    Check if text matches pattern with fuzzy matching.
    Returns True if:
    - Exact substring match, OR
    - Edit distance is within max_distance for similar pronunciations
    """
    text_lower = text.lower()
    pattern_lower = pattern.lower()
    
    # Exact substring match
    if pattern_lower in text_lower:
        return True
    
    # Extract words from text
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Check each word for fuzzy match
    for word in words:
        # Only check words of similar length (more efficient)
        if abs(len(word) - len(pattern_lower)) <= max_distance and len(word) >= 3:
            distance = _levenshtein_distance(word, pattern_lower)
            if distance <= max_distance:
                return True
    
    return False


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
            "도리아",  # 추가 변형
        ]
    # 기본: 영어/기타 - 더 많은 변형 추가
    return [
        "hey dori",
        "hey, dori",
        "hey dory",
        "hey, dory",
        "hey tori",
        "hey, tori",
        "dori",
        "dory",
        "tori",
        "doria",  # 추가: Doria
        "doary",  # 추가: Doary
        "doree",  # 추가: Doree
        "dorey",  # 추가: Dorey
        "dorry",  # 추가: Dorry
    ]


def is_wakeword(text: str, lang: str) -> bool:
    """
    향상된 민감도 로직:
    - 소문자/공백/구두점 제거 후 부분 문자열 검사
    - Fuzzy matching으로 발음이 비슷한 경우도 인식
    - 언어별 wakeword 리스트에 있는 키워드가 포함되어 있거나 유사하면 true
    """
    if not text:
        return False
    
    norm = text.lower().strip()
    # 구두점 제거
    for ch in [",", ".", "?", "!", "'", '"', "-", " "]:
        norm = norm.replace(ch, "")
    
    # 정확한 매칭 먼저 시도
    for w in _wakewords_for_lang(lang):
        candidate = w.replace(",", "").replace(".", "").replace("-", "").replace(" ", "").lower()
        if candidate in norm or norm in candidate:
            return True
    
    # Fuzzy matching으로 유사한 발음도 인식
    # "dori" 패턴에 대해 fuzzy match (더 관대한 매칭)
    core_patterns = ["dori", "dory", "tori", "도리"] if not lang.startswith("ko") else ["도리", "dori"]
    
    for pattern in core_patterns:
        if _fuzzy_match(norm, pattern, max_distance=2):
            return True
    
    return False


def wakeword_label(lang: str) -> str:
    return "도리야" if lang.lower().startswith("ko") else "hey dori"


def _voice_listener_loop(on_detect: WakeWordCallback, default_lang: str = "en"):
    """
    마이크로 'hey dori'를 듣고 감지하면 콜백 실행.
    Google STT를 사용하므로 GCP 자격증명이 필요합니다.
    """
    print(f"[WakeWord] Voice mode on. Please call Dori in any language! (e.g., 'hey dori', 'dori', '도리야').")
    last_trigger = 0.0
    while True:
        text, detected_lang = listen_for_seconds_with_lang(seconds=3)
        if text:
            normalized = text.lower().strip()
            # 제한: ko/en만 사용, 그 외는 en으로 처리
            if detected_lang and detected_lang.startswith("ko"):
                lang_to_use = "ko"
            else:
                lang_to_use = "en"
            print(f"[WakeWord] STT captured: {normalized} (detected={detected_lang}, used={lang_to_use})")
            now = time.time()
            if now - last_trigger < WAKEWORD_COOLDOWN:
                time.sleep(0.2)
                continue
            if is_wakeword(normalized, lang_to_use):
                print("[WakeWord] 'Hey, Dori' 감지됨 → 콜백 호출")
                on_detect(lang_to_use)
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
