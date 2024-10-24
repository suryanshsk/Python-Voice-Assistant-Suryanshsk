import speech_recognition as sr
import pyttsx3
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Captures voice input and returns the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Network error. Please try again.")
    return None

# Create a scheduler to manage tasks
scheduler = BackgroundScheduler()

def schedule_task(task, reminder_time):
    """Schedules a reminder to be spoken at a specific time."""
    def reminder():
        speak(f"Reminder: {task}")
    scheduler.add_job(reminder, 'date', run_date=reminder_time)
    scheduler.start()

def parse_command(command):
    """Extracts task and time from the command and schedules the task."""
    # Example command: "Remind me to attend a meeting at 2 PM"
    try:
        task = command.split(" to ")[1].split(" at ")[0]
        time_part = command.split(" at ")[1]
        reminder_time = datetime.strptime(time_part, '%I %p').replace(day=datetime.now().day)

        # Schedule the task
        schedule_task(task, reminder_time)
        speak(f"Task '{task}' scheduled at {reminder_time.strftime('%I %p')}.")

    except Exception as e:
        speak(f"Error scheduling task: {str(e)}")

def main():
    """Main loop to interact with the user."""
    speak("Hello, I am your voice assistant. How can I help you?")
    
    while True:
        command = recognize_speech()
        if command:
            if "remind me" in command.lower():
                parse_command(command)
            elif "exit" in command.lower():
                speak("Goodbye!")
                break

if __name__ == "__main__":
    main()
