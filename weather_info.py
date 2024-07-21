# weather_info.py
import requests

API_KEY = 'YOUR_API_KEY'  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city_name):
    complete_url = BASE_URL + "q=" + city_name + "&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"] - 273.15  # Convert from Kelvin to Celsius
        weather_info = f"Temperature: {temperature:.2f}°C\nDescription: {weather_description}"
    else:
        weather_info = "City not found"
    return weather_info
