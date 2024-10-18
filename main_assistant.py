import os
import subprocess
import sys
import logging
import webbrowser
import time
from datetime import datetime
from voice_recognition import recognize_speech
from text_to_speech import speak
from wikipedia_info import search_wikipedia
from weather_info import get_weather
from news_info import get_news
from jokes import tell_joke
from open_app import open_application
from gemini_info import get_gemini_response
from song_data import SONGS
from website_data import WEBSITES
import genai
import speech_recognition as sr

gemini_api_key = os.getenv("GEMINI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

genai.configure(api_key=gemini_api_key)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_greeting():
    """Get the appropriate greeting based on the current time."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def main():
    while True:
        logging.info("Listening for command...")
        try:
            query = recognize_speech(timeout=10)  # Add a timeout to prevent blocking
        except Exception as e:
            logging.error(f"Error recognizing speech: {e}")
            speak("Sorry, I didn't catch that.")
            continue

        if not query:
            logging.warning("No command recognized, continuing...")
            continue

        query = query.lower()
        logging.info(f"Recognized command: {query}")

        # Check for exit or stop commands
        if 'exit' in query or 'stop' in query:
            response = "Goodbye!"
            logging.info(response)
            speak(response)
            break

        if 'time' in query:
            greeting = get_greeting()
            current_time = datetime.now().strftime("%H:%M:%S")
            response = f"{greeting}! The current time is {current_time}."
            logging.info(response)
            speak(response)
            continue

        if 'wikipedia' in query:
            response = "Searching Wikipedia..."
            logging.info(response)
            speak(response)
            search_query = query.replace("search wikipedia for", "").strip()
            time.sleep(1)  # Short delay to improve response time
            try:
                results = search_wikipedia(search_query)
                response = f"According to Wikipedia, {results}"
            except Exception as e:
                response = "Sorry, I couldn't fetch the Wikipedia information."
                logging.error(f"Error fetching Wikipedia info: {e}")
            logging.info(response)
            speak(response)

        elif 'weather' in query:
            response = "Please provide the city name."
            logging.info(response)
            speak(response)
            city_name = recognize_speech()
            if city_name:
                try:
                    weather_info = get_weather(city_name)
                    response = f"The weather in {city_name} is: {weather_info}"
                except Exception as e:
                    response = "Sorry, I couldn't fetch the weather information."
                    logging.error(f"Error fetching weather info: {e}")
                logging.info(response)
                speak(response)

        elif 'news' in query:
            response = "Fetching the latest news..."
            logging.info(response)
            speak(response)
            try:
                news_headlines = get_news()
                for headline in news_headlines:
                    logging.info(headline)
                    speak(headline)
            except Exception as e:
                response = "Sorry, I couldn't fetch the news."
                logging.error(f"Error fetching news: {e}")
                speak(response)

        elif 'joke' in query:
            response = "Here's a joke for you."
            logging.info(response)
            speak(response)
            try:
                joke = tell_joke()
                logging.info(joke)
                speak(joke)
            except Exception as e:
                response = "Sorry, I couldn't fetch a joke."
                logging.error(f"Error fetching joke: {e}")
                speak(response)

        elif 'play music' in query:
            response = "Which song would you like to play?"
            logging.info(response)
            speak(response)
            song_name = recognize_speech()
            if song_name:
                youtube_url = SONGS.get(song_name.lower())
                if youtube_url:
                    response = f"Playing {song_name} in your browser."
                    logging.info(response)
                    speak(response)
                    webbrowser.open(youtube_url)
                else:
                    response = "Song not found in the database."
                    logging.warning(response)
                    speak(response)

        elif 'open' in query:
            if 'website' in query:
                response = "Which website would you like to open?"
                logging.info(response)
                speak(response)
                website_name = recognize_speech()
                if website_name:
                    website_url = WEBSITES.get(website_name.lower())
                    if website_url:
                        response = f"Opening {website_name} in your browser."
                        logging.info(response)
                        speak(response)
                        webbrowser.open(website_url)
                    else:
                        response = "Website not found in the database."
                        logging.warning(response)
                        speak(response)
            else:
                app_name = query.replace("open", "").strip()
                response = f"Opening {app_name}."
                logging.info(response)
                speak(response)
                try:
                    result = open_application(app_name)
                    logging.info(result)
                    speak(result)
                except Exception as e:
                    response = f"Sorry, I couldn't open {app_name}."
                    logging.error(f"Error opening app: {e}")
                    speak(response)

        else:
            # Use Gemini AI for general questions
            response = "Let me check that for you."
            logging.info(response)
            speak(response)
            try:
                ai_response = get_gemini_response(query)
                logging.info(ai_response)
                speak(ai_response)
            except Exception as e:
                response = "Sorry, I couldn't find the information."
                logging.error(f"Error fetching Gemini response: {e}")
                speak(response)
if __name__ == "__main__":
    RUNNING = True
    
    reminder_thread.start()
    response = "Hello, I'm Your PA. How can I assist you today?"
    logging.info(response)
    speak(response)
    try:
        main()
    except KeyboardInterrupt:
        RUNNING = False
