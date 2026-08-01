"""
Клавиатуры бота.

- Выбор языка и главное меню действий сделаны как INLINE-кнопки
  (прикреплены к сообщению, не занимают место под полем ввода).
- Reply-клавиатура тоже доступна как быстрый постоянный доступ к разделам,
  но основной способ взаимодействия - inline.
"""

from telebot import types
from locales import UI_MESSAGES


def language_selection_keyboard():
    """Inline-клавиатура выбора языка (используется в /start и при смене языка)."""
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_en = types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    btn_ru = types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")
    btn_hy = types.InlineKeyboardButton("Հայերեն 🇦🇲", callback_data="lang_hy")
    markup.add(btn_en, btn_ru, btn_hy)
    return markup


def main_menu_inline_keyboard(lang_code: str):
    """Основное inline-меню действий бота."""
    msgs = UI_MESSAGES[lang_code]
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn_tip = types.InlineKeyboardButton(msgs['btn_tip'], callback_data="action_tip")
    btn_clear = types.InlineKeyboardButton(msgs['btn_clear'], callback_data="action_clear")
    btn_crisis = types.InlineKeyboardButton(msgs['btn_crisis'], callback_data="action_crisis")
    btn_help = types.InlineKeyboardButton(msgs['btn_help'], callback_data="action_help")
    btn_about = types.InlineKeyboardButton(msgs['btn_about'], callback_data="action_about")
    btn_lang = types.InlineKeyboardButton(msgs['btn_lang'], callback_data="action_lang")

    markup.add(btn_tip, btn_clear)
    markup.add(btn_crisis, btn_help)
    markup.add(btn_about, btn_lang)
    return markup


def crisis_keyboard(lang_code: str):
    """Маленькая inline-клавиатура под сообщением с кризисной поддержкой,
    даёт быстрый путь обратно в главное меню."""
    msgs = UI_MESSAGES[lang_code]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(msgs['btn_help'], callback_data="action_help"))
    return markup


def ai_reply_keyboard(lang_code: str, message_id: int, show_music: bool = False):
    """Inline-клавиатура под каждым ответом ассистента: Copy, Hear (озвучить)
    и, если доступно, Music (сгенерировать песню через Suno).
    message_id - это telegram message_id именно этого сообщения бота,
    используется потом чтобы найти текст в базе данных."""
    msgs = UI_MESSAGES[lang_code]
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_copy = types.InlineKeyboardButton(msgs['btn_copy'], callback_data=f"copy_{message_id}")
    btn_hear = types.InlineKeyboardButton(msgs['btn_hear'], callback_data=f"hear_{message_id}")
    markup.add(btn_copy, btn_hear)

    if show_music:
        btn_music = types.InlineKeyboardButton(msgs['btn_music'], callback_data=f"music_{message_id}")
        markup.add(btn_music)

    return markup
