import speech_recognition as sr
import pyttsx3
import json
import random

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize empty user data
user_data = {}

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice input
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
            return None
        except sr.RequestError:
            speak("The speech recognition service is unavailable at the moment.")
            return None

# Function to load user profiles
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        print("No previous user data found.")
    except json.JSONDecodeError:
        print("Error reading user data. Starting with an empty user profile.")

# Function to save user profiles
def save_user_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)

# Create a user profile if it doesn't exist
def create_user_profile(user_name):
    if user_name not in user_data:
        user_data[user_name] = {"quiz_scores": [], "preferred_language": "Spanish"}

# Get the user's name
def get_user_name():
    speak("What is your name?")
    user_name = voice_to_text()
    if user_name:
        return user_name.lower()
    return "default_user"

# Math tutoring function
def math_tutor():
    speak("What math problem would you like help with?")
    user_input = voice_to_text()
    
    if user_input:
        if "2 plus 2" in user_input.lower():
            speak("The answer to 2 plus 2 is 4.")
        elif "quadratic formula" in user_input.lower():
            speak("The quadratic formula is negative b plus or minus the square root of b squared minus 4ac, all divided by 2a.")
        else:
            speak("I'm not sure of the answer. Would you like me to search online or provide a step-by-step explanation?")
    else:
        speak("I didn't understand your request. Could you please repeat?")

# Language practice function
def language_practice(language="Spanish"):
    supported_languages = ["spanish", "french"]
    if language.lower() not in supported_languages:
        speak(f"Sorry, I only support {', '.join(supported_languages)} at the moment.")
        return

    speak(f"Let's practice {language}. Please say a sentence in {language}, and I'll correct it if needed.")
    user_sentence = voice_to_text()

    if user_sentence:
        if language.lower() == "spanish" and "estoy aprendiendo español" in user_sentence.lower():
            speak("Great! Your sentence is correct.")
        elif language.lower() == "french" and "je parle français" in user_sentence.lower():
            speak("Great! Your sentence is correct.")
        else:
            speak(f"Sorry, I didn't understand that {language} sentence.")
    else:
        speak("Could you try that sentence again?")

# Interactive quiz function with randomization
def quiz(user_name, subject="math"):
    question_bank = {
        "math": [
            {"question": "What is 5 times 6?", "answer": "30"},
            {"question": "What is the square root of 64?", "answer": "8"},
            {"question": "What is 9 minus 3?", "answer": "6"}
        ],
        "science": [
            {"question": "What is the chemical symbol for water?", "answer": "H2O"},
            {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
            {"question": "What is the atomic number of hydrogen?", "answer": "1"}
        ]
    }

    # Ensure there are enough questions to sample from
    if len(question_bank[subject]) < 2:
        speak("Not enough questions available for this subject.")
        return

    questions = random.sample(question_bank[subject], 2)  # Select 2 random questions

    score = 0
    for q in questions:
        speak(q["question"])
        user_answer = voice_to_text()

        if not user_answer:
            speak("I didn't hear an answer. Could you try again?")
            continue

        if q["answer"].lower() in user_answer.lower():
            speak("That's correct!")
            score += 1
        else:
            speak(f"Sorry, the correct answer is {q['answer']}.")

    user_data[user_name]["quiz_scores"].append({"subject": subject, "score": score})
    speak(f"Your final score is {score} out of {len(questions)}.")

# Function to handle follow-up questions
def handle_follow_up():
    speak("Do you need help with anything else?")
    response = voice_to_text()
    if response and ("yes" in response.lower() or "sure" in response.lower()):
        return True
    else:
        speak("Okay, have a great day!")
        return False

# Main function for the voice assistant
if __name__ == "__main__":
    load_user_data()
    user_name = get_user_name()
    create_user_profile(user_name)

    speak(f"Hello {user_name.capitalize()}, how can I assist you today?")
    
    while True:
        command = voice_to_text()

        if command is None:
            continue  # Retry if the command was not understood

        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye! Stay curious and keep learning!")
            save_user_data()
            break

        # Trigger math tutoring
        elif "math" in command.lower() and "help" in command.lower():
            math_tutor()

        # Trigger language practice
        elif "practice" in command.lower() and "language" in command.lower():
            preferred_language = user_data[user_name]["preferred_language"]
            speak(f"Would you like to practice {preferred_language}, or a different language?")
            language_choice = voice_to_text()
            if "different" in language_choice.lower():
                speak("Which language would you like to practice?")
                preferred_language = voice_to_text()
                if preferred_language:
                    user_data[user_name]["preferred_language"] = preferred_language
            language_practice(preferred_language)

        # Trigger quiz
        elif "quiz" in command.lower():
            speak("Which subject would you like a quiz on? Math or Science?")
            subject_choice = voice_to_text()
            if "math" in subject_choice.lower():
                quiz(user_name, "math")
            elif "science" in subject_choice.lower():
                quiz(user_name, "science")
            else:
                speak("I only have quizzes for math and science at the moment.")

        else:
            speak("I didn't catch that. Please say a valid command, like 'math help' or 'start a quiz'.")

        if not handle_follow_up():
            save_user_data()
            break
