import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import random

# Expanded phrase databases categorized by languages, levels, and themes
phrase_databases = {
    'spanish': {
        'basic': {
            'greetings': [
                "hello - hola",
                "good morning - buenos días",
                "goodbye - adiós"
            ],
            'common_phrases': [
                "thank you - gracias",
                "please - por favor",
                "yes - sí",
                "no - no"
            ]
        },
        'intermediate': {
            'conversation': [
                "Can you help me? - ¿Puedes ayudarme?",
                "What is your name? - ¿Cuál es tu nombre?",
                "I am learning Spanish - Estoy aprendiendo español."
            ],
            'travel': [
                "Where is the bathroom? - ¿Dónde está el baño?",
                "I would like to order food - Me gustaría pedir comida.",
                "How much does it cost? - ¿Cuánto cuesta?"
            ],
            'food': [
                "I am vegetarian - Soy vegetariano.",
                "What do you recommend? - ¿Qué me recomiendas?",
                "Can I see the menu? - ¿Puedo ver el menú?"
            ],
            'shopping': [
                "Do you have this in another size? - ¿Tienes esto en otra talla?",
                "Can I try this on? - ¿Puedo probarme esto?",
                "I would like to buy this - Me gustaría comprar esto."
            ],
            'emergencies': [
                "I need a doctor - Necesito un médico.",
                "Call the police - Llame a la policía.",
                "I am lost - Estoy perdido."
            ],
            'culture': [
                "What is your favorite holiday? - ¿Cuál es tu festividad favorita?",
                "Tell me about your traditions - Cuéntame sobre tus tradiciones."
            ]
        }
    },
    'french': {
        'basic': {
            'greetings': [
                "hello - bonjour",
                "goodbye - au revoir",
                "thank you - merci"
            ],
            'common_phrases': [
                "please - s'il vous plaît",
                "yes - oui",
                "no - non"
            ]
        },
        'intermediate': {
            'conversation': [
                "Can I have the menu, please? - Puis-je avoir le menu, s'il vous plaît?",
                "I need help - J'ai besoin d'aide."
            ],
            'travel': [
                "Where is the train station? - Où est la gare?",
                "How do I get to the hotel? - Comment puis-je arriver à l'hôtel?"
            ],
            'food': [
                "I am allergic to nuts - Je suis allergique aux noix.",
                "What is the special today? - Quel est le plat du jour?",
                "Can I get this to go? - Puis-je emporter cela?"
            ],
            'shopping': [
                "How much is this? - Combien ça coûte?",
                "Do you accept credit cards? - Acceptez-vous les cartes de crédit?",
                "I’m just browsing - Je regarde seulement."
            ],
            'emergencies': [
                "I need help! - J'ai besoin d'aide!",
                "Where is the nearest hospital? - Où est l'hôpital le plus proche?",
                "I've lost my wallet - J'ai perdu mon portefeuille."
            ],
            'culture': [
                "What is a traditional dish? - Quel est un plat traditionnel?",
                "Tell me about French customs - Parlez-moi des coutumes françaises."
            ]
        }
    },
    'german': {
        'basic': {
            'greetings': [
                "hello - hallo",
                "goodbye - auf Wiedersehen",
                "thank you - danke"
            ],
            'common_phrases': [
                "please - bitte",
                "yes - ja",
                "no - nein"
            ]
        },
        'intermediate': {
            'conversation': [
                "What do you do? - Was machen Sie beruflich?",
                "Can you speak slowly? - Können Sie langsamer sprechen?"
            ],
            'travel': [
                "How do I get to the airport? - Wie komme ich zum Flughafen?",
                "Where can I find a taxi? - Wo kann ich ein Taxi finden?"
            ],
            'food': [
                "I would like a coffee - Ich hätte gern einen Kaffee.",
                "Is this dish spicy? - Ist dieses Gericht scharf?",
                "Can I have the bill, please? - Kann ich die Rechnung bitte haben?"
            ],
            'shopping': [
                "Do you have this in another color? - Haben Sie das in einer anderen Farbe?",
                "Can I return this? - Kann ich das zurückgeben?",
                "I am looking for a gift - Ich suche ein Geschenk."
            ],
            'emergencies': [
                "I need a doctor - Ich brauche einen Arzt.",
                "Call an ambulance - Rufen Sie einen Krankenwagen.",
                "I am in danger - Ich bin in Gefahr."
            ],
            'culture': [
                "What is your favorite German festival? - Was ist Ihr Lieblingsfest in Deutschland?",
                "Tell me about German traditions - Erzählen Sie mir von deutschen Traditionen."
            ]
        }
    },
    'italian': {
        'basic': {
            'greetings': [
                "hello - ciao",
                "goodbye - arrivederci",
                "thank you - grazie"
            ],
            'common_phrases': [
                "please - per favore",
                "yes - sì",
                "no - no"
            ]
        },
        'intermediate': {
            'conversation': [
                "What is your favorite food? - Qual è il tuo cibo preferito?",
                "Can you help me? - Puoi aiutarmi?"
            ],
            'travel': [
                "How far is the hotel? - Quanto dista l'hotel?",
                "I need a doctor - Ho bisogno di un dottore."
            ],
            'food': [
                "I would like a glass of wine - Vorrei un bicchiere di vino.",
                "What is the dessert of the day? - Qual è il dolce del giorno?",
                "Do you have gluten-free options? - Hai opzioni senza glutine?"
            ],
            'shopping': [
                "Can I get a discount? - Posso avere uno sconto?",
                "Where is the fitting room? - Dov'è il camerino?",
                "I want to buy this - Voglio comprare questo."
            ],
            'emergencies': [
                "I need help - Ho bisogno di aiuto.",
                "Where is the nearest hospital? - Dove si trova l'ospedale più vicino?",
                "I've lost my passport - Ho perso il mio passaporto."
            ],
            'culture': [
                "What is a famous Italian landmark? - Qual è un famoso monumento italiano?",
                "Tell me about Italian art - Parlami dell'arte italiana."
            ]
        }
    },
    'japanese': {
        'basic': {
            'greetings': [
                "hello - こんにちは (konnichiwa)",
                "goodbye - さようなら (sayōnara)",
                "thank you - ありがとうございます (arigatō gozaimasu)"
            ],
            'common_phrases': [
                "please - お願いします (onegai shimasu)",
                "yes - はい (hai)",
                "no - いいえ (iie)"
            ]
        },
        'intermediate': {
            'conversation': [
                "How was your day? - あなたの一日はどうでしたか？(anata no ichinichi wa dō deshita ka?)",
                "I love to travel - 旅行が好きです (ryokō ga suki desu)."
            ],
            'travel': [
                "Where is the nearest station? - 一番近い駅はどこですか？(ichiban chikai eki wa doko desu ka?)",
                "Can you recommend a good restaurant? - おすすめのレストランはありますか？(osusume no resutoran wa arimasu ka?)"
            ],
            'food': [
                "Is this dish vegetarian? - この料理はベジタリアンですか？(kono ryōri wa bejitarian desu ka?)",
                "I would like sushi - 寿司が食べたいです (sushi ga tabetai desu).",
                "What is the most popular food? - 一番人気のある食べ物は何ですか？(ichiban ninki no aru tabemono wa nan desu ka?)"
            ],
            'shopping': [
                "Do you have this in a different size? - これの違うサイズはありますか？(kore no chigau saizu wa arimasu ka?)",
                "Can I try this on? - これを試着できますか？(kore o shichaku dekimasu ka?)",
                "How much is this? - これはいくらですか？(kore wa ikura desu ka?)"
            ],
            'emergencies': [
                "I need assistance - 助けが必要です (tasuke ga hitsuyō desu).",
                "Call the police - 警察を呼んでください (keisatsu o yonde kudasai).",
                "I am lost - 道に迷いました (michi ni mayoimashita)."
            ],
            'culture': [
                "What is your favorite Japanese festival? - あなたの好きな日本の祭りは何ですか？(anata no sukina nippon no matsuri wa nan desu ka?)",
                "Tell me about traditional Japanese tea - 伝統的な日本の茶について教えてください (dentō-teki na nippon no cha ni tsuite oshiete kudasai)."
            ]
        }
    },
    'russian': {
        'basic': {
            'greetings': [
                "hello - привет (privet)",
                "goodbye - до свидания (do svidaniya)",
                "thank you - спасибо (spasibo)"
            ],
            'common_phrases': [
                "please - пожалуйста (pozhaluysta)",
                "yes - да (da)",
                "no - нет (net)"
            ]
        },
        'intermediate': {
            'conversation': [
                "How are you? - Как дела? (Kak dela?)",
                "What do you like to do? - Что ты любишь делать? (Chto ty lyubish' delat'?)"
            ],
            'travel': [
                "Where is the bus stop? - Где автобусная остановка? (Gde avtobusnaya ostanovka?)",
                "I need a hotel - Мне нужна гостиница (Mne nuzhna gostinitsa)."
            ],
            'food': [
                "I would like a bottle of water - Я хотел бы бутылку воды (Ya khotel by butylku vody).",
                "Is this dish spicy? - Это блюдо острое? (Eto blyudo ostroe?)",
                "What is a typical Russian dish? - Какое типичное русское блюдо? (Kakoye tipichnoye russkoye blyudo?)"
            ],
            'shopping': [
                "Can I get a refund? - Могу я получить возврат? (Mogu ya poluchit' vozvrat?)",
                "Where can I buy this? - Где я могу это купить? (Gde ya mogu eto kupit'?)",
                "I am just looking - Я просто смотрю (Ya prosto smotryu)."
            ],
            'emergencies': [
                "Help! - Помогите! (Pomogite!)",
                "I need a doctor - Мне нужен врач (Mne nuzhen vrach).",
                "Where is the nearest pharmacy? - Где ближайшая аптека? (Gde blizhayushchaya apteka?)"
            ],
            'culture': [
                "What is your favorite Russian tradition? - Какое ваше любимое русское традиционное событие? (Kakoye vashe lyubimoye russkoye traditsionnoye sobytiye?)",
                "Tell me about Russian literature - Расскажите мне о русской литературе (Rasskazhite mne o russkoy literaturе)."
            ]
        }
    },
    'chinese': {
        'basic': {
            'greetings': [
                "hello - 你好 (nǐ hǎo)",
                "goodbye - 再见 (zài jiàn)",
                "thank you - 谢谢 (xièxiè)"
            ],
            'common_phrases': [
                "please - 请 (qǐng)",
                "yes - 是 (shì)",
                "no - 不是 (bú shì)"
            ]
        },
        'intermediate': {
            'conversation': [
                "How old are you? - 你几岁？(nǐ jǐ suì?)",
                "What is your job? - 你做什么工作？(nǐ zuò shénme gōngzuò?)"
            ],
            'travel': [
                "Where is the nearest subway station? - 最近的地铁站在哪里？(zuìjìn de dìtiě zhàn zài nǎlǐ?)",
                "Can I have a taxi? - 我可以叫一辆出租车吗？(wǒ kěyǐ jiào yī liàng chūzūchē ma?)"
            ],
            'food': [
                "I am allergic to shellfish - 我对贝类过敏 (wǒ duì bèilèi guòmǐn).",
                "Can I have this without meat? - 我可以要这个不放肉吗？(wǒ kěyǐ yào zhège bù fàng ròu ma?)",
                "What is your signature dish? - 你的招牌菜是什么？(nǐ de zhāopái cài shì shénme?)"
            ],
            'shopping': [
                "Do you have this in another color? - 你有其他颜色吗？(nǐ yǒu qítā yánsè ma?)",
                "Can I pay with cash? - 我可以用现金支付吗？(wǒ kěyǐ yòng xiànjīn zhīfù ma?)",
                "How much is this? - 这个多少钱？(zhège duōshǎo qián?)"
            ],
            'emergencies': [
                "I need help - 我需要帮助 (wǒ xūyào bāngzhù).",
                "Call the police - 报警 (bàojǐng).",
                "I lost my phone - 我丢了我的手机 (wǒ diūle wǒ de shǒujī)."
            ],
            'culture': [
                "What is your favorite Chinese festival? - 你最喜欢的中国节日是什么？(nǐ zuì xǐhuān de zhōngguó jiérì shì shénme?)",
                "Tell me about Chinese art - 告诉我关于中国艺术的事 (gàosù wǒ guānyú zhōngguó yìshù de shì)."
            ]
        }
    }
}

