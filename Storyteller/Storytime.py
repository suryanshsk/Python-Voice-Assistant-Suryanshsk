import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.stories = self.fetch_stories()  # Fetch stories from an external API or website

    def fetch_stories(self):
        api_url = "https://api.example.com/stories"  # Replace with actual API URL
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return {str(i + 1): story['text'] for i, story in enumerate(response.json())}
            else:
                print("Failed to fetch stories from API. Trying to scrape a website.")
                return self.scrape_stories()  # Fallback to web scraping
        except Exception as e:
            print(f"An error occurred while fetching from API: {e}")
            return self.scrape_stories()  # Fallback to web scraping

    def scrape_stories(self):
        url = "https://www.example.com/stories"  # Replace with actual website URL
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            stories = {}
            for idx, story in enumerate(soup.find_all('div', class_='story-class')):  # Adjust class based on actual HTML structure
                stories[str(idx + 1)] = story.get_text(strip=True)
            return stories
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            return self.default_stories()  # Fallback to default stories

    def default_stories(self):
        return {
            "1": "The Tortoise and the Hare: A story about a race between a slow tortoise and a fast hare.",
            "2": "The Lion and the Mouse: A tale showing that even the smallest creature can help the mightiest.",
            "3": "Cinderella: A story about kindness, resilience, and finding happiness.",
            "4": "The Three Little Pigs: A tale about three pigs who build houses to protect themselves from a wolf.",
            "5": "Goldilocks and the Three Bears: A curious girl explores the home of three bears."
        }

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
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                return None

    def tell_story(self, story_choice):
        story = self.stories.get(story_choice, "I don't have a story for that choice.")
        self.speak(story)

    def run(self):
        self.speak("Hello! I can tell you stories. Say 'tell a story' to start.")
        while True:
            command = self.listen()
            if command:
                if "tell a story" in command:
                    self.speak("Great! Here are the stories you can choose from:")
                    for key, value in self.stories.items():
                        self.speak(f"Say {key} for {value[:30]}...")  # Preview story
                    choice = self.listen()
                    if choice in self.stories.keys():
                        self.tell_story(choice)
                    else:
                        self.speak("I didn't recognize that choice. Please try again.")
                elif "stop" in command:
                    self.speak("Goodbye! Have a great day!")
                    break

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
