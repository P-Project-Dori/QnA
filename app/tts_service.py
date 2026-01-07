# tts_service.py
import io
import os
import requests
import pygame

# ===== ElevenLabs Voice IDs =====
ELEVENLABS_VOICES = {
    "ko": "uyVNoMrnUku1dZyVEXwD",  # Korean voice
    "en": "nBoLwpO4PAjQaQwVKPI1",  # English voice
    # For other languages, default to English voice
    "zh": "nBoLwpO4PAjQaQwVKPI1",
    "ja": "nBoLwpO4PAjQaQwVKPI1",
    "fr": "nBoLwpO4PAjQaQwVKPI1",
    "es": "nBoLwpO4PAjQaQwVKPI1",
    "vi": "nBoLwpO4PAjQaQwVKPI1",
    "th": "nBoLwpO4PAjQaQwVKPI1",
}

# ElevenLabs API endpoint
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def get_voice_id(lang):
    """Get ElevenLabs voice ID for the given language."""
    return ELEVENLABS_VOICES.get(lang, ELEVENLABS_VOICES["en"])


def get_api_key():
    """Get ElevenLabs API key from environment variable."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is not set. "
            "Please set it with your ElevenLabs API key."
        )
    return api_key


# ===== TTS 메인 함수 =====
def speak(text: str, lang="ko", speaking_rate=1.0, pitch=0.0):
    """
    ElevenLabs TTS 기반 음성 출력
    - text: 말할 내용
    - lang: 언어 코드 (ko, en 등)
    - speaking_rate: 말 속도 (0.25 ~ 4.0, 기본 1.0)
    - pitch: 음 높낮이 (ElevenLabs는 stability와 similarity_preset 사용)
    """
    if not text or text.strip() == "":
        return

    voice_id = get_voice_id(lang)
    api_key = get_api_key()

    # ElevenLabs API 요청
    url = ELEVENLABS_API_URL.format(voice_id=voice_id)
    
    # Use MP3 format (most reliable, no format issues)
    headers = {
        "Accept": "audio/mpeg",  # Request MP3 format
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    # ElevenLabs API 파라미터 - Consistent settings for all TTS calls
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # 다국어 지원 모델
        "voice_settings": {
            "stability": 0.5,  # Consistent stability
            "similarity_boost": 0.75,  # Consistent similarity
            "style": 0.0,  # Consistent style
            "use_speaker_boost": True  # Always use speaker boost for maximum clarity
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        # MP3 오디오 데이터 받기
        mp3_data = response.content
        
        # Initialize pygame mixer if not already initialized
        # Use consistent audio settings for all playback to ensure uniform quality
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Stop any currently playing music to ensure clean playback
        pygame.mixer.music.stop()
        
        # Load MP3 from memory using pygame (no file I/O)
        mp3_file = io.BytesIO(mp3_data)
        pygame.mixer.music.load(mp3_file)
        
        # Always set volume to maximum (1.0) right before playback
        # This ensures consistent volume across all scripts and Q&A
        # Set volume multiple times to ensure it's applied
        pygame.mixer.music.set_volume(1.0)
        
        # Play and wait for completion
        pygame.mixer.music.play()
        
        # Set volume again after starting playback to ensure it's at maximum
        pygame.mixer.music.set_volume(1.0)
        
        # Wait until playback is finished
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)  # Check every 100ms
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ElevenLabs TTS API 오류: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   응답 내용: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ TTS 재생 오류: {e}")
        raise

    print(f"🔊 TTS ({lang}) → {text}")
