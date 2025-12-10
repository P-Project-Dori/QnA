# tts_service.py
import io
import os
import tempfile
import wave
import winsound
from google.cloud import texttospeech

# ===== 언어 코드 매핑 =====
LANGUAGE_CODES = {
    "ko": "ko-KR",
    "en": "en-US",
    "zh": "cmn-CN",
    "ja": "ja-JP",
    "fr": "fr-FR",
    "es": "es-ES",
    "vi": "vi-VN",
    "th": "th-TH",
}


def get_language_code(lang):
    return LANGUAGE_CODES.get(lang, "en-US")


# ===== 음성 스타일 매핑 =====
VOICE_STYLES = {
    "ko": "ko-KR-Wavenet-A",
    "en": "en-US-Wavenet-D",
    "zh": "cmn-CN-Wavenet-A",
    "ja": "ja-JP-Wavenet-B",
    "fr": "fr-FR-Wavenet-A",
    "es": "es-ES-Wavenet-A",
    "vi": "vi-VN-Neural2-A",
    "th": "th-TH-Neural2-A",
}


def get_voice_name(lang):
    return VOICE_STYLES.get(lang, "en-US-Wavenet-D")


# ===== TTS 메인 함수 =====
def speak(text: str, lang="ko", speaking_rate=1.0, pitch=0.0):
    """
    Google Cloud TTS 기반 음성 출력
    - text: 말할 내용
    - lang: 언어 코드
    - speaking_rate: 말 속도 (1.0 기본)
    - pitch: 음 높낮이 (-5 ~ +5 사이 추천)
    """
    if not text or text.strip() == "":
        return

    language_code = get_language_code(lang)
    voice_name = get_voice_name(lang)

    # Google TTS Client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    # Google TTS 기본 LINEAR16 샘플레이트는 24kHz이므로 동일하게 맞춘다.
    sample_rate = 24000

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
        sample_rate_hertz=sample_rate,
    )

    # API 호출
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    # 오디오 재생 (pydub/audioop 없이 winsound 사용)
    # Google TTS 응답은 LINEAR16 PCM이므로 임시 WAV 파일로 저장 후 재생
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp_name = tmp.name
        with wave.open(tmp, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # LINEAR16 = 2 bytes
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(response.audio_content)

    try:
        winsound.PlaySound(tmp_name, winsound.SND_FILENAME)
    finally:
        try:
            os.remove(tmp_name)
        except OSError:
            pass

    print(f"🔊 TTS ({lang}) → {text}")
