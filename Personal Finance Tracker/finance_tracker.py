import asyncio
import pyttsx3
import speech_recognition as sr
import json
import os

# Class to encapsulate finance data and operations
class FinanceAssistant:
    DATA_FILE = "finance_data.json"
    
    def __init__(self):
        self.expenses = {}
        self.budgets = {}
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.load_data()

    def load_data(self):
        """Loads data from the JSON file if it exists."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get("expenses", {})
                    self.budgets = data.get("budgets", {})
            except (json.JSONDecodeError, IOError):
                print("Warning: Data file is corrupted or unreadable. Starting with fresh data.")
    
    def save_data(self):
        """Saves the current state of expenses and budgets to the JSON file."""
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump({"expenses": self.expenses, "budgets": self.budgets}, f)
        except IOError:
            print("Warning: Could not save data to file.")

    def speak(self, text):
        """Synchronously convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()

    async def speak_async(self, text):
        """Async wrapper for speak to maintain code consistency."""
        await asyncio.to_thread(self.speak, text)

    async def recognize_speech(self):
        """Converts voice input to text asynchronously."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for your command...")
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio)
                return command.lower()
            except sr.UnknownValueError:
                await self.speak_async("I didn't catch that. Could you please repeat?")
            except sr.RequestError:
                await self.speak_async("The speech recognition service is unavailable.")
            except Exception as e:
                print(f"Error in speech recognition: {e}")
            return None

    async def log_expense(self, category, amount):
        """Logs an expense under a specific category."""
        self.expenses.setdefault(category, []).append(amount)
        self.save_data()
        await self.speak_async(f"Logged {amount} dollars for {category}.")

    async def set_budget(self, category, amount):
        """Sets a budget for a specific category."""
        self.budgets[category] = amount
        self.save_data()
        await self.speak_async(f"Set {category} budget to {amount} dollars.")

    async def check_budget(self):
        """Checks remaining budgets against expenses."""
        for category, budget in self.budgets.items():
            total_expense = sum(self.expenses.get(category, []))
            remaining = budget - total_expense
            if remaining < 0:
                await self.speak_async(f"You have exceeded your budget for {category} by {-remaining} dollars.")
            else:
                await self.speak_async(f"You have {remaining} dollars left in your budget for {category}.")

    async def provide_help(self):
        """Provides help instructions to the user."""
        await self.speak_async("You can log expenses by saying 'Log expense [category] [amount]', set budgets by saying 'Set budget [category] [amount]', check budgets by saying 'Check budget'. To exit, say 'exit'.")

    async def parse_command(self, command):
        """Parses the user's command and calls appropriate methods."""
        if "log expense" in command:
            try:
                _, _, category, amount_str = command.split(maxsplit=3)
                amount = float(amount_str)
                await self.log_expense(category, amount)
            except (ValueError, IndexError):
                await self.speak_async("Please specify a valid category and amount.")

        elif "set budget" in command:
            try:
                _, _, category, amount_str = command.split(maxsplit=3)
                amount = float(amount_str)
                await self.set_budget(category, amount)
            except (ValueError, IndexError):
                await self.speak_async("Please specify a valid category and budget amount.")

        elif "check budget" in command:
            await self.check_budget()

        elif "help" in command:
            await self.provide_help()

        elif "exit" in command:
            await self.speak_async("Goodbye!")
            return False  # Signal to exit the main loop

        return True  # Continue running

    async def run(self):
        """Main loop for voice command processing."""
        await self.speak_async("Welcome to your personal finance assistant! How can I assist you today?")
        
        while True:
            command = await self.recognize_speech()
            if command:
                keep_running = await self.parse_command(command)
                if not keep_running:
                    break

if __name__ == "__main__":
    assistant = FinanceAssistant()
    asyncio.run(assistant.run())
