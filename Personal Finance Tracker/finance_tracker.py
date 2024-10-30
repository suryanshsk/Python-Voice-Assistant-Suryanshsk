import asyncio
import pyttsx3
import speech_recognition as sr
import json
import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Class to encapsulate finance data and operations
class FinanceAssistant:
    DATA_FILE = "finance_data.json"
    
    def __init__(self):
        self.expenses = {}
        self.budgets = {}
        self.recurring_expenses = {}
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
                    self.recurring_expenses = data.get("recurring_expenses", {})
            except (json.JSONDecodeError, IOError):
                print("Warning: Data file is corrupted or unreadable. Starting with fresh data.")
    
    def save_data(self):
        """Saves the current state of expenses, budgets, and recurring expenses to the JSON file."""
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump({"expenses": self.expenses, "budgets": self.budgets, "recurring_expenses": self.recurring_expenses}, f)
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

    async def log_expense(self, category, amount, date=None):
        """Logs an expense under a specific category."""
        date = date or datetime.now().strftime("%Y-%m-%d")
        self.expenses.setdefault(category, []).append({"amount": amount, "date": date})
        self.save_data()
        await self.speak_async(f"Logged {amount} dollars for {category}.")

    async def set_budget(self, category, amount):
        """Sets a budget for a specific category."""
        self.budgets[category] = amount
        self.save_data()
        await self.speak_async(f"Set {category} budget to {amount} dollars.")

    async def check_budget(self):
        """Checks remaining budgets against expenses and provides alerts if limits are exceeded."""
        for category, budget in self.budgets.items():
            total_expense = sum(expense["amount"] for expense in self.expenses.get(category, []))
            remaining = budget - total_expense
            if remaining < 0:
                await self.speak_async(f"You have exceeded your budget for {category} by {-remaining} dollars.")
            elif remaining < budget * 0.1:
                await self.speak_async(f"Warning: You are approaching your budget limit for {category}.")
            else:
                await self.speak_async(f"You have {remaining} dollars left in your budget for {category}.")

    async def manage_recurring_expenses(self, category, amount):
        """Logs and manages recurring expenses for subscriptions."""
        self.recurring_expenses[category] = amount
        self.save_data()
        await self.speak_async(f"Recurring expense of {amount} dollars added for {category}.")

    def generate_expense_summary(self):
        """Generates a report summarizing expenses by category."""
        summary = {category: sum(expense["amount"] for expense in expenses) for category, expenses in self.expenses.items()}
        for category, total in summary.items():
            print(f"{category}: ${total:.2f}")
        return summary

    async def generate_monthly_report(self):
        """Generates a monthly report comparing expenses and budgets."""
        monthly_summary = self.generate_expense_summary()
        for category, total_expense in monthly_summary.items():
            budget = self.budgets.get(category, 0)
            await self.speak_async(f"For {category}, you spent {total_expense} out of {budget} dollars.")

    def export_data_to_csv(self):
        """Exports the expense summary to a CSV file."""
        with open("expense_summary.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Date", "Amount"])
            for category, expenses in self.expenses.items():
                for expense in expenses:
                    writer.writerow([category, expense["date"], expense["amount"]])

    def generate_charts(self):
        """Generates charts to visualize spending by category."""
        summary = self.generate_expense_summary()
        categories = list(summary.keys())
        expenses = list(summary.values())

        plt.figure(figsize=(8, 6))
        plt.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Spending by Category")
        plt.show()

    def currency_conversion(self, amount, from_currency, to_currency, rate):
        """Converts amount from one currency to another given an exchange rate."""
        converted_amount = amount * rate
        print(f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}.")
        return converted_amount

    async def detailed_expense_history(self):
        """Provides detailed history of expenses for each category."""
        for category, expenses in self.expenses.items():
            await self.speak_async(f"Expenses for {category}:")
            for expense in expenses:
                await self.speak_async(f"On {expense['date']}, spent {expense['amount']} dollars.")

    async def provide_help(self):
        """Provides help instructions to the user."""
        await self.speak_async("You can log expenses, set budgets, manage recurring expenses, check budgets, view expense history, and generate reports. To exit, say 'exit'.")

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

        elif "recurring expense" in command:
            try:
                _, _, category, amount_str = command.split(maxsplit=3)
                amount = float(amount_str)
                await self.manage_recurring_expenses(category, amount)
            except (ValueError, IndexError):
                await self.speak_async("Please specify a valid category and amount for the recurring expense.")

        elif "generate report" in command:
            await self.generate_monthly_report()

        elif "export data" in command:
            self.export_data_to_csv()
            await self.speak_async("Data exported to CSV.")

        elif "expense history" in command:
            await self.detailed_expense_history()

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
