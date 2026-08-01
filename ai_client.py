"""
Обёртка над OpenAI Chat Completions API.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE

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
