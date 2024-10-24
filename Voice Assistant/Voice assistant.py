import pyttsx3
#LIstening from user and typing
import speech_recognition as sr


def text_to_speech1(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 105) 
    engine.setProperty('volume', 1.0) 
    engine.setProperty('voice', voices[1].id)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

text = "I am listening to you, please speak something"
text_to_speech1(text)

# Initialize recognizer
recognizer = sr.Recognizer()


def listen_and_convert():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            # Convert speech to text
            print("Converting speech to text...")
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Error connecting to the speech recognition service.")
    
# Run the speech-to-text function
Prompt = listen_and_convert()

# ----
# Add your responce generation Function.
# ----

response = "REPLACE THIS FROM THE ACTUAL RESPONSE GENERATED"


#RESPONSE TOO SPEECH
def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init() 
    # Set properties (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[1].id)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

print (response)
text_to_speech(response)

def repeat_speech_if_needed(text):
    while True:
        # Ask the user if they understood
        text_to_speech1("Did you understand the message , Please response with either yes or no ")
        
        user_input = listen_and_convert()
        
        
        # Check user response
        if 'yes' in user_input.lower() :
            print("Great! Moving on.")
            text_to_speech1("Great! Moving on.")
            break  
        elif 'no' in user_input.lower() :
            print("Repeating the message...")
            # Convert text to speech
            text_to_speech(text)
        else:
            print("Please respond with yes or no.")

# Run the repeat_speech_if_needed function
repeat_speech_if_needed(response)

