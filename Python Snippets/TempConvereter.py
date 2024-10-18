import speech_recognition as sr
import pyttsx3

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def celsius_to_kelvin(c):
    return c + 273

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def fahrenheit_to_kelvin(f):
    c = fahrenheit_to_celsius(f)
    return celsius_to_kelvin(c)

def kelvin_to_celsius(k):
    return k - 273

def kelvin_to_fahrenheit(k):
    c = kelvin_to_celsius(k)
    return celsius_to_fahrenheit(c)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech(timeout=2, phrase_time_limit=5, language='en-in'):
    recognizer = sr.Recognizer()
    
    print("Adjusting for ambient noise...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return "None"
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language=language)
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio. Please try again.")
        return "None"
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

    return query.lower()

def retry_recognition(attempts=3):
    for _ in range(attempts):
        result = recognize_speech()
        if result != "None":
            return result
    print("Failed to recognize speech after multiple attempts.")
    return None

def main():
    speak("Welcome to the Temperature Converter.")

    speak("Please say the temperature value.")
    temp = retry_recognition()
    
    try:
        temp = float(temp)  # Convert the recognized value to float
        speak(f"You entered {temp} degrees.")
    except ValueError:
        speak("I could not understand the temperature value. Please try again.")
        return

    speak("Choose the original unit:")
    speak("Say Celsius, Fahrenheit, or Kelvin.")

    choice = retry_recognition()

    if "celsius" in choice:
        fahrenheit = celsius_to_fahrenheit(temp)
        kelvin = celsius_to_kelvin(temp)
        speak(f"{temp} degrees Celsius is {fahrenheit:.2f} degrees Fahrenheit.")
        speak(f"{temp} degrees Celsius is {kelvin:.2f} Kelvin.")
        
    elif "fahrenheit" in choice:
        celsius = fahrenheit_to_celsius(temp)
        kelvin = fahrenheit_to_kelvin(temp)
        speak(f"{temp} degrees Fahrenheit is {celsius:.2f} degrees Celsius.")
        speak(f"{temp} degrees Fahrenheit is {kelvin:.2f} Kelvin.")
        
    elif "kelvin" in choice:
        celsius = kelvin_to_celsius(temp)
        fahrenheit = kelvin_to_fahrenheit(temp)
        speak(f"{temp} Kelvin is {celsius:.2f} degrees Celsius.")
        speak(f"{temp} Kelvin is {fahrenheit:.2f} degrees Fahrenheit.")
        
    else:
        speak("Invalid choice! Please say Celsius, Fahrenheit, or Kelvin.")

if __name__ == "__main__":
    main()
