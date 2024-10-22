import os
import requests
import google.generativeai as genai
import pyttsx3 as p

# Set up API credentials
os.environ['GOOGLE_API_KEY'] = "your_gemini_api_key"  
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 
genai.configure(api_key=GOOGLE_API_KEY)

OPENWEATHERMAP_API_KEY = "your_weather_api_key"

# Initialize text-to-speech engine
engine = p.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_location():
    try:
        response = requests.get('http://ipinfo.io/json')
        data = response.json()
        city = data.get('city', 'Unknown city')
        return city
    except Exception as e:
        return f"Unable to fetch location data. Error: {str(e)}"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."
        else:
            return f"Unable to fetch weather data for {city}. Error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"An error occurred while fetching weather data: {str(e)}"

def generate_text(prompt):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(f'as a good weather reporter, first give the weather in the city and then recommend whether it is safe to go out and what kind of clothes can be worn from the given input: "{prompt}". Do not use bold words or asterisks in output. Provide the output in sentences.')
        text = response.text
        print(text)
        speak(text)
    except Exception as e:
        print(f"An error occurred while generating text: {str(e)}")

if __name__ == "__main__":
    city =  get_location()
    weather_info = get_weather(city)
    generate_text(weather_info)
