# stt_service.py

import io

import time

import tempfile

import re

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

# ===== Whisper Model Configuration =====
# Options: "tiny", "base", "small", "medium", "large"
# "base" provides better accuracy than "tiny" with reasonable speed
# "small" is even better but slower
WHISPER_MODEL_SIZE = "base"  # Upgraded from "tiny" for better accuracy

# Confidence threshold: reject transcriptions below this average logprob
# Typical values: -1.5 (very lenient) to -0.5 (strict)
# Lower (more negative) = more lenient, Higher (less negative) = more strict
# Set to -1.2 to be more lenient and avoid rejecting valid questions
MIN_AVG_LOGPROB = -1.2

# Minimum text quality checks
MIN_TEXT_LENGTH = 2  # Minimum characters for valid transcription
MAX_CONSECUTIVE_REPEATS = 3  # Max consecutive repeated characters (e.g., "aaa")

_whisper_model = None





def load_whisper():

    global _whisper_model

    if _whisper_model is None:

        print(f"🔵 Loading Whisper model: {WHISPER_MODEL_SIZE} (CPU)")

        # Force CPU usage to avoid CUDA memory issues
        import torch
        device = "cpu"
        _whisper_model = whisper.load_model(WHISPER_MODEL_SIZE, device=device)

    return _whisper_model





def record_audio(seconds=3.0, sample_rate=16000):

    """

    Record mono audio using sounddevice and return raw int16 bytes.

    """

    print(f"🎙 Recording {seconds}s ...")

    data = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

    sd.wait()

    return data.tobytes()





def _is_valid_transcription(text: str) -> bool:
    """
    Validate transcription quality to filter out gibberish.
    
    Checks:
    - Minimum length
    - No excessive consecutive character repeats
    - Contains at least some alphanumeric characters
    """
    if not text or len(text.strip()) < MIN_TEXT_LENGTH:
        return False
    
    # Check for excessive consecutive character repeats (e.g., "aaaaa", "sssss")
    if re.search(r'(.)\1{' + str(MAX_CONSECUTIVE_REPEATS) + ',}', text):
        return False
    
    # Must contain at least some alphanumeric characters
    if not re.search(r'[a-zA-Z0-9가-힣]', text):
        return False
    
    return True


def _looks_like_reasonable_text(text: str) -> bool:
    """
    Check if text looks like a reasonable question or phrase, even if confidence is low.
    This is used as a fallback to accept borderline transcriptions.
    
    Returns True if the text:
    - Contains common question words (what, when, where, who, how, why, etc.)
    - Contains common English/Korean words
    - Has a reasonable word-to-character ratio
    - Doesn't look like complete gibberish
    """
    if not text or len(text.strip()) < 3:
        return False
    
    text_lower = text.lower().strip()
    words = text_lower.split()
    
    # Must have at least 2 words to be considered reasonable
    if len(words) < 2:
        # But accept single words that are common question starters
        common_starters = ["what", "when", "where", "who", "how", "why", "tell", "explain", "describe"]
        if any(text_lower.startswith(starter) for starter in common_starters):
            return True
        return False
    
    # Check for common question words
    question_words = ["what", "when", "where", "who", "how", "why", "which", "whose", "whom"]
    if any(word in question_words for word in words):
        return True
    
    # Check for common English words (simple heuristic)
    common_words = ["the", "is", "was", "are", "were", "this", "that", "these", "those", 
                    "can", "could", "would", "should", "about", "with", "from", "for"]
    if sum(1 for word in words if word in common_words) >= 2:
        return True
    
    # Check word-to-character ratio (reasonable text should have spaces)
    if len(words) >= 2 and len(text) / len(words) < 8:  # Average word length < 8 chars
        return True
    
    return False


def _calculate_avg_logprob(result: dict) -> float:
    """
    Calculate average log probability from Whisper result.
    Higher values indicate better confidence.
    """
    segments = result.get("segments", [])
    if not segments:
        return -1.0  # Default to low confidence if no segments
    
    total_logprob = 0.0
    total_duration = 0.0
    
    for seg in segments:
        logprob = seg.get("avg_logprob", -1.0)
        duration = seg.get("end", 0) - seg.get("start", 0)
        if duration > 0:
            total_logprob += logprob * duration
            total_duration += duration
    
    if total_duration > 0:
        return total_logprob / total_duration
    return -1.0


