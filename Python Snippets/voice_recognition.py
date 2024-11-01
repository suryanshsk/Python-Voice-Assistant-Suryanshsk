import speech_recognition as sr

def recognize_speech(timeout=2, phrase_time_limit=5):
    recognizer = sr.Recognizer()

    # Try to open microphone and listen for speech
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source)
            
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")
        return "None"
    except Exception as e:
        print(f"Error accessing the microphone: {e}")
        return "None"

    # Try recognizing speech using Google Speech Recognition
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        
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

# Test the function
if __name__ == "__main__":
    recognize_speech()
 
