import os
import requests

API_KEY = os.getenv('OPENWEATHER_API_KEY') or input("Please enter your OpenWeather API key: ").strip()
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def validate_units(units):
    """Validate and return appropriate units for the weather data."""
    valid_units = {"metric": "°C", "imperial": "°F", "kelvin": "K"}
    return valid_units.get(units.lower(), "K")  # Default to Kelvin if units are invalid

def get_weather(city_name, units="metric"):
    """Fetch weather data for the provided city and display it in the selected units."""
    city_name = city_name.strip()
    if not city_name:
        return "Please provide a valid city name."
    
    if not API_KEY:
        return "API key not found. Please set the 'OPENWEATHER_API_KEY' environment variable."

    # Prepare the API URL
    units = units or "kelvin"
    unit_symbol = validate_units(units)
    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={units}"

    try:
        # Make the request to the OpenWeather API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        if data["cod"] != 200:
            error_messages = {
                "404": "City not found.",
                "401": "Invalid API key.",
                "429": "Too many requests. Please try again later."
            }
            return error_messages.get(str(data["cod"]), f"Error: {data.get('message', 'Unknown error occurred')}")

        # Extract weather details
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return f"Temperature: {temp:.2f}{unit_symbol}\nDescription: {description.capitalize()}"

    except requests.exceptions.RequestException as e:
        return f"Network error: Unable to retrieve data. Details: {e}"

    except ValueError:
        return "Error: Unable to parse response data. Please try again."

if __name__ == "__main__":
    while True:
        city = input("Enter city name (or type 'exit' to quit): ").strip()
        if city.lower() == 'exit':
            print("Goodbye!")
            break
        
        unit = input("Units (metric/imperial/kelvin, leave empty for Kelvin): ").strip() or None
        print(get_weather(city, unit))
