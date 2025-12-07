# tts_utils.py

import time
from typing import Literal

import pyaudio
from google.cloud import texttospeech

"""
전제:
- GOOGLE_APPLICATION_CREDENTIALS 환경변수에
  서비스 계정 JSON 경로가 설정되어 있어야 함.
- pip install pyaudio
"""

# 웹/사용자가 선택하는 언어 코드 (우리 기준)
UserLang = Literal["en", "ko", "zh", "ja", "fr", "es", "vi", "th"]

# 사용자 언어 코드 -> Google Cloud TTS 언어 코드 매핑
LANG_TO_GOOGLE = {
    "en": "en-US",   # 영어
    "ko": "ko-KR",   # 한국어
    "zh": "cmn-CN",  # 중국어(표준어) 예시
    "ja": "ja-JP",   # 일본어
    "fr": "fr-FR",   # 프랑스어
    "es": "es-ES",   # 스페인어
    "vi": "vi-VN",   # 베트남어
    "th": "th-TH",   # 태국어
}


def _get_google_lang_code(user_lang: UserLang) -> str:
    """
    내부에서 사용할 Google TTS 언어 코드로 변환.
    매핑에 없으면 영어(en-US)로 fallback.
    """
    return LANG_TO_GOOGLE.get(user_lang, "en-US")


def tts_play(text: str, user_lang: UserLang = "en") -> None:
    """
    메인 TTS 함수.
    - Google Cloud TTS로 LINEAR16(PCM) 오디오를 받아서
    - PyAudio로 바로 스피커에 재생한다.

    파일 저장 X, 완전 실시간 재생 구조.
    """
    if not text.strip():
        return

    # 1. Google TTS 클라이언트
    client = texttospeech.TextToSpeechClient()

    # 2. 입력 텍스트
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 3. 목소리/언어 설정
    google_lang = _get_google_lang_code(user_lang)
    voice = texttospeech.VoiceSelectionParams(
        language_code=google_lang,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # 4. 오디오 형식 설정 (LINEAR16 = 16bit PCM, mono)
    sample_rate_hz = 24000  # 재생에도 동일하게 사용할 샘플레이트
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz,
    )

    # 5. TTS API 호출
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_bytes = response.audio_content
    if not audio_bytes:
        print("[TTS] 빈 오디오가 반환되었습니다.")
        return

    # 6. PyAudio로 재생
    p = pyaudio.PyAudio()

    # LINEAR16 = 16bit PCM → paInt16
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate_hz,
        output=True,
    )

    # 한 번에 통으로 write해도 되고, 나중에 chunk로 나눠도 됨
    stream.write(audio_bytes)

    # 정리
    stream.stop_stream()
    stream.close()
    p.terminate()

    # (선택) 아주 긴 텍스트일 경우, 재생 끝까지 기다릴 시간 여유 주고 싶으면 여기서 sleep 조절 가능
    # time.sleep(0.1)
