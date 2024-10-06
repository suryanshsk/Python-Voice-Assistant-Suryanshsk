import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city_name, units="metric"):
    if not city_name.strip(): return "Please provide a valid city name."
    if not API_KEY: return "API key not found."

    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={units}"
    
    try:
        data = requests.get(url).json()
        if data["cod"] != 200:
            return {"404": "City not found.", "401": "Invalid API key.", "429": "Too many requests."}.get(str(data["cod"]), "Error occurred.")
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        unit_symbol = {"metric": "°C", "imperial": "°F"}.get(units, "K")
        
        return f"Temperature: {temp:.2f}{unit_symbol}\nDescription: {description}"
    
    except requests.RequestException as e:
        return f"Error retrieving data: {e}"

if __name__ == "__main__":
    city = input("Enter city name: ")
    unit = input("Units (metric/imperial/leave empty for Kelvin): ").strip() or None
    print(get_weather(city, unit))
