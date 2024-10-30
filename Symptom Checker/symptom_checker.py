import asyncio
import pyttsx3
import speech_recognition as sr
import json
import datetime
import time
import os

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# File to store reminders
REMINDER_FILE = "medication_reminders.json"
medication_reminders = {}

# Load reminders from file
def load_reminders():
    global medication_reminders
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'r') as f:
            medication_reminders = json.load(f)

# Save reminders to file
def save_reminders():
    with open(REMINDER_FILE, 'w') as f:
        json.dump(medication_reminders, f)

# Function to convert text to speech asynchronously
async def speak_async(text):
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0.5)

# Function to get user input through speech recognition
async def voice_to_text_async():
    recognizer = sr.Recognizer()
    await asyncio.sleep(0.5)
    with sr.Microphone() as source:
        print("Listening for your input...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            await speak_async("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            await speak_async("The speech recognition service is unavailable at the moment.")
            return None

# Provide health advice based on symptoms
async def provide_health_advice(symptoms):
    # Simple keyword-based advice (could be enhanced with more data or APIs)
    if "headache" in symptoms:
        await speak_async("For headaches, try to stay hydrated and rest in a dark, quiet room.")
    elif "fever" in symptoms:
        await speak_async("If you have a fever, consider taking fever-reducing medications and consult a doctor if it persists.")
    else:
        await speak_async("It's always best to consult with a healthcare professional for proper advice.")

# Set medication reminder with input validation
async def set_medication_reminder(medication, time_to_take):
    try:
        # Validate time format (HH:MM)
        datetime.datetime.strptime(time_to_take, "%H:%M")
        medication_reminders[medication] = time_to_take
        save_reminders()  # Save reminder to file
        await speak_async(f"Reminder set for {medication} at {time_to_take}.")
    except ValueError:
        await speak_async("Invalid time format. Please provide time in HH:MM format.")

# Parse command for medication and time (more flexible parsing)
def parse_reminder_command(command):
    parts = command.split("set reminder for")
    if len(parts) == 2:
        try:
            details = parts[1].strip().split("at")
            if len(details) == 2:
                medication = details[0].strip()
                time_to_take = details[1].strip()
                return medication, time_to_take
        except IndexError:
            return None, None
    return None, None

# Check and alert for medication reminders
async def check_medication_reminders():
    current_time = datetime.datetime.now().strftime("%H:%M")
    for medication, time_to_take in medication_reminders.items():
        if time_to_take == current_time:
            await speak_async(f"It's time to take your {medication}.")
    await asyncio.sleep(60)  # Check every minute

# Background task to continuously check reminders
async def reminder_task():
    while True:
        await check_medication_reminders()

# Main function for the health assistant
async def main():
    load_reminders()  # Load existing reminders at startup
    await speak_async("Welcome to your health assistant! Describe your symptoms or set a medication reminder.")
    
    # Start background task for checking reminders
    asyncio.create_task(reminder_task())

    while True:
        command = await voice_to_text_async()
        
        if command:
            if "symptoms" in command:
                symptoms = command.replace("symptoms", "").strip()
                await provide_health_advice(symptoms)
            
            elif "set reminder" in command:
                medication, time_to_take = parse_reminder_command(command)
                if medication and time_to_take:
                    await set_medication_reminder(medication, time_to_take)
                else:
                    await speak_async("Sorry, I didn't understand. Please say it in the format: set reminder for [medication] at [time].")
            
            elif "check reminders" in command:
                await check_medication_reminders()
                
            elif "exit" in command:
                await speak_async("Goodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
