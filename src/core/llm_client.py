from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMServiceError(RuntimeError):
    """Raised when the LLM service cannot safely complete a request."""


def call_llm(
    messages: list[dict],
    *,
    model: str = "gpt-4o-mini",
    temperature: float = 0,
    response_format: dict | None = None,
    timeout: float = 30.0,
    max_retries: int = 2,
):
    """
    Centralised LLM access with timeout, retry and safe failure.

    The application must never fabricate a response when the
    underlying model service fails.
    """

    client = OpenAI(
        timeout=timeout,
        max_retries=max_retries,
    )

    try:
        return client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=messages,
            response_format=response_format,
        )

    except Exception as exc:
        raise LLMServiceError(
            "LLM service unavailable or request failed. "
            "The application should fail safely rather than "
            "generate an unsupported result."
        ) from exc