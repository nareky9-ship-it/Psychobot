"""
Клавиатуры бота.
"""

from telebot import types
from locales import UI_MESSAGES


def language_selection_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_en = types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    btn_ru = types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")
    btn_hy = types.InlineKeyboardButton("Հայերեն 🇦🇲", callback_data="lang_hy")
    markup.add(btn_en, btn_ru, btn_hy)
    return markup


def main_menu_inline_keyboard(lang_code: str):
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
    msgs = UI_MESSAGES[lang_code]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(msgs['btn_help'], callback_data="action_help"))
    return markup


def ai_reply_keyboard(lang_code: str, message_id: int, show_music: bool = False, show_video: bool = True):
    """Inline-клавиатура под каждым ответом: Copy, Hear, Music, Video."""
    msgs = UI_MESSAGES[lang_code]
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_copy = types.InlineKeyboardButton(msgs['btn_copy'], callback_data=f"copy_{message_id}")
    btn_hear = types.InlineKeyboardButton(msgs['btn_hear'], callback_data=f"hear_{message_id}")
    markup.add(btn_copy, btn_hear)

    extra_buttons = []
    if show_music:
        extra_buttons.append(types.InlineKeyboardButton(msgs['btn_music'], callback_data=f"music_{message_id}"))
    if show_video:
        extra_buttons.append(types.InlineKeyboardButton(msgs['btn_video'], callback_data=f"video_{message_id}"))

    if extra_buttons:
        markup.add(*extra_buttons)

    return markup