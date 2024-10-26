import json
import logging
from datetime import datetime
import re
from gemini_info import get_gemini_response



RUNNING = True
REMINDERS = {}

def just_print(msg):
    print(msg)
# Placeholder functions for individual tools (you'll replace these with your actual implementations)
def set_reminder(time, message):
    print(f"Reminder set for {time}: {message}")
    REMINDERS[time] = message

def search_wikipedia(search_query):
    print(f"Searching Wikipedia for: {search_query}")
    # Simulated Wikipedia result
    return f"Wikipedia result for {search_query}"

def get_weather(city_name):
    print(f"Fetching weather for: {city_name}")
    # Simulated weather data
    return f"Weather data for {city_name}"

def tell_joke():
    print("Fetching a joke...")
    return "Why don't scientists trust atoms? Because they make up everything!"

def play_music(song_name):
    print(f"Playing {song_name} on YouTube.")
    # Simulate playing music

def open_website(website_name):
    print(f"Opening {website_name}.")
    # Simulate opening a website

def abort(message):
    global RUNNING
    RUNNING = False
    print(message)
# Tool list with descriptions and inputs
TOOLS = [
    {
        'name': 'just_print',
        'description': '',
        'inputs': ['msg'],
        'action': just_print
    },
    {
        'name': 'set_reminder',
        'description': 'Sets a reminder based on user query.',
        'inputs': ['time', 'message'],
        'action': set_reminder
    },
    {
        'name': 'search_wikipedia',
        'description': 'Searches Wikipedia for the given query.',
        'inputs': ['search_query'],
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
        'name': 'abort',
        'description': 'Aborts',
        'inputs': ['message'],
        'action': abort
    }
]


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
        1. "just_print": Requires "msg" , a generic conversational response if none of the following tools fits best.
        2. "set_reminder": Requires "time" (strictly in ISO format . that is,'date+T+time', including both date and time) and "message".
        3. "search_wikipedia": Requires "search_query".
        4. "get_weather": Requires "city_name".
        5. "tell_joke": Requires no inputs.
        6. "play_music": Requires "song_name".
        7. "open_website": Requires "website_name".
        8. "abort" : Requires a "message" . Call this if the user wants to leave.
        If the tool requires no inputs, leave the "inputs" field empty.

        Query: "{query}"
        """
        
        gemini_response = get_gemini_response(gemini_prompt)
        print(gemini_response)
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
        

def recognize_speech(timeout=10):
    # Simulate speech recognition
    return input("You: ")

def speak(message):
    print(f"Assistant: {message}")

if __name__ == "__main__":
    main()