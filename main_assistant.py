from voice_recognition import recognize_speech
from text_to_speech import speak
from wikipedia_info import search_wikipedia
from weather_info import get_weather
from news_info import get_news
from jokes import tell_joke
from open_app import open_application
from gemini_info import get_gemini_response
import webbrowser
from song_data import SONGS
from website_data import WEBSITES
import time
from datetime import datetime  # Import to get current time

def get_greeting():
    """Function to get the appropriate greeting based on the current time."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
def main():
    while True:
        print("Listening for command...")  # Debug print
        query = recognize_speech()
        print(f"Recognized command: {query}")  # Debug print
        
        if query == "None":
            print("No command recognized, continuing...")  # Debug print
            continue

        # Check for interrupt command
        if 'hey stop' in query.lower():
            response = "Stopping current operation."
            print(response)  # Debug print
            speak(response)
            continue  # Restart listening

        if 'time' in query.lower():
            greeting = get_greeting()  # Get the appropriate greeting
            current_time = datetime.now().strftime("%H:%M:%S")  # Get current time in HH:MM:SS format
            response = f"{greeting}! The current time is {current_time}."
            print(response)  # Debug print
            speak(response)
            continue  # Restart listening for the next command

        if 'wikipedia' in query.lower():
            response = "Searching Wikipedia..."
            print(response)  # Debug print
            speak(response)
            query = query.replace("search wikipedia for", "").strip()
            time.sleep(1)  # Add a short delay to improve response time
            results = search_wikipedia(query)
            response = f"According to Wikipedia, {results}"
            print(response)  # Debug print
            speak(response)
        elif 'weather' in query.lower():
            response = "Please provide the city name."
            print(response)  # Debug print
            speak(response)
            city_name = recognize_speech()
            if city_name != "None":
                response = f"Getting weather information for {city_name}"
                print(response)  # Debug print
                speak(response)
                weather_info = get_weather(city_name)
                print(weather_info)  # Debug print
                speak(weather_info)
        elif 'news' in query.lower():
            response = "Fetching the latest news..."
            print(response)  # Debug print
            speak(response)
            news_headlines = get_news()
            for headline in news_headlines:
                print(headline)  # Debug print
                speak(headline)
        elif 'joke' in query.lower():
            response = "Here's a joke for you."
            print(response)  # Debug print
            speak(response)
            joke = tell_joke()
            print(joke)  # Debug print
            speak(joke)
        elif 'play music' in query.lower():
            response = "Which song would you like to play?"
            print(response)  # Debug print
            speak(response)
            song_name = recognize_speech()
            if song_name != "None":
                youtube_url = SONGS.get(song_name.lower())
                if youtube_url:
                    response = "Opening the song in your browser..."
                    print(response)  # Debug print
                    speak(response)
                    webbrowser.open(youtube_url)
                    response = f"{song_name} is now playing in your browser."
                    print(response)  # Debug print
                    speak(response)
                else:
                    response = "Song not found in the database."
                    print(response)  # Debug print
                    speak(response)
        elif 'open' in query.lower():
            if 'website' in query.lower():
                response = "Which website would you like to open?"
                print(response)  # Debug print
                speak(response)
                website_name = recognize_speech()
                if website_name != "None":
                    website_url = WEBSITES.get(website_name.lower())
                    if website_url:
                        response = "Opening the website in your browser..."
                        print(response)  # Debug print
                        speak(response)
                        webbrowser.open(website_url)
                        response = f"{website_name} is now open in your browser."
                        print(response)  # Debug print
                        speak(response)
                    else:
                        response = "Website not found in the database."
                        print(response)  # Debug print
                        speak(response)
            else:
                app_name = query.replace("open", "").strip()
                response = f"Opening {app_name}"
                print(response)  # Debug print
                speak(response)
                response = open_application(app_name)
                if response:
                    print(response)  # Debug print
                    speak(response)
        elif 'stop music' in query.lower():
            response = "Sorry, I can't stop music from the browser. Please stop it manually."
            print(response)  # Debug print
            speak(response)
        elif 'suryanshsk' in query or 'suryansh sk' in query: 
            response = '''Certainly! Suryanshsk is a content creator and software developer known for sharing tech-related 
            content on platforms like YouTube. Here are some key points about Suryanshsk: YouTube Channel: Suryanshsk runs 
            a YouTube channel called Tech suryanshsk1. The channel covers various topics related to technology, coding, and
            software development. Content: Suryanshsk shares videos on topics such as: Application Development: Suryanshsk
            demonstrates how to develop applications using different technologies. For example, there’s a video on creating 
            a Calculator Application in Flutter2. Software Development: Suryanshsk has developed a Hotel Bill Management Software
            using Visual Basic 6.0. The software is open-source and free of cost1. Coding Shorts: Suryanshsk also shares short 
            coding videos, covering various programming languages and concepts 3.Social Media Presence: Instagram: You can find
            Suryanshsk on Instagram @suryanshsk. Twitter: Suryanshsk is active on Twitter as well (@suryanshsk). Blog: Suryanshsk 
            maintains a blog at suryanshsk.blogspot.com. 4. Software Projects: Hotel Bill Management Software: Suryanshsk developed 
            an open-source hotel bill management software using Visual Basic 6.0. The source code and setup files are available for 
            free Overall, Suryanshsk’s content focuses on programming, software development, and technology. If you’re interested in 
            learning more, check out the Tech suryanshsk YouTube channel! 😊👍'''
            print(response)  # Debug print
            speak(response)
        elif 'exit' in query.lower() or 'stop' in query.lower():
            response = "Goodbye!"
            print(response)  # Debug print
            speak(response)
            break
        else:
            # Use Gemini AI for general questions
            response = "Let me check that for you."
            print(response)  # Debug print
            speak(response)
            response = get_gemini_response(query)
            print(response)  # Debug print
            speak(response)

if __name__ == "__main__":
    response = "Hello, I'm Your PA. How can I assist you today?"
    print(response)  # Debug print
    speak(response)
    main()
