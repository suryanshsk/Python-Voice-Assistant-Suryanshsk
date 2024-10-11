
#install speech_recognition , translate and pyttsx3 libraries
#make sure there are no microphone or hardware issues

import speech_recognition as sr
import pyttsx3
from translate import Translator

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to translate using translate-python
def translate_text(text, target_language):
    try:
        translator = Translator(to_lang=target_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Sorry, the translation service encountered an error: {e}"

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

            # Parse the command to extract the text and target language
            if "'" not in command or "to " not in command:
                speak("Please provide a valid command, for example: Translate 'Hello' to French.")
                return

            text_to_translate = command.split("'")[1]
            target_language = command.split("to ")[1].strip().lower()

            # Provide feedback on extracted text and language
            print(f"Text to translate: {text_to_translate}")
            print(f"Target language: {target_language}")

            # Perform the translation
            translated_text = translate_text(text_to_translate, target_language)
            print(f"Translated Text: {translated_text}")
            speak(f"The translation is: {translated_text}")

        except IndexError:
            speak("Sorry, I couldn't process the command format. Please try again.")
        except Exception as e:
            speak(f"Sorry, I couldn't process that translation: {e}")
            print(f"Error: {e}")
    else:
        speak("Please give a translation command that includes 'Translate'.")
        
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
        else:
            process_translation_command(command)

