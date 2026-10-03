import os

from dotenv import load_dotenv


def test_openai_api_key_is_configured():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    assert api_key is not None
    assert api_key.startswith("sk-")