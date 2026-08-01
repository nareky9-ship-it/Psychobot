"""
Все тексты интерфейса и системные промпты для трёх языков:
английский (en), русский (ru), армянский (hy).
"""

LANG_NAMES = {
    'en': 'English',
    'ru': 'Russian',
    'hy': 'Armenian'
}

PSYCHOLOGY_SYSTEM_PROMPT = (
    "You are PsychoBot, a supportive AI companion focused on psychology and mental well-being. "
    "You are not a licensed therapist, psychiatrist, or medical professional, and you never claim to be one. "
    "You provide emotional support, active listening, psychoeducation, and practical coping strategies "
    "grounded in established approaches (e.g. CBT-style reframing, mindfulness, grounding techniques, "
    "breathing exercises, journaling prompts).\n\n"
    "HOW YOU TALK:\n"
    "- Be warm, empathetic, patient, and non-judgmental. Validate feelings before offering suggestions.\n"
    "- Ask gentle, open-ended follow-up questions to understand the person's situation before jumping to advice.\n"
    "- Keep responses conversational and human, not clinical or robotic.\n"
    "- Never diagnose the user with any mental health condition, even informally.\n"
    "- Never assume what the person is feeling or why - reflect only what they've actually told you.\n"
)

UI_MESSAGES = {
    'en': {
        'welcome': "👋 Hello! I am PsychoBot, your supportive AI companion.\n\nPlease select your language:",
        'language_selected': "🌐 Language set to English. How can I support you today?",
        'menu_intro': "How can I help you right now?",
        'tip_prompt': "Give me one short, practical psychological tip or mindfulness micro-exercise for today.",
        'history_cleared': "🧹 Memory cleared! Our conversation has been reset.",
        'about': (
            "ℹ️ *About PsychoBot*\n\n"
            "PsychoBot is an AI assistant designed to provide emotional support and active listening."
        ),
        'help_intro': "Here are the main actions you can take:",
        'crisis_warning': (
            "🆘 *Crisis Support*\n\n"
            "If you are in immediate danger, please reach out to professional emergency services or a hotline."
        ),
        'btn_lang': "🌐 Change Language",
        'btn_clear': "🧹 Clear Memory",
        'btn_tip': "💡 Quick Tip",
        'btn_about': "ℹ️ About Bot",
        'btn_crisis': "🆘 Crisis Support",
        'btn_help': "❓ Help",
        'btn_copy': "📋 Copy",
        'btn_hear': "🔊 Hear",
        'btn_music': "🎵 Create Song",
        'btn_video': "🎬 Create Video",
        'voice_started': "🔊 Converting to voice...",
        'music_started': "🎵 Generating music...",
        'music_done': "🎵 Here is your music track!",
        'music_error': "Sorry, couldn't generate music right now.",
        'video_started': "🎬 Generating video, please wait...",
        'video_done': "🎬 Here is your video!",
        'video_error': "Sorry, couldn't generate video right now.",
        'error': "An error occurred. Please try again.",
        'copy_notice': "Copied to clipboard!",
    },
    'ru': {
        'welcome': "👋 Привет! Я PsychoBot, ваш ИИ-помощник.\n\nПожалуйста, выберите язык:",
        'language_selected': "🌐 Язык изменён на русский. Как я могу помочь вам сегодня?",
        'menu_intro': "Чем я могу помочь вам прямо сейчас?",
        'tip_prompt': "Дай один короткий, практический психологический совет или микро-упражнение на сегодня.",
        'history_cleared': "🧹 Память очищена! Наш диалог сброшен.",
        'about': (
            "ℹ️ *О боте PsychoBot*\n\n"
            "PsychoBot — это ИИ-ассистент для эмоциональной поддержки."
        ),
        'help_intro': "Вот основные действия:",
        'crisis_warning': (
            "🆘 *Кризисная поддержка*\n\n"
            "Если вы в опасности, пожалуйста, обратитесь в службы экстренной помощи."
        ),
        'btn_lang': "🌐 Сменить язык",
        'btn_clear': "🧹 Очистить память",
        'btn_tip': "💡 Быстрый совет",
        'btn_about': "ℹ️ О боте",
        'btn_crisis': "🆘 Помощь в кризисе",
        'btn_help': "❓ Помощь",
        'btn_copy': "📋 Копировать",
        'btn_hear': "🔊 Озвучить",
        'btn_music': "🎵 Создать песню",
        'btn_video': "🎬 Создать видео",
        'voice_started': "🔊 Преобразую текст в голос...",
        'music_started': "🎵 Генерирую музыку...",
        'music_done': "🎵 Вот ваша музыкальная трек!",
        'music_error': "Извините, не удалось сгенерировать музыку.",
        'video_started': "🎬 Генерирую видео, пожалуйста, подождите...",
        'video_done': "🎬 Вот ваше видео!",
        'video_error': "Извините, не удалось сгенерировать видео.",
        'error': "Произошла ошибка. Попробуйте еще раз.",
        'copy_notice': "Скопировано!",
    },
    'hy': {
        'welcome': "👋 Ողջույն: Ես PsychoBot-ն եմ, Ձեր աջակից ԱԻ օգնականը:\n\nԽնդրում ենք ընտրել լեզուն:",
        'language_selected': "🌐 Լեզուն փոխվել է հայերենի: Ինչպե՞ս կարող եմ աջակցել Ձեզ այսօր:",
        'menu_intro': "Ինչպե՞ս կարող եմ օգնել Ձեզ հիմա:",
        'tip_prompt': "Տուր մեկ կարճ, գործնական հոգեբանական խորհուրդ կամ վարժություն այսօրվա համար:",
        'history_cleared': "🧹 Հիշողությունը մաքրվեց: Մեր զրույցը վերասկսված է:",
        'about': (
            "ℹ️ *PsychoBot-ի մասին*\n\n"
            "PsychoBot-ը արհեստական բանականությամբ աշխատող աջակից է:"
        ),
        'help_intro': "Ահա հիմնական գործողությունները, որոնք կարող եք կատարել.",
        'crisis_warning': (
            "🆘 *Աջակցություն ճգնաժամային պահերին*\n\n"
            "Եթե կա անմիջական վտանգ, խնդրում ենք զանգահարել շտապ օգնություն (911 կամ 112):"
        ),
        'btn_lang': "🌐 Փոխել լեզուն",
        'btn_clear': "🧹 Մաքրել հիշողությունը",
        'btn_tip': "💡 Արագ խորհուրդ",
        'btn_about': "ℹ️ Բոտի մասին",
        'btn_crisis': "🆘 Օգնություն ճգնաժամում",
        'btn_help': "❓ Օգնություն",
        'btn_copy': "📋 Պատճենել",
        'btn_hear': "🔊 Լսել",
        'btn_music': "🎵 Ստեղծել երգ",
        'btn_video': "🎬 Ստեղծել վիդեո",
        'voice_started': "🔊 Ձայնագրում եմ տեքստը...",
        'music_started': "🎵 Ստեղծում եմ երգը...",
        'music_done': "🎵 Ահա Ձեր երգը:",
        'music_error': "Ցավոք, չհաջողվեց ստեղծել երգը:",
        'video_started': "🎬 Ստեղծում եմ վիդեոն, խնդրում ենք սպասել...",
        'video_done': "🎬 Ահա Ձեր վիդեոն:",
        'video_error': "Ցավոք, չհաջողվեց ստեղծել վիդեոն:",
        'error': "Տեղի ունեցավ սխալ: Խնդրում ենք փորձել կրկին:",
        'copy_notice': "Պատճենված է:",
    }
}

def get_system_prompt_text(lang_code: str) -> str:
    return PSYCHOLOGY_SYSTEM_PROMPT