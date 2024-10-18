import speech_recognition as sr
import pyttsx3
import json
import random
import datetime
import dateparser
import threading
import time
import asyncio

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
user_data = {}
memory_data = {}

# Define personality modes
personalities = {
    "professional": {"humor": False, "formality": "high"},
    "casual": {"humor": True, "formality": "low"},
    "humorous": {"humor": True, "formality": "medium"},
    "formal": {"humor": False, "formality": "very_high"}
}

current_personality = "professional"

# Mood response based on time of day
def adjust_mood_based_on_time():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    elif 18 <= current_hour < 22:
        return "evening"
    else:
        return "night"

# Asynchronous speak function with personality
async def speak_async(text, personality="professional"):
    style = personalities.get(personality, personalities["professional"])
    
    if style["humor"] and random.random() > 0.5:  # Add humor randomly
        text = f"{text} 😄 Just kidding!"

    if style["formality"] == "high":
        text = f"Dear user, {text}"
    
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0.1)

# Asynchronous voice recognition input
async def voice_to_text_async():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            await speak_async("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            await speak_async("The speech recognition service is unavailable at the moment.")
            return None

# Load and save user/memory data
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

def save_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)
    with open("memory_data.json", "w") as f:
        json.dump(memory_data, f)

# User Profile creation
def create_user_profile(user_name):
    if user_name not in user_data:
        user_data[user_name] = {"quiz_scores": [], "preferred_language": "Spanish"}

# Get user name and personality
async def get_user_name_and_personality():
    await speak_async("What is your name?")
    user_name = await voice_to_text_async()

    if not user_name:
        user_name = "default_user"
    user_name = user_name.lower()
    
    # Ask for preferred personality
    await speak_async(f"Hello {user_name}, would you like me to be formal, casual, humorous, or professional?")
    personality_choice = await voice_to_text_async()
    personality_choice = personality_choice.lower() if personality_choice else "professional"
    
    if personality_choice in personalities:
        global current_personality
        current_personality = personality_choice
    
    return user_name

# Reminder functions
async def add_reminder(user, note, time=None):
    if user not in memory_data:
        memory_data[user] = []
    
    reminder = {"note": note, "reminder_time": time.isoformat() if time else None}
    memory_data[user].append(reminder)
    save_data()
    
    if time:
        await speak_async(f"Reminder set for {note} at {time.strftime('%Y-%m-%d %H:%M:%S')}.", current_personality)
    else:
        await speak_async(f"Note saved: {note}", current_personality)

async def list_active_reminders(user):
    if user in memory_data:
        active_reminders = [note for note in memory_data[user] if note.get("reminder_time")]
        if active_reminders:
            await speak_async("Here are your active reminders:", current_personality)
            for reminder in active_reminders:
                reminder_time = reminder.get("reminder_time")
                await speak_async(f"Reminder: {reminder['note']} at {reminder_time}", current_personality)
        else:
            await speak_async("You have no active reminders.", current_personality)
    else:
        await speak_async("You have no saved reminders.", current_personality)

# Contextual Memory Search
async def search_memory(user, keyword):
    if user in memory_data:
        results = [note for note in memory_data[user] if keyword.lower() in note["note"].lower()]
        if results:
            await speak_async(f"I found {len(results)} note(s) related to {keyword}:", current_personality)
            for result in results:
                await speak_async(result["note"], current_personality)
        else:
            await speak_async(f"No notes found containing {keyword}.", current_personality)
    else:
        await speak_async("No memory data available.", current_personality)

# Math Tutor
async def math_tutor():
    await speak_async("What math problem would you like help with?", current_personality)
    user_input = await voice_to_text_async()

    if user_input:
        if "2 plus 2" in user_input.lower():
            await speak_async("The answer to 2 plus 2 is 4.", current_personality)
        elif "quadratic formula" in user_input.lower():
            await speak_async("The quadratic formula is negative b plus or minus the square root of b squared minus 4ac, all divided by 2a.", current_personality)
        else:
            await speak_async("I'm not sure of the answer. Would you like me to search online or provide a step-by-step explanation?", current_personality)
    else:
        await speak_async("I didn't understand your request. Could you please repeat?", current_personality)

# Main loop for the assistant
async def main():
    load_data()
    user_name = await get_user_name_and_personality()
    create_user_profile(user_name)

    await speak_async(f"Hello {user_name.capitalize()}, how can I assist you today?", current_personality)

    while True:
        command = await voice_to_text_async()

        if command is None:
            continue

        if "exit" in command.lower() or "stop" in command.lower():
            await speak_async("Goodbye! Stay curious and keep learning!", current_personality)
            save_data()
            break
        
        elif "math" in command.lower() and "help" in command.lower():
            await math_tutor()
        
        elif "remind" in command.lower():
            await speak_async("What should I remind you about?", current_personality)
            reminder_note = await voice_to_text_async()
            
            await speak_async("When should I remind you?", current_personality)
            reminder_time_input = await voice_to_text_async()
            reminder_time = dateparser.parse(reminder_time_input)
            
            if reminder_note and reminder_time:
                await add_reminder(user_name, reminder_note, reminder_time)
            else:
                await speak_async("I couldn't set the reminder. Please try again.", current_personality)

        elif "search" in command.lower() and "memory" in command.lower():
            await speak_async("What would you like me to search for?", current_personality)
            keyword = await voice_to_text_async()
            await search_memory(user_name, keyword)
        
        elif "list" in command.lower() and "reminder" in command.lower():
            await list_active_reminders(user_name)
        
        else:
            await speak_async("I'm sorry, I didn't understand that command.", current_personality)

if __name__ == "__main__":
    asyncio.run(main())
