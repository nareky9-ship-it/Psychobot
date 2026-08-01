"""
Обёртка над OpenAI Chat Completions API.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE, OPENAI_IMAGE_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)


def get_ai_reply(messages: list, temperature: float = 0.7) -> str:
    """
    Отправляет историю сообщений в OpenAI и возвращает текст ответа.
    messages: список словарей {"role": ..., "content": ...}
    Может выбросить исключение при сетевой/API ошибке - обрабатывается вызывающим кодом.
    """
    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


def get_ai_speech(text: str) -> bytes:
    """
    Отправляет текст в OpenAI TTS и возвращает аудио (mp3) в виде байтов.
    Может выбросить исключение при сетевой/API ошибке - обрабатывается вызывающим кодом.
    """
    response = _client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text,
    )
    return response.content


def generate_image(prompt: str) -> bytes:
    """
    Генерирует изображение через OpenAI Images API (DALL-E) по
    текстовому описанию и возвращает готовые байты PNG-картинки.
    Может выбросить исключение при сетевой/API ошибке - обрабатывается вызывающим кодом.
    """
    import base64

    response = _client.images.generate(
        model=OPENAI_IMAGE_MODEL,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )
    b64_data = response.data[0].b64_json
    return base64.b64decode(b64_data)
