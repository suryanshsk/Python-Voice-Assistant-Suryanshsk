from new_weather_info import (
    get_weather, 
    get_weather_forecast, 
    get_weather_alerts, 
    save_favourite_city, 
    get_favourite_cities
)

def print_test_result(test_name, result, expected=None):
    """Utility function to print test results in a structured format."""
    print(f"\n--- {test_name} ---")
    if expected is not None:
        print(f"Expected: {expected}")
    print(f"Result: {result}")
    if isinstance(result, list):
        print(f"Number of items: {len(result)}")
    print("-" * 30)

def test_all_features():
    city_name = "Chennai"
    unit = "metric"
    chennai_coords = (13.0827, 80.2707)  # Correct coordinates for Chennai

    # Testing Current Weather
    try:
        print(f"Testing Current Weather of {city_name}")
        current_weather = get_weather(city_name, unit)
        print_test_result("Current Weather", current_weather, expected="Weather data with temperature.")
        assert 'temperature' in current_weather, "Current weather does not contain temperature data."
    except Exception as e:
        print(f"Error occurred while testing current weather: {e}")

    # Testing 5-Day Forecast
    try:
        print("\nTesting 5-Day Forecast:")
        forecast = get_weather_forecast(city_name, unit)
        print_test_result("5-Day Forecast", forecast, expected="List of 5 daily forecasts.")
        assert len(forecast) == 5, "Forecast does not contain 5 days of data."
    except Exception as e:
        print(f"Error occurred while testing 5-day forecast: {e}")

    # Testing Weather Alerts
    try:
        print("\nTesting Weather Alerts:")
        alerts = get_weather_alerts(*chennai_coords)
        print_test_result("Weather Alerts", alerts, expected="List of weather alerts.")
        assert isinstance(alerts, list), "Weather alerts should be a list."
    except Exception as e:
        print(f"Error occurred while testing weather alerts: {e}")

    # Testing Saving Favorite City
    try:
        print("\nTesting Saving Favorite City:")
        save_result = save_favourite_city(city_name)
        print_test_result("Saving Favorite City", save_result, expected=True)
        assert save_result is True, "Failed to save favorite city."
    except Exception as e:
        print(f"Error occurred while testing saving favorite city: {e}")

    # Testing Retrieving Favorite Cities
    try:
        print("\nTesting Retrieving Favorite Cities:")
        favourite_cities = get_favourite_cities()
        print_test_result("Retrieving Favorite Cities", favourite_cities, expected="List of favorite cities.")
        assert isinstance(favourite_cities, list), "Favorite cities should be a list."
    except Exception as e:
        print(f"Error occurred while testing retrieving favorite cities: {e}")

if __name__ == "__main__":
    test_all_features()
