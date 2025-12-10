# test_tts.py

from tts_service import speak
from typing import Literal

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

if __name__ == "__main__":
    # 여기서 언어를 바꿔가며 테스트할 수 있어요.
    user_lang: LanguageCode = "en"
    text = "Hello, I am Dori. This is a TTS test using sounddevice, not PyAudio."

    print(f"[TEST TTS] lang={user_lang}, text={text!r}")
    speak(text, lang=user_lang)
    print("[TEST TTS] 재생 완료.")
