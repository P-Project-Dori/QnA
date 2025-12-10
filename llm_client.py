# llm_client.py

import requests

LLAMA_URL = "http://127.0.0.1:8080/v1/chat/completions"


def call_llm(prompt: str, temperature=0.7, max_tokens=512) -> str:
    """
    Simple helper that wraps ask_local_llm-style payload but accepts a single prompt string.
    Used by translation_service and other modules expecting an OpenAI-compatible chat reply.
    """
    messages = [{"role": "user", "content": prompt}]
    return ask_local_llm(messages, temperature=temperature, max_tokens=max_tokens)


def ask_local_llm(messages, temperature=0.7, max_tokens=512):
    payload = {
        "model": "local",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    res = requests.post(LLAMA_URL, json=payload, timeout=60)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]


def answer_question_with_rag(question: str, context: str, lang="ko"):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Dori, a multilingual tour guide robot. "
                "Use ONLY the given context to answer. "
                "If the answer is not found in the context, say '저는 그 정보는 가지고 있지 않아요.'"
            ),
        },
        {
            "role": "user",
            "content": (
                f"[Context]\n{context}\n\n"
                f"[Question]\n{question}\n\n"
                f"답변은 반드시 {lang} 언어로 제공해줘."
            ),
        },
    ]

    return ask_local_llm(messages)
