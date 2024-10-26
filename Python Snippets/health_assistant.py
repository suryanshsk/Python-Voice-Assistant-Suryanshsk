import time
from datetime import datetime
from colorama import Fore, init
import requests
import threading

init(autoreset=True)


SPOONACULAR_API_KEY = 'YOUR_API_KEY'
EDAMAM_APP_ID = 'YOUR_APP_ID'
EDAMAM_APP_KEY = 'YOUR_API_KEY'


user_profile = {
    'Name': None,
    'age': None,
    'height': None,  
    'weight': None,  
    'gender': None,
    'activity_level': None,  
    'caloric_intake_goal': None,
    'water_goal': None,  
    'daily_water_intake': 0,  
    'logged_calories': 0,
    'logged_macros': {'protein': 0, 'fat': 0, 'carbs': 0},  
    'wake_up_time': None,
    'sleep_time': None,
    'water_interval': None,
}

def calorie_intake():
    if user_profile['gender'] == 'male':
        bmr = 88.362 + (13.397 * user_profile['weight']) + (4.799 * user_profile['height']) - (5.677 * user_profile['age'])
    else:
        bmr = 447.593 + (9.247 * user_profile['weight']) + (3.098 * user_profile['height']) - (4.330 * user_profile['age'])
    
    activity_factors = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'active': 1.55,
        'very_active': 1.725
    }
    
    user_profile['caloric_intake_goal'] = bmr * activity_factors[user_profile['activity_level']]
    print(Fore.GREEN + f"🥗 Your daily caloric intake goal: {user_profile['caloric_intake_goal']:.2f} calories.")

def log_calorie_intake(food_name, calories, protein, fat, carbs):
    
    user_profile['logged_calories'] += calories
    user_profile['logged_macros']['protein'] += protein
    user_profile['logged_macros']['fat'] += fat
    user_profile['logged_macros']['carbs'] += carbs
    print(Fore.CYAN + f"📦 {food_name} logged with {calories} calories (Protein: {protein}g, Fat: {fat}g, Carbs: {carbs}g).")
    print(Fore.MAGENTA + f"🔢 Total calories today: {user_profile['logged_calories']}")

def meal_plan():
    
    api_url = f"https://api.spoonacular.com/mealplanner/generate?apiKey={SPOONACULAR_API_KEY}&timeFrame=day&targetCalories={int(user_profile['caloric_intake_goal'])}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        meal_plan = response.json()
        print(Fore.LIGHTGREEN_EX + "🍽️ Spoonacular Meal Plan: ")
        for meal in meal_plan['meals']:
            print(Fore.LIGHTYELLOW_EX + f"🕒 Meal: {meal['title']}, Ready in {meal['readyInMinutes']} minutes. Source: {meal['sourceUrl']}")
    else:
        print(Fore.RED + '🚫 Error in fetching the meal plan.')

def fetch_nutrition(food_item):
    
    api_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food_item}&json=true"

    response = requests.get(api_url)

    if response.status_code == 200:
        nutrition_data = response.json()
        
        if nutrition_data['products']:
            product = nutrition_data['products'][0]  
            calories = product.get('nutriments', {}).get('energy-kcal', 'N/A')
            protein = product.get('nutriments', {}).get('proteins', 'N/A')
            fat = product.get('nutriments', {}).get('fat', 'N/A')
            carbs = product.get('nutriments', {}).get('carbohydrates', 'N/A')

            print(Fore.LIGHTGREEN_EX + f"📊 {product.get('product_name', food_item).capitalize()} Nutrition: Calories: {calories}, Protein: {protein}g, Fat: {fat}g, Carbs: {carbs}g")

            return {
                'calories': calories,
                'protein': protein,
                'fat': fat,
                'carbs': carbs
            }
        else:
            print(Fore.RED + "❌ No nutrition data found for the item by name.")
            barcode = input("🔍 Enter the barcode (or leave blank to skip): ")
            if barcode:
                return fetch_nutrition_by_barcode(barcode)  # New function to handle barcode lookup
            return None
    else:
        print(Fore.RED + f"🚫 Error fetching nutrition data from Open Food Facts: {response.status_code}")
        return None

def fetch_nutrition_by_barcode(barcode):
    api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(api_url)

    if response.status_code == 200:
        nutrition_data = response.json()
        
        if 'product' in nutrition_data:
            product = nutrition_data['product']
            calories = product.get('nutriments', {}).get('energy-kcal', 'N/A')
            protein = product.get('nutriments', {}).get('proteins', 'N/A')
            fat = product.get('nutriments', {}).get('fat', 'N/A')
            carbs = product.get('nutriments', {}).get('carbohydrates', 'N/A')

            print(Fore.LIGHTGREEN_EX + f"📦 {product.get('product_name', barcode).capitalize()} Nutrition: Calories: {calories}, Protein: {protein}g, Fat: {fat}g, Carbs: {carbs}g")

            return {
                'calories': calories,
                'protein': protein,
                'fat': fat,
                'carbs': carbs
            }
        else:
            print(Fore.RED + "❌ No product found with the provided barcode.")
            print(Fore.YELLOW + f"🔍 Please verify the barcode: {barcode}.")  
            return None
    else:
        print(Fore.RED + f"🚫 Error fetching nutrition data from Open Food Facts: {response.status_code}")
        return None

