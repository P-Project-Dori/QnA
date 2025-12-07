# stt_service.py
from typing import Literal
from google.cloud import speech_v1p1beta1 as speech
import sounddevice as sd
import numpy as np

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

LANG_TO_STT_CODE = {
    "ko": "ko-KR",
    "en": "en-US",
    "ja": "ja-JP",
    "zh": "cmn-Hans-CN",
    "fr": "fr-FR",
    "es": "es-ES",
    "vi": "vi-VN",
    "th": "th-TH",
}


def record_audio(seconds: float = 5.0, sample_rate: int = 16000) -> bytes:
    """
    마이크로부터 seconds초 동안 녹음해서
    16kHz, mono, 16bit PCM 바이트로 반환.
    """
    print(f"[STT] Recording {seconds} seconds...")
    audio = sd.rec(
        int(seconds * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    audio_bytes = audio.tobytes()
    return audio_bytes


def speech_to_text(audio_bytes: bytes, lang: LanguageCode, sample_rate: int = 16000) -> str:
    client = speech.SpeechClient()

    language_code = LANG_TO_STT_CODE.get(lang, "en-US")

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        language_code=language_code,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        model="default",
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return ""

    return response.results[0].alternatives[0].transcript
