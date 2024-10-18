import json
import datetime
import requests
import schedule
import time
import matplotlib.pyplot as plt 
from colorama import init, Fore, Style

init(autoreset=True)

def log_mood(mood, notes):
    try:
        with open('moods.json', 'r') as file:
            moods = json.load(file)  
    except FileNotFoundError:
        moods = []  

    mood_entry = {
        'mood': mood,
        'notes': notes
    }
    moods.append(mood_entry)

    with open('moods.json', 'w') as file:
        json.dump(moods, file, indent=4)

def log_gratitude():
    gratitude = input(Fore.GREEN + "What are you grateful for today? ")
    return gratitude

def log_habit():
    habit_done = input(Fore.GREEN + "Did you complete any positive habits today(exercise, meditation, jounaling)? (yes/no): ")
    return habit_done.lower() == "yes"

def get_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0]['q']  
    else:
        return "Stay Positive"

def get_meditation_tip():

    tips = [

        "Take 5 deep breaths, inhaling through your nose and exhaling through your mouth.",
        "Try a 5-minute body scan meditation to relax your muscles.",
        "Focus on your breath for 2 minutes, letting go of any distracting thoughts.",
        "Practice mindful walking—pay attention to each step and your surroundings.",
        "Try a loving-kindness meditation: Send positive thoughts to yourself and others.",
        "Spend 10 minutes meditating in silence, focusing on the rise and fall of your breath.",
        "Use a guided meditation app to center yourself for a few minutes.",
        "Visualize a peaceful scene while breathing slowly to calm your mind.",
        "Perform a gratitude meditation—list three things you're thankful for in the moment.",
        "Try progressive muscle relaxation—tense and relax each muscle group from head to toe."
    ]
    return tips[datetime.datetime.now().second % len(tips)]

def visualize_mood_trends():
    try:
        with open('moods.json', 'r') as f:
            moods = json.load(f)
        mood_counts = {}
        for entry in moods:
            mood = entry['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        plt.figure(figsize=(10, 5))
        plt.bar(mood_counts.keys(), mood_counts.values(), color='skyblue')
        plt.title('Mood Trends')
        plt.xlabel('Moods')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(Fore.RED + "Oops! No mood has been data found.")


def daily_check_in():

    print(Fore.GREEN + "How are you feeling today? Please type your mood.")
    mood = input(Fore.GREEN + "Enter your mood: ")
    notes = input(Fore.GREEN + "Any notes you'd like to add? ")
    gratitude = log_gratitude()
    habit_done = log_habit()
    habit_status = "Completed positive habit" if habit_done else "Didn't completed the positive habit"
    log_mood(mood, f"{notes}. Grateful for: {gratitude}. {habit_status}")

    quote = get_quote()
    meditation_tip = get_meditation_tip()
    print(Fore.BLUE + f"Quote for you: {quote}")
    print(Fore.MAGENTA + f"Meditation Tip: {meditation_tip}")

    music_suggestion = suggest_music(mood)
    print(Fore.YELLOW + music_suggestion) 

def mood_summary():

    try:
        with open('moods.json', 'r') as f:
            moods = json.load(f)
        mood_counts = {}
        for entry in moods:
            mood = entry['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        most_common_mood = max(mood_counts, key=mood_counts.get)
        total_entries = len(moods)

        print(Fore.CYAN + f"Most common mood: {most_common_mood}")
        print(Fore.CYAN + f"Total mood entries: {total_entries}" )

    except FileNotFoundError:
        print(Fore.RED + "No mood data is avilable for the summary")


def get_personalised_recommendation():

    try:
        with open('moods.json', 'r') as f:
            moods = json.load(f)

        last_mood = moods[-1]['mood']
        recommendations = {
            "happy": "Listen to your favorite music or call a friend!",
            "sad": "Try a short walk outside or practice deep breathing.",
            "anxious": "Consider yoga or meditation.",
            "calm": "Take a few minutes to enjoy the moment, maybe with a book or tea.",
            "excited": "Channel that energy into a fun activity like dancing or cooking!",
            "stressed": "Take a break, focus on your breath, or try a short stretching routine."
        }
        return recommendations.get(last_mood, "Do something you enjoy!")

    except FileNotFoundError:
        return "No mood data is available for recommendations."

def predict_moods_trend():

    try:
        with open('moods.json', 'r') as f:
            moods= json.load(f)

        mood_by_day = {}
        for entry in moods:
            day = datetime.datetime.fromisoformat(entry['date']).strftime('%A')
            mood = entry['mood']
            if day not in mood_by_day:
                mood_by_day[day] = []
            mood_by_day[day].append(mood)

        for day, moods in mood_by_day.items():
            most_common_mood = max(set(moods), key=moods.count)
            print(Fore.CYAN + f"On {day}s, you usually feel {most_common_mood}.")

    except FileNotFoundError:
        print(Fore.RED + "No mood data is available for prediction.")

def suggest_music(mood):

    if mood == "happy":
        return "How about some upbeat pop music? Try this Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
    elif mood == "sad":
        return "Maybe some relaxing acoustic tunes would help. Try this Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DWXnexX7CktaI"
    elif mood == "anxious":
        return "Classical or ambient music could calm you down. Try this Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO"
    elif mood == "stressed":
        return "Relax with some chill beats. Try this Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DX9RwfGbeGQwP"
    elif mood == "excited":
        return "You're full of energy! Try this dance playlist: https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n"
    elif mood == "angry":
        return "Some energetic rock might help. Try this playlist: https://open.spotify.com/playlist/37i9dQZF1DWX83CujKHHOn"
    elif mood == "relaxed":
        return "Enjoy some mellow vibes. Try this playlist: https://open.spotify.com/playlist/37i9dQZF1DWXbttAJcbphz"
    else:
        return "Music can always lift your spirits! Try this random playlist: https://open.spotify.com/playlist/37i9dQZF1DWYBO1MoTDhZI"

schedule.every().day.at("09:00").do(daily_check_in)
schedule.every().day.at("10:00").do(lambda: print(Fore.GREEN + "Reminder: Take 10 minutes for meditation."))
schedule.every().day.at("15:00").do(lambda: print(Fore.GREEN + "Reminder: Time for some light exercise!"))

if __name__ == "__main__":

    while True:

        print(Fore.CYAN + "Welcome to your mood tracker. Would you like to log your mood, see trends, or get recommendation?")
        command = input(Fore.GREEN + "Type 'log mood', 'trends', 'recommendations', 'summary', or 'predict trends': ").lower()

        if "log mood" in command:
            daily_check_in()

        elif "trends" in command:
            visualize_mood_trends()

        elif "recommendations" in command:
            recommendation = get_personalised_recommendation()
            print(Fore.BLUE + f"Recommendation based on your last mood: {recommendation}")

        elif "summary" in command:
            mood_summary()

        elif "predict trends" in command:
            predict_moods_trend()

        else:
            print(Fore.RED + "Sorry, I didn't understand that command.")

        schedule.run_pending()
        time.sleep(1)

