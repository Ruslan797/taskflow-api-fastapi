from openai import AsyncOpenAI
from google import genai
from google.genai import types

from app.core.config import settings


openai_client = AsyncOpenAI(
    api_key=settings.openai_api_key
)

gemini_client = genai.Client(
    api_key=settings.gemini_api_key,
    http_options=types.HttpOptions(
        timeout=30_000,
    ),
)