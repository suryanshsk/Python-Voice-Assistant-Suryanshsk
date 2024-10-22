import asyncio
import json
import pyttsx3
import speech_recognition as sr
import aiohttp  # For async API requests
import geopy.distance  # To calculate distance between coordinates

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Function to convert text to speech asynchronously
async def speak_async(text):
    engine.say(text)
    engine.runAndWait()
    await asyncio.sleep(0.5)  # Add a delay after speaking

# Function to get user input through speech recognition
async def voice_to_text_async():
    recognizer = sr.Recognizer()
    await asyncio.sleep(0.5)  # Ensure TTS finishes before listening
    with sr.Microphone() as source:
        print("Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            await speak_async("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            await speak_async("The speech recognition service is unavailable at the moment.")
            return None

# Simulate getting current location (replace this with a real GPS location API)
def get_current_location():
    return {"lat": 40.712776, "lng": -74.005974}  # New York City coordinates

# Asynchronous function to fetch nearby services using aiohttp
async def get_nearby_services(service_type):
    location = get_current_location()
    latitude = location["lat"]
    longitude = location["lng"]
    
    api_key = "your_actual_google_places_api_key"
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1500&type={service_type}&key={api_key}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    places = await response.json()
                    results = places.get('results', [])
                    if results:
                        await speak_async(f"Here are some {service_type} nearby:")
                        for place in results[:3]:
                            name = place.get('name', 'Unknown place')
                            await speak_async(f"{name}")
                    else:
                        await speak_async(f"Sorry, I couldn't find any {service_type} nearby.")
                else:
                    await speak_async(f"Failed to retrieve nearby services. Error Code: {response.status}")
        except aiohttp.ClientError as e:
            await speak_async(f"An error occurred: {str(e)}")

# Geofencing Alert: Set location-based reminders
async def set_geofencing_alert(reminder, target_location):
    current_location = get_current_location()
    target_coords = (target_location.get('lat'), target_location.get('lng'))
    
    if current_location and target_coords:
        try:
            distance_to_target = geopy.distance.distance((current_location['lat'], current_location['lng']), target_coords).km
            if distance_to_target < 0.5:
                await speak_async(f"Reminder: {reminder}")
            else:
                await speak_async(f"Geofencing reminder set. Distance: {distance_to_target:.2f} km.")
        except ValueError:
            await speak_async("Invalid coordinates provided for geofencing.")
    else:
        await speak_async("Unable to get current location or target location.")

# Background geofencing monitoring loop
async def geofencing_monitor(reminder, target_location, interval=60):
    while True:
        await set_geofencing_alert(reminder, target_location)
        await asyncio.sleep(interval)

# Example store location (replace this with a real location if necessary)
store_location = {"name": "Local Grocery Store", "lat": 40.713776, "lng": -74.006974}

# Main function for the assistant
async def main():
    await speak_async("Welcome! How can I assist you today?")
    
    while True:
        command = await voice_to_text_async()
        
        if command:
            if "nearby" in command.lower() and any(service in command.lower() for service in ["restaurant", "gas station", "hospital", "ATM"]):
                service_type = None
                if "restaurant" in command.lower():
                    service_type = "restaurant"
                elif "gas station" in command.lower():
                    service_type = "gas_station"
                elif "hospital" in command.lower():
                    service_type = "hospital"
                elif "ATM" in command.lower():
                    service_type = "atm"
                
                if service_type:
                    await get_nearby_services(service_type)
            
            elif "remind me" in command.lower() and "near store" in command.lower():
                await speak_async("Starting geofencing reminder for store.")
                asyncio.create_task(geofencing_monitor("pick up groceries", store_location))
            
            elif "exit" in command.lower():
                await speak_async("Goodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())
