import requests
import json
import logging
from datetime import datetime, timedelta
from email_sender import send_bulk_email


API_KEY = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key
import requests
import json
import logging
from datetime import datetime

API_KEY = 'YOUR_API_KEY'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"
ONE_CALL_URL = "http://api.openweathermap.org/data/2.5/onecall?"
FAVOURITE_CITIES_FILE = "favourite_cities.json"
DAILY_WEATHER_FILE = "daily_weather.json"

logging.basicConfig(filename="weather_info.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_api_call(city_name, response):
    if response.status_code == 200:
        logging.info(f"Successfully fetched weather for {city_name}")
    else:
        logging.error(f"Failed to fetch weather for {city_name}: {response.status_code} {response.text}")

def get_weather(city_name, unit="metric"):
    try:
        unit_param = {"metric": "°C", "imperial": "°F", "kelvin": "K"}
        complete_url = BASE_URL + f"q={city_name}&units={unit}&appid=" + API_KEY
        response = requests.get(complete_url)
        log_api_call(city_name, response)

        data = response.json()
        if response.status_code != 200:
            return None, f"Error: {data.get('message', 'Unable to retrieve weather data.')}"

        if data["cod"] == "404":
            return None, "City not found. Please check the city name."

        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        
        weather_info = {
            "temperature": f"{temperature:.2f}{unit_param[unit]}",
            "description": weather_description,
            "humidity": humidity,
            "pressure": pressure
        }

        save_daily_weather(city_name, weather_info)

        return weather_info, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return None, f"Error: Unable to fetch data. {str(e)}"

def save_daily_weather(city_name, weather_info):
    today = datetime.now().strftime('%Y-%m-%d')
    daily_data = {
        "city": city_name,
        "date": today,
        "weather_info": weather_info
    }

    try:
        with open(DAILY_WEATHER_FILE, 'r+') as file:
            weather_data = json.load(file)
            weather_data.append(daily_data)
            file.seek(0)
            json.dump(weather_data, file)
    except FileNotFoundError:
        with open(DAILY_WEATHER_FILE, 'w') as file:
            json.dump([daily_data], file)



def send_weather_alerts(email_settings):
    for city_name in email_settings['cities']:
        weather_info, error = get_weather(city_name)
        if error:
            continue
        
        subject = f"Weather Update for {city_name}"
        body_lines = [f"Hello,\n\nHere is the latest weather information for {city_name}:"]
        
        if email_settings['send_temperature']:
            body_lines.append(f"Temperature: {weather_info['temperature']}")
        if email_settings['send_humidity']:
            body_lines.append(f"Humidity: {weather_info['humidity']}%")
        if email_settings['send_pressure']:
            body_lines.append(f"Pressure: {weather_info['pressure']} hPa")
        if email_settings['send_description']:
            body_lines.append(f"Description: {weather_info['description']}")
        
        body = "\n".join(body_lines) + "\n\nBest Regards,\nWeather Alert System"
        send_bulk_email(email_settings['gmail_user'], email_settings['gmail_password'], email_settings['recipients'], subject, body)

def get_weather_forecast(city_name):
    complete_url = FORECAST_URL + "q=" + city_name + "&appid=" + API_KEY + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        forecast_list = data["list"]
        forecast_info = []
        for forecast in forecast_list[::8]:  
            date = forecast["dt_txt"].split(" ")[0]  
            temperature = forecast["main"]["temp"]  
            description = forecast["weather"][0]["description"]
            forecast_info.append(f"{date} - Temperature: {temperature:.2f}°C, Description: {description}")
        return "\n".join(forecast_info)
    else:
        return "City not found"

def get_weather_alerts(lat, lon):
    complete_url = ONE_CALL_URL + f"lat={lat}&lon={lon}&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()
    
    if "alerts" in data:
        alerts = data["alerts"]
        alert_info = []
        for alert in alerts:
            event = alert["event"]
            description = alert["description"]
            start = alert["start"]
            end = alert["end"]
            alert_info.append(f"Alert: {event}\nDescription: {description}\nStart: {start}\nEnd: {end}")
        return "\n".join(alert_info)
    else:
        return "No weather alerts"

def save_favourite_city(city_name):
    try:
        with open(FAVOURITE_CITIES_FILE, 'r+') as file:
            cities = json.load(file)
            if city_name not in cities:
                cities.append(city_name)
                file.seek(0)
                json.dump(cities, file)
        return "City added to favourites"
    except FileNotFoundError:
        with open(FAVOURITE_CITIES_FILE, 'w') as file:
            json.dump([city_name], file)
        return "Favourites file created and city added"

def get_favourite_cities():
    try:
        with open(FAVOURITE_CITIES_FILE, 'r') as file:
            cities = json.load(file)
        return cities
    except FileNotFoundError:
        return "No favourite cities saved"

email_settings = {
    'gmail_user': 'your_email@gmail.com',
    'gmail_password': 'your_email_password',
    'recipients': ['recipient1@example.com', 'recipient2@example.com'],
    'cities': ['New York', 'Los Angeles'],
    'send_temperature': True,
    'send_humidity': True,
    'send_pressure': True,
    'send_description': True
}

if __name__ == "__main__":
    send_weather_alerts(email_settings)
