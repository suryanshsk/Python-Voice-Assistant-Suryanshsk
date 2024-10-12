import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
from textblob import TextBlob

# Crisis-related keywords and phrases
crisis_keywords = ["I'm feeling sad", "I'm overwhelmed", "I need help", "I'm anxious", 
                   "I'm depressed", "I'm scared", "I'm in crisis", "I'm lonely", "I can't cope"]

# Helplines dictionary (example for US, UK, India, and global options)
helplines = {
    "US": {
        "general": "You can call the National Suicide Prevention Lifeline at 1-800-273-8255.",
        "text_support": "Text 'HELLO' to 741741 for 24/7 crisis support via text.",
        "emergency": "If it's an emergency, please call 911."
    },
    "UK": {
        "general": "You can call the Samaritans Helpline at 116 123.",
        "text_support": "Text 'SHOUT' to 85258 for crisis support via text.",
        "emergency": "If it's an emergency, please call 999."
    },
    "India": {
        "general": "You can call the Snehi Helpline at +91-22-2772-6771 or iCall at 022-25521111.",
        "text_support": "You can visit icallhelpline.org for online chat support.",
        "emergency": "In case of emergency, call 112 for immediate assistance."
    },
    "Global": {
        "general": "You can visit Befrienders.org for global suicide prevention helplines.",
        "text_support": "For text support, check regional options.",
        "emergency": "If it's an emergency, please contact local emergency services."
    }
}

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slower speaking rate for empathy

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice input with retry mechanism
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Timeout after 10 seconds
            command = recognizer.recognize_google(audio)
            print(f"Captured voice command: {command}")
            return command
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you please repeat?")
            return None  # Return None to retry
        except sr.RequestError:
            speak("The speech recognition service is unavailable at the moment.")
            return None

# Function to detect crisis-related commands using fuzzy matching and sentiment analysis
def detect_crisis(command):
    if command is None:
        return False

    # Check for strong negative sentiment
    sentiment = TextBlob(command).sentiment.polarity
    if sentiment < -0.5:
        return True

    # Check for crisis keywords using fuzzy matching
    for keyword in crisis_keywords:
        if fuzz.partial_ratio(keyword.lower(), command.lower()) > 80:
            return True

    return False

# Function to provide crisis support based on region
def provide_crisis_support(region="US"):
    speak("It sounds like you're going through a tough time. I'm here to help.")
    speak(helplines[region]["general"])
    speak(helplines[region]["text_support"])
    speak(helplines[region]["emergency"])
    print(helplines[region]["general"])
    print(helplines[region]["text_support"])
    print(helplines[region]["emergency"])

# Function to ask for user's region and provide crisis support accordingly
def ask_region_and_provide_support():
    speak("Can you tell me where you're located? For example, the US, UK, India, or another country?")
    command = voice_to_text()
    
    if command:
        if "us" in command.lower():
            provide_crisis_support("US")
        elif "uk" in command.lower():
            provide_crisis_support("UK")
        elif "india" in command.lower():
            provide_crisis_support("India")
        else:
            provide_crisis_support("Global")
    else:
        speak("Sorry, I couldn't determine your region. Providing global helpline information.")
        provide_crisis_support("Global")

# Main function for the voice assistant
if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    
    while True:
        command = voice_to_text()
        
        if command is None:
            continue  # If the command was not understood, retry

        print(f"Command received: {command}")

        # Exit the assistant if the user says "exit" or "stop"
        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye! Stay safe!")
            break

        # Detect crisis-related commands
        elif detect_crisis(command):
            ask_region_and_provide_support()

        # If no crisis detected, provide general support
        else:
            speak("How can I assist you with your other needs today?")
