#install speech_recognition , pint and pyttsx3 libraries
#make sure there are no microphone or hardware issues

import speech_recognition as sr
import pyttsx3
import pint

# Initialize the unit registry from pint and TTS engine
unit_registry = pint.UnitRegistry()
engine = pyttsx3.init()

# Function to speak output using TTS
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert units using pint with better error handling
def convert_units(value, from_unit, to_unit):
    try:
        # Create a quantity from the value and original unit
        quantity = value * unit_registry(from_unit)
        # Convert the quantity to the target unit
        converted_quantity = quantity.to(to_unit)
        return converted_quantity
    except pint.errors.DimensionalityError:
        return f"Incompatible units: cannot convert {from_unit} to {to_unit}."
    except Exception as e:
        return f"Error: {e}"

# Function to capture voice commands and convert speech to text
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            # Convert speech to text using Google Web Speech API
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Sorry, the speech recognition service is not available."

# Function to process voice commands related to unit conversion
def process_conversion_command(command):
    # Simple string-based parsing for unit conversion commands
    # Example command: "Convert 10 meters to feet"
    try:
        # Normalize the command string
        command = command.lower().replace("convert", "").replace("to", "").strip()
        words = command.split()

        # Check if the command contains the necessary components
        if len(words) < 3:
            speak("Sorry, the command format should be: convert [value] [from_unit] to [to_unit].")
            return

        # Parse the value and units from the command
        try:
            value = float(words[0])
        except ValueError:
            speak("The value to convert must be a number.")
            return

        from_unit = words[1]
        to_unit = words[2]

        # Perform the unit conversion
        result = convert_units(value, from_unit, to_unit)
        if isinstance(result, str):
            speak(result)  # Handle any error messages from the conversion
        else:
            speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
    except Exception as e:
        speak(f"An error occurred while processing your command: {e}")

# Main function to trigger the voice assistant
if __name__ == "__main__":
    speak("Hello! I'm your assistant. How can I help you with unit conversions?")
    
    while True:
        command = voice_to_text()
        print(f"Command received: {command}")
        
        if "exit" in command.lower() or "stop" in command.lower():
            speak("Goodbye!")
            break
        elif "convert" in command.lower():
            process_conversion_command(command)
        else:
            speak("Please give a command to convert units or say 'exit' to stop.")
