import requests
import json
import logging


logging.basicConfig(filename='weather_info.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

API_KEY = 'YOUR_API_KEY'  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"
ALERTS_URL = "http://api.openweathermap.org/data/2.5/onecall?"

FAVOURITES_FILE = 'favourite_cities.json'


def get_weather(city_name, unit="metric"):
    """Fetch current weather for a specific city with chosen unit (metric, imperial, kelvin)."""
    try:
        unit_param = {"metric": "°C", "imperial": "°F", "kelvin": "K"}
        complete_url = BASE_URL + f"q={city_name}&units={unit}&appid=" + API_KEY
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unable to retrieve weather data.')}"

        if data["cod"] == "404":
            return "City not found. Please check the city name."

        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        weather_info = f"Temperature: {temperature:.2f}{unit_param[unit]}\nDescription: {weather_description}"
        
        log_api_call(city_name, response)

        return weather_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return f"Error: Unable to fetch data. {str(e)}"


def get_5_day_forecast(city_name, unit="metric"):
    """Fetch 5-day weather forecast for a specific city."""
    try:
        complete_url = FORECAST_URL + f"q={city_name}&units={unit}&appid=" + API_KEY
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unable to retrieve weather data.')}"

        if data["cod"] == "404":
            return "City not found. Please check the city name."

        forecast_info = "5-Day Weather Forecast:\n"
        for forecast in data["list"]:
            dt_txt = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            forecast_info += f"{dt_txt}: {temp:.2f} {unit.capitalize()}, {description}\n"
        
        log_api_call(city_name, response)

        return forecast_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return f"Error: Unable to fetch forecast data. {str(e)}"


def get_weather_alerts(lat, lon):
    """Display any weather alerts for a specific city by geographic coordinates."""
    try:
        complete_url = ALERTS_URL + f"lat={lat}&lon={lon}&appid=" + API_KEY
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unable to retrieve weather alerts.')}"

        if "alerts" in data:
            alert_info = "Weather Alerts:\n"
            for alert in data["alerts"]:
                alert_info += f"{alert['event']} - {alert['description']}\n"
            return alert_info
        else:
            return "No weather alerts for this location."

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return f"Error: Unable to fetch alert data. {str(e)}"


def save_favourite_city(city_name):
    """Save a city to the list of favourite cities."""
    try:
        with open(FAVOURITES_FILE, 'r') as file:
            favourites = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        favourites = []

    if city_name not in favourites:
        favourites.append(city_name)
        with open(FAVOURITES_FILE, 'w') as file:
            json.dump(favourites, file)
        return f"{city_name} has been added to your favourites."
    else:
        return f"{city_name} is already in your favourites."


def remove_favourite_city(city_name):
    """Remove a city from the list of favourite cities."""
    try:
        with open(FAVOURITES_FILE, 'r') as file:
            favourites = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "No favourite cities found."

    if city_name in favourites:
        favourites.remove(city_name)
        with open(FAVOURITES_FILE, 'w') as file:
            json.dump(favourites, file)
        return f"{city_name} has been removed from your favourites."
    else:
        return f"{city_name} is not in your favourites."


def get_favourite_cities_weather(unit="metric"):
    """Get the weather for all favourite cities."""
    try:
        with open(FAVOURITES_FILE, 'r') as file:
            favourites = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "No favourite cities found."

    weather_info = "Weather for favourite cities:\n"
    for city in favourites:
        weather_info += get_weather(city, unit) + "\n"
    
    return weather_info


def log_api_call(city_name, response):
    logging.info(f"API call to {city_name}: {response.status_code}")


if __name__ == "__main__":
    print(get_weather("Kanpur"))
    print(get_5_day_forecast("Mumbai"))
    print(save_favourite_city("Mumbai"))
    print(get_favourite_cities_weather())
    print(remove_favourite_city("Mumbai"))
