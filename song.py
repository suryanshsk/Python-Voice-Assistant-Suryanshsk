import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to listen for voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you say it again?")
            speak("Sorry, I didn't catch that. Could you say it again?")
            return listen()  # Retry listening
        except sr.RequestError:
            print("I can't connect to the service. Please check your internet connection.")
            speak("I can't connect to the service. Please check your internet connection.")
            return ""

# Function to scrape song data
def scrape_songs():
    url = "https://www.billboard.com/charts/hot-100/"  # Billboard Hot 100 as an example
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    songs = []

    for item in soup.select(".o-chart-results-list-row-container"):
        title = item.select_one(".o-chart-results-list-row-container h3").get_text(strip=True)
        artist = item.select_one(".o-chart-results-list-row-container h3 + span").get_text(strip=True)
        songs.append({"title": title, "artist": artist})

    return songs

def play_quiz(songs):
    score = 0
    total_questions = len(songs)

    speak("Welcome to the song quiz! I'm excited to see how much you know about music.")

    for song in songs:
        question = f"Alright! Who is the artist of the song '{song['title']}'?"
        speak(question)
        print(question)

        answer = listen()

        if answer == song['artist'].lower():
            score += 1
            speak("That's correct! You're really good at this.")
        else:
            speak(f"Oops! The correct answer is {song['artist']}. Don't worry, let's keep going!")

    speak(f"Great job! You scored {score} out of {total_questions}.")
    if score == total_questions:
        speak("Perfect score! You're a music genius!")
    elif score > total_questions / 2:
        speak("Not bad! You really know your stuff!")
    else:
        speak("Keep practicing, and you'll get better!")

if __name__ == "__main__":
    songs = scrape_songs()
    random.shuffle(songs)  # Shuffle songs for randomness
    play_quiz(songs[:5])  # Limit to the first 5 songs for the quiz