def log_water_intake(liters):
    user_profile['daily_water_intake'] += liters
    print(Fore.BLUE + f"💧 {liters}L water logged. Total water intake today: {user_profile['daily_water_intake']}L")

def suggest_diet():
    if user_profile['age'] <= 18:
        diet_plan = "Focus on high protein foods like dairy, lean meats, and whole grains."
    elif 19 <= user_profile['age'] <= 50:
        diet_plan = "Balance your diet with carbohydrates, proteins, and healthy fats."
    else:
        diet_plan = "Ensure sufficient intake of calcium, vitamin D, and fiber."
        
    print(Fore.LIGHTGREEN_EX + f"🍏 Diet Suggestion: {diet_plan}")

def water_reminder():
    
    while True: 
        current_time = datetime.now().strftime("%H:%M")
        print(Fore.YELLOW + f"⏰ Checking time: {current_time}")  
        if user_profile['wake_up_time'] <= current_time <= user_profile['sleep_time']:
            print(Fore.YELLOW + "💦 Reminder: Time to drink water!")
            time.sleep(user_profile['water_interval'] * 60)
        else:
            break

def daily_summary():
    
    print(Fore.LIGHTMAGENTA_EX + "\n---- DAILY SUMMARY ----")
    print(Fore.LIGHTBLUE_EX + f"🔢 Total calories: {user_profile['logged_calories']} / {user_profile['caloric_intake_goal']:.2f}")
    print(Fore.LIGHTBLUE_EX + f"💧 Total water intake: {user_profile['daily_water_intake']}L / {user_profile['water_goal']}L")
    print(Fore.LIGHTBLUE_EX + f"🥗 Macronutrients: Protein: {user_profile['logged_macros']['protein']}g, Fat: {user_profile['logged_macros']['fat']}g, Carbs: {user_profile['logged_macros']['carbs']}g")

def setup_user_profile():
    
    print(Fore.LIGHTGREEN_EX + "Hello! I'm your health assistant.")
    user_profile['Name'] = input("👤 Enter your name: ")
    user_profile['age'] = int(input("🎂 Enter your age: "))
    user_profile['height'] = int(input("📏 Enter your height (in cm): "))
    user_profile['weight'] = int(input("⚖️ Enter your weight (in kg): "))
    user_profile['gender'] = input("🚻 Enter your gender (male/female): ").lower()
    user_profile['activity_level'] = input("🏃‍♂️ Enter your activity level (sedentary/lightly_active/active/very_active): ").lower()
    user_profile['water_goal'] = float(input("💧 Enter your daily water goal (in liters): "))
    user_profile['wake_up_time'] = input("🕖 Enter your wake-up time (HH:MM): ")
    user_profile['sleep_time'] = input("🕙 Enter your sleep time (HH:MM): ")
    user_profile['water_interval'] = int(input("⏲️ Enter your water reminder interval (in minutes): "))

    calorie_intake()
    print(Fore.GREEN + "🎉 Profile set up successfully!")

def main_menu():
    
    while True:
        print(Fore.LIGHTCYAN_EX + "\n==== Health Assistant Menu ====")
        print(Fore.YELLOW + "1. Log Food")
        print(Fore.YELLOW + "2. Meal Plan")
        print(Fore.YELLOW + "3. Water Intake Log")
        print(Fore.YELLOW + "4. Daily Summary")
        print(Fore.YELLOW + "5. Diet Suggestion")
        print(Fore.YELLOW + "6. Exit")

        choice = input(Fore.LIGHTWHITE_EX + "👉 Choose an option: ")

        if choice == '1':
            food_name = input("🍔 Enter the food name: ")
            nutrition_data = fetch_nutrition(food_name)
            if nutrition_data:
                log_calorie_intake(food_name, nutrition_data['calories'], nutrition_data['protein'], nutrition_data['fat'], nutrition_data['carbs'])

        elif choice == '2':
            meal_plan()

        elif choice == '3':
            liters = float(input("💧 Enter the amount of water consumed (in liters): "))
            log_water_intake(liters)

        elif choice == '4':
            daily_summary()

        elif choice == '5':
            suggest_diet()

        elif choice == '6':
            print(Fore.GREEN + "👋 Thank you for using the Health Assistant. Goodbye!")
            break

        else:
            print(Fore.RED + "❌ Invalid choice, please try again.")

if __name__ == "__main__":
    
    setup_user_profile()
    threading.Thread(target=water_reminder, daemon=True).start()  # Start water reminder in a separate thread
    main_menu()


