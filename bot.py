

import io
import threading

import telebot
from telebot import types

import config
import database as db
from locales import UI_MESSAGES, get_system_prompt_text
from keyboards import (
    language_selection_keyboard,
    main_menu_inline_keyboard,
    crisis_keyboard,
    ai_reply_keyboard,
)
from ai_client import get_ai_reply, get_ai_speech
from crisis_detector import contains_crisis_language

import os
from flask import Flask

config.validate_config()
db.init_db()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)


app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


def _lang(chat_id: int) -> str:
    return db.get_user_language(chat_id) or 'en'


def _reset_conversation(chat_id: int, lang_code: str):
    db.clear_history(chat_id)
    db.add_message(chat_id, "system", get_system_prompt_text(lang_code))


def _send_main_menu(chat_id: int, lang_code: str, text: str = None):
    msgs = UI_MESSAGES[lang_code]
    bot.send_message(
        chat_id,
        text or msgs['menu_title'],
        reply_markup=main_menu_inline_keyboard(lang_code)
    )


def _send_crisis_support(chat_id: int, lang_code: str):
    msgs = UI_MESSAGES[lang_code]
    text = f"*{msgs['crisis_title']}*\n\n{msgs['crisis_body']}"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=crisis_keyboard(lang_code))


def _get_ai_response_and_send(chat_id: int, lang_code: str):
    bot.send_chat_action(chat_id, "typing")
    history_for_ai = db.get_recent_history_for_ai(chat_id, config.MAX_HISTORY_MESSAGES_FOR_AI)

    try:
        ai_reply = get_ai_reply(history_for_ai)
        row_id = db.add_message(chat_id, "assistant", ai_reply)

        sent = bot.send_message(chat_id, ai_reply)
        db.set_message_telegram_id(chat_id, row_id, sent.message_id)

        # Клавиатура Copy/Hear(/Music) привязана к message_id именно этого
        # сообщения, поэтому добавляем её отдельным edit после отправки.
        bot.edit_message_reply_markup(
            chat_id,
            sent.message_id,
            reply_markup=ai_reply_keyboard(lang_code, sent.message_id, show_music=config.suno_enabled())
        )
    except Exception as e:
        print(f"[OpenAI error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['error'])



@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        UI_MESSAGES['en']['welcome'],
        reply_markup=language_selection_keyboard()
    )


@bot.message_handler(commands=['clear', 'reset'])
def clear_memory_command(message):
    chat_id = message.chat.id
    lang_code = _lang(chat_id)
    _reset_conversation(chat_id, lang_code)
    bot.send_message(chat_id, UI_MESSAGES[lang_code]['memory_cleared'])


@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    lang_code = _lang(chat_id)
    bot.send_message(chat_id, UI_MESSAGES[lang_code]['help_intro'],
                      reply_markup=main_menu_inline_keyboard(lang_code))


@bot.message_handler(commands=['menu'])
def menu_command(message):
    chat_id = message.chat.id
    _send_main_menu(chat_id, _lang(chat_id))



@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    chat_id = call.message.chat.id
    lang_code = call.data.split('_')[1]

    is_new_user = not db.user_exists(chat_id)

    db.set_user_language(chat_id, lang_code)
    _reset_conversation(chat_id, lang_code)

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, UI_MESSAGES[lang_code]['lang_selected'])
    _send_main_menu(chat_id, lang_code)



@bot.callback_query_handler(func=lambda call: call.data.startswith('action_'))
def handle_menu_action(call):
    chat_id = call.message.chat.id
    lang_code = _lang(chat_id)
    action = call.data.split('_', 1)[1]

    bot.answer_callback_query(call.id)

    if action == 'lang':
        bot.send_message(chat_id, UI_MESSAGES['en']['welcome'],
                          reply_markup=language_selection_keyboard())
        return

    if action == 'clear':
        _reset_conversation(chat_id, lang_code)
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['memory_cleared'])
        return

    if action == 'about':
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['about'], parse_mode="Markdown")
        return

    if action == 'help':
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['help_intro'],
                          reply_markup=main_menu_inline_keyboard(lang_code))
        return

    if action == 'crisis':
        _send_crisis_support(chat_id, lang_code)
        return

    if action == 'tip':
        prompt = UI_MESSAGES[lang_code]['tip_prompt']
        db.add_message(chat_id, "user", prompt)
        _get_ai_response_and_send(chat_id, lang_code)
        return