def speech_to_text(audio_bytes: bytes, lang="en", sample_rate=16000, min_confidence=None):

    """

    Transcribe given audio bytes with Whisper (offline).

    Args:
        audio_bytes: Audio data
        lang: Language code
        sample_rate: Sample rate
        min_confidence: Minimum average logprob threshold (uses global MIN_AVG_LOGPROB if None)

    Returns:
        Transcribed text or None if quality checks fail
    """

    if not audio_bytes:

        return None



    model = load_whisper()

    np_audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0



    language = WHISPER_LANGS.get(lang, "en") if lang not in (None, "auto") else None



    # Whisper accepts NumPy float32 PCM directly; avoids external ffmpeg dependency

    result = model.transcribe(np_audio, language=language, fp16=False)

    text = result.get("text", "").strip()
    
    # Quality checks
    if not text:
        return None
    
    # Check text validity (gibberish detection)
    if not _is_valid_transcription(text):
        print(f"⚠️  Rejected transcription (invalid format): '{text}'")
        return None
    
    # Check confidence threshold
    avg_logprob = _calculate_avg_logprob(result)
    confidence_threshold = min_confidence if min_confidence is not None else MIN_AVG_LOGPROB
    
    # Reject if confidence is too low
    if avg_logprob < confidence_threshold:
        # Fallback: accept if text looks reasonable even with low confidence
        # This helps catch valid questions that Whisper transcribed with borderline confidence
        if _looks_like_reasonable_text(text):
            print(f"✅ Accepted transcription (low confidence {avg_logprob:.2f} but looks reasonable): '{text}'")
            if text:
                print(f"🎤 User said: {text} (confidence: {avg_logprob:.2f})")
            return text
        else:
            print(f"⚠️  Rejected transcription (low confidence {avg_logprob:.2f} < {confidence_threshold:.2f}): '{text}'")
            return None
    
    if text:
        print(f"🎤 User said: {text} (confidence: {avg_logprob:.2f})")

    return text





def speech_to_text_with_lang(audio_bytes: bytes, sample_rate=16000, lang_hint=None, min_confidence=None):

    """

    Transcribe and return (text, detected_language).

    - lang_hint: use None or "auto" for detection; otherwise language code hint.
    - min_confidence: Minimum average logprob threshold

    """

    if not audio_bytes:

        return None, None



    model = load_whisper()

    np_audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0



    language = WHISPER_LANGS.get(lang_hint, lang_hint) if lang_hint not in (None, "auto") else None

    result = model.transcribe(np_audio, language=language, fp16=False)

    text = result.get("text", "").strip()

    detected_lang = result.get("language")
    
    # Quality checks
    if not text:
        return None, detected_lang
    
    # Check text validity (gibberish detection)
    if not _is_valid_transcription(text):
        print(f"⚠️  Rejected transcription (invalid format): '{text}'")
        return None, detected_lang
    
    # Check confidence threshold
    avg_logprob = _calculate_avg_logprob(result)
    confidence_threshold = min_confidence if min_confidence is not None else MIN_AVG_LOGPROB
    
    # Reject if confidence is too low
    if avg_logprob < confidence_threshold:
        # Fallback: accept if text looks reasonable even with low confidence
        if _looks_like_reasonable_text(text):
            print(f"✅ Accepted transcription (low confidence {avg_logprob:.2f} but looks reasonable): '{text}'")
            if text:
                print(f"🎤 User said: {text} (detected_lang={detected_lang}, confidence: {avg_logprob:.2f})")
            return (text if text else None), detected_lang
        else:
            print(f"⚠️  Rejected transcription (low confidence {avg_logprob:.2f} < {confidence_threshold:.2f}): '{text}'")
            return None, detected_lang

    if text:
        print(f"🎤 User said: {text} (detected_lang={detected_lang}, confidence: {avg_logprob:.2f})")

    return (text if text else None), detected_lang





def listen_for_seconds(lang="ko", seconds=10, max_retries=1):

    """

    Offline STT using Whisper.

    - records for `seconds`, returns transcript or None.
    - max_retries: Number of retries if transcription quality is low

    """

    for attempt in range(max_retries + 1):
        audio = record_audio(seconds=seconds, sample_rate=16000)

        if not audio:

            print("⏳ STT timeout (no speech)")

            return None

        result = speech_to_text(audio_bytes=audio, lang=lang, sample_rate=16000)
        
        # If we got a valid result, return it
        if result:
            return result
        
        # If this wasn't the last attempt, retry
        if attempt < max_retries:
            print(f"🔄 Retrying transcription (attempt {attempt + 2}/{max_retries + 1})...")
            time.sleep(0.5)  # Brief pause before retry
    
    # All attempts failed
    print("⚠️  Could not get valid transcription after retries")
    return None





def listen_for_seconds_with_lang(seconds=3):

    """

    Record audio and return (text, detected_language).

    """

    audio = record_audio(seconds=seconds, sample_rate=16000)

    if not audio:

        print("⏳ STT timeout (no speech)")

        return None, None

    return speech_to_text_with_lang(audio_bytes=audio, sample_rate=16000, lang_hint=None)
