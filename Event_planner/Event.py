import speech_recognition as sr
import pyttsx3
import datetime
import json
import os
from dateutil import parser

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.events = self.load_events()

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
                self.speak("Sorry, I did not understand that.")
                return ""
            except sr.RequestError:
                self.speak("Could not request results from the service.")
                return ""

    def load_events(self):
        if os.path.exists('events.json'):
            with open('events.json', 'r') as file:
                return json.load(file)
        return []

    def save_events(self):
        with open('events.json', 'w') as file:
            json.dump(self.events, file)

    def add_event(self, event_name, event_date):
        self.events.append({'name': event_name, 'date': event_date})
        self.save_events()
        self.speak(f"Event '{event_name}' added for {event_date}.")

    def list_events(self):
        if not self.events:
            self.speak("No events found.")
            return
        self.speak("Here are your upcoming events:")
        for event in self.events:
            self.speak(f"{event['name']} on {event['date']}")

    def exit_assistant(self):
        self.speak("Are you sure you want to exit? Say yes to confirm or no to continue.")
        command = self.listen()
        if "yes" in command:
            self.speak("Goodbye!")
            return True
        else:
            self.speak("Continuing to assist you.")
            return False

    def run(self):
        self.speak("Welcome to your event planner!")
        while True:
            command = self.listen()

            if "add event" in command:
                self.speak("What is the name of the event?")
                event_name = self.listen()
                self.speak("When is the event? Please say the date.")
                event_date = self.listen()

                try:
                    parsed_date = parser.parse(event_date)
                    formatted_date = parsed_date.strftime('%d %B %Y')
                    self.add_event(event_name, formatted_date)
                except (ValueError, TypeError):
                    self.speak("Sorry, I couldn't understand the date format. Please try again.")

            elif "list events" in command:
                self.list_events()

            elif "exit" in command:
                if self.exit_assistant():
                    break

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()