@bot.callback_query_handler(func=lambda call: call.data.startswith('copy_'))
def handle_copy(call):
    chat_id = call.message.chat.id
    lang_code = _lang(chat_id)
    telegram_message_id = int(call.data.split('_', 1)[1])

    text = db.get_message_by_telegram_id(chat_id, telegram_message_id)
    if not text:
        bot.answer_callback_query(call.id, UI_MESSAGES[lang_code]['error'], show_alert=True)
        return

    bot.answer_callback_query(call.id)
    # Telegram не даёт боту напрямую положить текст в буфer обмена,
    # поэтому переотправляем текст моноширинным блоком - его удобно
    # скопировать одним тапом/долгим нажатием в самом Telegram.
    escaped = text.replace('`', "'")
    bot.send_message(
        chat_id,
        f"{UI_MESSAGES[lang_code]['copy_preamble']}\n\n```\n{escaped}\n```",
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('hear_'))
def handle_hear(call):
    chat_id = call.message.chat.id
    lang_code = _lang(chat_id)
    telegram_message_id = int(call.data.split('_', 1)[1])

    text = db.get_message_by_telegram_id(chat_id, telegram_message_id)
    if not text:
        bot.answer_callback_query(call.id, UI_MESSAGES[lang_code]['error'], show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_chat_action(chat_id, "record_voice")

    try:
        audio_bytes = get_ai_speech(text)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "reply.mp3"
        bot.send_voice(chat_id, audio_file)
    except Exception as e:
        print(f"[TTS error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['hear_error'])


def _generate_and_send_song(chat_id: int, lang_code: str, text: str):
    """Выполняется в отдельном потоке: обращается к Suno API и после
    готовности отправляет песню пользователю. Генерация занимает 1-3
    минуты, поэтому не должна блокировать основной поток бота (иначе
    бот не сможет отвечать другим пользователям всё это время)."""
    try:
        audio_bytes = suno_client.generate_song_from_text(text)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "song.mp3"
        bot.send_audio(chat_id, audio_file)
    except suno_client.SunoError as e:
        print(f"[Suno error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['music_error'])
    except Exception as e:
        print(f"[Suno unexpected error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['music_error'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('music_'))
def handle_music(call):
    chat_id = call.message.chat.id
    lang_code = _lang(chat_id)

    if not config.suno_enabled():
        bot.answer_callback_query(call.id)
        return

    telegram_message_id = int(call.data.split('_', 1)[1])
    text = db.get_message_by_telegram_id(chat_id, telegram_message_id)
    if not text:
        bot.answer_callback_query(call.id, UI_MESSAGES[lang_code]['error'], show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, UI_MESSAGES[lang_code]['music_started'])

    # Генерация занимает 1-3 минуты - запускаем в фоновом потоке,
    # чтобы бот тем временем продолжал отвечать всем остальным.
    thread = threading.Thread(
        target=_generate_and_send_song,
        args=(chat_id, lang_code, text),
        daemon=True,
    )
    thread.start()



@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_questions(message):
    chat_id = message.chat.id

    if not db.user_exists(chat_id):
        send_welcome(message)
        return

    lang_code = _lang(chat_id)
    text = message.text

    # На случай, если у пользователя ещё осталась старая reply-клавиатура
    # с текстовыми кнопками - поддержим и её.
    msgs = UI_MESSAGES[lang_code]
    if text == msgs['btn_lang']:
        bot.send_message(chat_id, UI_MESSAGES['en']['welcome'], reply_markup=language_selection_keyboard())
        return
    if text == msgs['btn_clear']:
        clear_memory_command(message)
        return
    if text == msgs['btn_about']:
        bot.send_message(chat_id, msgs['about'], parse_mode="Markdown")
        return
    if text == msgs['btn_crisis']:
        _send_crisis_support(chat_id, lang_code)
        return
    if text == msgs['btn_help']:
        bot.send_message(chat_id, msgs['help_intro'], reply_markup=main_menu_inline_keyboard(lang_code))
        return

    is_crisis = contains_crisis_language(text)

    db.add_message(chat_id, "user", text)
    _get_ai_response_and_send(chat_id, lang_code)

    if is_crisis:
        _send_crisis_support(chat_id, lang_code)

if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("Bot is starting...")
    bot.infinity_polling()