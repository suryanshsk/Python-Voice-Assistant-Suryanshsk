import os
import json
from datetime import datetime

# File to store mood data
MOOD_FILE = "moods.json"
mood_data = []

def load_moods():
    global mood_data
    if os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "r") as file:
            mood_data = json.load(file)
        print("Loaded mood data.")
    else:
        print("No mood data to load.")

def save_moods_to_file():
    with open(MOOD_FILE, "w") as file:
        json.dump(mood_data, file, indent=4)

def show_moods():
    if mood_data:
        print("Mood History:")
        for entry in mood_data:
            date = entry['date']
            mood = entry['mood']
            print(f"{date}: {mood}")
    else:
        print("No mood entries available!")

def submit_mood():
    mood = input("Enter your current mood (e.g., happy, sad, anxious): ")
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood
    }
    mood_data.append(entry)
    print("Mood logged!")
    save_moods_to_file()

def analyze_moods():
    if mood_data:
        mood_count = {}
        for entry in mood_data:
            mood = entry['mood']
            mood_count[mood] = mood_count.get(mood, 0) + 1
        
        print("Mood Analysis:")
        for mood, count in mood_count.items():
            print(f"{mood}: {count} time(s)")
    else:
        print("No moods to analyze!")

def mood_tracker_system():
    load_moods()
    while True:
        print("\nMood Tracker System")
        print("1. Log Mood")
        print("2. Show Mood History")
        print("3. Analyze Moods")
        print("4. Exit")

        choice = input("Please select an option (1-4): ")

        if choice == "1":
            submit_mood()
        elif choice == "2":
            show_moods()
        elif choice == "3":
            analyze_moods()
        elif choice == "4":
            print("Exiting mood tracker system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    mood_tracker_system()
