import logging
import webbrowser
import requests
import re
from voice_recognition import recognize_speech
from text_to_speech import speak
import os
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv('GEMINI_API_KEY')

def strip_html_tags(text: str) -> str:
    """Remove HTML tags from a string."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_directions(start: str, destination: str) -> str:
    """Fetch directions from Google Maps."""
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        if data['status'] == 'OK':
            directions = data['routes'][0]['legs'][0]['steps']
            return " ".join([strip_html_tags(step['html_instructions']) for step in directions])
        else:
            return "I couldn't find directions for that route."
    except requests.exceptions.RequestException:
        return "There was an error fetching directions."

def find_nearby_places(location: str, place_type: str) -> str:
    """Fetch nearby places using Google Maps."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=1500&type={place_type}&key={GOOGLE_MAPS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        places = data.get('results', [])
        if places:
            return [place['name'] for place in places]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def main():
    response = "Welcome to the navigation tool. How can I assist you?"
    logging.info(response)
    speak(response)

    while True:
        logging.info("Listening for navigation command...")
        command = recognize_speech(timeout=10)

        if command:
            command = command.lower()
            logging.info(f"Recognized command: {command}")

            # Check for exit command
            if 'exit' in command or 'stop' in command:
                response = "Exiting navigation tool."
                logging.info(response)
                speak(response)
                break

            # Get directions
            if 'get directions' in command:
                response = "What is your starting point?"
                logging.info(response)
                speak(response)
                start_point = recognize_speech()

                if start_point:
                    response = "What is your destination?"
                    logging.info(response)
                    speak(response)
                    destination = recognize_speech()

                    if destination:
                        directions = get_directions(start_point, destination)
                        logging.info(directions)
                        speak(directions)
                        webbrowser.open(f"https://www.google.com/maps/dir/?api=1&origin={start_point}&destination={destination}")
                    else:
                        speak("I didn't catch the destination.")

                else:
                    speak("I didn't catch the starting point.")

            # Find nearby places
            elif 'find nearby' in command:
                response = "What type of places are you looking for?"
                logging.info(response)
                speak(response)
                place_type = recognize_speech()

                if place_type:
                    response = "What is your current location?"
                    logging.info(response)
                    speak(response)
                    location = recognize_speech()

                    if location:
                        places = find_nearby_places(location, place_type)
                        if places:
                            response = f"Nearby {place_type} include: " + ", ".join(places)
                        else:
                            response = "No nearby places found."
                        logging.info(response)
                        speak(response)
                    else:
                        speak("I didn't catch your location.")

                else:
                    speak("I didn't catch the type of places.")

if __name__ == "__main__":
    main()
