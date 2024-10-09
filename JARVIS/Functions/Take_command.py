import speech_recognition as sr

def take_command():
    recognizer = sr.Recognizer()  # Initialize recognizer
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            voice = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Limit listen time
            
            try:
                command = recognizer.recognize_google(voice)  # Convert speech to text
                command = command.lower()
                print(f"User said: {command}")
                return command
            
            except sr.UnknownValueError:
                # Handles when speech is not understood
                print("Sorry, I couldn't understand that.")
                return None
            
            except sr.RequestError as e:
                # Handles any errors related to Google's API
                print(f"API request error: {e}")
                return None
    
    except sr.WaitTimeoutError:
        # Handles the case when no speech is detected within the timeout
        print("No speech detected. Please try again.")
        return None
