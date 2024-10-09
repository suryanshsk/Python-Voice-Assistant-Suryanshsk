import pyttsx3
import speech_recognition as sr

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def talk(text):
    engine.say(text)
    engine.runAndWait()