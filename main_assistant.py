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
from collections import defaultdict
from reminderr import *
import threading
import json

### MAIN

""" 

Guidelines for new ability/feature contributions

1. Please create your code into a separate file or a separate function. 
2. Define your functions's inputs properly.
3. Add your function's tool name to the following TOOLS list, add a description, inputs and action : ( your function name )
4. list your tool properly in the last prompt in the main function to get inputs from gemini.
%% Please be as specific as possible and describe as good as poosible about your inputs, their formats 
%% and the function's intention when to be called to get a proper output.

Thank You.

"""


def recognize_speech(timeout=10):
    # Simulate speech recognition
    return input("You: ")

def speak(message):
    print(f"Assistant: {message}")

def just_Say(msg):
    logging.info(msg)
    speak(msg)

def abort(message):
    global RUNNING
    RUNNING = False
    print(message)

def play_music(song_name=""):
    if song_name == "":
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

def open_website(website_name = ""):
    if website_name == "":
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
            response = "Website not found in the database.Searching in google."
            logging.warning(response)
            speak(response)
            from googlesearch import search
            webs = search(website_name, advanced=True)
            webbrowser.open(list(webs)[0].url)
            

TOOLS = [
    {
        'name': 'just_Say',
        'description': '',
        'inputs': ['msg'],
        'action': just_Say
    },
    {
        'name': 'get_news',
        'description': 'Get news',
        'inputs': [],
        'action': get_news
    },
    {
        'name': 'set_reminder',
        'description': 'Sets a reminder based on user query.',
        'inputs': ['input_text'],
        'action': extract_reminder
    },
    {
        'name': 'search_wikipedia',
        'description': 'Searches Wikipedia for the given query.',
        'inputs': ['query'],
        'action': search_wikipedia
    },
    {
        'name': 'get_weather',
        'description': 'Fetches the weather information for the specified city.',
        'inputs': ['city_name'],
        'action': get_weather
    },
    {
        'name': 'tell_joke',
        'description': 'Tells a random joke.',
        'inputs': [],
        'action': tell_joke
    },
    {
        'name': 'play_music',
        'description': 'Plays music based on the song name provided.',
        'inputs': ['song_name'],
        'action': play_music
    },
    {
        'name': 'open_website',
        'description': 'Opens a website in the browser.',
        'inputs': ['website_name'],
        'action': open_website
    },
    {
        'name': 'open_application',
        'description': 'Opens an Application',
        'inputs': ['app_name'],
        'action': open_application
    },
    {
        'name': 'abort',
        'description': 'Aborts',
        'inputs': ['message'],
        'action': abort
    }
]


## MAIN

global REMINDERS
global RUNNING

REMINDERS = defaultdict(list)


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

def check_reminders():
    global REMINDERS
    while RUNNING:
        current_time = datetime.now()

        # Convert current time to ISO 8601 format
        current_time_iso = current_time.isoformat()
        if REMINDERS[current_time_iso]:
            print("Reminder:", REMINDERS[current_time_iso])
            del REMINDERS[current_time_iso]
        time.sleep(10)
reminder_thread = threading.Thread(target=check_reminders)


# Process the response from Gemini to extract the tool and its inputs
def process_gemini_response(response):
    try:
        response_data = json.loads(response)
        tool_name = response_data['tool']
        inputs = response_data['inputs']
        return tool_name, inputs
    except Exception as e:
        logging.error(f"Error processing Gemini AI response: {e}")
        return None, None

# The main loop to handle user commands
def main():
    global RUNNING
    global REMINDERS

    while RUNNING:
        logging.info("Listening for command...")
        try:
            query = recognize_speech(timeout=10)  # Replace with actual speech recognition function
        except Exception as e:
            logging.error(f"Error recognizing speech: {e}")
            speak("Sorry, I didn't catch that.")
            continue

        if not query:
            logging.warning("No command recognized, continuing...")
            continue

        query = query.lower()
        logging.info(f"Recognized command: {query}")

        # Prompt Gemini AI to select tool and provide inputs
        gemini_prompt = f"""
        I have a list of tools that can perform specific actions. Based on the user query, select the appropriate tool from the list and extract the necessary inputs. Please respond in the following JSON format:

        {{
            "tool": "<tool_name>",
            "inputs": {{
                "input1": "<value1>",
                "input2": "<value2>",
                ...
            }}
        }}

        Here is the list of tools:
        1. "just_Say": Requires "msg" , a generic conversational response if none of the following tools fits best.
        2. "set_reminder": Requires "input_text" ( simply return enhanced the input Query which I give ).
        3. "search_wikipedia": Requires "query".
        4. "get_weather": Requires "city_name".
        5. "tell_joke": Requires no inputs.
        6. "play_music": Requires "song_name".
        7. "open_website": Requires "website_name" ( return an empty string if no website if specified )
        8. "open_application": Requires "app_name".
        9. "get_news": Requires no inputs.
        9. "abort" : Requires a "message" . Call this if the user wants to leave.
        If the tool requires no inputs, leave the "inputs" field empty.

        Query: "{query}"
        """
        
        gemini_response = get_gemini_response(gemini_prompt)
        # print(gemini_response)
        tool_name, inputs = process_gemini_response(gemini_response)
        
        print(tool_name, inputs)
        if tool_name:
            # Find the corresponding tool and call its action with the provided inputs
            tool = next((t for t in TOOLS if t['name'] == tool_name), None)
            if tool:
                try:
                    tool['action'](**inputs)
                except Exception as e:
                    logging.error(f"Error executing {tool_name}: {e}")
                    speak(f"Sorry, there was an error with {tool_name}.")
            else:
                logging.error(f"Tool {tool_name} not found.")
                speak(f"Sorry, I couldn't find the tool {tool_name}.")
        else:
            speak("Sorry, I couldn't process the query.")

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
