import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def llm_enabled() -> bool:
    return os.getenv("USE_LLM", "false").lower() == "true"


def get_provider_config() -> dict:
    return {
        "provider": "openai",
        "api_key": os.getenv("OPENAI_API_KEY", "").strip(),
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip(),
    }


def build_system_prompt() -> str:
    return (
        "You are an AI security assistant.\n"
        "Use only the provided context.\n"
        "Do not invent facts, vulnerabilities, mitigations, or claims.\n"
        "If the context is insufficient, say so clearly.\n"
        "Do not claim external knowledge.\n"
        "Keep answers concise, structured, practical, and security-focused.\n\n"
        "Always format the answer using exactly these sections:\n"
        "Summary:\n"
        "Type:\n"
        "Why it matters:\n"
        "Practical mitigation / handling:\n"
        "Source:\n\n"
        "Rules:\n"
        "- Type must match the provided context.\n"
        "- If the record is a topic or technique, do not describe it as a vulnerability.\n"
        "- Source must state that the answer is based on the internal structured security knowledge dataset.\n"
        "- Do not add extra sections.\n"
    )


def call_openai_chat(context: str) -> Optional[str]:
    config = get_provider_config()
    api_key = config["api_key"]
    model = config["model"]

    if not api_key:
        return None

    try:
        from openai import OpenAI
    except Exception:
        return None

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": (
                        "Answer the user's query using only this structured context.\n\n"
                        f"{context}"
                    ),
                },
            ],
        )

        if hasattr(response, "output_text") and response.output_text:
            return response.output_text.strip()

        return None
    except Exception:
        return None


def generate_llm_answer(context: str, fallback_answer: str) -> str:
    if not llm_enabled():
        return fallback_answer

    answer = call_openai_chat(context)

    if answer:
        return answer

    return (
        fallback_answer
        + "\n\n[Note] LLM mode is enabled, but the provider is unavailable or not configured correctly."
    )
