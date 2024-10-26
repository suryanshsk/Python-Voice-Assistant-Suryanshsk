import speech_recognition as sr

def recognize_speech(timeout=2, phrase_time_limit=5, language='en-in'):
    recognizer = sr.Recognizer()
    
    # Inform user that the system is ready to listen
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
