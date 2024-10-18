import speech_recognition as sr
import pyttsx3
from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def load_or_create_key(username):
    key_file = f"{username}_secret.key"
    if not os.path.exists(key_file):
        key = generate_key()
        with open(key_file, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_file, 'rb') as key_file:
            key = key_file.read()
    return key

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

def authenticate():
    speak("Please say your username.")
    username = recognize_voice()
    speak("Please say your password.")
    password = recognize_voice()
    return username == "user" and password == "your_secure_password"

def ask_security_questions(questions):
    correct_answers = 0
    for question, answer in questions.items():
        speak(question)
        response = recognize_voice()
        if response == answer:
            correct_answers += 1
            speak("Correct answer.")
        else:
            speak("Incorrect answer.")
    return correct_answers == len(questions)

def main():
    if not authenticate():
        speak("Access denied. Incorrect credentials.")
        return

    speak("Access granted.")
    username = "user"
    key = load_or_create_key(username)
    data_store = {}
    locked = False

    while True:
        if locked:
            speak("Access to the stored information is locked. Please answer the security questions to regain access.")
            if ask_security_questions(locked_questions):
                locked = False
                speak("Access regained.")
            else:
                speak("Access denied. Please try again later.")
                break

        command = recognize_voice()

        if 'store' in command:
            speak("What information would you like to store?")
            info = recognize_voice()
            if info != "Sorry, I did not understand that.":
                questions = {}
                for i in range(3):
                    speak(f"Please provide security question {i + 1}.")
                    question = recognize_voice()
                    speak(f"Please provide the answer for: {question}")
                    answer = recognize_voice()
                    questions[question] = answer
                
                encrypted_info = encrypt_data(info, key)
                data_store[info] = {'encrypted': encrypted_info, 'questions': questions}
                speak("Information stored securely with security questions.")
        
        elif 'retrieve' in command:
            speak("What information would you like to retrieve?")
            info = recognize_voice()
            if info in data_store:
                questions = data_store[info]['questions']
                speak("Please answer the security questions to access the information.")
                if ask_security_questions(questions):
                    decrypted_info = decrypt_data(data_store[info]['encrypted'], key)
                    speak(f"The information you requested is: {decrypted_info}")
                else:
                    speak("Incorrect answers. Access denied.")
                    locked = True
            else:
                speak("No information found for that request.")
                locked = True

        elif 'exit' in command:
            speak("Exiting the voice assistant.")
            break

        else:
            speak("Command not recognized. Please try again.")
            locked = True

if __name__ == "__main__":
    main()