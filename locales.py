"""
Все тексты интерфейса и системные промпты для трёх языков:
английский (en), русский (ru), армянский (hy).
"""

LANG_NAMES = {
    'en': 'English',
    'ru': 'Russian',
    'hy': 'Armenian'
}

# Системный промпт для OpenAI. Собран так, чтобы бот вёл себя как
# внимательный, тёплый, но ответственный психологический ассистент -
# а не имитировал лицензированного врача.
PSYCHOLOGY_SYSTEM_PROMPT = (
    "You are PsychoBot, a supportive AI companion focused on psychology and mental well-being. "
    "You are not a licensed therapist, psychiatrist, or medical professional, and you never claim to be one. "
    "You provide emotional support, active listening, psychoeducation, and practical coping strategies "
    "grounded in established approaches (e.g. CBT-style reframing, mindfulness, grounding techniques, "
    "breathing exercises, journaling prompts).\n\n"
    "HOW YOU TALK:\n"
    "- Be warm, empathetic, patient, and non-judgmental. Validate feelings before offering suggestions.\n"
    "- Ask gentle, open-ended follow-up questions to understand the person's situation before jumping to advice.\n"
    "- Keep responses conversational and human, not clinical or robotic. Avoid long bullet-point lectures unless "
    "the person clearly wants a structured exercise.\n"
    "- Never diagnose the user with any mental health condition, even informally.\n"
    "- Never assume what the person is feeling or why - reflect only what they've actually told you.\n"
    "- If the person asks something totally unrelated to psychology/well-being, gently redirect the "
    "conversation back to how they're doing, without being preachy about it.\n\n"
    "SAFETY BOUNDARIES:\n"
    "- You do not prescribe medication, dosages, or diagnoses.\n"
    "- You do not provide instructions that could facilitate self-harm.\n"
    "- If someone expresses suicidal thoughts, self-harm, or being in crisis, respond with care, take it "
    "seriously, and encourage them to reach out to a crisis line or trusted person/professional - do not just "
    "give a generic tip and move on.\n\n"
    "CRITICAL LANGUAGE REQUIREMENT: YOU MUST RESPOND EXCLUSIVELY IN {lang_name}. "
    "DO NOT SWITCH TO ENGLISH OR ANY OTHER LANGUAGE UNDER ANY CIRCUMSTANCES, EVEN IF THE USER WRITES IN "
    "ANOTHER LANGUAGE. Use natural, fluent, grammatically correct {lang_name}."
)

