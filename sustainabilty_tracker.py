import speech_recognition as sr
import pyttsx3
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Slower speaking rate

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Persistent data storage
def save_data():
    with open("sustainability_data.json", "w") as file:
        json.dump(sustainability_data, file)

def load_data():
    global sustainability_data
    try:
        with open("sustainability_data.json", "r") as file:
            sustainability_data = json.load(file)
    except FileNotFoundError:
        print("No previous data found.")
        sustainability_data = {}

# Load data at the start of the program
load_data()

# Example user-specific sustainability data structure
def initialize_user_data(user):
    if user not in sustainability_data:
        sustainability_data[user] = {
            "transportation": [],
            "energy_usage": [],
            "water_usage": [],
            "waste": []
        }

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

# Function to log sustainability data with timestamp
def log_sustainability_data(user, category, value):
    timestamp = datetime.now().isoformat()
    sustainability_data[user][category].append({"date": timestamp, "value": value})
    save_data()

# Function to provide sustainability recommendations
def provide_recommendations(user):
    user_data = sustainability_data[user]
    
    if sum([item["value"] for item in user_data["transportation"]]) > 100:
        speak("You have logged over 100 kilometers in transportation. Consider using public transport or carpooling to reduce your carbon footprint.")
    
    if sum([item["value"] for item in user_data["energy_usage"]]) > 500:
        speak("Your energy consumption seems high. Try turning off appliances when not in use to save energy.")
    
    if sum([item["value"] for item in user_data["water_usage"]]) > 300:
        speak("You have logged high water usage. Consider taking shorter showers or fixing leaks to save water.")
    
    if sum([item["value"] for item in user_data["waste"]]) > 50:
        speak("You have logged a lot of waste. Consider recycling or composting to reduce your waste footprint.")

# Function to calculate carbon footprint for transportation (mocked API integration)
def get_carbon_footprint_km(km):
    # Mock API response for the carbon footprint
    carbon_per_km = 0.21  # Average kg CO2 per km for a car
    return round(km * carbon_per_km, 2)

# Function to plot sustainability data
def plot_sustainability_data(user):
    categories = ['transportation', 'energy_usage', 'water_usage', 'waste']
    values = [sum([item["value"] for item in sustainability_data[user][cat]]) for cat in categories]
    
    plt.bar(categories, values)
    plt.ylabel('Units')
    plt.title(f'{user.capitalize()}\'s Sustainability Tracker')
    plt.show()

# Function to provide historical data summary
def get_weekly_summary(user):
    categories = ['transportation', 'energy_usage', 'water_usage', 'waste']
    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_summary = {cat: 0 for cat in categories}
    
    for category in categories:
        for entry in sustainability_data[user][category]:
            entry_date = datetime.fromisoformat(entry['date'])
            if entry_date > one_week_ago:
                weekly_summary[category] += entry["value"]
    
    return weekly_summary

# Function to confirm user's entry
def confirm_entry(category, value):
    speak(f"Did you mean to log {value} units to {category}? Please say yes or no.")
    confirmation = voice_to_text()
    if confirmation and "yes" in confirmation.lower():
        return True
    return False

# Main function for the voice assistant
if __name__ == "__main__":
    user = "default_user"  # Placeholder for user identification
    initialize_user_data(user)  # Initialize user data if not present
    speak("Hello! I'm your sustainability assistant. How can I help you today?")
    
    while True:
        command = voice_to_text()
        
        if command is None:
            continue  # Retry if the command was not understood
        
        print(f"Command received: {command}")
        
        # Exit the assistant if the user says "exit" or "stop"
        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye! Stay sustainable!")
            break
        
        # Example: Log transportation
        elif "log" in command.lower() and "transportation" in command.lower():
            try:
                # Extract the number of kilometers from the command
                km = int(command.split()[-1])  # Assuming the last word is a number
                if confirm_entry("transportation", km):
                    carbon_footprint = get_carbon_footprint_km(km)
                    log_sustainability_data(user, "transportation", km)
                    speak(f"Logged {km} kilometers. This corresponds to a carbon footprint of {carbon_footprint} kilograms of CO2.")
            except ValueError:
                speak("I couldn't understand the number of kilometers. Please say it again.")
        
        # Example: Show weekly summary
        elif "weekly summary" in command.lower():
            weekly_data = get_weekly_summary(user)
            speak(f"Here is your weekly summary: Transportation {weekly_data['transportation']} kilometers, Energy usage {weekly_data['energy_usage']} units, Water usage {weekly_data['water_usage']} liters, Waste {weekly_data['waste']} kilograms.")
        
        # Example: Show data visualization
        elif "show graph" in command.lower():
            plot_sustainability_data(user)
        
        # Provide recommendations
        elif "recommend" in command.lower():
            provide_recommendations(user)

        else:
            speak("I didn't catch that. Please say a valid command, like 'log transportation' or 'show graph'.")
