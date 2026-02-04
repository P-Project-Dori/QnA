# llm_client.py

import os
from openai import OpenAI
from openai import APIError, APIConnectionError, AuthenticationError, RateLimitError

# OpenAI API configuration
# Client will be initialized lazily on first use
_client = None

def _get_client():
    """Lazy initialization of OpenAI client to ensure API key is set."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.\n"
                "   다음 중 하나의 방법으로 설정하세요:\n"
                "   1. 터미널에서: export OPENAI_API_KEY='your-api-key'\n"
                "   2. PowerShell에서: $env:OPENAI_API_KEY='your-api-key'\n"
                "   3. .env 파일을 사용하거나 시스템 환경 변수로 설정"
            )
        _client = OpenAI(api_key=api_key)
    return _client

# Default model (can be changed if needed)
DEFAULT_MODEL = "gpt-4.1-mini"


def call_llm(prompt: str, temperature=0.7, max_tokens=512, model: str = None) -> str:
    """
    Simple helper that wraps ask_openai_llm-style payload but accepts a single prompt string.
    Used by translation_service and other modules expecting an OpenAI-compatible chat reply.
    """
    messages = [{"role": "user", "content": prompt}]
    return ask_openai_llm(messages, temperature=temperature, max_tokens=max_tokens, model=model)


def ask_openai_llm(messages, temperature=0.7, max_tokens=512, model: str = None):
    """
    Call OpenAI's API for chat completions.
    Uses the model specified, or defaults to gpt-4.1-mini.
    """
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    
    except ValueError as e:
        # Handle missing API key gracefully instead of crashing
        error_msg = str(e)
        print(error_msg)
        return "죄송합니다. OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 설정해주세요."
    
    except AuthenticationError:
        error_msg = (
            "❌ OpenAI API 인증 오류가 발생했습니다.\n"
            "   OPENAI_API_KEY 환경 변수가 유효한지 확인하세요.\n"
            "   API 키는 OpenAI 대시보드에서 확인할 수 있습니다: https://platform.openai.com/api-keys"
        )
        print(error_msg)
        return "죄송합니다. OpenAI API 인증 오류가 발생했습니다. API 키를 확인해주세요."
    
    except APIConnectionError as e:
        error_msg = (
            f"❌ OpenAI API 서버에 연결할 수 없습니다.\n"
            f"   인터넷 연결을 확인하세요.\n"
            f"   오류: {e}"
        )
        print(error_msg)
        return "죄송합니다. OpenAI API 서버에 연결할 수 없습니다. 인터넷 연결을 확인해주세요."
    
    except RateLimitError:
        error_msg = (
            "❌ OpenAI API 요청 한도에 도달했습니다.\n"
            "   잠시 후 다시 시도해주세요."
        )
        print(error_msg)
        return "죄송합니다. API 요청 한도에 도달했습니다. 잠시 후 다시 시도해주세요."
    
    except APIError as e:
        error_msg = f"❌ OpenAI API 오류: {e}"
        print(error_msg)
        return "죄송합니다. OpenAI API 요청 중 오류가 발생했습니다."


# Backward compatibility alias
def ask_local_llm(messages, temperature=0.7, max_tokens=512):
    """
    Backward compatibility wrapper for ask_openai_llm.
    Previously used for LM Studio, now calls OpenAI API.
    """
    return ask_openai_llm(messages, temperature=temperature, max_tokens=max_tokens)


