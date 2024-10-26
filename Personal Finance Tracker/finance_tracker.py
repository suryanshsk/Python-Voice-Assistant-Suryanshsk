import asyncio
import pyttsx3
import speech_recognition as sr
import json
import os

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# File to store expenses and budgets
DATA_FILE = "finance_data.json"

# Global variables to store expenses and budgets
expenses = {}
budgets = {}

# Load data from file
def load_data():
    global expenses, budgets
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                expenses = data.get("expenses", {})
                budgets = data.get("budgets", {})
        except json.JSONDecodeError:
            expenses = {}
            budgets = {}
            print("Warning: Data file is corrupted. Starting fresh.")

# Save data to file
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({"expenses": expenses, "budgets": budgets}, f)

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
        print("Listening for your command...")
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

# Function to log expenses
async def log_expense(category, amount):
    if category not in expenses:
        expenses[category] = []
    expenses[category].append(amount)
    save_data()  # Save data after logging
    await speak_async(f"Logged {amount} dollars for {category}.")

# Function to set budget
async def set_budget(category, amount):
    budgets[category] = amount
    save_data()  # Save data after setting budget
    await speak_async(f"Set {category} budget to {amount} dollars.")

# Function to check budgets
async def check_budget():
    for category, budget in budgets.items():
        total_expense = sum(expenses.get(category, []))
        remaining = budget - total_expense
        if remaining < 0:
            await speak_async(f"You have exceeded your budget for {category} by {-remaining} dollars.")
        else:
            await speak_async(f"You have {remaining} dollars left in your budget for {category}.")

# Function to provide help
async def provide_help():
    await speak_async("You can log expenses by saying 'Log expense [category] [amount]', set budgets by saying 'Set budget [category] [amount]', and check budgets by saying 'Check budget'. To exit, say 'exit'.")

# Main function for the assistant
async def main():
    load_data()  # Load existing data at startup
    await speak_async("Welcome to your personal finance assistant! How can I assist you today?")
    
    while True:
        command = await voice_to_text_async()
        
        if command:
            if "log expense" in command:
                parts = command.split()
                if len(parts) == 4 and parts[1] == "expense":
                    category = parts[2]
                    try:
                        amount = float(parts[3])
                        await log_expense(category, amount)
                    except ValueError:
                        await speak_async("Please provide a valid amount.")

            elif "set budget" in command:
                parts = command.split()
                if len(parts) == 4 and parts[1] == "budget":
                    category = parts[2]
                    try:
                        amount = float(parts[3])
                        await set_budget(category, amount)
                    except ValueError:
                        await speak_async("Please provide a valid budget amount.")

            elif "check budget" in command:
                await check_budget()
                
            elif "help" in command:
                await provide_help()

            elif "exit" in command:
                await speak_async("Goodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
