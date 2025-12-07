# tts_service.py
from typing import Literal
from google.cloud import texttospeech
import sounddevice as sd
import numpy as np

LanguageCode = Literal["en", "ko", "ja", "zh", "fr", "es", "vi", "th"]

LANG_TO_TTS_CODE = {
    "ko": "ko-KR",
    "en": "en-US",
    "ja": "ja-JP",
    "zh": "cmn-Hans-CN",  # 중국어(표준어, 간체)
    "fr": "fr-FR",
    "es": "es-ES",
    "vi": "vi-VN",
    "th": "th-TH",
}

LANG_TO_VOICE_NAME = {
    "ko": "ko-KR-Wavenet-A",
    "en": "en-US-Wavenet-D",
    "ja": "ja-JP-Wavenet-A",
    "zh": "cmn-CN-Wavenet-A",
    "fr": "fr-FR-Wavenet-A",
    "es": "es-ES-Wavenet-A",
    "vi": "vi-VN-Wavenet-A",
    "th": "th-TH-Wavenet-A",
}


def _synthesize_google_tts(text: str, lang: LanguageCode) -> bytes:
    client = texttospeech.TextToSpeechClient()

    language_code = LANG_TO_TTS_CODE.get(lang, "en-US")
    voice_name = LANG_TO_VOICE_NAME.get(lang, "")

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name or None,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # 16-bit PCM
        speaking_rate=1.0,
        pitch=0.0,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    return response.audio_content  # raw PCM bytes


def _play_audio_pcm16(audio_bytes: bytes, sample_rate: int = 24000):
    """
    PCM 16bit 모노 데이터를 스피커로 재생.
    Google TTS 기본 샘플레이트는 24kHz인 경우가 많음.
    """
    # int16 → float32 (-1.0 ~ 1.0)
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    sd.play(audio_np, samplerate=sample_rate)
    sd.wait()


def speak(text: str, lang: LanguageCode):
    """
    최종 TTS 함수.
    나중에 로컬 TTS를 붙이고 싶으면 여기에서 먼저 로컬 시도 → 실패 시 구글로 fallback 하면 됨.
    """
    text = text.strip()
    if not text:
        return

    audio_bytes = _synthesize_google_tts(text, lang)
    _play_audio_pcm16(audio_bytes)
