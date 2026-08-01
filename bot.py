import io
import threading
import os
import telebot
from telebot import types
from flask import Flask

import config
import database as db
from locales import UI_MESSAGES, get_system_prompt_text
from keyboards import (
    language_selection_keyboard,
    main_menu_inline_keyboard,
    crisis_keyboard,
    ai_reply_keyboard,
)
from ai_client import get_ai_reply, get_ai_speech, generate_video
from crisis_detector import contains_crisis_language

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
        text or msgs['menu_intro'],
        reply_markup=main_menu_inline_keyboard(lang_code)
    )


def _send_crisis_support(chat_id: int, lang_code: str):
    msgs = UI_MESSAGES[lang_code]
    bot.send_message(
        chat_id,
        msgs['crisis_warning'],
        parse_mode="Markdown",
        reply_markup=crisis_keyboard(lang_code)
    )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if not db.user_exists(chat_id):
        db.create_user(chat_id, 'en')
        _reset_conversation(chat_id, 'en')
    
    bot.send_message(
        chat_id,
        UI_MESSAGES['en']['welcome'],
        reply_markup=language_selection_keyboard()
    )


def _generate_and_send_video(chat_id: int, lang_code: str, text: str):
    """Վիդեոյի գեներացիայի ֆոնային պրոցես"""
    try:
        video_bytes = generate_video(text)
        if video_bytes:
            video_file = io.BytesIO(video_bytes)
            video_file.name = "generated_video.mp4"
            bot.send_video(chat_id, video_file, caption=UI_MESSAGES[lang_code]['video_done'])
        else:
            bot.send_message(chat_id, UI_MESSAGES[lang_code]['video_error'])
    except Exception as e:
        print(f"[Video error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['video_error'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('video_'))
def handle_video(call):
    chat_id = call.message.chat.id
    lang_code = _lang(chat_id)

    telegram_message_id = int(call.data.split('_', 1)[1])
    text = db.get_message_by_telegram_id(chat_id, telegram_message_id)
    
    if not text:
        bot.answer_callback_query(call.id, UI_MESSAGES[lang_code]['error'], show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, UI_MESSAGES[lang_code]['video_started'])

    thread = threading.Thread(
        target=_generate_and_send_video,
        args=(chat_id, lang_code, text),
        daemon=True,
    )
    thread.start()


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call):
    chat_id = call.message.chat.id
    lang_code = call.data.split('_')[1]

    db.set_user_language(chat_id, lang_code)
    _reset_conversation(chat_id, lang_code)

    bot.answer_callback_query(call.id)
    bot.send_message(
        chat_id,
        UI_MESSAGES[lang_code]['language_selected'],
        reply_markup=main_menu_inline_keyboard(lang_code)
    )


@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer_questions(message):
    chat_id = message.chat.id

    if not db.user_exists(chat_id):
        send_welcome(message)
        return

    lang_code = _lang(chat_id)
    text = message.text

    is_crisis = contains_crisis_language(text)
    db.add_message(chat_id, "user", text)

    history = db.get_recent_history_for_ai(chat_id, config.MAX_HISTORY_MESSAGES_FOR_AI)

    try:
        reply_text = get_ai_reply(history)
        db.add_message(chat_id, "assistant", reply_text)

        sent_msg = bot.send_message(
            chat_id,
            reply_text,
            reply_markup=ai_reply_keyboard(lang_code, message.message_id, show_music=bool(config.SUNO_API_KEY), show_video=True)
        )
        db.update_telegram_message_id(chat_id, reply_text, sent_msg.message_id)

        if is_crisis:
            _send_crisis_support(chat_id, lang_code)

    except Exception as e:
        print(f"[Error] chat_id={chat_id}: {e}")
        bot.send_message(chat_id, UI_MESSAGES[lang_code]['error'])


if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot is starting...")
    bot.infinity_polling()