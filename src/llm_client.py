import os


def llm_enabled():
    return os.getenv("USE_LLM", "false").lower() == "true"


def generate_llm_answer(context, fallback_answer):
    """
    Safe wrapper:
    - If USE_LLM is false, return fallback answer
    - If USE_LLM is true later, this function becomes the integration point
    """
    if not llm_enabled():
        return fallback_answer

    # Placeholder for future provider integration
    # We intentionally keep this controlled for now.
    return (
        "LLM mode is enabled, but no provider integration is configured yet.\n\n"
        "Fallback answer:\n\n"
        f"{fallback_answer}\n\n"
        "Context passed to future LLM layer:\n"
        f"{context}"
    )
