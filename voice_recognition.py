import speech_recognition as sr

def recognize_speech(timeout=2, phrase_time_limit=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")
        return "None"
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except sr.RequestError:
        print("Could not request results; check your network connection")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"
    
    return query.lower()
