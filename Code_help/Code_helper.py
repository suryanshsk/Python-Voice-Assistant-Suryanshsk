import speech_recognition as sr
import pyttsx3
import openai

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
openai.api_key = 'YOUR_API_KEY'

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Generate code for: {prompt}"}]
    )
    return response['choices'][0]['message']['content']

def main():
    speak("Welcome to the voice-activated coding system. What code do you need? You can say 'exit' to end the program.")
    
    while True:
        prompt = listen()
        if prompt:
            if prompt.lower() == 'exit':
                speak("Exiting the program. Goodbye!")
                break
            
            code = generate_code(prompt)
            print("Generated Code:")
            print(code)
            speak("Here is the code I generated for you. You can ask for more code or say 'exit' to leave.")

if __name__ == "__main__":
    main()