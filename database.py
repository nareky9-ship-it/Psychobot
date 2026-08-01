"""
Слой работы с базой данных SQLite.

Хранит:
- users: chat_id пользователя и выбранный язык интерфейса
- messages: полная история сообщений (роль + текст) для каждого чата,
  используется и для восстановления контекста для OpenAI, и как архив истории.

SQLite выбран как простая встраиваемая база, не требующая отдельного сервера.
"""

import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DATABASE_PATH

_lock = threading.Lock()  # sqlite3 + многопоточность telebot требует простого лока


def _get_connection():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def _db_cursor():
    with _lock:
        conn = _get_connection()
        try:
            cur = conn.cursor()
            yield cur
            conn.commit()
        finally:
            conn.close()


def init_db():
    """Создаёт таблицы, если их ещё нет. Вызывается один раз при старте бота."""
    with _db_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                lang_code TEXT NOT NULL DEFAULT 'en',
                created_at TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('system', 'user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                telegram_message_id INTEGER,
                FOREIGN KEY (chat_id) REFERENCES users(chat_id)
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_chat_id
            ON messages(chat_id)
        """)

        # Миграция для существующих баз, созданных до добавления колонки.
        # Должна выполняться ДО создания индекса по этой колонке.
        cur.execute("PRAGMA table_info(messages)")
        existing_cols = {row[1] for row in cur.fetchall()}
        if "telegram_message_id" not in existing_cols:
            cur.execute("ALTER TABLE messages ADD COLUMN telegram_message_id INTEGER")

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_telegram_message_id
            ON messages(chat_id, telegram_message_id)
        """)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------- Пользователи / язык ----------

def set_user_language(chat_id: int, lang_code: str):
    with _db_cursor() as cur:
        cur.execute("""
            INSERT INTO users (chat_id, lang_code, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET lang_code = excluded.lang_code
        """, (chat_id, lang_code, _now()))


def get_user_language(chat_id: int):
    with _db_cursor() as cur:
        cur.execute("SELECT lang_code FROM users WHERE chat_id = ?", (chat_id,))
        row = cur.fetchone()
        return row[0] if row else None


def user_exists(chat_id: int) -> bool:
    return get_user_language(chat_id) is not None


# ---------- История сообщений ----------

def add_message(chat_id: int, role: str, content: str, telegram_message_id: int = None) -> int:
    """Возвращает id новой строки (нужен, чтобы позже проставить
    telegram_message_id через set_message_telegram_id)."""
    with _db_cursor() as cur:
        cur.execute("""
            INSERT INTO messages (chat_id, role, content, created_at, telegram_message_id)
            VALUES (?, ?, ?, ?, ?)
        """, (chat_id, role, content, _now(), telegram_message_id))
        return cur.lastrowid


def set_message_telegram_id(chat_id: int, row_id: int, telegram_message_id: int):
    """Проставляет telegram_message_id уже после отправки сообщения ботом
    (id самого сообщения в Telegram известен только после отправки)."""
    with _db_cursor() as cur:
        cur.execute("""
            UPDATE messages SET telegram_message_id = ?
            WHERE chat_id = ? AND id = ?
        """, (telegram_message_id, chat_id, row_id))


def get_message_by_telegram_id(chat_id: int, telegram_message_id: int):
    """Возвращает текст сообщения (для кнопок Copy/Hear под ответом ассистента)."""
    with _db_cursor() as cur:
        cur.execute("""
            SELECT content FROM messages
            WHERE chat_id = ? AND telegram_message_id = ?
            ORDER BY id DESC LIMIT 1
        """, (chat_id, telegram_message_id))
        row = cur.fetchone()
        return row[0] if row else None


def clear_history(chat_id: int):
    """Полностью удаляет историю сообщений пользователя (после /clear)."""
    with _db_cursor() as cur:
        cur.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))


def get_full_history(chat_id: int):
    """Возвращает всю сохранённую историю сообщений в хронологическом порядке."""
    with _db_cursor() as cur:
        cur.execute("""
            SELECT role, content FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
        """, (chat_id,))
        return [{"role": role, "content": content} for role, content in cur.fetchall()]


def get_recent_history_for_ai(chat_id: int, max_messages: int):
    """
    Возвращает системный промпт (если есть) + последние max_messages
    сообщений user/assistant - для отправки в OpenAI. Полная история
    всё равно остаётся в базе данных нетронутой.
    """
    with _db_cursor() as cur:
        cur.execute("""
            SELECT role, content FROM messages
            WHERE chat_id = ? AND role = 'system'
            ORDER BY id ASC LIMIT 1
        """, (chat_id,))
        system_row = cur.fetchone()

        cur.execute("""
            SELECT role, content FROM (
                SELECT id, role, content FROM messages
                WHERE chat_id = ? AND role IN ('user', 'assistant')
                ORDER BY id DESC LIMIT ?
            ) sub
            ORDER BY id ASC
        """, (chat_id, max_messages))
        recent_rows = cur.fetchall()

    messages = []
    if system_row:
        messages.append({"role": system_row[0], "content": system_row[1]})
    messages.extend({"role": role, "content": content} for role, content in recent_rows)
    return messages
