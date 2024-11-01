import requests
import speech_recognition as sr
import pyttsx3

class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __str__(self):
        ingredients_list = "\n".join(self.ingredients)
        return (f"Recipe: {self.name}\n"
                f"Ingredients:\n{ingredients_list}\n"
                f"Instructions:\n{self.instructions}")

class RecipeBook:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def view_recipes(self):
        if not self.recipes:
            return "No recipes available."
        return "\n".join([f"{index + 1}. {recipe.name}" for index, recipe in enumerate(self.recipes)])

    def search_recipe(self, name):
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return str(recipe)
        return "Recipe not found."

    def fetch_recipes(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            recipes_data = response.json()
            for recipe_data in recipes_data:
                name = recipe_data['title']
                ingredients = recipe_data['ingredients']
                instructions = recipe_data['instructions']
                self.add_recipe(Recipe(name, ingredients, instructions))
            return "Recipes fetched successfully."
        except Exception as e:
            return f"Error fetching recipes: {e}"

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.recipe_book = RecipeBook()
        self.api_url = "https://api.example.com/recipes"  # Replace with actual API URL
        self.recipe_book.fetch_recipes(self.api_url)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                return None

    def run(self):
        self.speak("Welcome to the Recipe Book! You can say 'view recipes' to see the recipes, 'search for a recipe' to find a recipe, or 'exit' to quit.")
        while True:
            command = self.listen()
            if command:
                if "view recipes" in command:
                    recipes = self.recipe_book.view_recipes()
                    self.speak(recipes)
                elif "search for a recipe" in command:
                    self.speak("What recipe do you want to search for?")
                    recipe_name = self.listen()
                    if recipe_name:
                        result = self.recipe_book.search_recipe(recipe_name)
                        self.speak(result)
                elif "exit" in command:
                    self.speak("Goodbye! Have a great day!")
                    break
                else:
                    self.speak("I didn't recognize that command. Please try again.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
