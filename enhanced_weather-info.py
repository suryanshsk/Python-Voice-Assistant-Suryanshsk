import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

VALID_UNITS = {"metric": "°C", "imperial": "°F", "kelvin": "K"}
DEFAULT_UNIT = "kelvin"

def kelvin_to_celsius(kelvin_temp):
    """Converts Kelvin to Celsius."""
    return kelvin_temp - 273.15

def get_weather(city_name, units="kelvin"):
    if not city_name.strip():
        return "Please provide a valid city name."
    
    if not API_KEY:
        return "API key not found. Please set the environment variable 'OPENWEATHER_API_KEY'."
    
    # Validate the unit; fallback to 'kelvin' if invalid
    if units not in VALID_UNITS:
        return f"Invalid units. Please choose from {', '.join(VALID_UNITS.keys())}."

    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={units}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if data["cod"] != 200:
            # Use API error message if available
            return f"Error: {data.get('message', 'An error occurred.')}"

        temp_kelvin = data["main"]["temp"]
        description = data["weather"][0]["description"]
        unit_symbol = VALID_UNITS.get(units, "K")

        # If units are 'kelvin', convert to Celsius manually
        if units == "kelvin":
            temp_celsius = kelvin_to_celsius(temp_kelvin)
            output = (
                f"City: {city_name.title()}\n"
                f"Temperature: {temp_kelvin:.2f}K (or {temp_celsius:.2f}°C)\n"
                f"Weather: {description.title()}\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind Speed: {data['wind']['speed']} m/s"
            )
        else:
            output = (
                f"City: {city_name.title()}\n"
                f"Temperature: {temp_kelvin:.2f}{unit_symbol}\n"
                f"Weather: {description.title()}\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind Speed: {data['wind']['speed']} m/s"
            )

        return output

    except requests.ConnectionError:
        return "Error: Unable to connect to the weather service."
    except requests.Timeout:
        return "Error: The request timed out."
    except requests.RequestException as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    unit = input("Units (metric/imperial/kelvin): ").strip().lower() or DEFAULT_UNIT
    print(get_weather(city, unit))
