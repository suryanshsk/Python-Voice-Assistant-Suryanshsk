import speech_recognition as sr
import pyttsx3
import json
import random
import datetime
import dateparser
import threading
import time

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize empty user data and memory data
user_data = {}
memory_data = {}

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

# Function to load user and memory data
def load_data():
    global user_data, memory_data
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        print("No previous user data found.")

    try:
        with open("memory_data.json", "r") as f:
            memory_data = json.load(f)
    except FileNotFoundError:
        print("No previous memory data found.")

# Function to save user and memory data
def save_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)
    with open("memory_data.json", "w") as f:
        json.dump(memory_data, f)

# Create a user profile if it doesn't exist
def create_user_profile(user_name):
    if user_name not in user_data:
        user_data[user_name] = {"quiz_scores": [], "preferred_language": "Spanish"}

# Get the user's name
def get_user_name():
    speak("What is your name?")
    user_name = voice_to_text()
    return user_name.lower() if user_name else "default_user"

# Function to handle reminders based on time and conversations
def add_reminder(user, note, time=None):
    if user not in memory_data:
        memory_data[user] = []

    reminder = {"note": note, "reminder_time": time.isoformat() if time else None}
    memory_data[user].append(reminder)
    save_data()

    if time:
        speak(f"Reminder set for {note} at {time.strftime('%Y-%m-%d %H:%M:%S')}.")
    else:
        speak(f"Note saved: {note}")

def list_active_reminders(user):
    if user in memory_data:
        active_reminders = [note for note in memory_data[user] if note.get("reminder_time")]
        if active_reminders:
            speak("Here are your active reminders:")
            for reminder in active_reminders:
                reminder_time = reminder.get("reminder_time")
                speak(f"Reminder: {reminder['note']} at {reminder_time}")
        else:
            speak("You have no active reminders.")
    else:
        speak("You have no saved reminders.")

def search_memory(user, keyword):
    if user in memory_data:
        results = [note for note in memory_data[user] if keyword.lower() in note["note"].lower()]
        if results:
            speak(f"I found {len(results)} note(s) related to {keyword}:")
            for result in results:
                speak(result["note"])
        else:
            speak(f"No notes found containing {keyword}.")
    else:
        speak("No memory data available.")

# Recurring reminder function
def set_recurring_reminder(user, note, interval="daily"):
    next_reminder_time = None
    if interval == "daily":
        next_reminder_time = datetime.datetime.now() + datetime.timedelta(days=1)
    elif interval == "weekly":
        next_reminder_time = datetime.datetime.now() + datetime.timedelta(weeks=1)

    memory_data[user].append({"note": note, "reminder_time": next_reminder_time.isoformat(), "interval": interval})
    save_data()
    speak(f"I have set a {interval} reminder for {note}.")

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

# Quiz function
def quiz(subject="math"):
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

    speak(f"Your final score is {score} out of {len(questions)}.")

# Background task to handle reminders asynchronously
def reminder_checker():
    while True:
        current_time = datetime.datetime.now().isoformat()
        for user, reminders in memory_data.items():
            for reminder in reminders:
                if reminder.get("reminder_time") and reminder["reminder_time"] <= current_time:
                    speak(f"Reminder: {reminder['note']}")
                    reminders.remove(reminder)
                    save_data()
        time.sleep(60)

# Main function for the voice assistant
if __name__ == "__main__":
    load_data()
    user_name = get_user_name()
    create_user_profile(user_name)

    # Start background thread for reminders
    threading.Thread(target=reminder_checker, daemon=True).start()

    speak(f"Hello {user_name.capitalize()}, how can I assist you today?")

    while True:
        command = voice_to_text()

        if command is None:
            continue  # Retry if the command was not understood

        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye! Stay curious and keep learning!")
            save_data()
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
                user_data[user_name]["preferred_language"] = preferred_language
            language_practice(preferred_language)

        # Trigger quiz
        elif "quiz" in command.lower():
            speak("Which subject would you like a quiz on? Math or Science?")
            subject_choice = voice_to_text()
            if "math" in subject_choice.lower():
                quiz("math")
            elif "science" in subject_choice.lower():
                quiz("science")
            else:
                speak("I only have quizzes for math and science at the moment.")

        # Add a reminder
        elif "remind" in command.lower():
            speak("What should I remind you about?")
            reminder_note = voice_to_text()

            speak("When should I remind you?")
            reminder_time_input = voice_to_text()
            reminder_time = dateparser.parse(reminder_time_input)

            if reminder_note and reminder_time:
                add_reminder(user_name, reminder_note, reminder_time)
            else:
                speak("I couldn't set the reminder. Please try again.")

        # Search memory
        elif "search" in command.lower() and "memory" in command.lower():
            speak("What would you like me to search for?")
            keyword = voice_to_text()
            search_memory(user_name, keyword)

        # List active reminders
        elif "list" in command.lower() and "reminder" in command.lower():
            list_active_reminders(user_name)

        else:
            speak("I'm sorry, I didn't understand that command.")
