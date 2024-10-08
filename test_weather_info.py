from weather_info import (
    get_weather, 
    get_weather_forecast, 
    weather_alerts, 
    save_favourite_city, 
    get_favourite_cities,
    remove_favourite_city
)

def test_all_features():
    city_name = "Jaipur" 
    unit = "metric"  

    
    print("Testing Current Weather:")
    print(get_weather(city_name, unit))

    
    print("\nTesting 5-Day Forecast:")
    print(get_weather_forecast(city_name))

   
    print("\nTesting Weather Alerts:")
    print(weather_alerts(26.4499, 80.3319))  

   
    print("\nTesting Saving Favorite City:")
    print(save_favourite_city(city_name))
    
    print("\nTesting Removing Favorite City:")
    print(remove_favourite_city(city_name))
   
    print("\nTesting Retrieving Favorite Cities:")
    print(get_favourite_cities())

if __name__ == "__main__":
    test_all_features()