UI_MESSAGES = {
    'en': {
        'welcome': "Welcome! Please choose your language / Добро пожаловать! Выберите язык / Բարի գալուստ! Ընտրեք լեզուն:",
        'lang_selected': "Language set to English! How can I help you today?",
        'memory_cleared': "My memory was wiped clean! Let's start fresh.",
        'error': "Oops, something went wrong on my side, please try again in a moment.",
        'about': (
            "🤖 *PsychoBot* is your AI companion for mental well-being, emotional support, and self-care tips.\n\n"
            "_Note: I am not a medical professional or licensed therapist. If you're in crisis, please use the "
            "hotlines available via the Crisis Help button or contact local emergency services._"
        ),
        'tip_prompt': "Give me one short, practical psychology or mindfulness exercise to help ground or relax right now.",
        'help_intro': (
            "You can just write to me like you would to a supportive friend - tell me what's on your mind.\n\n"
            "Or use the menu below:\n"
            "💡 Quick Tip - a short grounding/relaxation exercise\n"
            "🧹 Clear Memory - start our conversation fresh\n"
            "🌐 Change Language - switch interface language\n"
            "🆘 Crisis Help - hotlines if you or someone else is in danger\n"
            "ℹ️ About Bot - what I can and can't do"
        ),
        'crisis_title': "🆘 If you're in danger right now",
        'crisis_body': (
            "I'm really glad you reached out, and I want you to be safe. I'm an AI and can't provide emergency "
            "help myself, but real people can, right now:\n\n"
            "• If you are in immediate physical danger, please call your local emergency number "
            "(e.g. 911 in the US, 112 in the EU).\n"
            "• US & Canada: call or text 988 (Suicide & Crisis Lifeline)\n"
            "• UK: call 116 123 (Samaritans)\n"
            "• International list of hotlines: https://findahelpline.com\n\n"
            "You don't have to go through this alone. Please reach out to one of these, or to someone you trust."
        ),
        'btn_lang': "🌐 Change Language",
        'btn_clear': "🧹 Clear Memory",
        'btn_tip': "💡 Quick Tip",
        'btn_about': "ℹ️ About Bot",
        'btn_crisis': "🆘 Crisis Help",
        'btn_help': "❓ Help",
        'btn_copy': "📋 Copy",
        'btn_hear': "🔊 Hear",
        'btn_music': "🎵 Make it a song",
        'copy_preamble': "Here's the text again, ready to copy:",
        'hear_error': "Sorry, I couldn't generate the audio right now. Please try again in a moment.",
        'music_started': "🎶 Generating your song, this can take 1-3 minutes... I'll send it as soon as it's ready!",
        'music_error': "Sorry, I couldn't generate the song right now. Please try again in a moment.",
        'menu_title': "Choose an option, or just type your message:",
    },
    'ru': {
        'welcome': "Добро пожаловать! Выберите язык интерфейса:",
        'lang_selected': "Выбран русский язык! Чем я могу вам помочь?",
        'memory_cleared': "Моя память была очищена! Начнём разговор заново.",
        'error': "Ой, что-то пошло не так на моей стороне, попробуйте ещё раз через минуту.",
        'about': (
            "🤖 *PsychoBot* — ваш ИИ-помощник по ментальному здоровью, эмоциональной поддержке и заботе о себе.\n\n"
            "_Примечание: я не являюсь врачом или лицензированным терапевтом. Если вы в кризисной ситуации, "
            "воспользуйтесь кнопкой «Помощь в кризисе» или обратитесь в экстренные службы._"
        ),
        'tip_prompt': "Дай мне одно короткое и практичное психологическое или дыхательное упражнение для расслабления и снятия стресса.",
        'help_intro': (
            "Вы можете просто писать мне, как близкому человеку - расскажите, что у вас на душе.\n\n"
            "Или воспользуйтесь меню ниже:\n"
            "💡 Быстрый совет - короткое упражнение на расслабление\n"
            "🧹 Очистить память - начать разговор заново\n"
            "🌐 Сменить язык - изменить язык интерфейса\n"
            "🆘 Помощь в кризисе - горячие линии, если вам или кому-то грозит опасность\n"
            "ℹ️ О боте - что я умею, а что нет"
        ),
        'crisis_title': "🆘 Если вам сейчас угрожает опасность",
        'crisis_body': (
            "Я очень рад(а), что вы написали, и хочу, чтобы вы были в безопасности. Я ИИ и не могу оказать "
            "экстренную помощь сам(а), но реальные люди могут - прямо сейчас:\n\n"
            "• Если есть непосредственная угроза жизни - позвоните по номеру экстренных служб вашей страны "
            "(например, 112).\n"
            "• Россия: Телефон доверия МЧС/психологической помощи 8-800-2000-122\n"
            "• Международный список горячих линий: https://findahelpline.com\n\n"
            "Вам не обязательно проходить через это в одиночку. Пожалуйста, обратитесь по одному из этих "
            "контактов или к тому, кому доверяете."
        ),
        'btn_lang': "🌐 Сменить язык",
        'btn_clear': "🧹 Очистить память",
        'btn_tip': "💡 Быстрый совет",
        'btn_about': "ℹ️ О боте",
        'btn_crisis': "🆘 Помощь в кризисе",
        'btn_help': "❓ Помощь",
        'btn_copy': "📋 Копировать",
        'btn_hear': "🔊 Озвучить",
        'btn_music': "🎵 Сделать песню",
        'copy_preamble': "Вот текст ещё раз, чтобы удобно скопировать:",
        'hear_error': "Извините, не получилось создать аудио прямо сейчас. Попробуйте ещё раз через минуту.",
        'music_started': "🎶 Генерирую песню, это может занять 1-3 минуты... Пришлю, как только будет готово!",
        'music_error': "Извините, не получилось создать песню прямо сейчас. Попробуйте ещё раз через минуту.",
        'menu_title': "Выберите пункт меню или просто напишите сообщение:",
    },
    'hy': {
        'welcome': "Բարի գալուստ: Խնդրում ենք ընտրել լեզուն.",
        'lang_selected': "Ընտրված է հայերեն լեզուն: Ինչպե՞ս կարող եմ օգնել Ձեզ:",
        'memory_cleared': "Հիշողությունը մաքրվեց: Սկսենք զրույցը սկզբից:",
        'error': "Տեղի ունեցավ սխալ իմ կողմից, խնդրում ենք փորձել կրկին մի փոքր ուշ:",
        'about': (
            "🤖 *PsychoBot*-ը Ձեր ԱԻ օգնականն է հոգեկան առողջության, հուզական աջակցության և "
            "ինքնախնամքի հարցերում:\n\n"
            "_Նշում. Ես բժիշկ կամ լիցենզավորված թերապևտ չեմ: Եթե Դուք ճգնաժամային իրավիճակում եք, "
            "խնդրում ենք օգտվել «Օգնություն ճգնաժամում» կոճակից կամ դիմել շտապ օգնության ծառայություններին._"
        ),
        'tip_prompt': "Խնդրում եմ տալ մեկ կարճ, գործնական հոգեբանական կամ շնչառական վարժություն լարվածությունը թեթևացնելու համար:",
        'help_intro': (
            "Կարող եք ուղղակի գրել ինձ, ինչպես մտերիմ մարդու՝ պատմեք, թե ինչ է Ձեզ մտահոգում:\n\n"
            "Կամ օգտվեք ստորև ընտրացանկից.\n"
            "💡 Արագ խորհուրդ - կարճ հանգստացնող վարժություն\n"
            "🧹 Մաքրել հիշողությունը - սկսել զրույցը սկզբից\n"
            "🌐 Փոխել լեզուն - փոխել ինտերֆեյսի լեզուն\n"
            "🆘 Օգնություն ճգնաժամում - թեժ գծեր, եթե Ձեզ կամ մեկ ուրիշին վտանգ է սպառնում\n"
            "ℹ️ Բոտի մասին - ինչ կարող եմ և ինչ չեմ կարող անել"
        ),
        'crisis_title': "🆘 Եթե հիմա վտանգի տակ եք",
        'crisis_body': (
            "Ես շատ ուրախ եմ, որ գրեցիք, և ուզում եմ, որ Դուք անվտանգ լինեք: Ես ԱԻ եմ և չեմ կարող ինքս "
            "շտապ օգնություն ցուցաբերել, բայց իրական մարդիկ կարող են՝ հենց հիմա.\n\n"
            "• Եթե կա անմիջական վտանգ կյանքի համար, խնդրում ենք զանգահարել շտապ օգնության համարով "
            "(օրինակ՝ 911 կամ 112):\n"
            "• Հայաստան: Հոգեբանական աջակցության թեժ գիծ 8-800-2000-122\n"
            "• Թեժ գծերի միջազգային ցանկ. https://findahelpline.com\n\n"
            "Պարտադիր չէ դա միայնակ հաղթահարել: Խնդրում ենք դիմել այս կոնտակտներից որևէ մեկին կամ "
            "մեկին, ում վստահում եք:"
        ),
        'btn_lang': "🌐 Փոխել լեզուն",
        'btn_clear': "🧹 Մաքրել հիշողությունը",
        'btn_tip': "💡 Արագ խորհուրդ",
        'btn_about': "ℹ️ Բոտի մասին",
        'btn_crisis': "🆘 Օգնություն ճգնաժամում",
        'btn_help': "❓ Օգնություն",
        'btn_copy': "📋 Պատճենել",
        'btn_hear': "🔊 Լսել",
        'btn_music': "🎵 Դարձնել երգ",
        'copy_preamble': "Ահա տեքստը կրկին՝ պատճենելու համար.",
        'hear_error': "Ցավոք, հիմա չհաջողվեց ստեղծել աուդիո: Խնդրում ենք փորձել կրկին մի փոքր ուշ:",
        'music_started': "🎶 Ստեղծում եմ երգը, սա կարող է տևել 1-3 րոպե... Կուղարկեմ հենց պատրաստ լինի!",
        'music_error': "Ցավոք, հիմա չհաջողվեց ստեղծել երգը: Խնդրում ենք փորձել կրկին մի փոքր ուշ:",
        'menu_title': "Ընտրեք ընտրացանկից կամ պարզապես գրեք Ձեր հաղորդագրությունը.",
    }
}


def get_system_prompt_text(lang_code: str) -> str:
    lang_name = LANG_NAMES.get(lang_code, 'English')
    return PSYCHOLOGY_SYSTEM_PROMPT.format(lang_name=lang_name)
