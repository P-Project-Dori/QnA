# stt_service.py
import io
import time
import tempfile

import numpy as np
import sounddevice as sd
import whisper

# ===== 언어 코드 매핑 =====
WHISPER_LANGS = {
    "ko": "ko",
    "en": "en",
    "zh": "zh",
    "ja": "ja",
    "fr": "fr",
    "es": "es",
    "vi": "vi",
    "th": "th",
}

_whisper_model = None


def load_whisper():
    global _whisper_model
    if _whisper_model is None:
        print("🔵 Loading Whisper model: tiny")
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model


def record_audio(seconds=3.0, sample_rate=16000):
    """
    Record mono audio using sounddevice and return raw int16 bytes.
    """
    print(f"🎙 Recording {seconds}s ...")
    data = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    return data.tobytes()


def speech_to_text(audio_bytes: bytes, lang="en", sample_rate=16000):
    """
    Transcribe given audio bytes with Whisper tiny (offline).
    """
    if not audio_bytes:
        return None

    model = load_whisper()
    np_audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    language = WHISPER_LANGS.get(lang, "en")

    # Whisper accepts NumPy float32 PCM directly; avoids external ffmpeg dependency
    result = model.transcribe(np_audio, language=language, fp16=False)
    text = result.get("text", "").strip()
    if text:
        print(f"🎤 User said: {text}")
    return text if text else None


def listen_for_seconds(lang="ko", seconds=10):
    """
    Offline STT using Whisper tiny.
    - records for `seconds`, returns transcript or None.
    """
    audio = record_audio(seconds=seconds, sample_rate=16000)
    if not audio:
        print("⏳ STT timeout (no speech)")
        return None
    return speech_to_text(audio_bytes=audio, lang=lang, sample_rate=16000)
