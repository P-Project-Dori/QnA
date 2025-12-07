# llm_client.py

import os
from typing import Optional

import ollama  # pip install ollama


DEFAULT_MODEL_NAME = os.getenv("DORI_LLM_MODEL", "llama3.1:7b-q4_K_M")


def call_llm(prompt: str, max_tokens: int = 512) -> str:
    """
    주어진 prompt에 대해 Llama 3.1 7B Q4_K_M (Ollama) 응답 텍스트를 반환.

    - 모델 이름은 환경변수 DORI_LLM_MODEL 로 변경 가능.
    - 번역, RAG QA 등 모든 텍스트 생성에 공통으로 사용됨.
    """
    # Ollama chat API를 사용한 간단한 구현
    resp = ollama.chat(
        model=DEFAULT_MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt},
        ],
        options={
            "num_predict": max_tokens,
            # 필요하면 temperature, top_p 등 옵션 추가 가능
        },
    )

    # Ollama의 응답 구조에서 content 부분만 추출
    content = resp.get("message", {}).get("content", "")
    return content.strip()
