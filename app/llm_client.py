# llm_client.py

import requests
from requests.exceptions import ConnectionError, RequestException

# LM Studio default port is 1234
LLAMA_URL = "http://127.0.0.1:1234/v1/chat/completions"


def call_llm(prompt: str, temperature=0.7, max_tokens=512) -> str:
    """
    Simple helper that wraps ask_local_llm-style payload but accepts a single prompt string.
    Used by translation_service and other modules expecting an OpenAI-compatible chat reply.
    """
    messages = [{"role": "user", "content": prompt}]
    return ask_local_llm(messages, temperature=temperature, max_tokens=max_tokens)


def ask_local_llm(messages, temperature=0.7, max_tokens=512):
    # LM Studio accepts the model name from the loaded model
    # You can use the model name or leave it empty - LM Studio will use the currently loaded model
    payload = {
        "model": "",  # LM Studio uses the currently loaded model if empty
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        res = requests.post(LLAMA_URL, json=payload, timeout=60)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except ConnectionError:
        error_msg = (
            f"❌ LM Studio 서버에 연결할 수 없습니다.\n"
            f"   LM Studio가 {LLAMA_URL}에서 실행 중인지 확인하세요.\n"
            f"   다음을 확인하세요:\n"
            f"   1. LM Studio가 실행 중인지\n"
            f"   2. 모델이 로드되어 있는지 (Llama-3.1-8B-Instruct-GGUF)\n"
            f"   3. 'Local Server' 탭에서 서버가 시작되어 있는지\n"
            f"   4. 포트가 1234인지 확인 (설정에서 변경 가능)"
        )
        print(error_msg)
        # 기본 응답 반환하여 앱이 계속 작동하도록 함
        return "죄송합니다. LM Studio 서버에 연결할 수 없습니다. LM Studio가 실행 중이고 서버가 시작되어 있는지 확인해주세요."
    except RequestException as e:
        error_msg = f"❌ LLM 요청 오류: {e}"
        print(error_msg)
        return "죄송합니다. LLM 요청 중 오류가 발생했습니다."


