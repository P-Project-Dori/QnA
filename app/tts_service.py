# tts_service.py
import io
import os
import re
import time
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


# ElevenLabs credit calculation: ~0.15-0.18 credits per character for multilingual_v2
CREDITS_PER_CHAR = 0.17  # Average estimate
MAX_CHARS_PER_REQUEST = 5000  # ElevenLabs multilingual_v2 limit
# Conservative chunk size: estimate ~2000 chars = ~340 credits (safe buffer)
SAFE_CHUNK_SIZE = 2000  # Characters per chunk to stay well under limits (normal usage)
# Ultra-conservative chunk size for low credit situations: ~250 chars = ~42 credits
ULTRA_SAFE_CHUNK_SIZE = 250  # For when credits are very low (< 100 remaining)


def _chunk_text_intelligently(text: str, max_chars: int = SAFE_CHUNK_SIZE) -> list[str]:
    """
    Split long text into chunks at sentence boundaries.
    Tries to split at periods, exclamation marks, or question marks.
    Falls back to space-based splitting if needed.
    """
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Try to split at sentence boundaries first
    sentences = re.split(r'([.!?]\s+)', text)
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
        
        # If single sentence is too long, split by spaces
        if len(sentence) > max_chars:
            words = sentence.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 > max_chars:
                    if temp_chunk:
                        chunks.append(temp_chunk.strip())
                    temp_chunk = word
                else:
                    temp_chunk += (" " if temp_chunk else "") + word
            if temp_chunk:
                current_chunk = temp_chunk.strip()
            continue
        
        # Check if adding this sentence would exceed max_chars
        if len(current_chunk) + len(sentence) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [text]


def _estimate_credits_needed(text: str) -> float:
    """Estimate ElevenLabs credits needed for text based on character count."""
    return len(text) * CREDITS_PER_CHAR


# ===== TTS 메인 함수 =====
def speak(text: str, lang="ko", speaking_rate=1.0, pitch=0.0):
    """
    ElevenLabs TTS 기반 음성 출력
    - text: 말할 내용 (자동으로 긴 텍스트는 청크로 분할)
    - lang: 언어 코드 (ko, en 등)
    - speaking_rate: 말 속도 (0.25 ~ 4.0, 기본 1.0)
    - pitch: 음 높낮이 (ElevenLabs는 stability와 similarity_preset 사용)
    """
    if not text or text.strip() == "":
        return

    # Check text length and chunk if necessary (only for very long texts)
    char_count = len(text)
    
    # Only chunk if text exceeds safe size (keeps behavior simple)
    if char_count > SAFE_CHUNK_SIZE:
        chunks = _chunk_text_intelligently(text, SAFE_CHUNK_SIZE)
        
        # Process each chunk sequentially (silently, like before)
        for chunk in chunks:
            _speak_single_chunk(chunk, lang, speaking_rate, pitch)
            # Small delay between chunks for natural speech flow
            time.sleep(0.3)
        return
    
    # For normal texts, call directly
    _speak_single_chunk(text, lang, speaking_rate, pitch)


def _speak_single_chunk(text: str, lang: str, speaking_rate: float, pitch: float):
    """
    Internal function to handle a single TTS request (chunk).
    This is where the actual API call happens.
    """
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
        
        # Check for HTTP errors before processing
        if response.status_code == 401:
            # Check if it's a quota exceeded error
            try:
                error_detail = response.json().get("detail", {})
                if error_detail.get("status") == "quota_exceeded":
                    # Silently skip TTS when quota is exceeded (user said they don't need credit checking)
                    return
            except (ValueError, KeyError):
                pass
        
        # Raise for other HTTP errors
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
        
        print(f"🔊 TTS ({lang}) → {text}")
        
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (like 401, 403, 429, etc.) gracefully - silently skip
        # Don't crash - just skip TTS and continue
        return
        
    except requests.exceptions.RequestException as e:
        # Handle network/connection errors gracefully - silently skip
        return
        
    except Exception as e:
        # Handle any other unexpected errors gracefully - silently skip
        return
