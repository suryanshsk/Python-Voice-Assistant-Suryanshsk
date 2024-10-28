
# json , translate and pyttsx3 libraries
#make sure there are no microphone or hardware issues

import speech_recognition as sr
import pyttsx3
from translate import Translator
from langdetect import detect
import json
import os

# Initialize the TTS engine
engine = pyttsx3.init()

#Define a file to save the translaton history
HISTORY_FILE = 'translation_history.json'

#load previous history if it exists
def load_translation_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

#save translation history
def save_translation_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
        
#Initialize translation history
translation_history = load_translation_history()

# Function to translate using translate-python
def translate_text(text, target_language):
    translations = {}
    for lang in target_language:
        try:
            translator = Translator(to_lang=lang)
            translations[lang] = translator.translate(text)
        except Exception as e:
            translations[lang] = f"Error: {e}"
    return translations

# Function to speak the translated text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
# Function to capture voice commands and convert speech to text
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Captured voice command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return "Sorry, the speech recognition service is not available."

# Function to process translation commands via voice
def process_translation_command(command):
    if "translate" in command.lower():
        try:
            print(f"Command received for translation: {command}")

            # Parse the command to extract the text and target languages
            if "'" not in command or "to " not in command:
                speak("Please provide a valid command, for example: Translate 'Hello' to French, Spanish.")
                return

            text_to_translate = command.split("'")[1]
            target_languages = command.split("to ")[1].strip().lower().split(",")  # Support multiple languages
            target_languages = [lang.strip() for lang in target_languages]

            # Detect the language of the input text
            source_language = detect(text_to_translate)
            print(f"Detected language: {source_language}")

            # Perform the translation
            translated_texts = translate_text(text_to_translate, target_languages)

            # Log translations to history
            translation_entry = {
                'source': text_to_translate,
                'translations': translated_texts,
                'source_language': source_language
            }
            translation_history.append(translation_entry)
            save_translation_history(translation_history)

            # Provide feedback
            for lang, translated_text in translated_texts.items():
                print(f"Translation to {lang}: {translated_text}")
                speak(f"The translation to {lang} is: {translated_text}")

        except IndexError:
            speak("Sorry, I couldn't process the command format. Please try again.")
        except Exception as e:
            speak(f"Sorry, I couldn't process that translation: {e}")
            print(f"Error: {e}")
    else:
        speak("Please give a translation command that includes 'Translate'.")
        
def show_history():
    if translation_history:
        print("Translation History: ")
        for entry in translation_history:
            print(f"Source: {entry['source']} | Translations: {entry['translations']} | Detected Language: {entry['source_language']}")
    else:
        print("No translation history available")
        
# Main function for the voice assistant
if __name__ == "__main__":
    speak("Hello! I'm your translation assistant. How can I help you?")
    
    while True:
        command = voice_to_text()
        print(f"Command received: {command}")
        
        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye!")
            break
        elif command.lower() == "sorry, i didn't understand that.":
            continue  # If speech recognition fails, re-listen for a command
        elif "history" in command.lower():
            show_history()
        else:
            process_translation_command(command)

