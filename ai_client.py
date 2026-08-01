"""
Обёртка над OpenAI API и генерацией медиа.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE, OPENAI_IMAGE_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_reply(messages: list, temperature: float = 0.7) -> str:
    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def get_ai_speech(text: str) -> bytes:
    response = _client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text,
    )
    return response.content


def generate_image(prompt: str) -> bytes:
    response = _client.images.generate(
        model=OPENAI_IMAGE_MODEL,
        prompt=prompt,
        n=1,
        response_format="b64_json"
    )
    import base64
    image_bytes = base64.b64decode(response.data[0].b64_json)
    return image_bytes


def generate_video(prompt: str) -> bytes:
    """
    Ֆունկցիա վիդեո գեներացնելու համար (օրինակ Replicate / Runway / Stability API միջոցով):
    Այստեղ կարող եք տեղադրել Ձեր ընտրած Video API-ի կոդը:
    """
    # Օրինակ կոդ Replicate-ի կամ այլ API-ի համար.
    # raise NotImplementedError("Ավելացրեք Ձեր Video API-ի logic-ը")
    return b""