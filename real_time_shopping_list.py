mport speech_recognition as sr
import pyttsx3
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
shopping_list = []

# Function to recognize speech and return text
def recognize_speech():
with sr.Microphone() as source:
print("Listening...")
audio = recognizer.listen(source)
try:
            text = recognizer.recognize_google(audio)
            return text.lower()  # Standardize by returning lowercased input
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Service is unavailable."

# Function to speak text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to add an item to the shopping list
def add_to_shopping_list(item):
    shopping_list.append(item)
    speak_text(f"{item} has been added to your shopping list.")
    print(f"Shopping list: {shopping_list}")  # For debugging

# Function to ask for more items
def ask_for_more_items():
    speak_text("Would you like to add another item?")
    response = recognize_speech()
    if 'yes' in response:
        ask_for_item()
    elif 'no' in response:
        speak_text("Okay. Would you like to view your shopping list?")
        response = recognize_speech()
        if 'yes' in response:
            view_shopping_list()
        else:
            speak_text("All right.")
    else:
        speak_text("I didn't understand that. Please say yes or no.")
        ask_for_more_items()

# Function to ask the user what item to add
def ask_for_item():
    speak_text("What would you like to add to your shopping list?")
    item = recognize_speech()
    if item:
        add_to_shopping_list(item)
        ask_for_more_items()

# Function to view the shopping list
def view_shopping_list():
    if shopping_list:
        speak_text("Your shopping list includes:")
        for item in shopping_list:
            speak_text(item)
    else:
        speak_text("Your shopping list is empty.")


def main():
    speak_text("Hello, would you like to create a shopping list?")
    response = recognize_speech()
    if 'yes' in response:
        ask_for_item()
    else:
        speak_text("Okay, let me know if you need help.")

if __name__ == "__main__":
main()
