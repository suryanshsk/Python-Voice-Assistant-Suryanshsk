import speech_recognition as sr
import pyttsx3
import json
import datetime
import asyncio
import os
import dateparser
from textblob import TextBlob

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize user journal data
journal_data = {}

# Speak and wait until it's finished (non-blocking version of pyttsx3)
async def speak_async(text):
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0.1)

# Asynchronous voice recognition input with retries
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

# Function to load journal data
def load_journal_data(user_name):
    global journal_data
    if os.path.exists(f"{user_name}_journal.json"):
        with open(f"{user_name}_journal.json", "r") as f:
            journal_data = json.load(f)
    else:
        print("No previous journal data found.")

# Function to save journal data
def save_journal_data(user_name):
    with open(f"{user_name}_journal.json", "w") as f:
        json.dump(journal_data, f)

# Function to get today's journal entry
async def daily_journaling_prompt(user_name):
    await speak_async("How was your day today? Please reflect on anything significant.")
    journal_entry = await voice_to_text_async()

    if journal_entry:
        # Save the entry with timestamp
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if user_name not in journal_data:
            journal_data[user_name] = []
        
        journal_data[user_name].append({"date": current_date, "entry": journal_entry})
        save_journal_data(user_name)

        # Confirm journal entry saved
        await speak_async("Your journal entry has been saved. Would you like to add anything else?")
        extra_entry = await voice_to_text_async()
        if extra_entry and extra_entry.lower() in ["yes", "sure"]:
            await daily_journaling_prompt(user_name)

        # Perform emotion analysis
        await analyze_emotion(journal_entry)
    else:
        await speak_async("It seems there was an issue with your journal entry. Please try again.")

# Emotion Analysis and Suggestions
async def analyze_emotion(entry):
    sentiment = TextBlob(entry).sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    # More detailed emotion analysis
    if polarity > 0:
        if subjectivity > 0.5:
            await speak_async("It seems like you're feeling positive and reflective today. Keep up the good mood!")
        else:
            await speak_async("You're in a positive mood. Stay grounded!")
    elif polarity < 0:
        await speak_async("It seems like you're feeling a bit down. How about doing something relaxing or talking to a friend?")
    else:
        await speak_async("Your entry seems neutral today. Stay balanced and take care of yourself.")

# Background task for daily journaling with time customization
async def journal_prompt_scheduler(user_name, user_time="20:00"):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == user_time:
            await daily_journaling_prompt(user_name)
        await asyncio.sleep(60)

# Main function for the voice assistant
async def main():
    # Get user name for personalization
    await speak_async("Hello! What is your name?")
    user_name = await voice_to_text_async()

    if user_name is None:
        await speak_async("I didn't get your name. I'll call you user for now.")
        user_name = "user"  # Fallback to prevent overwriting journals

    load_journal_data(user_name)

    # Ask for user journaling time preference
    await speak_async("What time would you like to be reminded for your daily journaling? (e.g., 8 PM)")
    preferred_time = await voice_to_text_async()

    # Parsing user input for time using dateparser for flexible input
    try:
        if preferred_time:
            time_object = dateparser.parse(preferred_time)
            if time_object:
                user_time = time_object.strftime('%H:%M')
            else:
                raise ValueError
        else:
            user_time = "20:00"  # Default to 8 PM
    except ValueError:
        await speak_async("I couldn't understand the time. Setting it to 8 PM by default.")
        user_time = "20:00"

    # Start background task for daily journaling prompt
    asyncio.create_task(journal_prompt_scheduler(user_name, user_time))

    # Main interaction loop
    while True:
        command = await voice_to_text_async()

        if command is None:
            continue
        
        if "exit" in command.lower():
            await speak_async("Goodbye!")
            save_journal_data(user_name)
            break

if __name__ == "__main__":
    asyncio.run(main())