def speak(text, lang_code):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang=lang_code)
    tts_file = "temp.mp3"
    tts.save(tts_file)
    playsound.playsound(tts_file)
    os.remove(tts_file)

def listen():
    """Listen for a voice command and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def choose_language():
    """Prompt user to choose a language for learning."""
    languages = list(phrase_databases.keys())
    language_list = ", ".join(languages)
    speak(f"Choose a language to learn: {language_list}.", 'en')

    while True:
        user_language = listen()
        if user_language in languages:
            lang_code = 'es' if user_language == 'spanish' else \
                        'fr' if user_language == 'french' else \
                        'de' if user_language == 'german' else \
                        'it' if user_language == 'italian' else \
                        'ja' if user_language == 'japanese' else \
                        'ru' if user_language == 'russian' else \
                        'zh' if user_language == 'chinese' else 'en'
            return user_language, lang_code
        speak("I didn't understand that. Please choose a valid language.", 'en')

def learn_language(language, lang_code):
    """Main learning loop for chosen language."""
    speak(f"Welcome to the {language} learning program!", lang_code)
    
    for level in ['basic', 'intermediate']:
        user_theme = choose_theme(language, level)
        phrases = phrase_databases[language][level][user_theme]

        for phrase in phrases:
            english, translation = phrase.split(" - ")
            speak(f"Translate this: '{english}'.", lang_code)
            user_response = listen()
            
            if user_response and user_response.strip() == translation.strip():
                speak("Correct!", lang_code)
            else:
                speak(f"Wrong! The correct answer is '{translation}'.", lang_code)
            
            speak("Do you want to try another phrase? Say 'yes' or 'no'.", lang_code)
            continue_response = listen()
            
            if continue_response and 'no' in continue_response:
                break

        speak(f"Great job with the {level} level! Let's move to the next level!", lang_code)

    speak("Thank you for learning with me! Goodbye!", lang_code)

def choose_theme(language, level):
    """Prompt user to choose a theme for learning."""
    themes = phrase_databases[language][level].keys()
    theme_list = ", ".join(themes)
    speak(f"Choose a theme to learn: {theme_list}.", 'en')
    
    while True:
        user_theme = listen()
        if user_theme in themes:
            return user_theme
        speak("I didn't understand that. Please choose a valid theme.", 'en')

if __name__ == "__main__":
    language, lang_code = choose_language()
    learn_language(language, lang_code)