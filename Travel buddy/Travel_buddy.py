import speech_recognition as sr
import pyttsx3
import requests
from geopy.geocoders import Nominatim

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
geolocator = Nominatim(user_agent="travel_assistant")

# Cultural insights and fun facts about various cities
cultural_insights = {
    "tokyo": "Tokyo, a bustling metropolis, is known for its modern skyscrapers, vibrant neighborhoods, and delicious sushi. Don't forget to visit the historic Senso-ji Temple.",
    "paris": "Paris, the City of Light, is famous for its art, fashion, and the iconic Eiffel Tower. Stroll along the Seine for breathtaking views.",
    "new york": "New York City, often called the Big Apple, is renowned for its skyline, Central Park, and Broadway shows. Be sure to catch a performance!",
    "rome": "Rome, the Eternal City, is rich in history, with stunning architecture like the Colosseum and the Vatican. Enjoy a gelato while exploring the cobblestone streets.",
    "london": "London blends history and modernity with landmarks like the Tower of London and Buckingham Palace. Visit Camden Market for vibrant local culture.",
    "sydney": "Sydney is famous for its Opera House and beautiful harbor. Don't miss a walk across the Sydney Harbour Bridge for breathtaking views.",
    "mumbai": "Mumbai, the financial capital of India, is known for Bollywood, vibrant street food, and landmarks like the Gateway of India.",
    "cairo": "Cairo is home to the majestic Pyramids of Giza and the bustling markets of Khan El Khalili. Enjoy a felucca ride on the Nile.",
    "beijing": "Beijing, with its rich history, is famous for the Great Wall and the Forbidden City. Explore the vibrant hutongs for a taste of local life.",
    "rio de janeiro": "Rio de Janeiro is known for its stunning beaches, Carnival festival, and the iconic Christ the Redeemer statue atop Corcovado Mountain.",
    "barcelona": "Barcelona is renowned for its unique architecture by Antoni Gaudí, including the famous Sagrada Familia and Park Güell. Enjoy tapas in the Gothic Quarter.",
    "bangkok": "Bangkok is famous for its vibrant street life, ornate temples, and the bustling Chatuchak Market. Don't miss a boat ride through the canals.",
    "istanbul": "Istanbul bridges Europe and Asia, offering rich history with sites like the Hagia Sophia and the Grand Bazaar. Experience a traditional Turkish bath.",
    "los angeles": "Los Angeles is known for Hollywood, beautiful beaches, and diverse cuisine. Visit the Griffith Observatory for stunning city views.",
    "moscow": "Moscow is famous for historical landmarks, including Red Square and the Kremlin. Take a stroll through Gorky Park for a local experience.",
    "sao paulo": "São Paulo is Brazil's largest city, known for its vibrant cultural scene, including theaters, museums, and incredible street art.",
    "dublin": "Dublin, the capital of Ireland, is known for its literary history and the lively Temple Bar district. Visit the Guinness Storehouse for a taste of local beer.",
    "seoul": "Seoul combines modern skyscrapers with ancient palaces. Don't miss the bustling markets of Myeongdong.",
    "cape town": "Cape Town is known for its stunning Table Mountain, beautiful beaches, and rich history. Take a cable car ride for breathtaking views."
}

# Your Google Places API key and Knowledge Graph API key
GOOGLE_PLACES_API_KEY = 'YOUR_PLACES_API_KEY_HERE'
GOOGLE_KNOWLEDGE_GRAPH_API_KEY = 'YOUR_KNOWLEDGE_GRAPH_API_KEY_HERE'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is temporarily unavailable.")
            return None

def get_cultural_insight(city):
    insight = cultural_insights.get(city.lower())
    if insight:
        speak(insight)
    else:
        speak(f"I don't have specific insights about {city}. Let me find some information for you.")
        get_city_info(city)

def get_city_info(city):
    # Fetch general information about the city using the Knowledge Graph API
    url = f"https://kgsearch.googleapis.com/v1/entities:search?query={city}&key={GOOGLE_KNOWLEDGE_GRAPH_API_KEY}&limit=1&indent=True"
    response = requests.get(url)
    data = response.json()

    if data.get('itemListElement'):
        description = data['itemListElement'][0]['result'].get('description', 'No description available.')
        speak(f"Here is some information about {city}: {description}")
    else:
        speak("I'm sorry, I couldn't find any information about that city.")

def get_famous_places_to_visit(city):
    # Google Places API request to fetch famous attractions
    geolocator = Nominatim(user_agent="travel_assistant")
    location_info = geolocator.geocode(city)
    
    if location_info:
        lat = location_info.latitude
        lon = location_info.longitude
        
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=tourist_attraction&key={GOOGLE_PLACES_API_KEY}"
        response = requests.get(url)
        places = response.json()
        
        # Filter for well-known places
        if places['results']:
            speak("Here are some famous places you might consider visiting:")
            for place in places['results']:
                if 'user_ratings_total' in place and place.get('rating', 0) >= 4.5:
                    name = place['name']
                    speak(name)
                    print(name)  # Print the names for confirmation
            speak("These are some popular attractions you might enjoy.")
        else:
            speak("I'm sorry, but I couldn't find any famous places nearby.")
    else:
        speak("I couldn't locate that city.")

def main():
    speak("Hello! I'm your travel companion. I can help you with cultural insights and famous places to visit. Just ask me!")
    while True:
        command = listen()
        if command:
            if "cultural insight about" in command:
                city = command.split("cultural insight about")[-1].strip()
                get_cultural_insight(city)
            elif "famous places to visit in" in command:
                city = command.split("famous places to visit in")[-1].strip()
                get_famous_places_to_visit(city)
            elif "stop" in command:
                speak("Goodbye! Have a wonderful day!")
                break
            else:
                speak("You can ask me for cultural insights or famous places to visit. Just say 'stop' to end our chat.")

if __name__ == "__main__":
    main()
