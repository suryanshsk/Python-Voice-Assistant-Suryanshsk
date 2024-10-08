import datetime
import webbrowser
import pywhatkit
import wikipedia
from Functions.greet import greet_user
from Functions.talk import talk
from Functions.Take_command import take_command
from Functions.screenshot import take_screenshot
from Functions.application import open_application
def run_jarvis():
    while True:
        command = take_command()
        if command is None:
            continue
        elif 'activate' in command:
            talk("initializing jarvis")
            greet_user
            talk("how are you")
        elif 'launch' in command:
            open_application(command)
        elif 'open youtube' in command:
            talk("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in command:
            talk("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open facebook' in command:
            talk("Opening Facebook")
            webbrowser.open("https://www.facebook.com")

        elif 'open linkedin' in command:
            talk("Opening LinkedIn")
            webbrowser.open("https://www.linkedin.com")

        elif 'search google for' in command:
            search_query = command.replace('search google for', '')
            talk(f"Searching Google for {search_query}")
            pywhatkit.search(search_query)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {time}")

        elif 'tell me about' in command:
            topic = command.replace('tell me about', '')
            info = wikipedia.summary(topic, 1)
            talk(info)
        elif 'screenshot' in command:
            print("What should be the file name for the screenshot?")
            talk("What should be the file name for the screenshot?")
            file_name = take_command()  # Take voice input for the screenshot name
                
            if file_name:
                take_screenshot(file_name)  # Capture and save the screenshot
        elif 'exit' in command or 'stop' in command:
            talk("closing jarvis...")
            talk("take care")
            break

        else:
            talk("Sorry, I didn't understand. Please try again.")
