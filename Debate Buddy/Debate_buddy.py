import random
import requests
import speech_recognition as sr
import pyttsx3
import time
import threading

# Initialize the speech engine
engine = pyttsx3.init()

# Dictionary to store user arguments for analysis
user_arguments_log = []

# Initialize scores
user_score = 0
bot_score = 0

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

def timer(duration):
    for remaining in range(duration, 0, -1):
        print(f"Time left: {remaining} seconds", end="\r")
        time.sleep(1)
    speak("Time is up!")

def provide_feedback(user_argument):
    feedback = []
    if len(user_argument) < 10:
        feedback.append("Try to elaborate on your point.")
    if "evidence" not in user_argument:
        feedback.append("Including specific examples or evidence can make your argument stronger.")
    if not feedback:
        feedback.append("Great argument! Keep up the good work.")
    return feedback

def debate(topic, arguments):
    global user_score, bot_score
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

    speak(f"You are arguing for the {chosen_side} side. You have 30 seconds to make your argument.")

    # Start the timer in a separate thread so it doesn’t block listening
    timer_thread = threading.Thread(target=timer, args=(30,))
    timer_thread.start()

    user_argument = listen()  # Listen while the timer runs in background

    if user_argument:
        user_arguments_log.append((topic, chosen_side, user_argument))  # Record user argument
        speak("Thank you for sharing your thoughts! Now, here’s my response.")
        response = random.choice(arguments[chosen_side])
        speak(response)
        
        # Provide feedback 
        feedback = provide_feedback(user_argument)
        for comment in feedback:
            speak(comment)
            
        # Counter-question
        speak("I have a question for you. How would you address a counter-argument to your point?")
        user_response = listen()
        
        # Scoring
        if user_response:
            user_score += 1
            speak("Good response! You are improving your debating skills.")
        else:
            bot_score += 1  # bot scores if user struggles with counter question
            speak("It's okay if you're unsure. Practice makes perfect!")

def summarize_debate():
    speak("Here's a summary of today's debate session: ")
    for i, (topic, side, argument) in enumerate(user_arguments_log, 1):
        speak(f"Topic {i}: {topic}. Your side: {side}. Your argument: {argument[:50]}...")  # Summarize with a slice
    speak(f"Final score: You scored {user_score} points, and I scored {bot_score} points.")

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
            summarize_debate()
            speak("Thank you for debating with me today. I hope you found it helpful! Have a wonderful day!")
            break

if __name__ == "__main__":
    main()
