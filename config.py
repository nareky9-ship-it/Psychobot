"""
Конфигурация проекта.
Все секреты (токены, ключи) читаются из файла .env и НЕ хранятся в коде.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из файла .env в окружение

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "dall-e-3")
DATABASE_PATH = os.getenv("DATABASE_PATH", "psychobot.db")

# Suno API (sunoapi.org) - генерация музыки/песни на основе текста ответа бота.
# Необязательная функция: если ключ не задан, кнопка "Music" будет недоступна,
# но остальной бот продолжит работать нормально.
SUNO_API_KEY = os.getenv("SUNO_API_KEY")
SUNO_API_BASE_URL = os.getenv("SUNO_API_BASE_URL", "https://api.sunoapi.org")
SUNO_MODEL = os.getenv("SUNO_MODEL", "V4_5")
# Сколько максимум ждать (секунд) генерацию песни, прежде чем сдаться.
SUNO_MAX_WAIT_SECONDS = int(os.getenv("SUNO_MAX_WAIT_SECONDS", "240"))
# Как часто опрашивать статус задачи (секунд).
SUNO_POLL_INTERVAL_SECONDS = int(os.getenv("SUNO_POLL_INTERVAL_SECONDS", "5"))

# Максимальное количество последних сообщений (с учётом системного промпта),
# которые отправляются в OpenAI, чтобы не раздувать стоимость запроса.
# Полная история всё равно хранится в базе данных.
MAX_HISTORY_MESSAGES_FOR_AI = 20


def validate_config():
    """Проверяет, что обязательные переменные окружения заданы."""
    missing = []
    if not TELEGRAM_BOT_TOKEN or "REPLACE_ME" in TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not OPENAI_API_KEY or "REPLACE_ME" in OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if missing:
        raise RuntimeError(
            "Не заданы обязательные переменные окружения в файле .env: "
            + ", ".join(missing)
            + ".\nОткрой файл .env и впиши свои реальные ключи."
        )


def suno_enabled() -> bool:
    """True, если задан ключ Suno API - тогда кнопка 'Music' будет показана.
    Функция не обязательна для работы бота в целом."""
    return bool(SUNO_API_KEY and "REPLACE_ME" not in SUNO_API_KEY)
