import random
import requests
import speech_recognition as sr
import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

def fetch_debate_topics():
    # Hypothetical API endpoint
    url = "https://api.example.com/debate-topics"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Expecting a JSON response with topics and arguments
    else:
        speak("Sorry, I couldn't fetch the debate topics right now. Let's try again later.")
        return None

def choose_topic(topics):
    speak("Here are some interesting debate topics for you to choose from:")
    for i, topic in enumerate(topics, 1):
        speak(f"{i}. {topic}")
    
    speak("Please say the number of the topic you'd like to debate.")
    choice = listen()
    
    if choice and choice.isdigit() and 1 <= int(choice) <= len(topics):
        return topics[int(choice) - 1]
    else:
        speak("I didn't quite understand that. Let's go through the topics one more time.")
        return choose_topic(topics)

def debate(topic, arguments):
    speak(f"Great choice! Let's dive into the topic: {topic}")
    speak("Would you like to argue for the pro side or the con side?")

    side = listen()
    if side and ("pro" in side or "for" in side):
        chosen_side = "pro"
    elif side and ("con" in side or "against" in side):
        chosen_side = "con"
    else:
        speak("I didn't catch that. Let's clarify your choice.")
        return debate(topic, arguments)

    speak(f"You are arguing for the {chosen_side} side. Please share your argument.")
    user_argument = listen()
    if user_argument:
        speak("Thank you for sharing your thoughts! Now, here’s my response.")
        response = random.choice(arguments[chosen_side])
        speak(response)

def main():
    speak("Welcome to your Virtual Debate Partner! I'm here to help you practice your debating skills.")
    
    while True:
        topics = fetch_debate_topics()
        if not topics:
            break
        
        topic = choose_topic(list(topics.keys()))
        arguments = topics[topic]
        
        debate(topic, arguments)

        speak("Would you like to choose another topic? If yes, say 'yes'; if not, say 'no'.")
        continue_choice = listen()
        if continue_choice and ("no" in continue_choice):
            speak("Thank you for debating with me today. I hope you found it helpful! Have a wonderful day!")
            break

if __name__ == "__main__":
    main()
