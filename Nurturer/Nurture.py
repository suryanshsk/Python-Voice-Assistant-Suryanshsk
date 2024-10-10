import time
import random
import speech_recognition as sr
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
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
    reminder = random.choice(reminders)
    speak(reminder)

def main():
    speak("Welcome to the Mindfulness Assistant! I'm here to help you find a moment of peace and relaxation.")
    
    while True:
        speak("What would you like to do today?")
        speak("Say Guided Breathing, Body Scan, Gratitude Exercise, Mindfulness Reminder, or Exit.")
        
        command = listen()
        
        if command:
            if "guided breathing" in command:
                breathing_exercise()
            elif "body scan" in command:
                body_scan_exercise()
            elif "gratitude exercise" in command:
                gratitude_exercise()
            elif "mindfulness reminder" in command:
                mindfulness_reminder()
            elif "exit" in command:
                speak("Thank you for spending this time with me. Take care and be kind to yourself!")
                break
            else:
                speak("Hmm, I didn't quite understand that. Please try again.")

if __name__ == "__main__":
    main()
