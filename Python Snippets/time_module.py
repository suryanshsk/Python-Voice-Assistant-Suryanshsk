import datetime
import pytz
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    """This function takes the text as input and converts it to speech."""
    engine.say(text)
    engine.runAndWait()

def tell_current_time_and_date(timezone='Asia/Kolkata'):
    """This function fetches and announces the current local time and date for the specified timezone."""
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz)
        current_time = local_time.strftime('%H:%M:%S')
        current_date = local_time.strftime('%Y-%m-%d')
        speak(f"The current time and date in {timezone} is {current_time} on {current_date}")
    except pytz.exceptions.UnknownTimezoneError:
        speak("Invalid timezone. Please try again with a valid timezone.")


if __name__ == "__main__":
    tell_current_time_and_date('Asia/Kolkata')
