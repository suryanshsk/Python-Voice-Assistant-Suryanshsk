import time
import random
import speech_recognition as sr
import pyttsx3
import logging

# Initialize the speech engine and logging
engine = pyttsx3.init()
logging.basicConfig(level=logging.INFO)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            logging.info(f"Recognized command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            logging.warning("Speech recognition failed: UnknownValueError")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            logging.error("Speech recognition failed: RequestError")
            return None

def breathing_exercise():
    speak("Let's take a moment to focus on our breath.")
    speak("Inhale deeply through your nose for 4 seconds.")
    time.sleep(4)
    speak("Hold your breath for 4 seconds.")
    time.sleep(4)
    speak("Exhale slowly through your mouth for 6 seconds.")
    time.sleep(6)
    speak("Great! Let's repeat that cycle three more times.")
    for _ in range(3):
        speak("Inhale...")
        time.sleep(4)
        speak("Hold...")
        time.sleep(4)
        speak("Exhale...")
        time.sleep(6)
    speak("You've completed the breathing exercise!")

def body_scan_exercise():
    speak("Let's do a quick body scan.")
    speak("Close your eyes and take a deep breath.")
    speak("Starting from your toes, notice any sensations...")
    time.sleep(5)
    speak("Now, move up to your feet, then your legs...")
    time.sleep(5)
    speak("Continue to your hips, stomach, chest, and shoulders...")
    time.sleep(5)
    speak("Finally, focus on your neck and head...")
    time.sleep(5)
    speak("Take another deep breath and release any tension.")
    speak("Well done!")

def gratitude_exercise():
    speak("It's time for a gratitude exercise.")
    speak("Think of three things you are grateful for.")
    time.sleep(10)
    speak("Feel that gratitude filling you up.")
    speak("Thank you for practicing gratitude!")

def mindfulness_reminder():
    reminders = [
        "Take a moment to notice your surroundings. What do you see, hear, and feel?",
        "Remember to breathe deeply and relax your shoulders.",
        "Think of three things you're thankful for right now.",
        "Take a short break and stretch your body.",
        "Spend a few minutes observing your thoughts without judgment.",
        "Imagine a peaceful place. What does it look like, and how do you feel there?"
    ]
    
    # Track used reminders in session
    if not hasattr(mindfulness_reminder, "used_reminders"):
        mindfulness_reminder.used_reminders = set()
    
    remaining_reminders = [r for r in reminders if r not in mindfulness_reminder.used_reminders]
    
    if remaining_reminders:
        reminder = random.choice(remaining_reminders)
        mindfulness_reminder.used_reminders.add(reminder)
    else:
        speak("You have gone through all the reminders. Resetting reminders for a fresh start.")
        mindfulness_reminder.used_reminders.clear()
        reminder = random.choice(reminders)
        mindfulness_reminder.used_reminders.add(reminder)
    
    speak(reminder)

def main():
    speak("Welcome to the Mindfulness Assistant! I'm here to help you find a moment of peace and relaxation.")
    
    while True:
        speak("What would you like to do today? Say Guided Breathing, Body Scan, Gratitude Exercise, Mindfulness Reminder, or Exit.")
        
        command = listen()
        
        if command:
            if "guided breathing" in command:
                speak("You chose Guided Breathing.")
                breathing_exercise()
            elif "body scan" in command:
                speak("You chose Body Scan.")
                body_scan_exercise()
            elif "gratitude exercise" in command:
                speak("You chose Gratitude Exercise.")
                gratitude_exercise()
            elif "mindfulness reminder" in command:
                speak("You chose Mindfulness Reminder.")
                mindfulness_reminder()
            elif "exit" in command:
                speak("Thank you for spending this time with me. Take care and be kind to yourself!")
                time.sleep(2)  # Delay for graceful exit
                break
            else:
                speak("Hmm, I didn't quite understand that. Please try again.")
    
    engine.stop()  # Gracefully stop the engine before exiting
    logging.info("Program exited successfully.")

if __name__ == "__main__":
    main()
